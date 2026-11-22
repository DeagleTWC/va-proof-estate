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
    'Where is the complete public mathematics source code?'
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
