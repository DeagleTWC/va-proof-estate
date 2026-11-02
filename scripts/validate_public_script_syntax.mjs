/* Verify public static pages contain syntactically valid inline JavaScript.
   Static parser ONLY; no script is run, no network access, and no NEW-K calculation. */
import { readFileSync } from 'node:fs';
import { Script } from 'node:vm';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
export const publicPages = ['index.html', 'foundation.html', 'end-to-end.html', 'reviewer-route.html', 'source-reading.html'];

export function validateInlineScripts(html, label = '(inline page)') {
  const errors = [];
  const pattern = /<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi;
  const matches = [...html.matchAll(pattern)];
  const openings = [...html.matchAll(/<script\b/gi)].length;
  if (openings !== matches.length) errors.push(label + ': unmatched script tags');
  for (let i = 0; i < matches.length; i++) {
    const attrs = matches[i][1];
    const source = matches[i][2];
    if (/\bsrc\s*=/i.test(attrs)) {
      errors.push(label + ': externally loaded script found');
      continue;
    }
    const type = attrs.match(/\btype\s*=\s*(['"])(.*?)\1/i)?.[2] ?? '';
    if (type && !/^(application|text)\/javascript$|^module$/i.test(type)) {
      // Non-executable structured data need not be parsed as JavaScript.
      continue;
    }
    if (/^module$/i.test(type)) {
      errors.push(label + ': inline module requires a separately reviewed syntax check');
      continue;
    }
    try {
      new Script(source, { filename: label + ':script-' + (i + 1) });
    } catch (e) {
      errors.push(label + ': inline script ' + (i + 1) + ' invalid: ' + e.message);
    }
  }
  return errors;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const faults = [];
  for (const page of publicPages) {
    try {
      faults.push(...validateInlineScripts(readFileSync(resolve(root, page), 'utf8'), page));
    } catch (e) {
      faults.push(page + ': cannot read page: ' + e.message);
    }
  }
  faults.forEach(x => process.stderr.write('SCRIPT ERROR: ' + x + '\n'));
  process.stdout.write(faults.length ? 'FAIL: public JavaScript syntax\n' : 'PASS: public inline JavaScript parsed; not executed\n');
  if (faults.length) process.exitCode = 1;
}
