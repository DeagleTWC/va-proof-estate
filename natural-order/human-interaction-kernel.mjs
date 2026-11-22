// Conversation-local public teaching admission. No network, persistence,
// probabilities, or substitution of a keyword score for visitor intention.
const patience='I want to make sure I understand your question so I can help you find the answer you are looking for. Could you tell me a little more about what you mean?';
// Only an overt correction resets a pending inquiry. Ordinary "I mean ..."
// clarifications still belong to the visitor's original example.
const correctionPrefix=/^(?:actually[, ]+my (?:question|inquiry) is\b|(?:actually|no)[, ]+i meant\b|i have a (?:different|new|another) question\b|(?:new|different|another) question\s*:|forget (?:that|the previous question)\b|scratch that\b)/i;
function correctedRoute(question){
  const remainder=question.replace(correctionPrefix,'').replace(/^[\s:;,.!?-]+/,'').trim();
  // In "I meant X, not Y", Y is the rejected subject, not another route.
  return remainder.replace(/[,;]\s*not\s+.+$/i,'').trim()||question;
}
const sameQuestion=(a,b)=>a.toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim()===
  b.toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim();
// A complete changed-authority question or narrated payment event in a known
// public field has enough grounding to enter its cited route. A single field
// noun or unfinished event still needs clarification. Protected admission
// always runs first.
const realQuestion=/^(?:what|how|why|when|if|can|could|will|would|does|do|is|are)\b/i;
const changedApproval=/\b(?:approv(?:al|ed)|authori[sz](?:ation|ed)?|authority|revok(?:e|ed|ation)|withdraw(?:n|al)?|changes?|changed|expires?|expired)\b/i;
const paymentEffect=/\b(?:payment|transfer|settlement|settle[sd]?)\b/i;
// A declarative event is sufficient only when it includes the payment, an
// initial grant, a later change, and the settlement it might affect. Neither
// "A payment was approved..." nor "A payment was approved and settled" says
// enough to justify a changed-authority lesson without asking the visitor.
const paymentNarrative=/^(?:(?:a|the|our|my)\s+)?(?:payment|transfer)\b/i;
const initialAuthority=/\b(?:approv(?:ed|al)|authori[sz](?:ed|ation))\b/i;
const alteredAuthority=/\b(?:revok(?:e|ed|ation)|withdraw(?:n|al)?|expir(?:ed|es?)|(?:approval|authorization|authority)\s+(?:changed|changes))\b/i;
const sequence=/\b(?:then|but|before|after|once|later|subsequently)\b/i;
const settlement=/\b(?:settle[sd]?|settlement)\b/i;
const completePaymentNarrative=question=>paymentNarrative.test(question)&&initialAuthority.test(question)&&
  alteredAuthority.test(question)&&sequence.test(question)&&settlement.test(question);
const strongChangedCondition=(question,result)=>result.kind==='lesson'&&result.selection==='inferred'&&
  result.topic?.id==='consequence'&&result.bridge?.domain==='financial operations'&&
  (realQuestion.test(question)||completePaymentNarrative(question))&&
  changedApproval.test(question)&&paymentEffect.test(question);

export function createHumanInteractionKernel({resolve,topics}) {
  if(typeof resolve!=='function'||!Array.isArray(topics))throw new TypeError('public lesson router and topics required');
  const topicIds=new Set(topics.map(topic=>topic.id));
  let pending=null;

  const clarify=(originalQuestion,options=[],context='')=>({
    kind:'map',
    originalQuestion,
    options:[...new Set(options.filter(id=>topicIds.has(id)))],
    introduction:`${patience}${context ? ` ${context}` : ''}`,
  });

  function ask(input) {
    const question=String(input??'').trim().slice(0,800);
    if(!question&&pending)return clarify(pending.originalQuestion,pending.options);
    if(pending&&sameQuestion(question,pending.originalQuestion))return clarify(pending.originalQuestion,pending.options);
    // Check the complete visitor text before interpreting a correction: even
    // rejected clauses must never smuggle a protected request past the gate.
    const rawResult=resolve(question);
    if(rawResult.kind==='access'){pending=null;return rawResult;}
    const replaced=correctionPrefix.test(question);
    if(pending&&replaced)pending=null;
    const routeQuestion=replaced?correctedRoute(question):question;
    const result=replaced?resolve(routeQuestion):rawResult;
    if(result.kind==='access'||result.kind==='empty') {
      pending=null;
      return result;
    }
    if(result.kind==='lesson') {
      // A newly supplied exact, source-specific public question outranks a
      // previous guessed choice, even when both mention the same subject.
      if(result.originalQuestion&&result.sources?.length){
        pending=null;
        return result;
      }
      if(pending?.options.includes(result.topic.id)) {
        const answer=resolve(pending.routeQuestion,result.topic.id);
        const originalQuestion=pending.originalQuestion;
        pending=null;
        return answer.kind==='lesson'?{...answer,originalQuestion}:answer;
      }
      const directlyAdmitted=strongChangedCondition(routeQuestion,result);
      if(result.selection!=='inferred'||directlyAdmitted) {
        pending=null;
        return directlyAdmitted?{...result,originalQuestion:result.originalQuestion||routeQuestion}:result;
      }
    }
    const options=result.kind==='map' ? result.options||[] : [result.topic.id];
    const originalQuestion=pending?.originalQuestion||question;
    const pendingRoute=pending?.routeQuestion||routeQuestion;
    const response=clarify(originalQuestion,options,result.introduction);
    pending={originalQuestion,routeQuestion:pendingRoute,options:response.options};
    return response;
  }

  function choose(topicId) {
    if(!pending)return {kind:'empty'};
    if(!pending.options.includes(topicId))return clarify(pending.originalQuestion,pending.options);
    const answer=resolve(pending.routeQuestion,topicId);
    const originalQuestion=pending.originalQuestion;
    pending=null;
    return answer.kind==='lesson'?{...answer,originalQuestion}:answer;
  }

  function reset(){pending=null;}
  return Object.freeze({ask,choose,reset});
}
