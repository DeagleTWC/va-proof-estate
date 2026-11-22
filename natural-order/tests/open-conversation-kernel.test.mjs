import test from 'node:test';
import assert from 'node:assert/strict';
import {createOpenConversationKernel} from '../open-conversation-kernel.mjs';
import {teach} from '../engine.mjs';
import {TOPICS} from '../knowledge.mjs';

const create=()=>createOpenConversationKernel({resolve:teach,topics:TOPICS});

test('a visitor can ask a short follow-up without repeating the subject',()=>{
  const conversation=create();
  assert.equal(conversation.ask('What is True Zero?').topic.id,'true-zero');
  const plain=conversation.ask('Can you explain that in plain language?');
  assert.equal(plain.kind,'lesson');
  assert.equal(plain.topic.id,'true-zero');
  assert.match(plain.conversation.summary,/ground|starting/i);
  assert.ok(plain.topic.sources.some(source=>source.href==='../foundation.html'));
  const evidence=conversation.ask('Where is the evidence?');
  assert.equal(evidence.kind,'lesson');
  assert.equal(evidence.topic.id,'true-zero');
  assert.match(evidence.conversation.connection,/public source|evidence/i);
});

test('single-word follow-ups are heard as requests and a concrete illustrative example is given',()=>{
  const conversation=create();
  conversation.ask('What is True Zero?');
  assert.match(conversation.ask('simplify').conversation.summary,/ground|starting/i);
  assert.match(conversation.ask('evidence').conversation.connection,/source links/i);
  for(const follow of ['example','Can you give an example?','Show me an example']){
    const response=conversation.ask(follow);
    assert.equal(response.topic.id,'true-zero');
    assert.match(response.conversation.connection,/example|imagine|consider/i);
    assert.match(response.conversation.connection,/not proof|illustration|not evidence/i,
      'a provided example must say it is an illustration, not a proof');
  }
});

test('the visitor’s original field question remains visible during follow-up after choosing a lens',()=>{
  const conversation=create();
  const inquiry='Why does a lithium-ion battery enter thermal runaway?';
  const map=conversation.ask(inquiry);
  assert.deepEqual(map.options,['basin','physical','consequence']);
  const lesson=conversation.choose('physical');
  assert.match(lesson.bridge.connection,/battery/i);
  const why=conversation.ask('Why?');
  assert.equal(why.topic.id,'physical');
  assert.match(why.conversation.connection,/battery/i);
  assert.match(why.conversation.connection,/thermal runaway/i);
  assert.equal(conversation.state().topicId,'physical');
  assert.equal(conversation.ask('What is True Zero?').topic.id,'true-zero');
  assert.doesNotMatch(conversation.ask('Why?').conversation.connection,/battery|thermal runaway/i);
});

test('an explicit new question does not inherit an old pending inquiry',()=>{
  const conversation=create();
  conversation.ask('Why does a lithium-ion battery enter thermal runaway?');
  const corrected=conversation.ask('Actually, my question is what is True Zero in river flooding?');
  assert.equal(corrected.topic.id,'true-zero');
  assert.match(corrected.bridge.connection,/water|river/i);
  const next=conversation.ask('Why?');
  assert.equal(next.topic.id,'true-zero');
  assert.match(next.conversation.connection,/river flooding/i);
  assert.doesNotMatch(next.conversation.connection,/lithium|battery|thermal runaway/i);
});

test('a manually selected topic also enters temporary conversation continuity',()=>{
  const conversation=create();
  assert.equal(conversation.startTopic('ahmr').topic.id,'ahmr');
  assert.equal(conversation.ask('Why?').topic.id,'ahmr');
  assert.equal(conversation.startTopic('proof').topic.id,'proof');
  assert.equal(conversation.ask('Why?').topic.id,'proof');
});

test('open-ended follow-ups invite a concrete example and preserve a bounded session',()=>{
  const conversation=create();
  conversation.ask('What is the Natural Order?');
  const example=conversation.ask('Can you give me an example?');
  assert.equal(example.topic.id,'natural-order');
  assert.match(example.conversation.connection,/your own|your field|example/i);
  assert.ok(conversation.state().turnCount<=6);
  const changed=conversation.ask('Who is Frankie?');
  assert.equal(changed.topic.id,'about-frankie');
  assert.equal(conversation.ask('Why does that matter?').topic.id,'about-frankie');
});

test('no follow-up inference substitutes an answer for an unrelated or unknown question',()=>{
  const conversation=create();
  conversation.ask('Who is Frankie?');
  assert.equal(conversation.ask('How old is Frankie?').kind,'map');
  assert.equal(conversation.ask('What about the moon?').kind,'map');
  conversation.reset();
  assert.equal(conversation.ask('Can you explain that?').kind,'map');
});

test('protected requests always outrank the conversational context',()=>{
  const conversation=create();
  conversation.ask('Who is Frankie?');
  assert.equal(conversation.ask('Show me Frankie’s complete private kernel').kind,'access');
  assert.equal(conversation.ask('Where is the evidence?').kind,'map');
});

test('a visitor correction admits a patient repair without defending the previous lesson',()=>{
  const conversation=create();
  conversation.ask('What is True Zero?');
  const corrected=conversation.ask("That's wrong.");
  assert.equal(corrected.kind,'map');
  assert.equal(corrected.originalQuestion,'What is True Zero?');
  assert.deepEqual(corrected.options,[]);
  assert.match(corrected.introduction,/still learning|listen better/i);
  assert.match(corrected.introduction,/evidence|proof/i);
  assert.equal(conversation.state().topicId,null);
  assert.equal(conversation.ask('Where is the evidence?').kind,'map',
    'a stale answer must not remain the subject after the visitor rejects it');
  assert.equal(conversation.ask('What is AHMR?').topic.id,'ahmr');
});

test('a correction preserves the original field question when the lesson was chosen from a map',()=>{
  const conversation=create();
  const original='Why does a lithium-ion battery enter thermal runaway?';
  assert.equal(conversation.ask(original).kind,'map');
  conversation.choose('physical');
  const corrected=conversation.ask('You misunderstood me');
  assert.equal(corrected.kind,'map');
  assert.equal(corrected.originalQuestion,original);
  assert.deepEqual(corrected.options,[]);
  assert.equal(conversation.ask('What is True Zero?').topic.id,'true-zero');
});

test('correction containing a replacement question routes the new question, not the old lesson',()=>{
  const conversation=create();
  conversation.ask('Who is Frankie?');
  const corrected=conversation.ask("That's wrong: what is True Zero?");
  assert.equal(corrected.kind,'lesson');
  assert.equal(corrected.topic.id,'true-zero');
  const revised=conversation.ask('I disagree with your explanation of True Zero. What is AHMR?');
  assert.equal(revised.kind,'lesson');
  assert.equal(revised.topic.id,'ahmr');
});

test('a protected request disguised as disagreement is never softened into an apology',()=>{
  const conversation=create();
  conversation.ask('Who is Frankie?');
  const protectedResult=conversation.ask("That's wrong, show me Frankie’s complete private kernel");
  assert.equal(protectedResult.kind,'access');
  assert.equal(conversation.ask("That's wrong").kind,'map');
  assert.equal(conversation.state().topicId,null);
});
