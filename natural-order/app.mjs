import {TOPICS} from './knowledge.mjs?v=20261122-natural-order-14';
import {teach,publicHref} from './engine.mjs?v=20261122-natural-order-14';
import {initFrankie,FRANKIE_GATEWAY_URL} from './frankie-client.mjs?v=20261122-natural-order-14';
import {kernelForTopic,assessTeachingKernel,nextTeachingKernel} from './teaching-kernels.mjs?v=20261122-natural-order-14';
import {definitionsForLesson,convertTermDefinitions} from './definition-kernel.mjs?v=20261122-natural-order-14';

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
let currentTopic=null;
let currentInquiryQuestion='';
let mapInquiryQuestion='';
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

function showMapOptions(result) {
  const options=byId('map-options');
  options.replaceChildren();
  const originalQuestion=mapInquiryQuestion;
  const choices=Array.isArray(result.options) ? result.options.map(id=>TOPICS.find(topic=>topic.id===id)).filter(Boolean) : [];
  byId('map-explanation').textContent=result.introduction || (choices.length
    ? 'Your question connects to more than one public subject. Choose which one you want to examine first.'
    : 'The public catalog has no direct answer for those words. Pick a subject below, or narrow your question. We will not invent a result.');
  for (const topic of choices) {
    const button=document.createElement('button');
    button.type='button';
    button.className='map-choice';
    button.textContent=topic.title;
    button.addEventListener('click',()=>startTopic(topic.id,originalQuestion));
    options.append(button);
  }
}

function showKernelForTopic(topicId){
  const panel=byId('kernel-panel');
  currentKernel=kernelForTopic(topicId);
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

function present(result,{scroll=true,originQuestion=''}={}) {
  currentTopic=null;
  currentInquiryQuestion='';
  mapInquiryQuestion=result.kind==='map'?originQuestion:'';
  switch(result.kind){
    case 'lesson': {
      const topic=result.topic;
      currentTopic=topic;
      currentInquiryQuestion=result.bridge?.question || topic.question;
      const connection=result.bridge?.connection || topic.connection;
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
      byId('lesson-summary').textContent=convertTermDefinitions(topic.summary,{explained});
      byId('lesson-connection').textContent=convertTermDefinitions(connection,{explained});
      byId('lesson-question').textContent=convertTermDefinitions(currentInquiryQuestion,{explained});
      showTermDefinitions(topic,connection,currentInquiryQuestion);
      byId('reflect-prompt').textContent=currentInquiryQuestion;
      sourceList(topic.sources);
      showKernelForTopic(topic.id);
      byId('reflection-choice').value='align';
      showPanel('lesson');
      break;
    }
    case 'access': currentKernel=null;byId('kernel-panel').hidden=true;showPanel('access'); break;
    case 'map': currentKernel=null;byId('kernel-panel').hidden=true;showMapOptions(result); showPanel('map'); break;
    case 'empty': currentKernel=null;byId('kernel-panel').hidden=true;showPanel('placeholder'); question.focus(); break;
  }
  if(scroll && result.kind!=='empty') {
    stage.scrollIntoView({behavior:reducedMotion()?'auto':'smooth',block:'start'});
    stage.focus({preventScroll:true});
  }
}

function startTopic(topicId,fieldQuestion='',{focusKernel=false}={}) {
  present(teach(fieldQuestion,topicId),{scroll:!focusKernel});
  if(focusKernel&&currentKernel){
    const panel=byId('kernel-panel');
    panel.scrollIntoView({behavior:reducedMotion()?'auto':'smooth',block:'start'});
    panel.focus({preventScroll:true});
  }
}

byId('start-kernel-bank').addEventListener('click',()=>startTopic('true-zero'));
byId('kernel-next').addEventListener('click',()=>{
  if(!currentKernel)return;
  const next=nextTeachingKernel(currentKernel.id);
  if(next)startTopic(next.topicId,'',{focusKernel:true});
});

form.addEventListener('submit',event=>{
  event.preventDefault();
  const submittedQuestion=question.value;
  present(teach(submittedQuestion),{originQuestion:submittedQuestion});
});
// Fail closed: with scripts disabled or a module error the button is disabled,
// and the textarea has no name, so it cannot leak a question via a GET URL.
byId('teach-submit').disabled=false;

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
