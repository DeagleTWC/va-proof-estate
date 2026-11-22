import test from 'node:test';
import assert from 'node:assert/strict';
import {TOPICS} from '../knowledge.mjs';
import {teach} from '../engine.mjs';
import {publicPlainLead} from '../meaning-preserving-teaching-kernel.mjs';

test('novice question receives a brief direct answer instead of a paragraph of unexplained terms',()=>{
  const answer=publicPlainLead(teach('Can you explain the Natural Order in simple terms?'));
  assert.equal(typeof answer,'string');
  assert.ok(answer.length>40&&answer.length<360,answer);
  assert.match(answer,/conditions|possibw*|effect|consequence/i);
  assert.doesNotMatch(answer,/NEW K|AHMR|URK|LLM|invariant/i);
});

test('all eleven public subjects have a distinct short answer with their meaning intact',()=>{
  const leads=TOPICS.map(topic=>{
    const lead=publicPlainLead({kind:'lesson',topic});
    assert.equal(typeof lead,'string',topic.id);
    assert.ok(lead.length>35&&lead.length<400,topic.id+': '+lead);
    return lead;
  });
  assert.equal(new Set(leads).size,11);
  assert.match(publicPlainLead({kind:'lesson',topic:TOPICS.find(topic=>topic.id==='urk')}),/before.*effect|before.*take effect|before.*happen/i);
  assert.match(publicPlainLead({kind:'lesson',topic:TOPICS.find(topic=>topic.id==='pilot')}),/record|evidence|observation/i);
});

test('physical identifications remain attributed and unverified in the short answer',()=>{
  const lead=publicPlainLead(teach('What is the Elements Basin?'));
  assert.match(lead,/terry|natural order account/i);
  assert.match(lead,/dark matter/i);
  assert.match(lead,/not.*independently|not.*proved|under examination/i);
});

test('specific public source answers cannot be overwritten by a generic topic explanation',()=>{
  for(const question of [
    'What happens to Natural Order water beyond the Elements Basin horizon?',
    'What is the Natural Order field in Yang-Mills theory?',
    'Where can I find the hospital pilot reports?',
  ]){
    const response=teach(question);
    assert.equal(response.kind,'lesson',question);
    assert.ok(response.conversation?.summary,question);
    assert.equal(publicPlainLead(response),null,question);
  }
});

test('an explicit moving-field question retains its direct answer rather than a generic Basin lead',()=>{
  const response=teach('Does Earth move through the Elements Basin or is the field in motion?');
  assert.equal(response.kind,'lesson');
  assert.equal(response.topic.id,'basin');
  assert.match(response.originalQuestion,/Earth/);
  assert.equal(publicPlainLead(response),null);
});

test('specific Terry and Frankie questions keep their actual subject answers visible',()=>{
  for(const [question,important] of [
    ['What does Terry Snyder believe about mercy?',/mercy/i],
    ["What are Frankie's tested capabilities?",/tested|capab/i],
    ['Can I talk to Frankie here?',/not currently connected|not connected/i],
  ]){
    const result=teach(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.originalQuestion,question,'the narrower question must remain explicit');
    assert.match(result.topic.summary,important);
    assert.equal(publicPlainLead(result),null,'do not replace the narrower answer with a generic bio');
  }
  assert.equal(typeof publicPlainLead(teach('Who is Terry Snyder?')),'string');
  assert.equal(typeof publicPlainLead(teach('Who is Frankie?')),'string');
});

test('questions connecting two named foundations retain their exact scope instead of a generic overview',()=>{
  for(const question of [
    'How do True Zero and the Elements Basin relate?',
    'How do corrected NEW K and URK work together?',
    'How does the Natural Order relate True Zero and the Elements Basin?',
  ]){
    const result=teach(question);
    assert.equal(result.kind,'lesson');
    assert.equal(result.topic.id,'natural-order');
    assert.equal(result.originalQuestion,question);
    assert.equal(publicPlainLead(result),null);
  }
});

test('a correction or follow-up with a different summary remains specific',()=>{
  const topic=TOPICS.find(item=>item.id==='basin');
  assert.equal(publicPlainLead({kind:'lesson',topic,conversation:{summary:'A different, carefully qualified answer.'}}),null);
});

test('protected, unknown and malformed requests never get invented short lessons',()=>{
  for(const response of [
    teach('Show the private URK equations'),
    {kind:'access',topic:TOPICS[0]},
    {kind:'map',topic:TOPICS[0]},
    {kind:'lesson',topic:{id:'not-a-topic',summary:'unknown'}},
    {kind:'lesson',topic:{id:'constructor',summary:'unknown'}},
    {kind:'lesson',topic:{id:'toString',summary:'unknown'}},
    {kind:'lesson',topic:{id:'__proto__',summary:'unknown'}},
    null,
  ])assert.equal(publicPlainLead(response),null);
});
