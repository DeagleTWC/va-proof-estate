import test from 'node:test';
import assert from 'node:assert/strict';
import {TOPICS} from '../knowledge.mjs';
import {TEACHING_KERNELS,auditTeachingKernelBank,kernelForTopic,assessTeachingKernel,nextTeachingKernel} from '../teaching-kernels.mjs';

test('each of the eleven public subjects has exactly one finite admitted teaching exercise',()=>{
  assert.equal(TEACHING_KERNELS.length,11);
  assert.deepEqual(TEACHING_KERNELS.map(k=>k.topicId).sort(),TOPICS.map(t=>t.id).sort());
  assert.deepEqual(auditTeachingKernelBank(TEACHING_KERNELS),[]);
  assert.equal(kernelForTopic('safeguarding').id,'TK-10');
  assert.equal(kernelForTopic('not-a-subject'),null);
  for(const kernel of TEACHING_KERNELS){
    assert.equal(kernel.scope,'finite-public-lesson');
    assert.equal(kernel.reversible,true);
    assert.deepEqual(kernel.channels,['local-lesson']);
    assert.ok(TOPICS.find(t=>t.id===kernel.topicId)?.sources.length);
  }
});

test('a public lesson answers with a bounded witness explanation, not an action authority',()=>{
  const accepted=assessTeachingKernel('TK-05','revalidate');
  assert.equal(accepted.status,'assessed');
  assert.equal(accepted.kernelId,'TK-05');
  assert.equal(accepted.isWitness,true);
  assert.match(accepted.feedback,/authority|change|standing/i);
  assert.match(accepted.witness,/record|observation|state/i);
  const weaker=assessTeachingKernel('TK-05','old-approval');
  assert.equal(weaker.status,'assessed');
  assert.equal(weaker.isWitness,false);
  assert.match(weaker.feedback,/old|earlier|prior|changed/i);
  assert.equal(weaker.witness,accepted.witness);
  assert.equal('allow' in accepted,false);
  assert.equal('deny' in accepted,false);
});

test('unknown or malformed choices do not produce an invented educational result',()=>{
  assert.deepEqual(assessTeachingKernel('TK-00','revalidate'),{status:'held'});
  assert.deepEqual(assessTeachingKernel('TK-05','unlisted'),{status:'held'});
  assert.deepEqual(assessTeachingKernel('TK-05',''),{status:'held'});
});

test('bank admission rejects unsafe or structurally incomplete exercises',()=>{
  const base=TEACHING_KERNELS[0];
  for(const altered of [
    {...base,scope:'private-construction'},
    {...base,reversible:false},
    {...base,channels:['local-lesson','external-effect']},
    {...base,invariants:['source-bound']},
    {...base,options:[base.options[0],base.options[0],base.options[2]]},
    {...base,witnessId:'not-a-choice'},
    {...base,topicId:'nonexistent'},
    {...base,scenario:''},
    {...base,privatePayload:'should-not-be-published'},
    {...base,options:[{...base.options[0],privateData:'none'},...base.options.slice(1)]},
  ]){
    assert.notDeepEqual(auditTeachingKernelBank([altered]),[],`unsafe variant of ${base.id} was admitted`);
  }
  assert.notDeepEqual(auditTeachingKernelBank([base,base]),[]);
  assert.notDeepEqual(auditTeachingKernelBank([]),[],'an empty bank must not pass');
  assert.notDeepEqual(auditTeachingKernelBank([base]),[],'one valid kernel is not a complete curriculum');
});

test('the bank continues from the last admitted exercise back to its first without losing state',()=>{
  assert.equal(nextTeachingKernel('TK-11')?.id,'TK-01');
  assert.equal(nextTeachingKernel('TK-01')?.id,'TK-02');
  assert.equal(nextTeachingKernel('invalid'),null);
});

test('evaluating a lesson does not mutate the original bank or share mutable state',()=>{
  const before=JSON.stringify(TEACHING_KERNELS);
  assessTeachingKernel('TK-05','revalidate');
  assessTeachingKernel('TK-05','old-approval');
  assert.equal(JSON.stringify(TEACHING_KERNELS),before);
});
