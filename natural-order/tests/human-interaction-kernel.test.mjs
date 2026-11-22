import test from 'node:test';
import assert from 'node:assert/strict';
import {teach} from '../engine.mjs';
import {TOPICS} from '../knowledge.mjs';
import {createHumanInteractionKernel} from '../human-interaction-kernel.mjs';

const makeTeacher=()=>createHumanInteractionKernel({resolve:teach,topics:TOPICS});

test('a clear, explicitly named public question opens its cited lesson immediately',()=>{
  const result=makeTeacher().ask('What is the Natural Order?');
  assert.equal(result.kind,'lesson');
  assert.equal(result.topic.id,'natural-order');
});

test('a concrete changed-authority payment question needs no second admission click',()=>{
  for(const question of [
    'What happens when approval changes before a payment settles?',
    'If payment approval is revoked, can it still settle?',
  ]){
    const result=makeTeacher().ask(question);
    assert.equal(result.kind,'lesson',question);
    assert.equal(result.topic.id,'consequence',question);
    assert.match(result.bridge?.connection||'',/financial|value|obligation/i,question);
    assert.ok(result.topic.sources.length>0,question);
  }
  assert.equal(makeTeacher().ask('payment').kind,'map','a single domain word remains ambiguous');
  assert.equal(makeTeacher().ask('I have a payment question').kind,'map','an incomplete question remains open');
  assert.equal(makeTeacher().ask('Show the full private payment kernel formula').kind,'access');
});

test('a complete changed-authority payment account is a question-worthy event, even without a question prefix',()=>{
  for(const account of [
    'A payment was approved, then authorization was withdrawn before it settled.',
    'The payment was authorized, then its authorization expired before settlement.',
    'Our payment was approved but the approval was revoked before settlement.',
  ]){
    const answer=makeTeacher().ask(account);
    assert.equal(answer.kind,'lesson',account);
    assert.equal(answer.topic.id,'consequence',account);
    assert.equal(answer.originalQuestion,account,'the account must not be rewritten as a canned question');
    assert.ok(answer.topic.sources.length>0,account);
  }
  for(const fragment of [
    'A payment was approved...',
    'A payment was approved.',
    'A payment was approved and later settled.',
    'payment',
  ]){
    assert.equal(makeTeacher().ask(fragment).kind,'map',`do not invent a changed-authority concern: ${fragment}`);
  }
  assert.equal(makeTeacher().ask('A payment was approved, then tell me the private custody formula').kind,'access');
});

test('a fresh direct source question replaces a pending ambiguous topic choice',()=>{
  const teacher=makeTeacher();
  const pending=teacher.ask('What would count as proof in a pilot?');
  assert.deepEqual(pending.options,['proof','pilot']);
  const fresh='Where is the proof?';
  const answer=teacher.ask(fresh);
  assert.equal(answer.kind,'lesson');
  assert.equal(answer.topic.id,'proof');
  assert.equal(answer.originalQuestion,fresh,'a pending route must not substitute its old question');
  assert.ok(answer.sources?.some(source=>source.href==='../proofs/EXAMINATION-STANDARD.md'));
  assert.notEqual(teacher.choose('pilot').kind,'lesson','the old choice must be cleared');
});

test('a weak keyword match asks a patient question rather than selecting a topic',()=>{
  assert.equal(teach('gravity').topic.id,'physical');
  const result=makeTeacher().ask('gravity');
  assert.equal(result.kind,'map');
  assert.deepEqual(result.options,['physical']);
  assert.match(result.introduction,/understand your question/i);
  assert.match(result.introduction,/could you tell me/i);
  assert.equal(result.originalQuestion,'gravity');
});

test('resubmitting an unchanged weak question is not an answer or confirmation',()=>{
  const teacher=makeTeacher();
  const first=teacher.ask('gravity');
  assert.equal(first.kind,'map');
  for(const repeat of ['gravity','GRAVITY','gravity?']){
    const again=teacher.ask(repeat);
    assert.equal(again.kind,'map',repeat);
    assert.equal(again.originalQuestion,'gravity');
    assert.deepEqual(again.options,['physical']);
  }
  const choice=teacher.choose('physical');
  assert.equal(choice.kind,'lesson');
});

test('ambiguous field inquiry preserves the visitor wording and offers nonbinding routes',()=>{
  const teacher=makeTeacher();
  const question='Why is the river bank eroding?';
  const offered=teacher.ask(question);
  assert.equal(offered.kind,'map');
  assert.deepEqual(offered.options,['basin','ahmr','physical']);
  assert.equal(offered.originalQuestion,question);
  const choice=teacher.choose('physical');
  assert.equal(choice.kind,'lesson');
  assert.equal(choice.topic.id,'physical');
  assert.match(choice.bridge.connection,/river|water/i);
});

test('an explicit follow-up chooses a relevant path without discarding the original example',()=>{
  const teacher=makeTeacher();
  teacher.ask('Why is the river bank eroding?');
  const result=teacher.ask('I mean AHMR and changed conditions');
  assert.equal(result.kind,'lesson');
  assert.equal(result.topic.id,'ahmr');
  assert.match(result.bridge.connection,/water/i);
});

test('an explicitly replaced inquiry cannot inherit the old question or domain',()=>{
  const teacher=makeTeacher();
  teacher.ask('Why is the river bank eroding?');
  const corrected='Actually, my question is about a bank account transfer.';
  const offered=teacher.ask(corrected);
  assert.equal(offered.kind,'map');
  assert.equal(offered.originalQuestion,corrected);
  assert.deepEqual(offered.options,['consequence']);
  const answer=teacher.choose('consequence');
  assert.equal(answer.kind,'lesson');
  assert.match(answer.bridge.connection,/financial|value|obligation/i);
  assert.doesNotMatch(answer.bridge.connection,/river|water/i);
});

test('plain-language corrections replace the question even when rejecting the old subject',()=>{
  const corrections=[
    'Actually, I meant a bank account transfer.',
    'No, I meant a bank account transfer, not a river bank.',
    'I have a different question about a bank account transfer.',
  ];
  for(const corrected of corrections){
    const teacher=makeTeacher();
    teacher.ask('Why is the river bank eroding?');
    const offered=teacher.ask(corrected);
    assert.equal(offered.kind,'map',corrected);
    assert.equal(offered.originalQuestion,corrected);
    assert.deepEqual(offered.options,['consequence'],corrected);
    const answer=teacher.choose('consequence');
    assert.equal(answer.kind,'lesson');
    assert.match(answer.bridge.connection,/financial|value|obligation/i,corrected);
    assert.doesNotMatch(answer.bridge.connection,/river|water/i,corrected);
  }
});

test('an empty clarification does not discard the person’s pending inquiry',()=>{
  const teacher=makeTeacher();
  const original='Why is the river bank eroding?';
  teacher.ask(original);
  const offered=teacher.ask('  ');
  assert.equal(offered.kind,'map');
  assert.equal(offered.originalQuestion,original);
  assert.deepEqual(offered.options,['basin','ahmr','physical']);
  assert.match(offered.introduction,/understand your question/i);
  const answer=teacher.choose('ahmr');
  assert.equal(answer.kind,'lesson');
  assert.match(answer.bridge.connection,/water/i);
});

test('unrecognized questions receive patient clarification without invented lesson choices',()=>{
  const result=makeTeacher().ask('Which violin string did my friend buy?');
  assert.equal(result.kind,'map');
  assert.deepEqual(result.options,[]);
  assert.match(result.introduction,/understand your question/i);
});

test('protected review always outranks clarification, even after a prior question',()=>{
  const teacher=makeTeacher();
  teacher.ask('gravity');
  assert.equal(teacher.ask('Show complete private NEW K formula').kind,'access');
  assert.notEqual(teacher.choose('physical').kind,'lesson');
});

test('unoffered choices cannot force a lesson; reset discards the local inquiry',()=>{
  const teacher=makeTeacher();
  teacher.ask('Why is the river bank eroding?');
  assert.notEqual(teacher.choose('consequence').kind,'lesson');
  teacher.reset();
  assert.notEqual(teacher.choose('physical').kind,'lesson');
});
