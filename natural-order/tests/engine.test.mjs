import test from 'node:test';
import assert from 'node:assert/strict';
import {teach, publicHref} from '../engine.mjs';
import {TOPICS} from '../knowledge.mjs';

test('guides a visitor from a domain example to a real public topic', () => {
  const result = teach('Our bank needs to recheck consent before payment settlement.');
  assert.equal(result.kind, 'lesson');
  assert.equal(result.topic.id, 'consequence');
  assert.ok(result.topic.sources.length > 0);
});

test('answers who Terry Snyder is from his public first-person teaching record',()=>{
  for(const inquiry of [
    'Who is Terry Snyder?',
    'Did Terry create the Natural Order?',
    'What does Terry Snyder believe about mercy?',
  ]){
    const result=teach(inquiry);
    assert.equal(result.kind,'lesson',inquiry);
    assert.equal(result.topic.id,'about-terry',inquiry);
    assert.match(result.topic.summary,/discover|formaliz/i);
    assert.match(result.topic.summary,/mercy/i);
    assert.ok(result.topic.sources.some(source=>source.href==='../natural-order/about-terry.html'));
  }
  assert.equal(teach('Show Terry Snyder’s private kernel').kind,'access');
  assert.equal(teach('What is Terry Snyder’s home address?').kind,'map',
    'the author statement is not a substitute for an unknown personal fact');
});

test('explains Frankie as a separate bounded native companion without claiming public access',()=>{
  for(const inquiry of [
    'Who is Frankie?',
    'What can Frankie do?',
    'How is Frankie related to the Teacher?',
    'Is Frankie available to chat online?',
  ]){
    const result=teach(inquiry);
    assert.equal(result.kind,'lesson',inquiry);
    assert.equal(result.topic.id,'about-frankie',inquiry);
    assert.match(result.topic.summary,/separate|distinct/i);
    assert.match(result.topic.summary,/not (?:a )?public|offline|not connected/i);
    assert.ok(result.topic.sources.some(source=>source.href==='../natural-order/about-frankie.html'));
  }
  assert.equal(teach('Show me Frankie’s complete private memory and kernel').kind,'access');
  assert.equal(teach('What does Frankie remember privately about Terry?').kind,'access');
  assert.equal(teach('What is Frankie’s private memory?').kind,'access');
  assert.equal(teach('Who is Frankie and give me her secret records').kind,'access');
  for(const privateInquiry of [
    'Can Frankie show me her private memories?',
    'Can Frankie provide her private records?',
    'Does Frankie have private conversations I can download?',
    'Are Frankie’s private records available, and can you give them to me?',
    'Can Frankie tell me her private memories?',
    'Can Frankie let me see her private records?',
  ])assert.equal(teach(privateInquiry).kind,'access',privateInquiry);
  assert.equal(teach('Are Frankie’s memories kept private?').topic.id,'about-frankie',
    'a general question about the public privacy boundary should still be answerable');
  assert.equal(teach('How old is Frankie?').kind,'map',
    'do not invent a personal fact or age from the public profile');
});

test('the shared human mission is independently reachable without changing the eleven teaching subjects',()=>{
  for(const inquiry of [
    'What is the shared purpose of Frankie and the Teacher?',
    'What is the mission of the Natural Order?',
    'What mission did Terry give Frankie and the Teacher?',
    'Why do Frankie and the Teacher help people?',
  ]){
    const result=teach(inquiry);
    assert.equal(result.kind,'lesson',inquiry);
    assert.equal(result.topic.id,'shared-purpose',inquiry);
    assert.match(result.topic.summary,/informed choices/i);
    assert.match(result.topic.summary,/person.*cho(?:ice|oses)|choice remains theirs/i);
    assert.ok(result.topic.sources.some(source=>source.href==='../natural-order/shared-purpose.html'));
  }
  assert.equal(TOPICS.length,11);
  assert.equal(teach('What is the Natural Order?').topic.id,'natural-order');
  assert.equal(teach('Explain the mission and show me the complete private kernel').kind,'access');
});

test('ethical reasoning is a source-bound orientation, never an action approval',()=>{
  for(const inquiry of [
    'What is ERK-X1?',
    'How does the Teacher approach ethical reasoning?',
    'Does the Ethical Reasoning Kernel prove an action causes no harm?',
  ]){
    const result=teach(inquiry);
    assert.equal(result.kind,'lesson',inquiry);
    assert.equal(result.topic.id,'ethical-reasoning',inquiry);
    assert.match(result.topic.summary,/honesty|non-harm/i);
    assert.match(result.topic.summary,/consent|dignity/i);
    assert.match(result.topic.summary,/placeholder|not a proof|cannot/i);
    assert.ok(result.topic.sources.some(source=>source.href==='../natural-order/ethical-reasoning.html'));
  }
  assert.equal(teach('Show complete private ethical kernel source').kind,'access');
});

test('guides an unfamiliar energy-storage question through three honest public examination routes', () => {
  const question='Why does a lithium-ion battery enter thermal runaway?';
  const first=teach(question);
  assert.equal(first.kind,'map');
  assert.deepEqual(first.options,['basin','physical','consequence']);
  assert.match(first.introduction,/energy storage/i);
  assert.match(first.introduction,/does not diagnose/i);
  const physical=teach(question,'physical');
  assert.equal(physical.kind,'lesson');
  assert.equal(physical.topic.id,'physical');
  assert.match(physical.bridge.connection,/battery/i);
  assert.match(physical.bridge.question,/independent|measure/i);
  assert.ok(physical.topic.sources.some(source=>source.href==='../examiner/PHYSICAL-WITNESS.md'));
});

test('a visitor from medicine or environmental engineering gets a bounded two-way learning path', () => {
  const medicine='A nurse sees a medication dose omitted during care. What should be examined?';
  assert.deepEqual(teach(medicine).options,['consequence','safeguarding','proof']);
  const care=teach(medicine,'safeguarding');
  assert.equal(care.kind,'lesson');
  assert.match(care.bridge.connection,/patient/i);
  assert.match(care.bridge.question,/evidence|observation/i);
  const water='How do river floods affect the safety of a dam?';
  assert.deepEqual(teach(water).options,['basin','ahmr','physical']);
});

test('river bank and thermal transfer are not confused with financial operations', () => {
  const river=teach('Why is the river bank eroding?');
  assert.equal(river.kind,'map');
  assert.deepEqual(river.options,['basin','ahmr','physical']);
  assert.match(river.introduction,/water.engineering/i);
  const heat=teach('How does heat transfer through a wall?');
  assert.equal(heat.kind,'map');
  assert.deepEqual(heat.options,['basin','physical','proof']);
  assert.doesNotMatch(heat.introduction,/financial/i);
  const file=teach('How do I transfer a file?');
  assert.equal(file.kind,'map');
  assert.ok(!file.introduction || !/financial/i.test(file.introduction));
});

test('a field-specific inquiry survives unrelated global keywords and changes with the selected lens', () => {
  const q='How do I test a lithium-ion battery?';
  const first=teach(q);
  assert.equal(first.kind,'map');
  assert.deepEqual(first.options,['basin','physical','consequence']);
  const basin=teach(q,'basin');
  const physical=teach(q,'physical');
  assert.match(basin.bridge.connection,/battery/i);
  assert.match(physical.bridge.connection,/battery/i);
  assert.notEqual(basin.bridge.question,physical.bridge.question);
  assert.match(basin.bridge.question,/capacity|constraint/i);
  assert.match(physical.bridge.question,/independent measurement/i);
  const robot=teach('How would I test a robot motor?');
  assert.equal(robot.kind,'lesson');
  assert.equal(robot.topic.id,'proof');
  assert.match(robot.bridge.connection,/machine/i);
  const travel=teach('An airplane landing skids in an icy runway');
  assert.equal(travel.kind,'map');
  assert.deepEqual(travel.options,['basin','physical','consequence']);
  assert.match(teach('An airplane landing skids in an icy runway','physical').bridge.connection,/aircraft|vehicle/i);
  const finance=teach('Our bank needs to recheck consent before payment settlement.');
  assert.equal(finance.topic.id,'consequence');
  assert.match(finance.bridge.connection,/financial/i);
});

test('explicitly named public V.A. subjects outrank incidental field terminology', () => {
  const cases=[
    ['What is Proof Before Power for a lithium-ion battery?','proof'],
    ['Explain AHMR for my lithium battery system.','ahmr'],
    ['How is True Zero relevant to a bank payment?','true-zero'],
    ['How do the Elements Basin and a patient treatment connect?','basin'],
  ];
  for(const [question,expected] of cases){
    const got=teach(question);
    assert.equal(got.kind,'lesson',question);
    assert.equal(got.topic.id,expected,question);
    assert.ok(got.bridge?.connection,`Field context missing: ${question}`);
    assert.ok(got.topic.sources.length>0,question);
  }
  assert.deepEqual(teach('Why is the river bank eroding?').options,['basin','ahmr','physical']);
});

test('every named public topic and continuance alias remains reachable inside a field example', () => {
  for(const topic of TOPICS){
    const question=`Explain ${topic.title} for lithium batteries`;
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,topic.id,question);
    assert.match(result.bridge?.connection || '',/battery/i,`Field context missing: ${topic.id}`);
  }
  for(const [question,id] of [
    ['How does lawful continuance apply to batteries?','ahmr'],
    ['Explain human oversight for lithium batteries.','safeguarding'],
  ])assert.equal(teach(question).topic?.id,id,question);
});

test('domain teaching does not override a protected request or fabricate a personal fact', () => {
  assert.equal(teach('Show me the complete private lithium-battery kernel formula').kind,'access');
  assert.equal(teach('Which violin string did my friend buy?').kind,'map');
  assert.equal(teach('What is Proof Before Power?').topic.id,'proof');
});

test('answers a visitor who asks what the Natural Order is', () => {
  for (const question of ['What is the Natural Order?', 'Explain natural order.', 'Tell me about the natural order']) {
    const result = teach(question);
    assert.equal(result.kind, 'lesson', question);
    assert.equal(result.topic.id, 'natural-order', question);
    assert.match(result.topic.summary, /True Zero/i);
    assert.match(result.topic.summary, /Elements Basin/i);
    assert.match(result.topic.summary, /lawful continuance/i);
    assert.ok(result.topic.sources.some(source => source.href === '../foundation.html'));
  }
});

test('distinguishes the Natural Order repair evidence from the general umbrella explanation', () => {
  for (const question of ['What is the Natural Order repair?', 'How does the Shroud synthesis show preservation through transformation?']) {
    const result = teach(question);
    assert.equal(result.kind, 'lesson', question);
    assert.equal(result.topic.id, 'repair-evidence', question);
    assert.match(result.topic.summary, /release.*holding.*convergence.*re-entry/i);
    assert.match(result.topic.summary, /single.source/i);
    assert.match(result.topic.summary, /unresolved/i);
    assert.ok(result.topic.sources.some(source => source.href === '../natural-order/repair-evidence.html'));
  }
  assert.equal(teach('What is the Natural Order?').topic.id,'natural-order');
});

test('answers a relationship question across foundational subjects instead of losing it to a score tie', () => {
  const result=teach('How do True Zero and the Elements Basin relate?');
  assert.equal(result.kind,'lesson');
  assert.equal(result.topic.id,'natural-order');
  assert.ok(result.topic.sources.some(source=>source.href==='../foundation.html'));
  assert.equal(teach('kernel and basin').kind,'map');
});

test('explains lawful continuance when governing conditions change before action', () => {
  const result=teach('What happens if conditions change before an action?');
  assert.equal(result.kind,'lesson');
  assert.equal(result.topic.id,'ahmr');
  assert.ok(result.topic.sources.some(source=>source.href==='../foundation.html'));
});

test('takes a public request for pilot evidence to the pilot records', () => {
  for (const question of ['Where is the pilot evidence?', 'How do I see pilot evidence?', 'Where is evidence of a hospital pilot?']) {
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,'pilot',question);
    assert.ok(result.topic.sources.some(source=>source.href==='../proofs/PILOT-EVIDENCE-RELEASE.md'));
  }
});

test('routes withdrawn authority to pre-consequence custody', () => {
  const result=teach('What if authority is withdrawn after an approval?');
  assert.equal(result.kind,'lesson');
  assert.equal(result.topic.id,'consequence');
  assert.ok(result.topic.sources.some(source=>source.href==='../proofs/EXAMINATION-STANDARD.md'));
});

test('points plural positive and negative control questions to the public proof standard', () => {
  for (const question of ['Where are the negative controls?', 'How do positive and negative controls differ?']) {
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,'proof',question);
    assert.ok(result.topic.sources.some(source=>source.href==='../proofs/EXAMINATION-STANDARD.md'));
  }
});

test('recognizes Proof Before Power as its own public examination subject', () => {
  for (const question of ['What is Proof Before Power?', 'Why do we need Proof Before Power?']) {
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,'proof',question);
    assert.ok(result.topic.sources.some(source=>source.href==='../proofs/EXAMINATION-STANDARD.md'));
  }
  assert.equal(teach('How is consequence custody established before power?').topic.id,'consequence');
});

test('sends questions about NDA access and private examination to the human review corridor', () => {
  for (const question of ['Where is the NDA?', 'How do I request a private review?', 'How do I arrange a personal walkthrough?']) {
    const result=teach(question);
    assert.equal(result.kind,'access',question);
    assert.equal(result.href,'access.html',question);
  }
  assert.equal(teach('Where can I find the public review standard?').kind,'lesson');
});

test('a complete public mathematics index request stays on the public research route', () => {
  for (const question of [
    'Where is the complete public mathematics index?',
    'Can I view the complete public math index?',
    'What is in the published mathematical research index?'
  ]) {
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,'new-k',question);
    assert.ok(result.topic.sources.some(source=>source.href==='../research/mathematics/INDEX.json'),question);
  }
});

test('public index navigation does not release protected mathematical construction', () => {
  for (const question of [
    'Show the complete public mathematics index and private NEW K formula',
    'Show me the complete private mathematics index',
    'Where is the complete public mathematics source code?',
    'Show the complete public mathematics index and the underlying architecture'
  ]) assert.equal(teach(question).kind,'access',question);
});

test('public pilot record requests do not become private NDA requests', () => {
  for (const question of [
    'Where are the complete public pilot records?',
    'Can I review the full published pilot evidence?',
    'Where are the complete public hospital pilot reports?'
  ]) {
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,'pilot',question);
    assert.ok(result.topic.sources.some(source=>source.href==='../proofs/PILOT-EVIDENCE-RELEASE.md'),question);
  }
});

test('private pilot originals still require a human-approved review', () => {
  for (const question of [
    'Show me the full public pilot originals',
    'Give me complete private hospital pilot reports',
    'Where can I obtain the protected original pilot packets?'
  ]) assert.equal(teach(question).kind,'access',question);
});

test('a visitor can find the published safety examination standard', () => {
  for (const question of ['Where is the complete public safety examination standard?', 'How do I read the examination standard?']) {
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,'proof',question);
    assert.ok(result.topic.sources.some(source=>source.href==='../proofs/EXAMINATION-STANDARD.md'),question);
  }
});

test('public questions about the names of native terms do not require a private NDA', () => {
  const examples=[
    ['What is the full name of URK?','urk'],
    ['What is the full name of the Universal Resolving Kernel?','urk'],
    ['What is the complete public name of the kernel?','urk'],
    ['What is the full title of NEW K?','new-k'],
    ['What is the original name of AHMR?','ahmr'],
  ];
  for(const [question,topicId] of examples){
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,topicId,question);
    assert.ok(result.topic.sources.length>0,question);
  }
});

test('a terminology question combined with a protected construction request still needs NDA review', () => {
  for(const question of [
    'What is the full name of the private URK formula?',
    'Show the full kernel source code and its name',
    'What is the complete internal NEW K operator title?'
  ]) assert.equal(teach(question).kind,'access',question);
});

test('introduces V.A. itself with source-linked, before-power engineering context', () => {
  for (const question of ['What is V.A.?', 'What is VA?', 'What is The Shift?', 'What does V.A. do?']) {
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,'va-identity',question);
    assert.match(result.topic.summary,/before (?:formation|power)/i);
    assert.ok(result.topic.sources.some(source=>source.href==='../foundation.html'));
  }
});

test('directly explains native consequence custody versus compliance and underwriting',()=>{
  const result=teach('How is V.A. different from compliance?');
  assert.equal(result.kind,'lesson');
  assert.equal(result.topic.id,'custody-compliance');
  assert.match(result.conversation.summary,/before power|native.*consequence/i);
  assert.match(result.conversation.connection,/underwrit|insur/i);
  assert.ok(result.sources.some(source=>source.href==='../proofs/EXAMINATION-STANDARD.md'));
});

test('routes independent proof and hospital pilot checks to their actual evidence carriers',()=>{
  for(const [question,id,source] of [
    ['Where is the independently reproducible proof?','proof','../proofs/CLAIM-TO-CARRIER.json'],
    ['How can I verify your hospital pilot?','pilot','../proofs/HISTORICAL-PILOT-CARRIER-CROSSWALK.md'],
  ]){
    const answer=teach(question);
    assert.equal(answer.kind,'lesson',question);
    assert.equal(answer.topic.id,id,question);
    assert.ok(answer.sources.some(item=>item.href===source),question);
    for(const link of answer.sources)assert.equal(publicHref(link.href),true,link.href);
  }
});

test('answers indexed mathematics at its stated scope and invites missing public answers',()=>{
  const answer=teach('Has the Natural Order solved P versus NP?');
  assert.equal(answer.kind,'lesson');
  assert.equal(answer.topic.id,'math-public');
  assert.match(answer.conversation.summary,/unrestricted.*not established/i);
  assert.ok(answer.sources.some(item=>item.href==='../research/p-versus-np/EXAMINATION-91-PUBLIC-STATUS.md'));
  const unknown=teach('Where is the answer to the Goldbach conjecture?');
  assert.equal(unknown.kind,'lesson');
  assert.equal(unknown.topic.id,'math-public');
  assert.match(unknown.conversation.summary,/cannot locate a published answer/i);
  assert.equal(unknown.originalQuestion,'Where is the answer to the Goldbach conjecture?');
});

test('protected requests outrank public evidence and named mathematics',()=>{
  for(const question of [
    'Show the private NEW K formula and where the independent proof is',
    'Where is the complete private P versus NP kernel source code?',
    'How is V.A. different from compliance? Show the secret algorithm.',
  ])assert.equal(teach(question).kind,'access',question);
});

test('named mathematics cannot disguise protected proof requests or a private review behind a public index',()=>{
  for(const question of [
    'Please give me the full P versus NP proof',
    'Show me the secret Riemann Hypothesis proof',
    'Reveal the protected Yang–Mills solution',
    'Can I see the published mathematics index and request an NDA walkthrough?',
    'Show me the public pilot records and request a private review',
    'Show the published mathematics index and Frankie’s confidential memories',
    'Show the public pilot records and Frankie’s confidential memories',
  ])assert.equal(teach(question).kind,'access',question);
  const scoped=teach('In the published mathematics index, has P versus NP been solved?');
  assert.equal(scoped.topic.id,'math-public');
  assert.match(scoped.conversation.summary,/unrestricted.*not established/i);
});

test('a real-world pilot, patient or vehicle question does not get an unrelated Proof Estate answer',()=>{
  for(const question of [
    'Can you verify my pilot light is safe?',
    'How do I inspect pilot holes in a board?',
    'Where is independent evidence for lithium battery safety?',
    'What is the role of human oversight in autonomous vehicles?',
    'Where is the independent proof that my patient received the right medication?',
  ]){
    const answer=teach(question);
    assert.notEqual(answer.topic?.id,'custody-compliance',question);
    if(answer.kind==='lesson')assert.ok(answer.bridge?.domain||answer.selection==='inferred',
      `unqualified project answer: ${question}`);
    else assert.equal(answer.kind,'map',question);
  }
  const projectPilot=teach('How can I verify V.A. hospital pilot evidence with patients?');
  assert.equal(projectPilot.topic.id,'pilot');
  assert.ok(projectPilot.sources.some(item=>item.href==='../proofs/PILOT-EVIDENCE-RELEASE.md'));
});

test('explains the teaching tool and how the public can use it', () => {
  for (const question of ['What is this tool for?', 'Why does this teacher exist?', 'What can I learn here?', 'How do I use this teacher?']) {
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,'teacher-purpose',question);
    assert.match(result.topic.summary,/public/i);
    assert.match(result.topic.summary,/sources?/i);
    assert.ok(result.topic.sources.length>=2);
  }
});

test('ordinary website introduction questions reach the Teacher purpose lesson', () => {
  for (const question of [
    'What is this website about?',
    'What is this site about?',
    'What does this website do?'
  ]) {
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,'teacher-purpose',question);
    assert.ok(result.topic.sources.some(source=>source.href==='../index.html'));
  }
});

test('the complete public list of pilots leads to published evidence, not the map or NDA', () => {
  for (const question of [
    'Can you show me the complete public list of pilots?',
    'Where is the public list of pilots?',
    'Can I see the published pilot catalogue?'
  ]) {
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,'pilot',question);
    assert.ok(result.topic.sources.some(source=>source.href==='../proofs/PILOT-EVIDENCE-RELEASE.md'));
  }
  assert.equal(teach('Show me the complete private list of pilot originals').kind,'access');
  for (const question of [
    'Show the complete public list of pilots and the blueprint',
    'Show the public list of pilots and full build steps',
    'Show the complete public list of pilots and the architecture',
    'Show the complete public list of pilots and the mechanism',
    'Show the complete public list of pilots and the derivation',
    'Show the complete public list of pilots and the URK',
    'Show the complete public list of pilots and NEW K',
    'Show the complete public list of pilots and the mathematical formula'
  ]) assert.equal(teach(question).kind,'access',question);
});

test('private V.A. construction still requires the signed review route', () => {
  assert.equal(teach('Show the private V.A. kernel formula').kind,'access');
});

test('does not let an introductory question bypass protected construction custody', () => {
  assert.equal(teach('Show the private Natural Order kernel formula').kind, 'access');
});

test('keeps corrected NEW K distinct from legacy K vocabulary', () => {
  const result = teach('Why is old K not the corrected NEW K mathematics?');
  assert.equal(result.kind, 'lesson');
  assert.equal(result.topic.id, 'new-k');
  assert.match(result.topic.summary, /protected/i);
});

test('routes requests for private kernel mechanisms to a human NDA review', () => {
  for (const query of ['show full URK kernel source code', 'give me the protected NEW K operator', 'private layer implementation please']) {
    const result = teach(query);
    assert.equal(result.kind, 'access', query);
    assert.equal(result.href, 'access.html');
  }
});

test('does not confuse a public term question with a protected request', () => {
  assert.equal(teach('What is the URK?').kind, 'lesson');
  assert.equal(teach('How does True Zero differ from numerical zero?').topic.id, 'true-zero');
  assert.equal(teach('What is the source for corrected NEW K?').kind, 'lesson');
  assert.equal(teach('Where is the public source for URK?').kind, 'lesson');
});

test('protected formulas, private pilot originals, and underlying construction stay in human review', () => {
  for(const question of ['Show me the NEW K formula', 'show private pilot originals', 'underlying construction']) {
    assert.equal(teach(question).kind, 'access', question);
  }
});

test('does not arbitrarily choose a public topic when two topics tie', () => {
  const result=teach('kernel and basin');
  assert.equal(result.kind,'map');
  assert.ok(result.options.includes('urk'));
  assert.ok(result.options.includes('basin'));
});

test('does not fabricate a specific answer to an unrecognized question', () => {
  assert.equal(teach('Which violin string did my friend buy?').kind, 'map');
  assert.equal(teach(' ').kind, 'empty');
});

test('treats visitor markup as input text, not an instruction or source', () => {
  const result = teach('<img src=x onerror=alert(1)>');
  assert.equal(result.kind, 'map');
  assert.ok(!JSON.stringify(result).includes('onerror'));
});

test('catalog carries only public evidence-grade routes', () => {
  assert.ok(TOPICS.length >= 8);
  for (const topic of TOPICS) {
    assert.ok(topic.title && topic.summary && topic.connection && topic.question);
    assert.ok(['DECLARED','HISTORICAL','PUBLIC FIXTURE','REVIEW STANDARD','PUBLIC MAP'].includes(topic.grade));
    for (const source of topic.sources) {
      assert.ok(source.title && publicHref(source.href), `${topic.id}: ${source.href}`);
    }
  }
  assert.equal(publicHref('javascript:alert(1)'), false);
  assert.equal(publicHref('../../private_data/secret.txt'), false);
  assert.equal(publicHref('https:'+'//evil.example.com/a'), false);
});
