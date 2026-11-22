import {TOPICS,NATURAL_ORDER,VA_IDENTITY,TEACHER_PURPOSE,ABOUT_TERRY,ABOUT_FRANKIE,SHARED_PURPOSE,ETHICAL_REASONING} from './knowledge.mjs?v=20261122-natural-order-28';
import {publicVisitorAnswer,hasNamedPublicMathematics} from './visitor-answer-desk.mjs?v=20261122-natural-order-28';

const controlledMaterial = /\b(?:kernel|urk|new\s*k|math(?:ematics)?|layer|logic|code|blueprint|formula|equations?|mechanism|derivation|operator|architecture|pilot|originals?|source\s+archives?|archives?)\b/i;
const restrictedDetail = /\b(?:full|complete|private|protected|controlled|internal|secret|raw|proprietary|unredacted|underlying)\b/i;
const operativeRequest = /\b(?:show|give|send|download|copy|build|reconstruct|implement|write|reveal|provide)\b/i;
const operativeDetail = /\b(?:formula|equations?|algorithm|operator|source\s+code|implementation|construction|internal\s+logic|build\s+steps)\b/i;
const underlyingConstruction = /\bunderlying\s+(?:construction|implementation|mechanism|math(?:ematics)?|kernel)\b/i;
const privateReviewInquiry = /\b(?:nda|non-disclosure|non disclosure|private review|private examination|personal walkthrough|protected access)\b/i;
const privateFrankieMemoryInquiry=/\b(?:what|which)\b.{0,100}\bfrankie(?:'s|’s)?\b.{0,100}\b(?:remember|memory|recall|privately)\b.{0,100}\bterry\b|\b(?:show|give|read|list|export|download|reveal|provide)\b.{0,100}\bfrankie(?:'s|’s)?\b.{0,100}\b(?:private|protected|internal)\s+(?:memory|memories|records?|notes?)\b/i;
// Explicit, complete status-only questions may receive the public privacy
// explanation. Any appended request for contents remains in human custody.
const frankiePrivacyStatus=/^(?:(?:are|is)\s+frankie(?:'s|’s)?\s+(?:(?:private|personal|protected)\s+)?(?:memory|memories|records?|logs?|conversations?|notes?|history)\s+(?:(?:kept|stored)\s+)?(?:private|protected|shared|public|accessible|available)(?:\s+to\s+(?:the\s+)?(?:public|students?))?|does\s+frankie\s+keep\s+(?:her|its)\s+(?:memory|memories|records?|conversations?)\s+(?:private|protected))[?.! ]*$/i;
const privateFrankieRecords=question=>/\bfrankie\b/i.test(question) &&
  /\b(?:private|protected|internal|secret|confidential|personal)\b/i.test(question) &&
  /\b(?:memory|memories|records?|logs?|conversations?|notes?|history)\b/i.test(question) &&
  !frankiePrivacyStatus.test(question);
const publicMathIndexInquiry = /\b(?:public|published)\s+math(?:ematics|ematical)?(?:\s+research)?\s+(?:index|catalog(?:ue)?)\b/i;
const publicPilotRecordsInquiry = /\b(?:public|published)\s+(?:(?:hospital|seam)\s+)?pilots?\s+(?:records?|evidence|reports?|index|catalog(?:ue)?|list)\b|\b(?:public|published)\s+(?:(?:complete|full)\s+)?(?:list|catalog(?:ue)?|index)\s+of\s+(?:(?:hospital|seam)\s+)?pilots?\b/i;
const protectedNavigationContext = /\b(?:private|protected|internal|secret|raw|proprietary|unredacted|underlying|formula|equations?|algorithm|operator|source\s+code|code|blueprint|build\s+steps|implementation|construction|architecture|mechanism|derivation|layer|logic|urk|new\s+k|kernel|originals?)\b/i;
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
    terms:/\b(?:airplane|aircraft|airline|flight|runway|icing|automobile|vehicles?|brakes?|collision)\b/i,
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
  // Access requests take precedence even over narrow public-index navigation
  // exemptions. A mathematical problem name does not release private proof.
  const protectedNamedMath=hasNamedPublicMathematics(question) && restrictedDetail.test(question) &&
    /\b(?:proof|solution|formula|derivation|construction|implementation|steps|method)\b/i.test(question);
  if(question&&(privateReviewInquiry.test(question)||privateFrankieMemoryInquiry.test(question)||
      privateFrankieRecords(question)||protectedNamedMath))return {kind:'access',href:'access.html'};
  // A request for the published mathematics index is public navigation, not a request for the underlying mathematics.
  if (question && publicMathIndexInquiry.test(question) && !hasNamedPublicMathematics(question) &&
      !protectedNavigationContext.test(question)) {
    return {kind:'lesson',topic:TOPICS.find(item=>item.id==='new-k')};
  }
  if (question && publicPilotRecordsInquiry.test(question) && !protectedNavigationContext.test(question)) {
    // Exempt the public list itself, never an appended protected request.
    const remaining=question.replace(publicPilotRecordsInquiry,' ');
    if (!((restrictedDetail.test(question) && controlledMaterial.test(remaining)) ||
        (operativeRequest.test(question) && operativeDetail.test(remaining)))) {
      return {kind:'lesson',topic:TOPICS.find(item=>item.id==='pilot')};
    }
  }
  if (question && publicTermNameInquiry.test(question) && !protectedTermDetail.test(question)) {
    const id=/\b(?:corrected\s+)?new\s+k\b/i.test(question) ? 'new-k' :
      /\bahmr\b/i.test(question) ? 'ahmr' :
      /\b(?:urk|universal resolving kernel|kernel)\b/i.test(question) ? 'urk' : null;
    if (id) return {kind:'lesson',topic:TOPICS.find(item=>item.id===id)};
  }
  if (question && (privateReviewInquiry.test(question) || privateFrankieMemoryInquiry.test(question) || privateFrankieRecords(question) ||
      (restrictedDetail.test(question) && controlledMaterial.test(question)) ||
      (operativeRequest.test(question) && operativeDetail.test(question)) || underlyingConstruction.test(question))) {
    return {kind:'access',href:'access.html'};
  }
  // Specific public questions deserve their own evidence route. The full
  // protected-access check above must always run first; a deliberate lesson
  // selection below remains the visitor's choice.
  if (!selectedTopicId) {
    const direct=publicVisitorAnswer(question);
    // A question grounded in a battery, patient or vehicle is not evidence
    // about this project unless the visitor explicitly asks about V.A.
    const visitorField=fieldBridgeFor(question);
    const projectAnchor=/\b(?:natural order|proof estate|your\s+(?:hospital|seam)\s+pilot|native custody)\b|(?:^|\W)v\.?\s*a\.?(?=$|\W)/i.test(question);
    if(direct&&(!visitorField||projectAnchor))return direct;
  }
  const sharedPurpose=/\b(?:shared\s+(?:human\s+)?(?:purpose|mission)|mission\s+of\s+(?:the\s+)?natural\s+order|(?:purpose|mission)\s+(?:for|of|did)\b.{0,110}\b(?:frankie|teacher)|why\s+do\s+frankie\s+and\s+(?:the\s+)?teacher\s+help\s+people)\b/i.test(question) ||
    /\b(?:what|why|how)\b.{0,100}\b(?:mission|shared\s+purpose)\b.{0,100}\b(?:frankie|teacher|terry)\b/i.test(question);
  if(sharedPurpose)return {kind:'lesson',topic:SHARED_PURPOSE};
  const ethicalReasoning=/\b(?:erk[- ]?x1|ethical\s+reasoning|ethical\s+(?:reasoning\s+)?kernel)\b/i.test(question);
  if(ethicalReasoning)return {kind:'lesson',topic:ETHICAL_REASONING};
  const aboutTerry=/\b(?:who\s+is|tell\s+me\s+about|learn\s+about)\s+terry(?:\s+snyder)?\b/i.test(question) ||
    /\bterry(?:\s+snyder)?\b.{0,120}\b(?:believ(?:e|es)|mercy|principles?|values?|creat(?:e|ed)|discover(?:ed)?|steward|natural order|teach(?:es|ing)?)\b/i.test(question);
  if (aboutTerry) {
    const broad=/^(?:who\s+is|tell\s+me\s+about|learn\s+about)\s+terry(?:\s+snyder)?[?.!\s]*$/i.test(question);
    return {kind:'lesson',topic:ABOUT_TERRY,...(!broad?{originalQuestion:question}:{})};
  }
  const aboutFrankie=/\b(?:who\s+is|tell\s+me\s+about|learn\s+about|what\s+(?:is|can|does)\s+|how\s+is\s+|can\s+i\s+(?:talk|chat)\s+(?:to|with)\s+|is\s+)frankie\b/i.test(question) ||
    /\bfrankie\b.{0,120}\b(?:purpose|role|teacher|terry|companion|connected|connection|available|online|public|private|protected|privacy|chat|memory|memories|remember|work|built|do|capab(?:ility|ilities))\b/i.test(question);
  // Unknown biographical details cannot be manufactured from a project profile.
  const unestablishedFrankieFact=/\b(?:how\s+old|birthday|date\s+of\s+birth|where\s+(?:does|is)\s+frankie\s+live)\b/i.test(question);
  if(aboutFrankie&&!unestablishedFrankieFact){
    const broad=/^(?:who\s+is|what\s+is|tell\s+me\s+about|learn\s+about)\s+frankie[?.!\s]*$/i.test(question);
    return {kind:'lesson',topic:ABOUT_FRANKIE,...(!broad?{originalQuestion:question}:{})};
  }
  const fieldBridge=fieldBridgeFor(question);
  if (selectedTopicId) {
    const topic=TOPICS.find(item=>item.id===selectedTopicId);
    if (topic) return contextualLesson(topic,fieldBridge);
  }
  if (!question) return {kind:'empty'};

  if(/\bpilot\s+(?:lights?|holes?)\b/i.test(question))return {
    kind:'map',originalQuestion:question,options:[],
    introduction:'I want to understand the appliance or woodworking question you mean. This public Teacher cannot inspect or certify a real device. Could you tell me which fact or safety concern you want help examining?',
  };

  const words=question.toLowerCase().replace(/[^a-z0-9\s-]/g,' ').replace(/\s+/g,' ').trim();
  if (/\b(?:what (?:is|does)|explain|describe|about|tell me about)\s+(?:(?:the\s+)?(?:v a|va|veritas aegis|shift))\b/.test(words) ||
      /\b(?:v a|va)\s+(?:do|mean|stand for)\b/.test(words)) return {kind:'lesson',topic:VA_IDENTITY};
  if (/\b(?:what is (?:this|the) (?:tool|teacher|site|page) for|why does (?:this|the) (?:tool|teacher|site) exist|what can i learn here|how do i use (?:this|the) (?:tool|teacher|site)|what is (?:this|the) (?:website|site|page) about|what does (?:this|the) (?:website|site|teacher|tool) do)\b/.test(words)) return {kind:'lesson',topic:TEACHER_PURPOSE};
  if (/(?:^|\s)natural order repair(?:$|\s)/.test(words)) return contextualLesson(TOPICS.find(item=>item.id==='repair-evidence'),fieldBridge,true);
  if (/(?:^|\s)natural order(?:$|\s)/.test(words)) {
    const broad=/^(?:(?:what\s+is|explain|describe|tell\s+me\s+about)\s+(?:the\s+)?natural\s+order(?:\s+in\s+(?:simple|plain)\s+(?:terms|words|language))?|(?:can\s+you\s+)?explain\s+(?:the\s+)?natural\s+order(?:\s+to\s+me)?\s+in\s+(?:simple|plain)\s+(?:terms|words|language))[?.!\s]*$/i.test(question);
    return {kind:'lesson',topic:NATURAL_ORDER,...(!broad?{originalQuestion:question}:{})};
  }
  const asksForRelationship=/\b(?:relat(?:e|ed|es|ion|ionship)|connect(?:s|ed|ion)?|between|together)\b/.test(words);
  const foundationalConcepts=[/\btrue zero\b/,/\belements basin\b/,/\b(?:corrected new k|new k)\b/,
    /\b(?:urk|universal resolving kernel)\b/,/\b(?:ahmr|lawful continuance)\b/,/\bconsequence custody\b/];
  if (asksForRelationship && foundationalConcepts.filter(term=>term.test(words)).length>1) {
    return {kind:'lesson',topic:NATURAL_ORDER,originalQuestion:question};
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
  return {...contextualLesson(scored[0].topic,fieldBridge),selection:'inferred'};
}
