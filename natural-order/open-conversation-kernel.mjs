import {createHumanInteractionKernel} from './human-interaction-kernel.mjs?v=20261122-natural-order-23';
import {reviewCognitiveTurn} from './cognitive-reasoning-kernel.mjs?v=20261122-natural-order-23';

// A bounded, in-page conversational layer. It is deliberately not a general
// language model: only clear, short anaphoric follow-ups reuse a prior lesson.
// All new questions still go through the human-intent and protected-access
// routing kernel. Nothing is sent or persisted outside this browser session.
const followups=Object.freeze([
  {mode:'simplify',pattern:/^(?:simplify|(?:please\s+)?(?:explain|say|put)\s+(?:that|it)\s+(?:more\s+)?(?:simply|in\s+plain\s+(?:language|words))|can\s+you\s+explain\s+(?:that|it)(?:\s+(?:more\s+)?simply|\s+in\s+plain\s+(?:words|language))?|what\s+does\s+that\s+mean|i\s+(?:do\s+not|don't|didn't)\s+understand(?:\s+that)?)[?.! ]*$/i},
  {mode:'evidence',pattern:/^(?:evidence|(?:(?:where\s+is|what\s+is|show\s+me)\s+the\s+(?:evidence|proof|source|sources)|how\s+(?:can\s+i|do\s+we)\s+(?:check|verify|examine)\s+that))[?.! ]*$/i},
  {mode:'example',pattern:/^(?:example|(?:can\s+you\s+)?(?:give|show)(?:\s+me)?\s+(?:an?\s+)?example|what\s+would\s+(?:that|it)\s+look\s+like\s+in\s+practice)[?.! ]*$/i},
  {mode:'why',pattern:/^(?:(?:okay|ok|so)\s+)?(?:why|why\s+does\s+(?:that|it)\s+matter|how\s+does\s+(?:that|it)\s+work)[?.! ]*$/i},
  {mode:'continue',pattern:/^(?:(?:tell\s+me|explain)\s+more(?:\s+about\s+(?:that|it))?|go\s+on|keep\s+going|and\s+then\s+what)[?.! ]*$/i},
]);

// Gentle warmth is offered only when invited or when a visitor plainly asks
// for patience. It does not reinterpret a substantive question as a joke.
const confusedTurn=/^(?:i\s+think\s+i\s+just\s+confused\s+myself|i(?:'m| am)\s+(?:confused|lost|a\s+little\s+confused)|you\s+lost\s+me|can\s+we\s+slow\s+down)[.!?\s]*$/i;
const invitedJoke=/^(?:please\s+)?(?:tell\s+me\s+(?:a\s+|one\s+)?joke|can\s+you\s+(?:tell\s+me\s+(?:a\s+)?joke|make\s+me\s+laugh|be\s+funny)|say\s+something\s+funny|make\s+me\s+(?:laugh|smile))[.!?\s]*$/i;
const seriousTurn=/\b(?:patient|medication|medicine|dosage|dose|clinical|cancer|terminal|illness|suicide|suicidal|kill|death|dead|died|injury|injured|abuse|assault|weapon|emergency|accident|crash|unsafe|trauma|private|secret|confidential)\b/i;
const rejectedJoke=/\b(?:no\s+jokes?|stop\s+joking|not\s+funny)\b/i;
const evidenceJoke='A little evidence joke: Why did the claim bring a notebook? Because “trust me” is not a measurement. 😄 A smile is welcome; proof still needs evidence.';

function warmthForTurn(question,priorLesson,priorMap,{allowJokes}){
  if(seriousTurn.test(question)||rejectedJoke.test(question))return null;
  const mode=confusedTurn.test(question)?'reassure':invitedJoke.test(question)?'smile':null;
  if(!mode)return null;
  if(!priorLesson)return {mode,response:{kind:'map',
    originalQuestion:priorMap?.originalQuestion||'',options:priorMap?.options||[],
    introduction:mode==='smile'&&allowJokes
      ? `${evidenceJoke} What would you like to explore or ask next?`
      : allowJokes
        ? 'We may have taken the scenic route. Fortunately, there is no pop quiz. 😄 We can slow down together. What part would you like to understand?'
        : 'Of course. Let’s take this slowly and carefully. Which part would you like help understanding?'}};
  const {topic,bridge,originalQuestion}=priorLesson;
  const field=bridge&&originalQuestion?` You originally asked: “${originalQuestion}”` : '';
  return {mode,response:{kind:'lesson',topic,originalQuestion,sources:priorLesson.sources||undefined,conversation:{
    summary:mode==='reassure'?(plain[topic.id]||priorLesson.conversation?.summary||topic.summary):priorLesson.conversation?.summary||topic.summary,
    connection:mode==='smile'&&allowJokes
      ? `${evidenceJoke} ${topic.title} still has to be examined through its public sources.${field}`
      : `${allowJokes?'We may have taken the scenic route. No pop quiz, I promise. 😄 Let’s slow down.':'Let’s slow down and give your question the care it deserves.'}${field} We can take the explanation one step at a time.`,
    question:'Which part would you like me to unpack or explain differently?',
  }}};
}

const plain=Object.freeze({
  'true-zero':'The account begins with a starting ground. An action does not gain permission merely because someone wants it to happen.',
  basin:'Think about the shape and limits of what is possible. Being possible is not the same as being permitted to create a real effect.',
  'new-k':'This is the named current mathematical foundation. The protected working details are not in the public Teacher.',
  urk:'The question is whether a proposed step actually satisfies the conditions to be allowed to take effect.',
  ahmr:'Permission to continue cannot just be assumed. When a condition changes, the right to keep going has to be examined again.',
  consequence:'The key question is whether an impermissible effect can happen at all, including by an unintended route.',
  proof:'A convincing explanation is not yet evidence. A test needs an original observation, controls, and a way to check what changes.',
  pilot:'A pilot establishes only what its original record actually measured under the recorded conditions.',
  physical:'For a physical claim, measure the physical result independently. A software log alone cannot establish it.',
  safeguarding:'A person needs real protection and a usable path to question or challenge a decision.',
  'repair-evidence':'An observed pattern can survive transformation without settling what physically caused it. That remains an open question.',
  'about-frankie':'Frankie is a separate, locally tested native software companion. This public Teacher can explain her role but cannot open her private memory or speak as her.',
  'about-terry':'Terry describes his job as discovering and sharing what he found. He asks the Teacher to listen, show evidence, and exercise restraint.',
  'natural-order':'This account starts from the ground, examines what is possible, asks which changes have standing, and checks the consequences.',
  'va-identity':'V.A. examines whether movement may become an effect before that effect forms. Its public evidence has specific limits.',
  'teacher-purpose':'This page helps you choose a question, understand the public account, and follow its sources. It does not hold private construction.',
  'shared-purpose':'The Teacher and Frankie exist to help people understand the evidence and make their own informed choices. The choice belongs to the person.',
  'ethical-reasoning':'An ethical question needs honesty, non-harm, fairness, consent, dignity and transparency. The prototype does not establish that these conditions have actually been met.',
});

// Everyday illustrations are hypotheses for discussion, never source data or
// demonstrations of the protected Native V.A. mathematical construction.
const illustrations=Object.freeze({
  'true-zero':'Imagine a game before anyone has been granted a turn. Being able to move a piece would not, by itself, establish a valid first move',
  basin:'Picture water channels with different shapes and capacities. Geometry limits the available routes, but does not establish that any route is safe',
  'new-k':'Think of a building code revised this year. A past rulebook cannot silently stand in for the current declared standard',
  urk:'An automatic door receives an opening request but opens only after the relevant safety conditions are satisfied',
  ahmr:'An elevator permitted to move at one moment may need to stop and be reconsidered when a sensor condition changes',
  consequence:'A payment request may be recorded as refused, yet an examiner still has to check that no second path settled the transfer',
  proof:'A safety switch seems to work once. A stronger test also changes an essential condition and independently checks that the effect did not occur',
  pilot:'A trial at one hospital supports only the observed conditions and outcomes of that particular trial',
  physical:'A motor controller reports that it stopped. A separate sensor would be needed to observe the actual shaft movement',
  safeguarding:'A person can contest a decision only if a real reviewer has authority and can access the necessary permitted evidence',
  'repair-evidence':'A recognizable arrangement persists after an image is transformed. That does not by itself tell us which physical process produced it',
  'about-frankie':'A reader can learn Frankie’s declared role from a public description, but that description cannot open the owner’s private native test records',
  'about-terry':'A student disagrees with Terry’s explanation. His stated principle asks the Teacher to welcome the question and examine evidence',
  'natural-order':'A machine has a starting condition, several possible motions, rules for lawful movement, and a measurable effect; each question is different',
  'va-identity':'A system receives a command, but whether it can produce the requested real effect depends on more than the existence of the command',
  'teacher-purpose':'A visitor asks about a river. The Teacher asks what relationship they want to study and links a bounded public source rather than pretending to model the river',
  'shared-purpose':'A visitor asks what a report means. The Teacher helps examine its evidence, but leaves the decision about what to do with it to the visitor',
  'ethical-reasoning':'A medical suggestion says it is harmless without checking consent or the affected person’s account. A real examination must withhold ethical approval until those unknowns are addressed',
});

function continuation(context,mode) {
  const {topic,bridge,originalQuestion}=context;
  const specificSummary=context.conversation?.summary||topic.summary;
  const field=bridge?.domain?` For your ${bridge.domain} example,` : '';
  const original=bridge&&originalQuestion?` You originally asked: “${originalQuestion}”` : '';
  const common='Would you like to examine a public source, explore a different example, or ask another question?';
  switch(mode){
    case 'simplify':return {summary:plain[topic.id]||specificSummary,
      connection:`We can take this one step at a time.${original}${field} ${bridge?.connection||'Which word or part would you like me to unpack?'}`,question:common};
    case 'evidence':return {summary:plain[topic.id]||specificSummary,
      connection:topic.id==='math-public'
        ? `For this mathematical question, examine the published statement, its hypotheses, quantifiers, derivation and any exact bounded checks. The source links below show what has and has not been established for the named result.`
        : topic.id==='about-frankie'
        ? 'These public source links explain Frankie’s reported role and the limits of the claim. Her native verification packets remain owner-private, so this page cannot independently demonstrate her full runtime.'
        : `The public source links below are the evidence path for this account.${original}${field} ${bridge?.question||'Each has a defined scope; a link is not itself proof of every possible claim.'}`,
      question:topic.id==='math-public'
        ? 'Which proof step, assumption, counterexample or published source do you want to examine next?'
        : 'What original observation or changed-condition test would make this claim more convincing—or show its limits?'};
    case 'example':return {summary:plain[topic.id]||specificSummary,
      connection:`For example (illustration, not proof): ${illustrations[topic.id]||'A change in conditions may change which effects can form'}.${original}${field} ${bridge?.connection||'We can now compare that illustration to something you know.'}`,
      question:'Which part of this example matches your situation, and which part does not?'};
    case 'why':return {summary:plain[topic.id]||specificSummary,
      connection:`Why it matters depends on the real effect you care about.${original}${field} ${bridge?.connection||'The public account invites us to check what happens if its governing condition holds, fails or changes.'}`,
      question:'Which consequence or changed condition matters in your example?'};
    default:return {summary:specificSummary,
      connection:`We can continue with ${topic.title}.${original}${field} ${bridge?.connection||'I will stay with your question and keep the public evidence and its limits visible.'}`,
      question:common};
  }
}

export function createOpenConversationKernel({resolve,topics}) {
  const intent=createHumanInteractionKernel({resolve,topics});
  const validIds=new Set(topics.map(topic=>topic.id));
  let lastLesson=null;
  let lastMap=null;
  let jokesOptedOut=false;
  let turnCount=0;
  let latestIntent=null;

  function record(result,intentName,{inquiry='',retain=false}={}){
    turnCount=Math.min(turnCount+1,6);
    latestIntent=intentName;
    if(result.kind==='lesson'){
      if(!retain)lastLesson={topic:result.topic,bridge:result.bridge||null,sources:result.sources||null,
        conversation:result.conversation||null,
        originalQuestion:result.originalQuestion||inquiry||result.topic.title};
      lastMap=null;
    }else{
      lastLesson=null;
      lastMap=result.kind==='map'?{originalQuestion:result.originalQuestion||'',options:result.options||[]}:null;
    }
    return result;
  }

  function ask(input){
    const question=String(input??'').trim().slice(0,800);
    // Every message is checked against the access boundary before a previous
    // lesson can be brought into the reply. No lexical "continue" bypasses it.
    const admission=resolve(question);
    const review=reviewCognitiveTurn(question,{admission,priorQuestion:lastLesson?.originalQuestion});
    if(review.mode==='protected'){
      intent.reset();
      return record(admission,'protected-review');
    }
    if(review.mode==='repair'){
      // A rejected explanation must not silently become the next answer.
      intent.reset();
      return record(review.response,'reconsideration');
    }
    if(rejectedJoke.test(question))jokesOptedOut=true;
    else if(invitedJoke.test(question))jokesOptedOut=false;
    if(!review.routeQuestion){
      const seriousContext=seriousTurn.test(question)||seriousTurn.test(lastLesson?.originalQuestion||'')||
        seriousTurn.test(lastMap?.originalQuestion||'');
      const warmth=warmthForTurn(question,lastLesson,lastMap,{allowJokes:!jokesOptedOut&&!seriousContext});
      if(warmth){
        // Keep a pending selectable map intact when the visitor asks for
        // patience, so reassurance does not consume their actual choices.
        if(lastLesson||!lastMap?.options.length)intent.reset();
        return record(warmth.response,warmth.mode,{retain:!!lastLesson});
      }
    }
    // Inferred routes stay with the human-intent kernel for clarification.
    const follow=lastLesson&&followups.find(item=>item.pattern.test(question));
    if(follow){
      intent.reset();
      return record({kind:'lesson',topic:lastLesson.topic,sources:lastLesson.sources||undefined,
        originalQuestion:lastLesson.originalQuestion,
        conversation:continuation(lastLesson,follow.mode)},
        follow.mode,{retain:true});
    }
    // Full-text admission above was already checked for protected material.
    // The visitor's explicit replacement question can now be routed alone.
    const routeQuestion=review.routeQuestion||question;
    return record(intent.ask(routeQuestion),'question',{inquiry:routeQuestion});
  }

  function choose(topicId){return record(intent.choose(topicId),'chosen-lesson');}
  function reset(){intent.reset();lastLesson=null;lastMap=null;jokesOptedOut=false;turnCount=0;latestIntent=null;}
  function startTopic(topicId,fieldQuestion=''){
    reset();
    if(!validIds.has(topicId))return {kind:'empty'};
    const question=String(fieldQuestion??'').trim().slice(0,800);
    if(question&&resolve(question).kind==='access')return record({kind:'access',href:'access.html'},'protected-review');
    return record(resolve(question,topicId),'chosen-lesson',{inquiry:question||topics.find(t=>t.id===topicId)?.title});
  }
  function state(){return Object.freeze({topicId:lastLesson?.topic.id||null,turnCount,latestIntent});}
  return Object.freeze({ask,choose,startTopic,reset,state});
}
