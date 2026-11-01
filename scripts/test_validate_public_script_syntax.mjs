/* Negative controls for public inline script parsing; never executes webpage code. */
import assert from 'node:assert/strict';
import { Script } from 'node:vm';
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
const homepage = readFileSync(resolve(root, 'index.html'), 'utf8');
const start = homepage.indexOf('function resolveLedgerSelection(');
const end = homepage.indexOf('function renderLedger(', start);
assert.ok(start > 0 && end > start, 'Claim filter resolver missing');
const resolveLedgerSelection = new Script(homepage.slice(start,end)+'\nresolveLedgerSelection').runInNewContext({});
const claims=[{id:'VA-F01',class:'formal'},{id:'VA-F02',class:'formal'},{id:'VA-N01',class:'software'},{id:'VA-P01',class:'physical'}];
assert.equal(resolveLedgerSelection(claims,'all','VA-N01').activeId,'VA-N01');
assert.equal(resolveLedgerSelection(claims,'formal','VA-N01').activeId,'VA-F01');
assert.deepEqual([...resolveLedgerSelection(claims,'formal','VA-N01').selected].map(x=>x.id),['VA-F01','VA-F02']);
assert.equal(resolveLedgerSelection(claims,'physical','VA-F01').activeId,'VA-P01');
assert.equal(resolveLedgerSelection(claims,'missing','VA-N01').activeId,null);
const renderer=homepage.slice(end,homepage.indexOf("byId('matrixFilter').onchange=renderLedger;",end));
assert.ok(renderer.indexOf('activeLedger=selection.activeId')<renderer.indexOf('for(const record of selected)'));
assert.ok(renderer.includes("tr.setAttribute('aria-selected'"));
assert.ok(renderer.includes("byId('claimPacket').disabled=!activeLedger"));
process.stdout.write('PASS: inline JavaScript parser and 3 negative controls\n');
