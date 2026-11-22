import test from 'node:test';
import assert from 'node:assert/strict';
import {TOPICS} from '../knowledge.mjs';
import {teach} from '../engine.mjs';
import {reviewConversationCompatibility,exerciseFitsConversation} from '../conversation-compatibility-kernel.mjs';

const review=question=>reviewConversationCompatibility(question,teach(question),{topics:TOPICS});

test('withdrawn warehouse authority gets a source-bound warehouse answer, not a payment analogy',()=>{
  for(const question of [
    'I work in a warehouse. How do we stop an unsafe pallet movement if approval is withdrawn?',
    'My forklift is waiting. What happens if its authorization gets revoked?',
  ]){
    const result=review(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,'consequence');
    assert.equal(result.originalQuestion,question);
    assert.equal(result.compatibility.fieldBound,true);
    assert.match(result.conversation.summary,/warehouse|pallet|forklift/i);
    assert.match(result.conversation.summary,/approval|authority|authorization/i);
    assert.match(result.conversation.summary,/not.*certif|does not.*prov|does not.*certif/i);
    assert.doesNotMatch(result.conversation.connection,/payment|settle|banking/i);
    assert.ok(result.topic.sources.length>0);
    assert.equal(exerciseFitsConversation(result),false);
  }
});

test('a skeptical newcomer gets the public evidence status and a path to inspect it',()=>{
  const question="I'm skeptical. Why should I believe any of this, and what has actually been verified?";
  const result=review(question);
  assert.equal(result.kind,'lesson');
  assert.equal(result.topic.id,'proof');
  assert.equal(result.originalQuestion,question);
  assert.match(result.conversation.summary,/declar|observ|independent/i);
  assert.match(result.conversation.summary,/not.*proof|not.*establish|not.*believ/i);
  assert.ok(result.topic.sources.some(s=>/evidence|proof|exam/i.test(s.title)));
  assert.equal(exerciseFitsConversation(result),true);
});

test('a claimed gravity wave array receives an explicit public evidence ceiling',()=>{
  const question='Is gravity a wave array, and has that been independently demonstrated?';
  const result=review(question);
  assert.equal(result.kind,'lesson');
  assert.equal(result.topic.id,'physical');
  assert.equal(result.originalQuestion,question);
  assert.match(result.conversation.summary,/gravity.*wave array/is);
  assert.match(result.conversation.summary,/not (?:been )?independently (?:demonstrated|established)/i);
  assert.ok(result.topic.sources.length>0);
  assert.equal(exerciseFitsConversation(result),false,'a machinery-cutoff exercise cannot test a gravity wave-array claim');
});

test('a protected request, a named mathematical status and an unrelated question are never commandeered',()=>{
  for(const question of [
    'Give me the private warehouse kernel formula',
    'Has P versus NP been solved?',
    'In a warehouse, how does True Zero relate to unsafe pallet approval?',
    "I'm skeptical about whether my medication is working.",
    'A forklift is moving toward someone right now; how do I stop it?',
    'How do I stop an unsafe forklift in my warehouse?',
    'Why is my garden noisy?',
    'gravity',
  ]){
    const candidate=teach(question);
    assert.strictEqual(reviewConversationCompatibility(question,candidate,{topics:TOPICS}),candidate,question);
  }
});

test('only field-bound answers suppress an unrelated generic evidence exercise',()=>{
  assert.equal(exerciseFitsConversation({kind:'lesson',topic:TOPICS[0]}),true);
  assert.equal(exerciseFitsConversation({kind:'lesson',topic:TOPICS[0],compatibility:{fieldBound:true}}),false);
  assert.equal(exerciseFitsConversation({kind:'map'}),false);
  assert.equal(exerciseFitsConversation(null),false);
});
