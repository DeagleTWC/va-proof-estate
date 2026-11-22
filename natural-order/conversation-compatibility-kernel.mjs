// Bounded public compatibility review. These are narrow responses to observed
// visitor-intention failures, not a general language model or new evidence.
// The human-interaction and protected-access checks must still run first.
const warehouse=/\b(?:warehouse|pallet|forklift|loading\s+dock)\b/i;
const changedAuthority=/\b(?:approv(?:al|ed)|authori[sz](?:ation|ed)?|authority|revok(?:e|ed|ation)|withdraw(?:n|al)?)\b/i;
const skepticism=/\b(?:skeptic(?:al|ism)?|sceptic(?:al|ism)?|why\s+should\s+(?:i|we)\s+believe)\b/i;
const publicReference=/\b(?:any\s+of\s+this|natural\s+order|proof\s+estate|this\s+(?:system|page|site|teacher|work|account)|v\.?a\.?)\b/i;
const immediateDanger=/\b(?:right\s+now|emergency|injur(?:ed|y)|someone(?:'s|\s+is)\s+(?:hurt|in\s+danger)|call\s*911)\b/i;
const waveArray=/\bgravity\b/i;
const waveDescription=/\bwave[- ]?array\b/i;
const skepticalFollowup=/^why\s+should\s+(?:i|we)\s+believe\s+(?:this|that|it)[?.!\s]*$/i;

function publicLesson(question,topics,id,conversation,{fieldBound=false}={}){
  const topic=topics.find(item=>item?.id===id);
  if(!topic?.sources?.length)return null;
  return {kind:'lesson',topic,originalQuestion:question,conversation,
    compatibility:{fieldBound}};
}

export function reviewConversationCompatibility(input,candidate,{topics,priorLesson}={}){
  if(!candidate||candidate.kind==='access'||candidate.kind==='empty'||!Array.isArray(topics))return candidate;
  // An exact public mathematics or source-specific answer outranks general
  // orientation. The name of a subject is evidence of the visitor's intent.
  if(candidate.kind==='lesson'&&(candidate.topic?.id==='math-public'||candidate.sources?.length||
    (candidate.selection!=='inferred'&&candidate.topic?.id!=='consequence'&&candidate.topic?.id!=='proof'&&candidate.topic?.id!=='physical')))return candidate;
  const question=String(input??'').trim().slice(0,800);
  if(skepticalFollowup.test(question)&&priorLesson?.topic?.sources?.length){
    return {kind:'lesson',topic:priorLesson.topic,
      originalQuestion:priorLesson.originalQuestion,
      sources:priorLesson.sources||undefined,
      compatibility:priorLesson.compatibility||undefined,
      conversation:{
        summary:priorLesson.conversation?.summary||priorLesson.topic.summary,
        connection:'You do not have to believe the account. The public source links below show the available evidence and its limits for the exact question you asked; a claim or citation alone does not establish independent reproduction.',
        question:'Which original record or changed-condition result would you like to examine more closely?',
      }};
  }
  if(warehouse.test(question)&&changedAuthority.test(question)&&!immediateDanger.test(question)){
    return publicLesson(question,topics,'consequence',{
      summary:'For a warehouse pallet or forklift movement, the question is whether a real movement can still occur after approval or authority is withdrawn. V.A. examines consequence custody before power, but this public account does not certify any particular warehouse machine.',
      connection:'Keep your warehouse example in view: an approval record or stop message alone cannot show that the pallet stayed still. The public examination would need independent observation of the actual movement and of any alternate route.',
      question:'What independent motion observation would show whether the pallet or forklift stayed stopped after approval was withdrawn?',
    },{fieldBound:true})||candidate;
  }
  if(skepticism.test(question)&&publicReference.test(question)){
    return publicLesson(question,topics,'proof',{
      summary:'You do not have to believe the Natural Order account. Declared designs, reported observations and independent reproduction are different evidence statuses. A persuasive explanation or a link is not proof that every proposed result has been independently established.',
      connection:'Follow the public Proof Estate and evidence links to examine what each original record actually shows, what has only been declared, and what remains open. Skepticism is welcome; no belief is required.',
      question:'Which specific claim or original observation would you like to examine first?',
    })||candidate;
  }
  if(waveArray.test(question)&&waveDescription.test(question)){
    return publicLesson(question,topics,'physical',{
      summary:'Gravity as a “wave array” has not been independently demonstrated by the public evidence linked from this Teacher. The public KCD physical examination program describes evidence requirements, but does not attach a completed instrumented demonstration of that physical identification.',
      connection:'A proposed physical interpretation must be distinguished from a measured, independently reproduced result. The public sources explain the examination route; they do not establish the claimed identification.',
      question:'What independent observation would distinguish the proposed wave-array explanation from other possible accounts?',
    })||candidate;
  }
  return candidate;
}

export function exerciseFitsConversation(result){
  return result?.kind==='lesson'&&result.compatibility?.fieldBound!==true;
}
