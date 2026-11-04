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

// Public navigation checks: preserve every original section destination and the two Stage A entry links.
const navStart=homepage.indexOf('<nav class="navlinks"');
const navEnd=homepage.indexOf('</nav>',navStart);
assert.ok(navStart>=0 && navEnd>navStart,'Primary navigation missing');
const nav=homepage.slice(navStart,navEnd);
const navLinks=[...nav.matchAll(/href="([^"]+)"/g)].map(x=>x[1]).sort();
const expectedNav=[
  'reviewer-route.html','end-to-end.html','#systems-category','#kcd-next',
  '#floor','#witness','#claims','#physical','#challenge','#proof-desk',
  '#runnable-proof','#byo-seam','consequence-challenge.html',
  'consequence-aperture.html','consequence-aperture.html'
].sort();
assert.deepEqual(navLinks,expectedNav,'Original public navigation routes must be retained');
assert.ok(nav.includes('<details class="nav-more">') && nav.includes('<summary>Explore sections'),
          'Accessible native section menu missing');
assert.equal([...nav.matchAll(/<details\b/g)].length,1,'Only one section menu is expected');
assert.ok(homepage.includes("const labels=['Bounded claim','Carrier and identity','Evidence class','Current public standing','Falsification condition']"),
          'Mobile labels must preserve the source table headings');
assert.ok(homepage.includes('cell.dataset.label=labels[i]'),
          'Ledger renderer must attach corresponding accessible mobile labels');
assert.ok(homepage.includes('content:attr(data-label)'),
          'Narrow-screen claim labels must remain visible');
assert.ok(homepage.includes('.matrix tbody tr.is-selected'),
          'Mobile card selection affordance must remain visible');
// Negative controls: changed navigation or label wiring must not pass source checks.
const hasOriginalRoutes=(s)=>{
  const n=s.slice(s.indexOf('<nav class="navlinks"'),s.indexOf('</nav>',s.indexOf('<nav class="navlinks"')));
  return [...n.matchAll(/href="([^"]+)"/g)].map(x=>x[1]).sort().join('|')===expectedNav.join('|');
};
assert.equal(hasOriginalRoutes(homepage.replace('href="#claims"','href="#removed-claim-link"')),false);
assert.equal(homepage.replace('cell.dataset.label=labels[i]','').includes('cell.dataset.label=labels[i]'),false);

process.stdout.write('PASS: inline JavaScript parser and 3 negative controls\n');
