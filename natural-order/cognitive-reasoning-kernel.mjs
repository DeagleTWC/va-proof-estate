// Bounded public reasoning review, not an autonomous general-reasoning model.
// Each visitor turn is examined before prior conversation state is reused.
// The Teacher can recognize an explicit correction or weak inferred route;
// it cannot independently settle unfamiliar claims from this lexical check.
const correctionOnly=/^(?:no[, ]+)?(?:wrong|you(?:'re| are)\s+wrong|(?:that(?:'s| is)|this(?:'s| is)|it(?:'s| is))\s+(?:wrong|incorrect|not\s+(?:right|correct|what\s+i\s+meant)|backwards|the\s+opposite)|you\s+(?:misunderstood\s+me|did(?:n't| not)\s+understand\s+me|got\s+(?:that|it)\s+wrong)|(?:i\s+)?disagree(?:\s+with\s+(?:that|you))?|i\s+(?:don't|do not)\s+agree|(?:that's|that is)\s+not\s+what\s+i\s+asked)[.!?\s]*$/i;
// A full explicit replacement question may follow a correction. Only a
// recognizable interrogative clause is extracted; context alone stays open.
const replacementQuestion=/^(?:i\s+disagree\b|(?:that's|that is)\s+(?:wrong|incorrect)\b|you\s+(?:misunderstood\s+me|got\s+(?:that|it)\s+wrong)\b)[^?]*?[.!;:,]\s*((?:what|why|how|who|which|where|when|can|could|is|are|does|do|did)\b[^?]*\?)$/i;

const repairIntroduction="Thank you for telling me. I'm still learning, too, especially how to listen and explain clearly. The Natural Order can challenge familiar assumptions; some relationships may even appear reversed from what we expected. That appearance alone is not proof—we should examine both interpretations against evidence. I want to listen better and communicate more clearly. If you can be patient, we can keep looking for the answer together, or at least identify what information is missing. Which part did I misunderstand?";

export function reviewCognitiveTurn(input,{admission,priorQuestion}={}){
  const question=String(input??'').trim().slice(0,800);
  // Access takes priority even if the text also looks like disagreement.
  if(admission?.kind==='access')return {mode:'protected'};
  const canonical=question.replace(/\u2019/g,"'");
  const replacement=canonical.match(replacementQuestion);
  if(replacement)return {mode:'continue',routeQuestion:replacement[1]};
  // The phrase must be the entire correction, so a revised actual question
  // still reaches the ordinary human-intent router.
  if(priorQuestion&&correctionOnly.test(canonical))return {
    mode:'repair',
    response:{kind:'map',originalQuestion:priorQuestion,options:[],introduction:repairIntroduction},
  };
  if(admission?.kind==='lesson'&&admission.selection==='inferred')return {mode:'clarify'};
  return {mode:'continue'};
}
