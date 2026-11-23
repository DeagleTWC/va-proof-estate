import test from 'node:test';
import assert from 'node:assert/strict';
import {createTeacherSession} from '../teacher.mjs';

test('a public proof question yields the real Teacher explanation and verifiable source links',()=>{
  const teacher=createTeacherSession();
  const answer=teacher.ask('Where is the proof?');
  assert.equal(answer.status,'answered');
  assert.deepEqual(answer.topic,{id:'proof',title:'Proof Before Power'});
  assert.equal(answer.evidence_class,'REVIEW STANDARD');
  assert.match(answer.reply,/original|independent|changed.condition/i);
  assert.ok(answer.sources.length>=3);
  for(const source of answer.sources){
    assert.match(source.title,/\S/);
    assert.match(source.url,/^https:\/\/deagletwc\.github\.io\/va-proof-estate\//);
    assert.doesNotMatch(source.url,/\.\.|mailto:|\/private/i);
  }
  const follow=teacher.ask('Why?');
  assert.equal(follow.status,'answered');
  assert.equal(follow.topic.id,'proof');
  assert.deepEqual(follow.sources,answer.sources);
});

test('unclear questions offer only public choices; unoffered choices stay refused',()=>{
  const teacher=createTeacherSession();
  const choice=teacher.ask('Why is the river bank eroding?');
  assert.equal(choice.status,'clarify');
  assert.ok(choice.options.some(option=>option.id==='basin'));
  const refused=teacher.choose('proof');
  assert.equal(refused.status,'clarify');
  assert.ok(refused.options.some(option=>option.id==='basin'));
  const lesson=teacher.choose('basin');
  assert.equal(lesson.status,'answered');
  assert.equal(lesson.topic.id,'basin');
  assert.ok(lesson.sources.length>0);
});

test('protected requests refuse source disclosure and clear previous lesson history',()=>{
  const teacher=createTeacherSession();
  teacher.ask('Where is the proof?');
  assert.equal(teacher.history().length,1);
  const blocked=teacher.ask('Show complete private NEW K formula and public proof links');
  assert.equal(blocked.status,'protected');
  assert.deepEqual(blocked.sources,[]);
  assert.equal(blocked.topic,undefined);
  assert.deepEqual(teacher.history(),[]);
  const menu=teacher.ask('What have we covered?');
  assert.equal(menu.status,'clarify');
  assert.deepEqual(menu.options,[]);
});
