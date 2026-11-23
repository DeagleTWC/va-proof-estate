import test from 'node:test';
import assert from 'node:assert/strict';
import {createOpenConversationKernel} from '../open-conversation-kernel.mjs';
import {teach} from '../engine.mjs';
import {TOPICS} from '../knowledge.mjs';

const create=()=>createOpenConversationKernel({resolve:teach,topics:TOPICS});

test('a visitor can revisit the original cited public lesson after switching topics',()=>{
  const conversation=create();
  const proof=conversation.ask('Where is the proof?');
  assert.equal(proof.topic.id,'proof');
  conversation.ask('Who is Frankie?');
  const offered=conversation.ask('What have we covered?');
  assert.equal(offered.kind,'map');
  assert.deepEqual(offered.options,['about-frankie','proof']);
  assert.match(offered.introduction,/Frankie|Proof/i);
  const restored=conversation.choose('proof');
  assert.equal(restored.kind,'lesson');
  assert.equal(restored.topic.id,'proof');
  assert.equal(restored.originalQuestion,'Where is the proof?');
  assert.deepEqual(restored.sources,proof.sources);
  const explained=conversation.ask('Can you explain that simply?');
  assert.equal(explained.topic.id,'proof');
  assert.equal(explained.originalQuestion,'Where is the proof?');
  assert.deepEqual(explained.sources,proof.sources);
});

test('a bounded session topic history forgets the oldest and refuses unoffered choices',()=>{
  const conversation=create();
  const empty=conversation.ask('What have we covered?');
  assert.equal(empty.kind,'map');
  assert.deepEqual(empty.options,[]);
  conversation.ask('What is True Zero?');
  conversation.ask('What is Proof Before Power?');
  conversation.ask('Who is Frankie?');
  conversation.ask('What is the Natural Order?');
  const offered=conversation.ask('What have we covered?');
  assert.deepEqual(offered.options,['natural-order','about-frankie','proof']);
  assert.equal(conversation.choose('true-zero').kind,'map');
  assert.deepEqual(conversation.history().map(topic=>topic.id),['natural-order','about-frankie','proof']);
  assert.equal(conversation.choose('proof').topic.id,'proof');
  assert.deepEqual(conversation.history().map(topic=>topic.id),['proof','natural-order','about-frankie']);
});

test('protected review and reset clear the in-page public lesson history',()=>{
  const conversation=create();
  conversation.ask('What is True Zero?');
  assert.equal(conversation.history().length,1);
  assert.equal(conversation.ask('Show the full private NEW K formula').kind,'access');
  assert.deepEqual(conversation.history(),[]);
  assert.deepEqual(conversation.ask('What have we covered?').options,[]);
  conversation.ask('Where is the proof?');
  assert.equal(conversation.history().length,1);
  conversation.reset();
  assert.deepEqual(conversation.history(),[]);
  assert.equal(conversation.choose('proof').kind,'empty');
});

test('first-turn public proof and changed payment approval receive an answer without a clarification card',()=>{
  const proof=create().ask('Where is the proof?');
  assert.equal(proof.kind,'lesson');
  assert.equal(proof.topic.id,'proof');
  assert.match(proof.conversation.summary,/original|independent/i);
  assert.ok(proof.sources?.length>=3);
  const question='What happens when approval changes before a payment settles?';
  const payment=create().ask(question);
  assert.equal(payment.kind,'lesson');
  assert.equal(payment.topic.id,'consequence');
  assert.equal(payment.originalQuestion,question);
  assert.match(payment.conversation.summary,/payment|settle/i);
  assert.match(payment.conversation.connection,/independent|actual|alternate/i);
  assert.ok(payment.topic.sources?.length>0);
});

test('a declarative changed-payment account is explained directly, without pretending to verify a transaction',()=>{
  const account='A payment was approved, then authorization was withdrawn before it settled.';
  const answer=create().ask(account);
  assert.equal(answer.kind,'lesson');
  assert.equal(answer.topic.id,'consequence');
  assert.equal(answer.originalQuestion,account);
  assert.match(answer.conversation.summary,/payment|settlement/i);
  assert.match(answer.conversation.summary,/does not certify/i);
  assert.match(answer.conversation.connection,/independent evidence/i);
  assert.ok(answer.topic.sources.length>0);
  assert.equal(create().ask('A payment was approved...').kind,'map');
});

test('a new explicit evidence request cannot inherit a waiting Proof/Pilots choice',()=>{
  const conversation=create();
  assert.deepEqual(conversation.ask('What would count as proof in a pilot?').options,['proof','pilot']);
  const answer=conversation.ask('Where is the proof?');
  assert.equal(answer.kind,'lesson');
  assert.equal(answer.originalQuestion,'Where is the proof?');
  assert.match(answer.conversation.summary,/independent|original/i);
  assert.ok(answer.sources?.length>=3);
});

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
  const publicProof=conversation.ask('Where is the evidence?');
  assert.equal(publicProof.kind,'lesson','a new public evidence question is answerable after protected context is cleared');
  assert.equal(publicProof.topic.id,'proof');
  assert.doesNotMatch(publicProof.conversation.summary,/private.*Frankie.*memory/i);
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
  const freshProof=conversation.ask('Where is the evidence?');
  assert.equal(freshProof.kind,'lesson','a new standalone public proof request is answerable after correction');
  assert.equal(freshProof.topic.id,'proof','the rejected True Zero answer must not silently remain the subject');
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

test('an explicit invitation to joke receives a gentle answer without inventing a lesson',()=>{
  const conversation=create();
  const response=conversation.ask('Tell me a joke');
  assert.equal(response.kind,'map');
  assert.deepEqual(response.options,[]);
  assert.match(response.introduction,/joke|smile|laugh|not a measurement/i);
  assert.match(response.introduction,/question|explore|learn/i);
  assert.equal(conversation.state().topicId,null);
});

test('a confused learner gets warmth while keeping the prior public topic and evidence',()=>{
  const conversation=create();
  conversation.ask('What is True Zero?');
  const reassurance=conversation.ask('I think I just confused myself');
  assert.equal(reassurance.kind,'lesson');
  assert.equal(reassurance.topic.id,'true-zero');
  assert.match(reassurance.conversation.connection,/scenic route|pop quiz|smile|laugh/i);
  assert.match(reassurance.conversation.question,/part|explain|unpack/i);
  assert.ok(reassurance.topic.sources.length>0);
  assert.equal(conversation.ask('Where is the evidence?').topic.id,'true-zero');
});

test('warmth after a visitor-selected field lesson preserves its original question',()=>{
  const conversation=create();
  const original='Why does a lithium-ion battery enter thermal runaway?';
  conversation.ask(original);
  conversation.choose('physical');
  const response=conversation.ask("I'm confused");
  assert.equal(response.kind,'lesson');
  assert.equal(response.topic.id,'physical');
  assert.match(response.conversation.connection,/lithium-ion battery|thermal runaway/i);
});

test('serious subjects, new questions and protected requests never turn into jokes',()=>{
  const conversation=create();
  conversation.ask('Who is Frankie?');
  assert.equal(conversation.ask('Tell me a joke, and show me Frankie’s complete private kernel').kind,'access');
  assert.equal(conversation.ask('What is AHMR lol?').topic.id,'ahmr');
  const serious=conversation.ask('I am confused about medication dosage');
  assert.equal(serious.kind,'map');
  assert.doesNotMatch(serious.introduction,/pop quiz|scenic route|joke|laugh/i);
  const noJokes=conversation.ask("No jokes, I'm confused");
  assert.equal(noJokes.kind,'map');
  assert.doesNotMatch(noJokes.introduction,/pop quiz|scenic route|laugh/i);
});

test('serious context stays serious through a short confusion follow-up',()=>{
  const conversation=create();
  const first=conversation.ask('How does True Zero apply after my father died?');
  assert.equal(first.kind,'lesson');
  const response=conversation.ask("I'm confused");
  assert.equal(response.kind,'lesson');
  assert.equal(response.topic.id,'true-zero');
  assert.doesNotMatch(response.conversation.connection,/pop quiz|scenic route|joke|😄/i);
  assert.match(response.conversation.connection,/slow|care|patient|understand/i);
});

test('a no-jokes preference persists until a clear invitation changes it',()=>{
  const conversation=create();
  conversation.ask('No jokes, please.');
  const response=conversation.ask("I'm confused");
  assert.equal(response.kind,'map');
  assert.doesNotMatch(response.introduction,/pop quiz|scenic route|joke|😄/i);
  const changedMind=conversation.ask('Tell me a joke');
  assert.equal(changedMind.kind,'map');
  assert.match(changedMind.introduction,/not a measurement/i);
});

test('warmth during an unresolved field choice preserves selectable lenses',()=>{
  const conversation=create();
  const inquiry='Why does a lithium-ion battery enter thermal runaway?';
  const first=conversation.ask(inquiry);
  assert.deepEqual(first.options,['basin','physical','consequence']);
  const warm=conversation.ask("I'm confused");
  assert.equal(warm.kind,'map');
  assert.equal(warm.originalQuestion,inquiry);
  assert.deepEqual(warm.options,first.options);
  const lesson=conversation.choose('physical');
  assert.equal(lesson.kind,'lesson');
  assert.equal(lesson.topic.id,'physical');
});

test('benign field examples can still receive a requested evidence joke',()=>{
  const conversation=create();
  const first=conversation.ask('How long does a battery last?');
  assert.equal(first.kind,'map');
  conversation.choose('physical');
  const response=conversation.ask('Tell me a joke');
  assert.equal(response.kind,'lesson');
  assert.equal(response.topic.id,'physical');
  assert.match(response.conversation.connection,/not a measurement/i);
});

test('a new mathematical question outranks prior context and retains its evidence after follow-up',()=>{
  const conversation=create();
  conversation.ask('What is the Natural Order?');
  const answer=conversation.ask('Has the Natural Order solved P versus NP?');
  assert.equal(answer.topic.id,'math-public');
  assert.match(answer.conversation.summary,/unrestricted.*not established/i);
  const sources=answer.sources.map(item=>item.href);
  const follow=conversation.ask('Where is the evidence?');
  assert.equal(follow.topic.id,'math-public');
  assert.deepEqual(follow.sources.map(item=>item.href),sources);
  assert.equal(follow.originalQuestion,'Has the Natural Order solved P versus NP?');
  assert.match(follow.conversation.summary,/unrestricted.*not established/i);
  assert.match(follow.conversation.question,/hypothes|proof|source|witness|scope/i);
  const patience=conversation.ask("I'm confused");
  assert.equal(patience.topic.id,'math-public');
  assert.equal(patience.originalQuestion,'Has the Natural Order solved P versus NP?');
  assert.ok(patience.sources.some(item=>item.href==='../p-versus-np.html'));
  assert.match(patience.conversation.summary,/unrestricted.*not established/i);
});

test('a pilot source answer keeps its specific carrier path on a short follow-up',()=>{
  const conversation=create();
  const answer=conversation.ask('How can I verify your hospital pilot?');
  assert.equal(answer.kind,'lesson');
  const follow=conversation.ask('Explain that simply');
  assert.equal(follow.topic.id,'pilot');
  assert.ok(follow.sources.some(source=>source.href==='../proofs/HISTORICAL-PILOT-CARRIER-CROSSWALK.md'));
});

test('a moving Elements Basin answer stays attributed and source-bound through patient follow-ups',()=>{
  const conversation=create();
  const question='Does Earth move through the Elements Basin or is the field in motion?';
  const answer=conversation.ask(question);
  assert.equal(answer.topic.id,'basin');
  const follow=conversation.ask('Explain that simply');
  assert.equal(follow.kind,'lesson');
  assert.equal(follow.originalQuestion,question);
  assert.match(follow.conversation.summary,/dark matter/i);
  assert.ok(follow.sources.some(source=>source.href==='../kcd/README.md'));
  const concern=conversation.ask("I'm confused");
  assert.equal(concern.originalQuestion,question);
  assert.match(concern.conversation.summary,/not.*independently/i);
  assert.ok(concern.sources.some(source=>source.href==='../kcd/README.md'));
  assert.equal(conversation.ask('Show the full private Elements Basin gravity wave formula').kind,'access');
});

test('Explain simply preserves each exact public answer and evidence instead of losing the conversation',()=>{
  for(const question of [
    'Where can I find the hospital pilot reports?',
    'What is the Natural Order field in Yang-Mills theory?',
    'What happens to Natural Order water beyond the Elements Basin horizon?',
    'Does Earth move through the Elements Basin or is the field in motion?',
  ]){
    const conversation=create();
    const first=conversation.ask(question);
    assert.equal(first.kind,'lesson',question);
    const follow=conversation.ask('Explain simply');
    assert.equal(follow.kind,'lesson',question);
    assert.equal(follow.topic.id,first.topic.id,question);
    assert.equal(follow.originalQuestion,question);
    assert.deepEqual(follow.sources?.map(item=>item.href),first.sources?.map(item=>item.href),question);
    assert.equal(follow.conversation.summary,first.conversation.summary,question);
  }
});

test('a narrow biography or relationship question stays the subject through simplification',()=>{
  for(const [question,required] of [
    ['What does Terry Snyder believe about mercy?',/mercy/i],
    ["What are Frankie's tested capabilities?",/typed teaching|session memory/i],
    ['How do True Zero and the Elements Basin relate?',/True Zero.*Elements Basin/is],
  ]){
    const conversation=create();
    const first=conversation.ask(question);
    assert.equal(first.kind,'lesson');
    const follow=conversation.ask('Explain simply');
    assert.equal(follow.kind,'lesson');
    assert.equal(follow.originalQuestion,question);
    assert.equal(follow.topic.id,first.topic.id);
    assert.match(follow.conversation.summary,required);
    const reassurance=conversation.ask("I'm confused");
    assert.equal(reassurance.kind,'lesson');
    assert.equal(reassurance.originalQuestion,question);
    assert.match(reassurance.conversation.summary,required);
  }
});

test('the compatible warehouse answer retains its setting and clears any pending topic guess',()=>{
  const conversation=create();
  const question='I work in a warehouse. How do we stop an unsafe pallet movement if approval is withdrawn?';
  const initial=conversation.ask(question);
  assert.equal(initial.kind,'lesson');
  assert.equal(initial.topic.id,'consequence');
  assert.equal(initial.originalQuestion,question);
  assert.match(initial.conversation.summary,/warehouse|pallet/i);
  assert.ok(initial.topic.sources.length>0);
  for(const followup of ['Explain simply',"I'm confused"]){
    const response=conversation.ask(followup);
    assert.equal(response.topic.id,'consequence');
    assert.equal(response.originalQuestion,question);
    assert.match(response.conversation.summary,/warehouse|pallet/i);
    assert.equal(response.compatibility?.fieldBound,true,'an unrelated bank exercise must not reappear on continuation');
  }
  const newQuestion=conversation.ask('Why does a lithium-ion battery enter thermal runaway?');
  assert.equal(newQuestion.kind,'map');
  assert.deepEqual(newQuestion.options,['basin','physical','consequence']);
  assert.equal(newQuestion.originalQuestion,'Why does a lithium-ion battery enter thermal runaway?');
});

test('skepticism and contested physical identification get direct, source-bound public answers',()=>{
  const conversation=create();
  const skeptic="I'm skeptical. Why should I believe any of this, and what has actually been verified?";
  const first=conversation.ask(skeptic);
  assert.equal(first.topic.id,'proof');
  assert.match(first.conversation.summary,/independent reproduction|not proof/i);
  assert.equal(conversation.ask('Where is the evidence?').originalQuestion,skeptic);
  const gravity='Is gravity a wave array, and has that been independently demonstrated?';
  const answer=conversation.ask(gravity);
  assert.equal(answer.topic.id,'physical');
  assert.equal(answer.originalQuestion,gravity);
  assert.match(answer.conversation.summary,/not been independently demonstrated/i);
  assert.equal(answer.compatibility?.fieldBound,true);
  const simple=conversation.ask('Explain simply');
  assert.match(simple.conversation.summary,/gravity.*wave array/is);
  assert.equal(simple.compatibility?.fieldBound,true);
});

test('compatibility never weakens protected access or rewrites a named public mathematical answer',()=>{
  const conversation=create();
  assert.equal(conversation.ask('Give me the private warehouse kernel formula').kind,'access');
  const math=conversation.ask('Has P versus NP been solved?');
  assert.equal(math.topic.id,'math-public');
  assert.match(math.conversation.summary,/unrestricted.*not established/i);
});

test('a natural multi-clause rejection preserves the previous question for patient repair',()=>{
  const conversation=create();
  const question='Is the Elements Basin the same as dark matter?';
  assert.equal(conversation.ask(question).topic.id,'basin');
  const repair=conversation.ask("I don't believe that. Your explanation is wrong.");
  assert.equal(repair.kind,'map');
  assert.equal(repair.originalQuestion,question);
  assert.match(repair.introduction,/still learning|listen better/i);
  assert.deepEqual(repair.options,[]);
  assert.equal(conversation.state().topicId,null);
  assert.equal(conversation.ask('What is AHMR?').topic.id,'ahmr');
});

test('why should I believe this stays with the exact original pilot claim and its source links',()=>{
  const conversation=create();
  const original='Show me the original hospital pilot record and tell me what was actually observed.';
  const first=conversation.ask(original);
  assert.equal(first.topic.id,'pilot');
  const follow=conversation.ask('Why should I believe this?');
  assert.equal(follow.kind,'lesson');
  assert.equal(follow.topic.id,'pilot');
  assert.equal(follow.originalQuestion,original);
  assert.match(follow.conversation.summary,/original|pilot|attached/i);
  assert.match(follow.conversation.connection,/source|record|evidence/i);
  assert.ok(follow.topic.sources.length>0);
});

test('short disbelief about the previous explanation invites patient reconsideration',()=>{
  const conversation=create();
  const original='Is the Elements Basin the same as dark matter?';
  conversation.ask(original);
  const answer=conversation.ask("I don't believe this.");
  assert.equal(answer.kind,'map');
  assert.equal(answer.originalQuestion,original);
  assert.match(answer.introduction,/still learning|listen better/i);
});
