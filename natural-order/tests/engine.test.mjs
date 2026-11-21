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
