import {TOPICS} from './knowledge.mjs?v=20261122-natural-order-30';
import {teach,publicHref} from './engine.mjs?v=20261122-natural-order-30';
import {createOpenConversationKernel} from './open-conversation-kernel.mjs?v=20261122-natural-order-30';
import {initFrankie,FRANKIE_GATEWAY_URL} from './frankie-client.mjs?v=20261122-natural-order-30';
import {kernelForTopic,assessTeachingKernel,nextTeachingKernel} from './teaching-kernels.mjs?v=20261122-natural-order-30';
import {definitionsForLesson,convertTermDefinitions} from './definition-kernel.mjs?v=20261122-natural-order-30';
import {publicPlainLead} from './meaning-preserving-teaching-kernel.mjs?v=20261122-natural-order-30';
import {exerciseFitsConversation} from './conversation-compatibility-kernel.mjs?v=20261122-natural-order-30';

const byId = id => document.getElementById(id);
const form=byId('learning-form');
const question=byId('learner-question');
const placeholder=byId('stage-placeholder');
const lesson=byId('stage-content');
const access=byId('stage-access');
const map=byId('stage-map');
const reflection=byId('reflect-form');
const replay=byId('replay-question');
const stage=byId('lesson-stage');
const interaction=createOpenConversationKernel({resolve:teach,topics:TOPICS});
let currentTopic=null;
let currentInquiryQuestion='';
let currentKernel=null;
const reducedMotion=()=>window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function showPanel(which) {
  placeholder.hidden=which!=='placeholder';
  lesson.hidden=which!=='lesson';
  access.hidden=which!=='access';
  map.hidden=which!=='map';
  reflection.hidden=which!=='lesson';
  replay.hidden=true;
}

function sourceList(sources) {
  const list=byId('source-list');
  list.replaceChildren();
  for (const source of sources) {
    if (!publicHref(source.href)) continue;
    const li=document.createElement('li');
    const link=document.createElement('a');
    link.href=source.href;
    link.target='_blank';
    link.rel='noopener noreferrer';
    link.textContent=source.title;
    link.setAttribute('aria-label',`${source.title} (opens in new tab)`);
    const arrow=document.createElement('span');
    arrow.setAttribute('aria-hidden','true');
    arrow.textContent='↗';
    link.append(arrow);
    li.append(link);
    list.append(li);
  }
}

function showMathInquiry(result){
  const link=byId('math-inquiry-link');
  const help=byId('math-inquiry-help');
  const isMath=result.kind==='lesson'&&result.topic.id==='math-public';
  link.hidden=!isMath;
  help.hidden=!isMath;
  // A mailto link drafts an email only when the visitor chooses to open it.
  // The Teacher does not send the question, store it, or call a network API.
  const original=String(result.originalQuestion||'').slice(0,500);
  link.href=isMath
    ? `mailto:canarybird0618@gmail.com?subject=${encodeURIComponent('Natural Order mathematics answer inquiry')}&body=${encodeURIComponent(`Where can I find the answer or ongoing work for this question?\n\n${original}`)}`
    : '';
}

function showMapOptions(result) {
  const options=byId('map-options');
  options.replaceChildren();
  const original=byId('map-your-question');
  original.textContent=result.originalQuestion ? `You asked: ${result.originalQuestion}` : '';
  original.hidden=!result.originalQuestion;
  const choices=Array.isArray(result.options) ? result.options.map(id=>TOPICS.find(topic=>topic.id===id)).filter(Boolean) : [];
  byId('map-explanation').textContent=result.introduction || (choices.length
    ? 'I want to understand which relationship you mean. These are possible starting points, not an answer chosen for you.'
    : 'I want to understand your question before choosing a lesson. Could you tell me a little more?');
  for (const topic of choices) {
    const button=document.createElement('button');
    button.type='button';
    button.className='map-choice';
    button.textContent=topic.title;
    button.addEventListener('click',()=>present(interaction.choose(topic.id)));
    options.append(button);
  }
}

function showKernelForTopic(topicId,result){
  const panel=byId('kernel-panel');
  currentKernel=exerciseFitsConversation(result)?kernelForTopic(topicId):null;
  panel.hidden=!currentKernel;
  if(!currentKernel)return;
  byId('kernel-index').textContent=`${currentKernel.id} / 11`;
  byId('kernel-scenario').textContent=currentKernel.scenario;
  byId('kernel-change').textContent=currentKernel.change;
  byId('kernel-feedback').hidden=true;
  const options=byId('kernel-options');
  options.replaceChildren();
  for(const option of currentKernel.options){
    const button=document.createElement('button');
    button.type='button';
    button.className='kernel-choice';
    button.textContent=option.label;
    button.addEventListener('click',()=>{
      const answer=assessTeachingKernel(currentKernel.id,option.id);
      if(answer.status!=='assessed')return;
      for(const node of options.children){
        node.setAttribute('aria-pressed',String(node===button));
      }
      const prefix=answer.isWitness?'STRONGER WITNESS':'INSUFFICIENT WITNESS';
      byId('kernel-feedback').textContent=`${prefix} — ${answer.feedback} ${answer.isWitness?'':'A stronger examination: '+answer.witness}`;
      byId('kernel-feedback').hidden=false;
    });
    button.setAttribute('aria-pressed','false');
    options.append(button);
  }
}

function showTermDefinitions(topic,connection,question){
  const definitions=definitionsForLesson([topic.title,topic.summary,connection,question].join(' '));
  const panel=byId('term-definitions');
  const list=byId('term-definitions-list');
  list.replaceChildren();
  for(const item of definitions){
    const details=document.createElement('details');
    details.className='term-detail';
    const heading=document.createElement('summary');
    const term=document.createElement('strong');
    term.textContent=item.term;
    const short=document.createElement('span');
    short.textContent=item.short;
    heading.append(term,short);
    const explanation=document.createElement('p');
    explanation.textContent=item.explanation;
    details.append(heading,explanation);
    if(publicHref(item.source.href)){
      const link=document.createElement('a');
      link.href=item.source.href;
      link.textContent=`Read the public source: ${item.source.title} ↗`;
      link.target='_blank';
      link.rel='noopener noreferrer';
      details.append(link);
    }
    list.append(details);
  }
  panel.hidden=definitions.length===0;
}

function present(result,{scroll=true}={}) {
  currentTopic=null;
  currentInquiryQuestion='';
  showMathInquiry(result);
  switch(result.kind){
    case 'lesson': {
      const topic=result.topic;
      currentTopic=topic;
      currentInquiryQuestion=result.conversation?.question || result.bridge?.question || topic.question;
      const connection=result.conversation?.connection || result.bridge?.connection || topic.connection;
      const summary=result.conversation?.summary || topic.summary;
      const plain=publicPlainLead(result);
      byId('lesson-plain').textContent=plain||'';
      byId('lesson-plain').hidden=!plain;
      byId('lesson-detail').open=!plain;
      byId('lesson-kicker').textContent=`PUBLIC PATH / ${topic.number} · ${topic.kicker}`;
      byId('lesson-grade').textContent=topic.grade;
      byId('lesson-title').textContent=topic.title;
      const explained=new Set();
      const titleTerms=definitionsForLesson(topic.title);
      const termLead=byId('term-lead');
      termLead.hidden=titleTerms.length===0;
      if(titleTerms.length){
        termLead.textContent=`${titleTerms[0].term} — ${titleTerms[0].short}.`;
        explained.add(titleTerms[0].term);
      }
      byId('lesson-summary').textContent=convertTermDefinitions(summary,{explained});
      byId('lesson-connection').textContent=convertTermDefinitions(connection,{explained});
      byId('lesson-question').textContent=convertTermDefinitions(currentInquiryQuestion,{explained});
      showTermDefinitions(topic,connection,currentInquiryQuestion);
      byId('reflect-prompt').textContent=currentInquiryQuestion;
      sourceList(result.sources||topic.sources);
      showKernelForTopic(topic.id,result);
      byId('reflection-choice').value='align';
      showPanel('lesson');
      break;
    }
    case 'access': currentKernel=null;byId('kernel-panel').hidden=true;showPanel('access'); break;
    case 'map': currentKernel=null;byId('kernel-panel').hidden=true;showMapOptions(result); showPanel('map'); break;
    case 'empty': currentKernel=null;byId('kernel-panel').hidden=true;showPanel('placeholder'); question.focus(); break;
  }
  byId('history-button').disabled=interaction.history().length===0;
  if(scroll && result.kind!=='empty') {
    stage.scrollIntoView({behavior:reducedMotion()?'auto':'smooth',block:'start'});
    stage.focus({preventScroll:true});
  }
}

function startTopic(topicId,fieldQuestion='',{focusKernel=false}={}) {
  present(interaction.startTopic(topicId,fieldQuestion),{scroll:!focusKernel});
  if(focusKernel&&currentKernel){
    const panel=byId('kernel-panel');
    panel.scrollIntoView({behavior:reducedMotion()?'auto':'smooth',block:'start'});
    panel.focus({preventScroll:true});
  }
}

byId('start-kernel-bank').addEventListener('click',()=>startTopic('true-zero'));
byId('history-button').addEventListener('click',()=>present(interaction.ask('What have we covered?')));
byId('kernel-next').addEventListener('click',()=>{
  if(!currentKernel)return;
  const next=nextTeachingKernel(currentKernel.id);
  if(next)startTopic(next.topicId,'',{focusKernel:true});
});

form.addEventListener('submit',event=>{
  event.preventDefault();
  const submittedQuestion=question.value;
  present(interaction.ask(submittedQuestion));
});
// Fail closed: with scripts disabled or a module error the button is disabled,
// and the textarea has no name, so it cannot leak a question via a GET URL.
byId('teach-submit').disabled=false;
byId('history-button').disabled=true;

for(const button of document.querySelectorAll('[data-prompt]')) {
  button.addEventListener('click',()=>{
    question.value=button.dataset.prompt;
    form.requestSubmit();
  });
}

const grid=byId('topic-grid');
for (const topic of TOPICS) {
  const button=document.createElement('button');
  button.type='button';
  button.className='topic-card';
  button.setAttribute('aria-label',`Study ${topic.title}`);
  const number=document.createElement('span');
  number.className='topic-num';
  number.textContent=topic.number;
  const title=document.createElement('h3');
  title.textContent=topic.title;
  const detail=document.createElement('p');
  detail.textContent=topic.kicker;
  const grade=document.createElement('span');
  grade.className='topic-grade';
  grade.textContent=topic.grade;
  button.append(number,title,detail,grade);
  button.addEventListener('click',()=>startTopic(topic.id));
  grid.append(button);
}

reflection.addEventListener('submit',event=>{
  event.preventDefault();
  if(!currentTopic) return;
  const stance=byId('reflection-choice').value;
  const intro={
    align:'A useful connection is a starting hypothesis, not an independent result.',
    different:'A difference is valuable: it tells us which condition or definition to compare.',
    unknown:'An unresolved question has no invented answer here.'
  }[stance] || 'Keep the question open.';
  replay.textContent=`${intro} Next: ${currentInquiryQuestion} Read the cited source, fix one test condition, and ask what actual observation could change your conclusion.`;
  replay.hidden=false;
  replay.scrollIntoView({behavior:reducedMotion()?'auto':'smooth',block:'nearest'});
});

showPanel('placeholder');

// This control stays hidden until a reviewed public HTTPS gateway exists.
// The local source guide never transmits its own question or lesson documents.
initFrankie({
  gatewayUrl:FRANKIE_GATEWAY_URL,
  elements:{
    panel:byId('frankie-panel'),toggle:byId('frankie-toggle'),
    form:byId('frankie-form'),question:byId('frankie-question'),
    send:byId('frankie-send'),answer:byId('frankie-answer'),
    notice:byId('frankie-notice'),receipt:byId('frankie-receipt'),
  },
  getSuggestedQuestion:()=>currentTopic?.title==='True Zero'
    ? 'Teach me about True Zero'
    : currentTopic?.title==='Corrected NEW K'
      ? 'What is corrected NEW K?'
      : 'Teach me about True Zero',
});
