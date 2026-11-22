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
      if(pending?.options.includes(result.topic.id)) {
        const answer=resolve(pending.routeQuestion,result.topic.id);
        const originalQuestion=pending.originalQuestion;
        pending=null;
        return answer.kind==='lesson'?{...answer,originalQuestion}:answer;
      }
      if(result.selection!=='inferred') {
        pending=null;
        return result;
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
