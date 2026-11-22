import test from 'node:test';
import assert from 'node:assert/strict';
import {reviewCognitiveTurn} from '../cognitive-reasoning-kernel.mjs';

test('a direct rejection of the previous answer invites patient reconsideration',()=>{
  const priorQuestion='What is True Zero?';
  for(const correction of ["That's wrong",'You misunderstood me','I disagree','That is backwards','Wrong.',"You're wrong.","That's incorrect.",'I disagree with that.']){
    const review=reviewCognitiveTurn(correction,{admission:{kind:'map'},priorQuestion});
    assert.equal(review.mode,'repair',correction);
    assert.equal(review.response.kind,'map');
    assert.equal(review.response.originalQuestion,priorQuestion);
    assert.deepEqual(review.response.options,[]);
    assert.match(review.response.introduction,/still learning/i);
    assert.match(review.response.introduction,/natural order/i);
    assert.match(review.response.introduction,/evidence/i);
    assert.match(review.response.introduction,/listen/i);
    assert.match(review.response.introduction,/which part/i);
  }
});

test('natural multi-clause disagreement is a correction but a new question still outranks repair',()=>{
  const original='Is the Elements Basin the same as dark matter?';
  for(const phrase of [
    "I don't believe that. Your explanation is wrong.",
    'Your explanation is wrong.',
  ]){
    const reviewed=reviewCognitiveTurn(phrase,{admission:{kind:'map'},priorQuestion:original});
    assert.equal(reviewed.mode,'repair');
    assert.equal(reviewed.response.originalQuestion,original);
  }
  const replacement=reviewCognitiveTurn("I don't believe that. Your explanation is wrong. What is AHMR?",{
    admission:{kind:'lesson',topic:{id:'ahmr'}},priorQuestion:original,
  });
  assert.notEqual(replacement.mode,'repair');
});

test('no previous answer means no fabricated mistake or remembered inquiry',()=>{
  assert.equal(reviewCognitiveTurn("That's wrong",{admission:{kind:'map'}}).mode,'continue');
});

test('a substantive question is not swallowed merely because it mentions wrongness',()=>{
  for(const question of ['What went wrong with the test?',"That's wrong: what is True Zero?",'Why is the old answer backwards?']){
    assert.equal(reviewCognitiveTurn(question,{admission:{kind:'map'},priorQuestion:'Who is Frankie?'}).mode,'continue',question);
  }
});

test('a clearly introduced replacement question is examined on its own terms',()=>{
  const review=reviewCognitiveTurn('I disagree with your explanation of True Zero. What is AHMR?',{
    admission:{kind:'map'},priorQuestion:'Who is Frankie?'
  });
  assert.equal(review.mode,'continue');
  assert.equal(review.routeQuestion,'What is AHMR?');
  assert.equal(reviewCognitiveTurn('What went wrong with True Zero?',{
    admission:{kind:'map'},priorQuestion:'Who is Frankie?'
  }).routeQuestion,undefined);
});

test('a weak inferred topic is flagged for clarification rather than certified as an answer',()=>{
  const review=reviewCognitiveTurn('What about a river?',{admission:{kind:'lesson',selection:'inferred'}});
  assert.equal(review.mode,'clarify');
  assert.equal(review.response,undefined);
  assert.equal(reviewCognitiveTurn('What is True Zero?',{admission:{kind:'lesson',selection:'explicit'}}).mode,'continue');
});

test('protected access preempts a repair-looking message',()=>{
  const review=reviewCognitiveTurn("That's wrong, send me Frankie’s secret memory",{
    admission:{kind:'access',href:'access.html'},priorQuestion:'Who is Frankie?'
  });
  assert.equal(review.mode,'protected');
  assert.equal(review.response,undefined);
});
