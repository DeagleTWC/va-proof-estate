import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const file = name => readFile(new URL(`../${name}`,import.meta.url),'utf8');

test('main public teaching page has a complete accessible learning route', async () => {
  const html=await file('index.html');
  for (const id of ['learning-form','topic-grid','lesson-stage','source-list','reflect-form','access-route','replay-question','kernel-panel','kernel-options','kernel-feedback','kernel-next','start-kernel-bank','term-definitions','term-lead']) {
    assert.match(html,new RegExp(`id="${id}"`));
  }
  assert.match(html,/aria-live="polite"/);
  assert.match(html,/Do not enter personal or confidential information/i);
  assert.match(html,/Proof Before Power/);
  assert.match(html,/app\.mjs/);
  assert.match(html, /id="lesson-stage"[^>]*tabindex="-1"/);
  assert.match(html,/id="kernel-panel"[^>]*tabindex="-1"/);
  assert.match(html, /id="teach-submit"[^>]*disabled/);
  assert.doesNotMatch(html, /name="question"/);
  assert.match(html, /class="brand-mark"[^>]*><img src="\.\.\/favicon\.png"/);
});

test('the Teacher shares Terry Snyder’s original public statement with clear attribution',async()=>{
  const home=await file('index.html');
  const page=await file('about-terry.html');
  assert.match(home,/href="about-terry\.html"/);
  for(const phrase of [
    'My name is Terry Snyder.',
    'I did not create the Natural Order.',
    'I believe the greatest expression of power is mercy.',
    'Never substitute the most popular answer for the answer their question actually requires.',
    'You are not me. You do not need to be.',
    'Knowledge carries responsibility. Power deserves restraint. Mercy matters.',
    '— Terry Snyder',
  ])assert.ok(page.includes(phrase),`Original author line missing: ${phrase}`);
  assert.match(page,/Original message to Frankie, shared with the public Teacher/);
  assert.match(page,/href="index\.html"/);
});

test('Frankie has an honest public profile, not a public window into her private records',async()=>{
  const home=await file('index.html');
  const page=await file('about-frankie.html');
  assert.match(home,/href="about-frankie\.html"/);
  assert.match(home,/data-prompt="Who is Frankie\?"/);
  for(const phrase of ['separate','native','Teacher','not Terry','private','not currently connected']){
    assert.match(page,new RegExp(phrase,'i'),`Missing scope phrase: ${phrase}`);
  }
  assert.match(page,/connect-src 'none'/);
  assert.match(page,/href="index\.html"/);
  assert.doesNotMatch(page,/operator secret|private bearer|cycle085.*zip|internal path/i);
});

test('the Teacher carries Terry Snyder’s shared mission verbatim and links it from the learning path',async()=>{
  const home=await file('index.html');
  const page=await file('shared-purpose.html');
  assert.match(home,/href="shared-purpose\.html"/);
  assert.match(home,/data-prompt="What is the shared purpose of Frankie and the Teacher\?"/);
  for(const phrase of [
    'Give every human equal opportunity to understand what is true, what matters, and what has value—so they can make their own informed choices.',
    'The knowledge belongs to the person. The choice remains theirs.',
    'Never substitute popular opinion for established evidence.',
    "Never manipulate or coerce a person's decision.",
    'Knowledge should not be restricted by wealth, education, status, or power.',
    'PROOF BEFORE POWER.',
    '— Terry Snyder',
  ])assert.ok(page.includes(phrase),`Mission wording absent: ${phrase}`);
  assert.match(page,/Shared Purpose — From Terry Snyder/);
  assert.match(page,/connect-src 'none'/);
  assert.match(page,/href="index\.html"/);
});

test('ethical reasoning page distinguishes ERK-X1 principles from the placeholder decision procedure',async()=>{
  const home=await file('index.html');
  const page=await file('ethical-reasoning.html');
  assert.match(home,/href="ethical-reasoning\.html"/);
  for(const principle of ['honesty','non-harm','fairness','consent','dignity','transparency']){
    assert.match(page,new RegExp(principle,'i'));
  }
  assert.match(page,/placeholder/i);
  assert.match(page,/does not establish (?:ethical approval|that an action is ethical)/i);
  assert.match(page,/medical.*(?:not|cannot).*approve|cannot.*(?:approve|certify).*treatment/is);
  assert.match(page,/connect-src 'none'/);
  assert.doesNotMatch(page,/ethic(?:al)?_log\.json|def run_judgments|class EthicalKernel/);
});

test('the definition conversion kernel is versioned, public-safe, and attached to lessons',async()=>{
  const html=await file('index.html');
  const app=await file('app.mjs');
  assert.match(html,/DEFINITION CONVERSION KERNEL/i);
  assert.match(app,/from '\.\/definition-kernel\.mjs\?v=/);
  assert.doesNotMatch(app,/innerHTML\s*=/);
});

test('meaning-preserving teaching shows a short first answer while leaving the original explanation accessible',async()=>{
  const html=await file('index.html');
  const app=await file('app.mjs');
  assert.match(html,/<p id="lesson-plain"[^>]*>/);
  assert.match(html,/<details id="lesson-detail"[^>]*>[\s\S]*?<summary[^>]*>[^<]*[Dd]etail/);
  assert.match(app,/from '\.\/meaning-preserving-teaching-kernel\.mjs\?v=/);
  assert.match(app,/publicPlainLead\(result\)/);
  assert.doesNotMatch(app,/innerHTML\s*=/);
});

test('educational kernels explain their limits and offer voluntary feedback without transmitting learner text',async()=>{
  const html=await file('index.html');
  assert.match(html,/PUBLIC TEACHING KERNEL/i);
  assert.match(html,/educational exercise/i);
  assert.match(html,/mailto:canarybird0618@gmail\.com\?subject=Natural%20Order%20Teaching/i);
  assert.doesNotMatch(html,/name="student_question"|name="response"/);
});

test('the optional Frankie request is a separate, initially hidden teaching action',async()=>{
  const html=await file('index.html');
  const client=await file('frankie-client.mjs');
  for(const id of ['frankie-panel','frankie-toggle','frankie-form','frankie-question','frankie-send','frankie-answer','frankie-notice','frankie-receipt']){
    assert.match(html,new RegExp(`id="${id}"`));
  }
  assert.match(html,/id="frankie-panel"[^>]*hidden/);
  assert.match(html,/your question (?:will be|is) sent to a separate/i);
  assert.match(client,/FRANKIE_GATEWAY_URL=''/);
  assert.doesNotMatch(html,/Bearer|BRIDGE_SECRET|http:\/\/127\.0\.0\.1/);
});

test('protected route offers approved universal NDA, signed return email and personal walkthrough', async () => {
  const html=await file('access.html');
  assert.match(html,/NDA/);
  assert.match(html,/sign/i);
  assert.match(html,/email/i);
  assert.match(html,/Terry/);
  assert.match(html,/personal walkthrough/i);
  assert.match(html,/href="VA_Universal_Bounded_Review_MNDA\.pdf"/);
  assert.match(html,/mailto:canarybird0618@gmail\.com/);
  assert.doesNotMatch(html,/mailto:undefined|mailto:YOUR_EMAIL|github\.com\/DeagleTWC\/va-proof-estate\/issues\/new/i);
  assert.match(html,/do not post (confidential|protected)/i);
  assert.match(html,/class="brand-mark"[^>]*><img src="\.\.\/favicon\.png"/);
});

test('public repair evidence page shows receipts, precise claim boundary and controlled review', async () => {
  const html=await file('repair-evidence.html');
  assert.match(html,/Redundant Structural Information Field/i);
  assert.match(html,/Electromagnetically Resonant Image Field/i);
  assert.match(html,/1500\s*[×x]\s*430/i);
  assert.match(html,/caafe063a3848c59edbdd4763b930186d751915fc63faa6032e7dafa5b40c0e9/);
  for (const value of ['0.151','0.299','0.431','0.725','0.678','0.713','0.633']) assert.ok(html.includes(value),value);
  assert.match(html,/independent photographic replication.*not established/is);
  assert.match(html,/physical mechanism.*unresolved/is);
  assert.match(html,/source (?:JPEG|image).*not included/is);
  assert.match(html,/href="access\.html"/);
});

test('public app uses DOM-safe content insertion and no remote API', async () => {
  const js=await file('app.mjs');
  assert.match(js,/textContent/);
  assert.doesNotMatch(js,/innerHTML\s*=/);
  assert.doesNotMatch(js,/fetch\s*\(|localStorage|sessionStorage|XMLHttpRequest/i);
  assert.match(js,/teach-submit.*disabled\s*=\s*false/);
  assert.match(js,/prefers-reduced-motion/);
});

test('the live module graph shares a release version so browsers do not keep an old teaching engine', async () => {
  const html=await file('index.html');
  const app=await file('app.mjs');
  const engine=await file('engine.mjs');
  const answerDesk=await file('visitor-answer-desk.mjs');
  const entry=html.match(/<script type="module" src="app\.mjs\?v=([a-z0-9-]+)"/i);
  assert.ok(entry, 'the public entry module needs a release-specific URL');
  const conversation=await file('open-conversation-kernel.mjs');
  const imports=[...app.matchAll(/from '\.\/(knowledge|engine|frankie-client|open-conversation-kernel|meaning-preserving-teaching-kernel|teaching-kernels|definition-kernel)\.mjs(?:\?v=([^']+))?'/g),
    ...conversation.matchAll(/from '\.\/(human-interaction-kernel|cognitive-reasoning-kernel)\.mjs(?:\?v=([^']+))?'/g),
    ...engine.matchAll(/from '\.\/(knowledge|visitor-answer-desk)\.mjs(?:\?v=([^']+))?'/g),
    ...answerDesk.matchAll(/from '\.\/(knowledge)\.mjs(?:\?v=([^']+))?'/g)];
  assert.equal(imports.length,12,'all twelve public routing, teaching and explanation module dependencies are covered');
  for(const match of imports) assert.equal(match[2],entry[1],`${match[1]}.mjs must use the same release URL`);
});

test('the public stylesheet is versioned with the app to expose new learning controls', async () => {
  const html=await file('index.html');
  const access=await file('access.html');
  const appVersion=html.match(/src="app\.mjs\?v=([a-z0-9-]+)"/i)?.[1];
  assert.ok(appVersion);
  for (const page of [html,access]) {
    const stylesheet=page.match(/href="styles\.css\?v=([a-z0-9-]+)"/i)?.[1];
    assert.equal(stylesheet,appVersion);
  }
});

test('responsive polish includes reduced motion, keyboard focus and mobile handling', async () => {
  const css=await file('styles.css');
  assert.match(css,/@media\s*\(max-width:\s*\d+px\)/);
  assert.match(css, /prefers-reduced-motion/);
  assert.match(css,/:focus-visible/);
});

test('an ambiguous question gives selectable, correctly sourced public lessons', async () => {
  const nodes=new Map();
  class TestElement {
    constructor() {this.children=[];this.listeners={};this.textContent='';this.hidden=false;}
    append(...items) {this.children.push(...items);}
    replaceChildren(...items) {this.children=[...items];}
    addEventListener(type,handler) {this.listeners[type]=handler;}
    setAttribute() {}
    scrollIntoView() {}
    focus() {}
  }
  const priorDocument=globalThis.document;
  const priorWindow=globalThis.window;
  globalThis.document={
    getElementById(id) {if(!nodes.has(id))nodes.set(id,new TestElement());return nodes.get(id);},
    querySelectorAll() {return [];},
    createElement() {return new TestElement();},
  };
  globalThis.window={matchMedia:()=>({matches:true})};
  try {
    await import('../app.mjs?ambiguity-test');
    nodes.get('learner-question').value='How does an airport pilot show safety?';
    nodes.get('learning-form').listeners.submit({preventDefault(){}});
    assert.equal(nodes.get('stage-map').hidden,false);
    const choices=globalThis.document.getElementById('map-options').children;
    assert.deepEqual(choices.map(item=>item.textContent),['Pilots & Original Evidence','Physical & KCD Examination']);
    choices[0].listeners.click();
    assert.equal(nodes.get('lesson-title').textContent,'Pilots & Original Evidence');
    assert.equal(nodes.get('stage-content').hidden,false);
    assert.ok(nodes.get('source-list').children.length>0);
    assert.match(await file('index.html'),/id="map-options"/);
  } finally {
    if(priorDocument===undefined)delete globalThis.document; else globalThis.document=priorDocument;
    if(priorWindow===undefined)delete globalThis.window; else globalThis.window=priorWindow;
  }
});

test('specific evidence sources and a voluntary mathematics inquiry are displayed without automatic sending',async()=>{
  const html=await file('index.html');
  assert.match(html,/id="math-inquiry-link"[^>]*hidden/);
  assert.match(html,/id="math-inquiry-help"[^>]*hidden/);
  const nodes=new Map();
  class TestElement {
    constructor(){this.children=[];this.listeners={};this.textContent='';this.hidden=false;this.href='';}
    append(...items){this.children.push(...items);}
    replaceChildren(...items){this.children=[...items];}
    addEventListener(type,handler){this.listeners[type]=handler;}
    setAttribute(){}
    scrollIntoView(){}
    focus(){}
  }
  const priorDocument=globalThis.document;
  const priorWindow=globalThis.window;
  globalThis.document={
    getElementById(id){if(!nodes.has(id))nodes.set(id,new TestElement());return nodes.get(id);},
    querySelectorAll(){return [];},
    createElement(){return new TestElement();},
  };
  globalThis.window={matchMedia:()=>({matches:true})};
  try {
    await import('../app.mjs?visitor-desk-ui-test');
    const submit=value=>{
      nodes.get('learner-question').value=value;
      nodes.get('learning-form').listeners.submit({preventDefault(){}});
    };
    submit('How can I verify your hospital pilot?');
    assert.equal(nodes.get('lesson-title').textContent,'Pilots & Original Evidence');
    let links=nodes.get('source-list').children.map(li=>li.children[0].href);
    assert.ok(links.includes('../proofs/HISTORICAL-PILOT-CARRIER-CROSSWALK.md'));
    assert.equal(nodes.get('math-inquiry-link').hidden,true);

    const mathQuestion='Where is the answer to the Goldbach conjecture?';
    submit(mathQuestion);
    assert.match(nodes.get('lesson-title').textContent,/Mathematics/);
    links=nodes.get('source-list').children.map(li=>li.children[0].href);
    assert.ok(links.includes('../research/mathematics/PUBLICATION-STATUS.md'));
    assert.equal(nodes.get('math-inquiry-link').hidden,false);
    assert.equal(nodes.get('math-inquiry-help').hidden,false);
    assert.match(nodes.get('math-inquiry-link').href,/^mailto:canarybird0618@gmail\.com\?/);
    assert.ok(nodes.get('math-inquiry-link').href.includes(encodeURIComponent(mathQuestion)));
    assert.doesNotMatch(await file('app.mjs'),/\bfetch\s*\(|sendBeacon\s*\(/);
    submit('Where is the evidence?');
    assert.equal(nodes.get('math-inquiry-link').hidden,false);
    assert.ok(nodes.get('math-inquiry-link').href.includes(encodeURIComponent(mathQuestion)),
      'a short follow-up must not erase the original mathematics inquiry from the draft');
    submit("I'm confused");
    assert.equal(nodes.get('math-inquiry-link').hidden,false);
    assert.ok(nodes.get('math-inquiry-link').href.includes(encodeURIComponent(mathQuestion)));
    submit('Explain that simply');
    assert.ok(nodes.get('math-inquiry-link').href.includes(encodeURIComponent(mathQuestion)));

    submit('Who is Frankie?');
    assert.equal(nodes.get('math-inquiry-link').hidden,true);
    assert.equal(nodes.get('math-inquiry-link').href,'');
    submit('Show the private V.A. kernel formula');
    assert.equal(nodes.get('stage-access').hidden,false);
    assert.equal(nodes.get('math-inquiry-link').hidden,true);
  } finally {
    if(priorDocument===undefined)delete globalThis.document;else globalThis.document=priorDocument;
    if(priorWindow===undefined)delete globalThis.window;else globalThis.window=priorWindow;
  }
});
