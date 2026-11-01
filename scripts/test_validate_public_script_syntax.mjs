/* Negative controls for public inline script parsing; never executes webpage code. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { publicPages, validateInlineScripts } from './validate_public_script_syntax.mjs';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
for (const path of publicPages) {
  assert.deepEqual(validateInlineScripts(readFileSync(resolve(root, path), 'utf8'), path), []);
}
const valid = '<script>const x = { identity: "source", standing: "DECLARED" };<\/script>';
const invalid = "<script>const x = { identity: 'source'], standing: 'DECLARED' };<\/script>";
assert.deepEqual(validateInlineScripts(valid), []);
assert.ok(validateInlineScripts(invalid).some(x => x.includes('invalid')));
assert.ok(validateInlineScripts('<script>let x = 1;').some(x => x.includes('unmatched')));
assert.ok(validateInlineScripts('<script src="https://outside.example/script.js"></script>').some(x => x.includes('externally')));
process.stdout.write('PASS: inline JavaScript parser and 3 negative controls\n');
