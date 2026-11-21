import {TOPICS} from './knowledge.mjs?v=20261121-natural-order-5';
import {teach,publicHref} from './engine.mjs?v=20261121-natural-order-5';

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

function present(result,{scroll=true}={}) {
  currentTopic=null;
  switch(result.kind){
    case 'lesson': {
      const topic=result.topic;
      currentTopic=topic;
      byId('lesson-kicker').textContent=`PUBLIC PATH / ${topic.number} · ${topic.kicker}`;
      byId('lesson-grade').textContent=topic.grade;
      byId('lesson-title').textContent=topic.title;
      byId('lesson-summary').textContent=topic.summary;
      byId('lesson-connection').textContent=topic.connection;
      byId('lesson-question').textContent=topic.question;
      byId('reflect-prompt').textContent=topic.question;
      sourceList(topic.sources);
      byId('reflection-choice').value='align';
      showPanel('lesson');
      break;
    }
    case 'access': showPanel('access'); break;
    case 'map': showPanel('map'); break;
    case 'empty': showPanel('placeholder'); question.focus(); break;
  }
  if(scroll && result.kind!=='empty') {
    stage.scrollIntoView({behavior:reducedMotion()?'auto':'smooth',block:'start'});
    stage.focus({preventScroll:true});
  }
}

function startTopic(topicId) {
  present(teach('',topicId));
}

form.addEventListener('submit',event=>{
  event.preventDefault();
  present(teach(question.value));
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
  replay.textContent=`${intro} Next: ${currentTopic.question} Read the cited source, fix one test condition, and ask what actual observation could change your conclusion.`;
  replay.hidden=false;
  replay.scrollIntoView({behavior:reducedMotion()?'auto':'smooth',block:'nearest'});
});

showPanel('placeholder');
