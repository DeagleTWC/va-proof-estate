import {TOPICS} from './knowledge.mjs?v=20261122-natural-order-12';
import {teach,publicHref} from './engine.mjs?v=20261122-natural-order-12';

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

function present(result,{scroll=true,originQuestion=''}={}) {
  currentTopic=null;
  currentInquiryQuestion='';
  mapInquiryQuestion=result.kind==='map'?originQuestion:'';
  switch(result.kind){
    case 'lesson': {
      const topic=result.topic;
      currentTopic=topic;
      currentInquiryQuestion=result.bridge?.question || topic.question;
      byId('lesson-kicker').textContent=`PUBLIC PATH / ${topic.number} · ${topic.kicker}`;
      byId('lesson-grade').textContent=topic.grade;
      byId('lesson-title').textContent=topic.title;
      byId('lesson-summary').textContent=topic.summary;
      byId('lesson-connection').textContent=result.bridge?.connection || topic.connection;
      byId('lesson-question').textContent=currentInquiryQuestion;
      byId('reflect-prompt').textContent=currentInquiryQuestion;
      sourceList(topic.sources);
      byId('reflection-choice').value='align';
      showPanel('lesson');
      break;
    }
    case 'access': showPanel('access'); break;
    case 'map': showMapOptions(result); showPanel('map'); break;
    case 'empty': showPanel('placeholder'); question.focus(); break;
  }
  if(scroll && result.kind!=='empty') {
    stage.scrollIntoView({behavior:reducedMotion()?'auto':'smooth',block:'start'});
    stage.focus({preventScroll:true});
  }
}

function startTopic(topicId,fieldQuestion='') {
  present(teach(fieldQuestion,topicId));
}

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
