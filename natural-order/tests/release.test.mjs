import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {auditRelease} from '../release-audit.mjs';

const release = new URL('../',import.meta.url);

test('actual deploy contents are limited to the reviewed public files', async () => {
  const result=await auditRelease(release);
  assert.deepEqual(result.errors,[]);
  assert.ok(result.files.includes('index.html'));
  assert.ok(result.files.includes('knowledge.mjs'));
});

test('rejects a private or binary file accidentally added to a site directory', async () => {
  const dir=await mkdtemp(join(tmpdir(),'va-public-audit-'));
  try {
    await writeFile(join(dir,'index.html'),'<h1>safe</h1>');
    await writeFile(join(dir,'full-kernel-private.zip'),'confidential-bytes');
    const result=await auditRelease(dir);
    assert.ok(result.errors.some(e=>e.includes('full-kernel-private.zip')));
  } finally { await rm(dir,{recursive:true}); }
});

test('rejects nested private directories and secrets even when stored as text', async () => {
  const dir=await mkdtemp(join(tmpdir(),'va-public-audit-'));
  try {
    await mkdir(join(dir,'private_data'));
    await writeFile(join(dir,'private_data','orig.txt'),'protected');
    await writeFile(join(dir,'index.html'),'-----BEGIN RSA PRIVATE KEY-----');
    const result=await auditRelease(dir);
    assert.ok(result.errors.some(e=>e.includes('private_data')));
    assert.ok(result.errors.some(e=>e.includes('index.html')&&e.includes('secret')));
  } finally { await rm(dir,{recursive:true}); }
});
