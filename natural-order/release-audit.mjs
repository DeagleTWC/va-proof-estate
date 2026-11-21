import {readdir,readFile,lstat} from 'node:fs/promises';
import {join,relative,sep} from 'node:path';
import {fileURLToPath} from 'node:url';

const allowed = new Set(['.html','.css','.mjs','.md']);
const forbiddenPath = /(?:^|\/)(?:private_data|uploads?|artifacts|originals|secrets?|signatures?)(?:\/|$)|(?:kernel|nda|mnda).*(?:\.pdf|\.zip)$/i;
const secretPattern = /-----BEGIN\s+(?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}/;

export async function auditRelease(root) {
  const base=typeof root==='string'?root:fileURLToPath(root);
  const errors=[];
  const files=[];

  async function inspect(directory) {
    for (const item of await readdir(directory,{withFileTypes:true})) {
      const absolute=join(directory,item.name);
      const rel=relative(base,absolute).split(sep).join('/');
      if (rel==='tests' || rel.startsWith('tests/')) continue; // tests are not deployed
      if (item.isSymbolicLink()) { errors.push(`${rel}: symlinks must not be deployed`); continue; }
      if (item.isDirectory()) { if(forbiddenPath.test(`${rel}/`)) errors.push(`${rel}: forbidden directory`); await inspect(absolute); continue; }
      if (!item.isFile()) { errors.push(`${rel}: unexpected file type`); continue; }
      files.push(rel);
      const ext=item.name.slice(item.name.lastIndexOf('.'));
      if (!allowed.has(ext) || forbiddenPath.test(rel) || item.name.startsWith('.')) { errors.push(`${rel}: file not cleared for web release`); continue; }
      const stat=await lstat(absolute);
      if (stat.size>500000) { errors.push(`${rel}: too large for curated web release`); continue; }
      const data=await readFile(absolute,'utf8');
      if (secretPattern.test(data)) errors.push(`${rel}: possible secret key in release`);
    }
  }
  await inspect(base);
  return {files:files.sort(),errors};
}

if (process.argv[1] && import.meta.url===new URL(`file://${process.argv[1]}`).href) {
  const result=await auditRelease(new URL('.',import.meta.url));
  for (const file of result.files) process.stdout.write(`PUBLIC ${file}\n`);
  if (result.errors.length) {
    for (const error of result.errors) process.stderr.write(`FAIL ${error}\n`);
    process.exitCode=1;
  } else process.stdout.write('RELEASE AUDIT PASSED\n');
}
