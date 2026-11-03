/* Static-site negative controls for V.A. Proof in Motion.
   Tests public presentation, source custody and truthful passport outputs;
   never runs V.A. or third-party inputs. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {Script} from 'node:vm';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=(p)=>readFileSync(resolve(ROOT,p),'utf8');
const js=read('consequence-challenge.js');
const css=read('consequence-challenge.css');
const registry=JSON.parse(read('proofs/CLAIM-TO-CARRIER.json'));
const manifest=JSON.parse(read('proof-estate-manifest.json'));
const htmlPages=[
 ['consequence-challenge.html','authority',''],
 ['challenge/standing.html','standing','../'],
 ['challenge/authority.html','authority','../'],
 ['challenge/alternate-route.html','alternate','../']
];

assert.doesNotThrow(()=>new Script(js,{filename:'consequence-challenge.js'}));
assert.equal(css.split('{').length,css.split('}').length,'CSS braces must balance');
assert.ok(css.includes('@media(max-width:760px)'), 'Mobile layout missing');
assert.ok(css.includes('prefers-reduced-motion:reduce'),'Reduced-motion support missing');
assert.ok(css.includes('body.cc-examiner-mode'),'Technical examiner mode missing');

for(const [path,scenario,prefix] of htmlPages){
  const html=read(path);
  for(const required of [
    'name="viewport"',
    '<main id="cc-main">',
    'id="cc-app"',
    'href="'+prefix+'va-gold-design.css"',
    'href="'+prefix+'consequence-challenge.css"',
    'src="'+prefix+'consequence-challenge.js"',
    'data-root="'+prefix+'"',
    'data-scenario="'+scenario+'"',
    'https://deagletwc.github.io/va-proof-estate/'+path,
    '<meta property="og:title"'
  ]) assert.ok(html.includes(required),path+': missing '+required);
  assert.ok(html.includes('role="status"'),path+': loading fallback must be accessible');
  assert.ok(html.includes('<noscript>'),path+': original records must remain accessible without JS');
  assert.ok(html.includes('social-card-1200x630.jpg'),path+': brand preview missing');
  assert.ok(!/https?:\/\/(?:cdn|fonts|unpkg|analytics)[\w.-]*\//i.test(html),path+': external dependency');
  assert.equal([...html.matchAll(/<script\b/g)].length,1,path+': unexpected additional scripts');
}
const titles=htmlPages.map(([p])=>read(p).match(/<meta property="og:title" content="([^"]+)"/)[1]);
assert.equal(new Set(titles).size,4,'Social links must have distinct share preview titles');
assert.ok(js.includes('navigator.share') && js.includes('navigator.clipboard'),
  'Native share and local copy fallback required');
assert.ok(js.includes('canvas.toBlob') && js.includes('image/png'),
  'Locally generated gold challenge card required');
assert.ok(js.includes('URL.createObjectURL') && js.includes('application/json'),
  'Local Passport export required');
assert.ok(js.includes("fetch(registerURL,{cache:'no-store'})"),
  'Every visitor view must be based on current public register bytes');
assert.ok(js.includes("crypto.subtle.digest('SHA-256'"),
  'Public record identity hashing missing');
assert.ok(js.includes('state.error')&&js.includes('Required claim '),
  'Missing original data must not be presented as a result');
for(const banned of ['sendBeacon(', 'localStorage.', 'sessionStorage.', 'XMLHttpRequest(', 'indexedDB.']){
  assert.ok(!js.includes(banned),'No tracking or client record capture: '+banned);
}

const scenStart=js.indexOf('  const SCENARIOS = Object.freeze([');
const scenEnd=js.indexOf('  const EXPECTATIONS = ',scenStart);
assert.ok(scenStart>=0 && scenEnd>scenStart);
const scenarios=new Script(js.slice(scenStart,scenEnd)+'\nSCENARIOS').runInNewContext({});
assert.equal(scenarios.length,3);
assert.deepEqual([...scenarios].map(x=>x.id),['standing','authority','alternate']);
assert.deepEqual([...scenarios].map(x=>x.claimId),['VA-N01','VA-N02','VA-P02']);
assert.deepEqual([...scenarios].map(x=>x.expected),['bind','no-bind','no-bind']);
assert.equal(new Set(scenarios.map(x=>x.page)).size,3);
for(const scenario of scenarios){
  const source=registry.entries.find(x=>x.id===scenario.claimId);
  assert.ok(source,scenario.claimId+' original entry not found');
  assert.equal(source.standing,'DECLARED','Never silently promote native public standing');
  assert.equal(source.nativeVAEvidence,false);
  assert.ok(scenario.falsifier.length>25,'An exact falsification question must be stated');
  assert.ok(scenario.boundary.includes('not attached'),'Missing public original witness must remain stated');
}
assert.equal(registry.nativeRuntimeReceiptsAttached,0);
assert.equal(registry.independentNativeReproductionsAttached,0);

const passStart=js.indexOf('  function buildPassport(');
const passEnd=js.indexOf('  function buttonLabel(',passStart);
assert.ok(passStart>=0 && passEnd>passStart);
const passSource="const WEBSITE='https://deagletwc.github.io/va-proof-estate/';\n"+
  "const REGISTER_PATH='proofs/CLAIM-TO-CARRIER.json';\n"+js.slice(passStart,passEnd)+'\nbuildPassport';
const builder=new Script(passSource).runInNewContext({Date});
for(const scenario of scenarios){
  const original=registry.entries.find(x=>x.id===scenario.claimId);
  const passport=builder(original,'abc123',scenario,'unknown',registry.published);
  assert.equal(passport.recordType,'VISITOR_GENERATED_EXAMINATION_NOT_NATIVE_PROOF');
  assert.equal(passport.claimPromotion,false);
  assert.equal(passport.publicClaimCarrier.standing,original.standing);
  assert.equal(passport.publicClaimCarrier.id,original.id);
  assert.equal(passport.publicClaimCarrier.nativeVAEvidence,false);
  assert.equal(passport.sourceRegister.exactBytesSHA256,'abc123');
  assert.equal(passport.evidenceBoundary.observedNativeEffect,'NOT ATTACHED HERE');
  assert.equal(passport.evidenceBoundary.independentlyReproducedNativeEffect,'NOT ATTACHED HERE');
  assert.equal(passport.challenge.expectedResultIsNotObservedResult,true);
  assert.equal(passport.challenge.visitorPrediction,'unknown');
  assert.equal(passport.publicReference,'https://deagletwc.github.io/va-proof-estate/'+scenario.page);
}
const record=registry.entries.find(x=>x.id==='VA-N02');
const original=builder(record,null,scenarios[1],null,registry.published);
assert.equal(original.sourceRegister.exactBytesSHA256,'NOT VERIFIED IN THIS BROWSER');
assert.equal(original.challenge.visitorPrediction,'NOT SELECTED');

// Counterexamples: a wrong standing or falsely promoted passport must fail the test predicate.
const safePassport=p=>p.claimPromotion===false && p.publicClaimCarrier.standing==='DECLARED'
  && p.evidenceBoundary.observedNativeEffect==='NOT ATTACHED HERE';
assert.equal(safePassport(original),true);
assert.equal(safePassport({...original,claimPromotion:true}),false);
assert.equal(safePassport({...original,publicClaimCarrier:{...original.publicClaimCarrier,standing:'INDEPENDENTLY REPRODUCED'}}),false);

const home=read('index.html'),review=read('reviewer-route.html');
assert.ok(home.includes('id="proof-in-motion"')&&home.includes('href="consequence-challenge.html"'));
assert.ok(review.includes('href="consequence-challenge.html"'));
assert.equal(manifest.interactiveChallenge?.nativeExecutionClaimed,false);
assert.equal(manifest.interactiveChallenge?.publicSourceRegister,'proofs/CLAIM-TO-CARRIER.json');
assert.equal(manifest.interactiveChallenge?.entryPages.length,4);

process.stdout.write('PASS: 4 branded share pages, 3 source-bound cases, examiner mode, passbook/PNG/share, safety ceilings and negative controls\n');