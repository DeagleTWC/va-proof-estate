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

test('teaches the Natural Order repair witness without promoting image evidence to a physical mechanism', () => {
  for (const question of ['What is the Natural Order repair?', 'How does the Shroud synthesis show preservation through transformation?']) {
    const result = teach(question);
    assert.equal(result.kind, 'lesson', question);
    assert.equal(result.topic.id, 'repair-evidence', question);
    assert.match(result.topic.summary, /release.*holding.*convergence.*re-entry/i);
    assert.match(result.topic.summary, /single.source/i);
    assert.match(result.topic.summary, /unresolved/i);
    assert.ok(result.topic.sources.some(s => s.href === '../natural-order/repair-evidence.html'));
  }
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
