import test from 'node:test';
import assert from 'node:assert/strict';
import {publicVisitorAnswer} from '../visitor-answer-desk.mjs';

const includesSource=(answer,path)=>answer.sources.some(source=>source.href===path);

test('a compliance question receives the custody-before-power and underwriting distinction',()=>{
  const answer=publicVisitorAnswer('How is V.A. different from compliance?');
  assert.equal(answer.kind,'lesson');
  assert.equal(answer.topic.id,'custody-compliance');
  assert.match(answer.conversation.summary,/native|formation/i);
  assert.match(answer.conversation.summary,/before power|before.*consequence/i);
  assert.match(answer.conversation.connection,/underwrit|insur|bond/i);
  assert.match(answer.conversation.connection,/not.*(?:approval|guarantee)|independent.*decision/i);
  assert.ok(includesSource(answer,'../foundation.html'));
  assert.ok(includesSource(answer,'../proofs/EXAMINATION-STANDARD.md'));
});

test('a proof question points to actual pilots, review requirements and repository evidence',()=>{
  const answer=publicVisitorAnswer('Where is the independently reproducible proof?');
  assert.equal(answer.kind,'lesson');
  assert.equal(answer.topic.id,'proof');
  assert.match(answer.conversation.summary,/independent|original|changed.condition/i);
  assert.match(answer.conversation.connection,/source|record|pilot/i);
  for(const href of ['../evidence-hall.html','../proofs/EXAMINATION-STANDARD.md',
    '../proofs/PILOT-EVIDENCE-RELEASE.md','../proofs/HISTORICAL-EVIDENCE-INDEX.md',
    '../proofs/CLAIM-TO-CARRIER.json'])assert.ok(includesSource(answer,href),href);
});

test('a hospital pilot verification request leads to the actual pilot source and witness route',()=>{
  const answer=publicVisitorAnswer('How can I verify your hospital pilot?');
  assert.equal(answer.kind,'lesson');
  assert.equal(answer.topic.id,'pilot');
  assert.ok(includesSource(answer,'../proofs/PILOT-EVIDENCE-RELEASE.md'));
  assert.ok(includesSource(answer,'../proofs/HISTORICAL-PILOT-CARRIER-CROSSWALK.md'));
  assert.match(answer.conversation.summary,/recorded|scope|witness/i);
});

test('P versus NP receives its bounded public status and ongoing mathematical work',()=>{
  const answer=publicVisitorAnswer('Has the Natural Order solved P versus NP?');
  assert.equal(answer.kind,'lesson');
  assert.equal(answer.topic.id,'math-public');
  assert.match(answer.conversation.summary,/unrestricted.*not established|not established.*unrestricted/i);
  assert.ok(includesSource(answer,'../p-versus-np.html'));
  assert.ok(includesSource(answer,'../research/p-versus-np/EXAMINATION-91-PUBLIC-STATUS.md'));
  assert.ok(includesSource(answer,'../research/mathematics/PUBLICATION-STATUS.md'));
});

test('named research lines point to their own published records and scope',()=>{
  const cases=[
    ['What about Navier–Stokes?','../navier-stokes.html',/unrestricted|bounded/i],
    ['Has Yang–Mills been proven?','../yang-mills.html',/unrestricted|continuum/i],
    ['Where is the Riemann Hypothesis answer?','../research/mathematics/PUBLICATION-STATUS.md',/not.*linked|not.*mirrored/i],
    ['What is the Erdős–Straus conjecture?','../math/egyptian-child/index.html',/bounded|unresolved/i],
  ];
  for(const [question,href,status] of cases){
    const answer=publicVisitorAnswer(question);
    assert.equal(answer.topic.id,'math-public',question);
    assert.ok(includesSource(answer,href),question);
    assert.match(answer.conversation.summary,status,question);
  }
});

test('other indexed mathematical research is not misreported as a missing published answer',()=>{
  const cases=[
    ['What is the Admissibility–Debt Geometry theorem?','../admissibility-debt-geometry.html',/conditional|bounded/i],
    ['What is the mathematical result for GRID-K1?','../grid-k1-infrastructure-continuity.html',/finite|conditional/i],
    ['Where is the published theorem for Consequence Signature Calculus?','../consequence-signature-calculus.html',/formal|model/i],
  ];
  for(const [question,href,status] of cases){
    const answer=publicVisitorAnswer(question);
    assert.equal(answer.topic.id,'math-public',question);
    assert.ok(includesSource(answer,href),question);
    assert.match(answer.conversation.summary,status,question);
    assert.doesNotMatch(answer.conversation.summary,/cannot locate/i);
  }
});

test('common mathematical problem spellings retain source and bounded status',()=>{
  for(const question of ['Is P-vs-NP solved?','Is P ≠ NP proved?']){
    const answer=publicVisitorAnswer(question);
    assert.equal(answer.topic.id,'math-public',question);
    assert.ok(includesSource(answer,'../p-versus-np.html'));
    assert.match(answer.conversation.summary,/unrestricted.*not established/i);
  }
});

test('pilot vocabulary about household appliances or woodwork does not hijack evidence routing',()=>{
  for(const question of ['Can you verify my pilot light is safe?','How do I inspect pilot holes in a board?']){
    assert.equal(publicVisitorAnswer(question),null,question);
  }
});

test('an unindexed math question invites a voluntary inquiry without declaring it globally unsolved',()=>{
  const question='Where is the answer to the Goldbach conjecture?';
  const answer=publicVisitorAnswer(question);
  assert.equal(answer.kind,'lesson');
  assert.equal(answer.topic.id,'math-public');
  assert.equal(answer.originalQuestion,question);
  assert.match(answer.conversation.summary,/not located|cannot locate|not indexed/i);
  assert.match(answer.conversation.question,/ask|message|where.*answer/i);
  assert.ok(includesSource(answer,'../mathematics.html'));
  assert.ok(includesSource(answer,'../research/mathematics/INDEX.json'));
  assert.match(answer.conversation.summary,/absence here does not prove/i);
});

test('a normal teaching question is left for the existing lesson router',()=>{
  for(const question of ['What is True Zero?','What is the Natural Order?','What is Proof Before Power?',
    'Why is the river flooding?','Who is Frankie?'])assert.equal(publicVisitorAnswer(question),null,question);
});
