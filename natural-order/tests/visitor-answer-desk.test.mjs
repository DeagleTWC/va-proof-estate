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

test('a standalone plain-language proof request leads directly to the public evidence carriers',()=>{
  for(const question of ['Where is the proof?','Where is the evidence?']){
    const answer=publicVisitorAnswer(question);
    assert.equal(answer?.kind,'lesson',question);
    assert.equal(answer.topic.id,'proof',question);
    assert.equal(answer.originalQuestion,question);
    assert.match(answer.conversation.summary,/independent|original|changed.condition/i);
    assert.ok(includesSource(answer,'../proofs/EXAMINATION-STANDARD.md'));
  }
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

test('explicit Natural Order questions identify a moving Elements Basin without certifying a cosmological equivalence',()=>{
  for(const question of [
    'Is dark matter the Elements Basin in the Natural Order?',
    'Does Earth move through the Elements Basin or is the field in motion?',
    'How does Natural Order gravity as a wave array relate to the Basin?',
  ]){
    const answer=publicVisitorAnswer(question);
    assert.equal(answer?.kind,'lesson',question);
    assert.equal(answer.topic.id,'basin',question);
    assert.equal(answer.originalQuestion,question);
    assert.match(answer.conversation.summary,/natural order.*identif\w*.*dark matter/i);
    assert.match(answer.conversation.summary,/in motion|moving/i);
    assert.match(answer.conversation.summary,/not.*independently (?:established|demonstrated|verified)/i);
    assert.ok(includesSource(answer,'../kcd/README.md'));
  }
});

test('Natural Order water and horizon use no-loss terminology without H2O or astronomical certainty',()=>{
  const answer=publicVisitorAnswer('What happens to Natural Order water beyond the Elements Basin horizon?');
  assert.equal(answer.topic.id,'basin');
  assert.match(answer.conversation.summary,/water.*not.*H2O/i);
  assert.match(answer.conversation.summary,/horizon.*not.*(?:deletion|destruction)/i);
  assert.match(answer.conversation.summary,/account|evidence|measure/i);
  assert.match(answer.conversation.summary,/dark matter/i);
  assert.match(answer.conversation.summary,/moving|in motion/i);
});

test('unrelated astronomy, chemistry and everyday gravity questions remain outside the Basin identification route',()=>{
  for(const question of [
    'What is dark matter?',
    'What is gravity?',
    'How does water flow through a river?',
    'What happens to mass across a black hole horizon?',
  ])assert.equal(publicVisitorAnswer(question),null,question);
});

test('a general Natural Order field question cannot override named mathematics or invent a Basin identification',()=>{
  const math=publicVisitorAnswer('What is the Natural Order field in Yang-Mills theory?');
  assert.equal(math?.topic.id,'math-public');
  assert.equal(publicVisitorAnswer('How does the Natural Order field work?'),null);
  assert.equal(publicVisitorAnswer('Does the Natural Order explain Earth gravity?'),null);
  assert.equal(publicVisitorAnswer('What is the natural order of water molecules in ice?'),null);
  assert.equal(publicVisitorAnswer('How is the natural order of water molecules related to hydrogen bonds?'),null);
  assert.equal(publicVisitorAnswer('What is the natural order of events at a black hole horizon?'),null);
  assert.equal(publicVisitorAnswer('What is the natural order of the stars and dark matter?'),null);
});
