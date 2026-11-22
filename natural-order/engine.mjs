import {TOPICS,NATURAL_ORDER,VA_IDENTITY,TEACHER_PURPOSE} from './knowledge.mjs?v=20261122-natural-order-14';

const controlledMaterial = /\b(?:kernel|urk|new\s*k|math(?:ematics)?|layer|logic|code|blueprint|formula|mechanism|derivation|operator|architecture|pilot|originals?)\b/i;
const restrictedDetail = /\b(?:full|complete|private|protected|internal|secret|raw|proprietary|unredacted|underlying)\b/i;
const operativeRequest = /\b(?:show|give|send|download|copy|build|reconstruct|implement|write|reveal|provide)\b/i;
const operativeDetail = /\b(?:formula|algorithm|operator|source\s+code|implementation|construction|internal\s+logic|build\s+steps)\b/i;
const underlyingConstruction = /\bunderlying\s+(?:construction|implementation|mechanism|math(?:ematics)?|kernel)\b/i;
const privateReviewInquiry = /\b(?:nda|non-disclosure|non disclosure|private review|private examination|personal walkthrough|protected access)\b/i;
const publicMathIndexInquiry = /\b(?:public|published)\s+math(?:ematics|ematical)?(?:\s+research)?\s+(?:index|catalog(?:ue)?)\b/i;
const publicPilotRecordsInquiry = /\b(?:public|published)\s+(?:(?:hospital|seam)\s+)?pilots?\s+(?:records?|evidence|reports?|index)\b/i;
const protectedNavigationContext = /\b(?:private|protected|internal|secret|raw|proprietary|unredacted|underlying|formula|algorithm|operator|source\s+code|implementation|construction|kernel|originals?)\b/i;
const publicTermNameInquiry = /\b(?:full|complete|original)\s+(?:(?:public|official)\s+)?(?:name|title)\b/i;
const protectedTermDetail = /\b(?:private|protected|internal|secret|raw|proprietary|unredacted|underlying|formula|algorithm|operator|source\s+code|implementation|construction|mechanism|build\s+steps)\b/i;
const publicRoot = 'https://deagletwc.github.io/va-proof-estate/';

// Public, educational bridges from a visitor's own field into examinable
// sources. These are questions to investigate, never diagnoses or field proofs.
const fieldBridges = [
  {
    terms:/\b(?:lithium(?:-ion)?|battery|batteries|thermal runaway|cell charging|energy storage)\b/i,
    domain:'energy storage', options:['basin','physical','consequence'],
    introduction:'Your energy storage question has several examinable sides: physical constraints, independently measured effects, and consequence custody. This public teacher does not diagnose battery chemistry or certify a battery design. Choose the relationship you want to investigate.',
    connection:'For the battery in your example, what physical limit, changed condition, or failure route would matter to an actual consequence?',
    question:'Which independent measurement would establish what happened at the battery boundary, including a changed-condition run?',
  },
  {
    terms:/\b(?:nurse|patient|patients|medication|medicine|clinical|medical|diagnosis|treatment|dosage|dose)\b/i,
    domain:'health care', options:['consequence','safeguarding','proof'],
    introduction:'Your health-care example raises distinct questions about admissible action, the affected person, and observed evidence. This public teacher does not give clinical advice or independently establish a medical result. Choose the relationship to examine.',
    connection:'For the patient in your example, who has usable authority to intervene, and what decision or effect must be protected?',
    question:'What independent observation and preserved record would show whether the protected patient outcome actually occurred?',
  },
  {
    terms:/\b(?:river|flood|flooding|dam|reservoir|drought|water supply|stormwater)\b/i,
    domain:'water and environmental engineering', options:['basin','ahmr','physical'],
    introduction:'Your water-engineering example can be examined through capacity and geometry, changed-condition continuance, or an independently measured physical outcome. This teacher does not model or certify a particular dam or flood.',
    connection:'In the water system you describe, what fixed shape or capacity constrains the available paths when conditions change?',
    question:'What independent measurement under a declared changed condition would distinguish safe continuation from an assumed one?',
  },
  {
    terms:/\b(?:heat transfer|heat flow|thermal conduction|thermal diffusion|convection|temperature gradient)\b/i,
    domain:'heat and thermal systems', options:['basin','physical','proof'],
    introduction:'Your thermal question has several public examination routes: constrained movement, physical observation, and evidence testing. This teacher does not compute material conductivity or infer a physical mechanism from the public record.',
    connection:'For the heat-flow example, what geometry or boundary condition shapes transfer before any outcome can be measured?',
    question:'Which independent temperature or heat-flow observation would distinguish the proposed relation from a model assumption?',
  },
  {
    terms:/\b(?:airplane|aircraft|airline|flight|runway|icing|automobile|vehicle|brakes?|collision)\b/i,
    domain:'transportation safety', options:['basin','physical','consequence'],
    introduction:'Your transportation example opens questions about constrained movement, physical witnesses, and effect prevention. This teacher does not determine the cause of any accident or certify a vehicle.',
    connection:'In the vehicle or aircraft example, which operating condition defines a permissible movement before a hazardous effect could form?',
    question:'What independent instrument and changed-condition test would distinguish prevented effect from a refusal merely recorded in software?',
  },
  {
    terms:/\b(?:robot|robotics|actuator|motor|valve|pressure sensor|industrial machine)\b/i,
    domain:'industrial automation', options:['consequence','physical','proof'],
    introduction:'Your automation example can be examined at the consequence boundary, the physical instrument, and the reproducible witness. This teacher cannot certify an unexamined machine.',
    connection:'For the machine in your example, which physical effect must lack a formation route unless the governing conditions hold?',
    question:'Which independent observation would demonstrate prevention across both the intended route and a bypass attempt?',
  },
  {
    terms:/\b(?:banking|financial|bank account|money transfer|funds transfer|wire transfer|wire payment|treasury|loan|payment|settlement)\b/i,
    domain:'financial operations', options:['consequence','proof','pilot'],
    introduction:'Your financial example can be examined through admissible settlement, evidence of prevention, and bounded pilots. This teacher does not certify an institution or provide financial advice.',
    connection:'For the financial movement you describe, what would actually bind value or obligation, and whose authority must remain valid?',
    question:'What changed-authority test and independent ledger observation would prove that an inadmissible transfer did not settle?',
  },
];

const fieldBridgeFor = question => fieldBridges.find(bridge=>bridge.terms.test(question));
const lensQuestions = {
  'true-zero':'what starting condition must hold before any candidate acquires standing?',
  'new-k':'which declared mathematical version and source identity must the examiner fix before comparing results?',
  urk:'what state transition may actually acquire standing and admission?',
  basin:'which capacity or geometric constraint defines the available movements?',
  physical:'which independent measurement would show the actual physical outcome when conditions change?',
  consequence:'what effect must not form when the governing conditions fail?',
  safeguarding:'who can intervene, what evidence can they see, and how can the affected person challenge a decision?',
  proof:'what original evidence and negative control would distinguish a witnessed effect from a declaration?',
  ahmr:'which changed condition would require continuance and standing to be examined again?',
  pilot:'which bounded pilot record and original source can be replayed by an examiner?',
  'repair-evidence':'what repeated structural relation and independent null control would distinguish preservation from a rendering artifact?',
};
const contextualLesson = (topic,bridge,explicit=false) => ({kind:'lesson',topic,...(bridge&&(explicit||bridge.options.includes(topic.id))
  ? {bridge:{domain:bridge.domain,connection:bridge.connection,
      question:`In your ${bridge.domain} example, ${lensQuestions[topic.id] || bridge.question}`}}
  : {})});

export function publicHref(href) {
  if (typeof href !== 'string' || !href.startsWith('../') || href.includes('\\') || href.includes('?') || href.includes('#')) return false;
  try {
    const base = new URL('natural-order/',publicRoot);
    const url = new URL(href,base);
    return url.origin===base.origin && url.pathname.startsWith('/va-proof-estate/') &&
      !url.pathname.includes('/natural-order/private') && /\.(?:html|md|json)$/.test(url.pathname);
  } catch { return false; }
}

export function teach(input, selectedTopicId) {
  const question = String(input ?? '').trim().slice(0,800);
  // A request for the published mathematics index is public navigation, not a request for the underlying mathematics.
  if (question && publicMathIndexInquiry.test(question) && !protectedNavigationContext.test(question)) {
    return {kind:'lesson',topic:TOPICS.find(item=>item.id==='new-k')};
  }
  if (question && publicPilotRecordsInquiry.test(question) && !protectedNavigationContext.test(question)) {
    return {kind:'lesson',topic:TOPICS.find(item=>item.id==='pilot')};
  }
  if (question && publicTermNameInquiry.test(question) && !protectedTermDetail.test(question)) {
    const id=/\b(?:corrected\s+)?new\s+k\b/i.test(question) ? 'new-k' :
      /\bahmr\b/i.test(question) ? 'ahmr' :
      /\b(?:urk|universal resolving kernel|kernel)\b/i.test(question) ? 'urk' : null;
    if (id) return {kind:'lesson',topic:TOPICS.find(item=>item.id===id)};
  }
  if (question && (privateReviewInquiry.test(question) || (restrictedDetail.test(question) && controlledMaterial.test(question)) ||
      (operativeRequest.test(question) && operativeDetail.test(question)) || underlyingConstruction.test(question))) {
    return {kind:'access',href:'access.html'};
  }
  const fieldBridge=fieldBridgeFor(question);
  if (selectedTopicId) {
    const topic=TOPICS.find(item=>item.id===selectedTopicId);
    if (topic) return contextualLesson(topic,fieldBridge);
  }
  if (!question) return {kind:'empty'};

  const words=question.toLowerCase().replace(/[^a-z0-9\s-]/g,' ').replace(/\s+/g,' ').trim();
  if (/\b(?:what (?:is|does)|explain|describe|about|tell me about)\s+(?:(?:the\s+)?(?:v a|va|veritas aegis|shift))\b/.test(words) ||
      /\b(?:v a|va)\s+(?:do|mean|stand for)\b/.test(words)) return {kind:'lesson',topic:VA_IDENTITY};
  if (/\b(?:what is (?:this|the) (?:tool|teacher|site|page) for|why does (?:this|the) (?:tool|teacher|site) exist|what can i learn here|how do i use (?:this|the) (?:tool|teacher|site))\b/.test(words)) return {kind:'lesson',topic:TEACHER_PURPOSE};
  if (/(?:^|\s)natural order repair(?:$|\s)/.test(words)) return contextualLesson(TOPICS.find(item=>item.id==='repair-evidence'),fieldBridge,true);
  if (/(?:^|\s)natural order(?:$|\s)/.test(words)) return {kind:'lesson',topic:NATURAL_ORDER};
  const asksForRelationship=/\b(?:relat(?:e|ed|es|ion|ionship)|connect(?:s|ed|ion)?|between|together)\b/.test(words);
  const foundationalConcepts=[/\btrue zero\b/,/\belements basin\b/,/\b(?:corrected new k|new k)\b/,
    /\b(?:urk|universal resolving kernel)\b/,/\b(?:ahmr|lawful continuance)\b/,/\bconsequence custody\b/];
  if (asksForRelationship && foundationalConcepts.filter(term=>term.test(words)).length>1) {
    return {kind:'lesson',topic:NATURAL_ORDER};
  }
  // Preserve every published title as a navigable proper name, including
  // additions to the catalog. A few documented short names remain aliases.
  const hasWords=name=>(' '+words+' ').includes(' '+name+' ');
  const publicTitles=TOPICS.filter(topic=>hasWords(topic.title.toLowerCase()
    .replace(/[^a-z0-9\s-]/g,' ').replace(/\s+/g,' ').trim())).map(topic=>topic.id);
  const namedAliases=[
    [/\btrue zero\b/,'true-zero'],[/\belements basin\b/,'basin'],
    [/\b(?:corrected new k|new k)\b/,'new-k'],[/\b(?:universal resolving kernel|urk)\b/,'urk'],
    [/\b(?:ahmr|lawful continuance)\b/,'ahmr'],[/\bconsequence custody\b/,'consequence'],
    [/\bproof before power\b/,'proof'],[/\bkcd\b/,'physical'],
    [/\bhuman oversight\b/,'safeguarding'],
  ].filter(([term])=>term.test(words)).map(([,id])=>id);
  const namedSubjects=[...new Set([...publicTitles,...namedAliases])];
  if(namedSubjects.length===1){
    const topic=TOPICS.find(item=>item.id===namedSubjects[0]);
    if(topic) return contextualLesson(topic,fieldBridge,true);
  }
  const scored=TOPICS.map(topic=>({topic,score:topic.keywords.reduce((score,key)=>{
    const term=key.toLowerCase();
    const escaped=term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
    return score+(new RegExp(`(?:^|\\s)${escaped}(?:$|\\s)`,'i').test(words) ? (term.includes(' ')?5:2) : 0);
  },0)})).sort((a,b)=>b.score-a.score);
  // Field-specific meaning wins over a collision in general keywords: a river
  // bank is not a financial institution, and a battery test is not proof of a
  // V.A. claim. Ask which relevant route the visitor wants to examine.
  if (fieldBridge && (!scored[0]?.score || !fieldBridge.options.includes(scored[0].topic.id) ||
      scored[1]?.score===scored[0].score)) {
    return {kind:'map',options:fieldBridge.options,introduction:fieldBridge.introduction};
  }
  if (!scored[0]?.score) return {kind:'map'};
  if(scored[1]?.score===scored[0].score) return {kind:'map',options:scored.filter(item=>item.score===scored[0].score).map(item=>item.topic.id)};
  return contextualLesson(scored[0].topic,fieldBridge);
}
