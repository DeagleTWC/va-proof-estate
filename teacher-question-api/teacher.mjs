import {teach,publicHref} from '../natural-order/engine.mjs';
import {createOpenConversationKernel} from '../natural-order/open-conversation-kernel.mjs';
import {TOPICS,NATURAL_ORDER,VA_IDENTITY,TEACHER_PURPOSE,ABOUT_TERRY,ABOUT_FRANKIE,
  SHARED_PURPOSE,ETHICAL_REASONING} from '../natural-order/knowledge.mjs';

const PUBLIC_ROOT='https://deagletwc.github.io/va-proof-estate/natural-order/';
const PUBLIC_TOPICS=[...TOPICS,NATURAL_ORDER,VA_IDENTITY,TEACHER_PURPOSE,ABOUT_TERRY,
  ABOUT_FRANKIE,SHARED_PURPOSE,ETHICAL_REASONING];
const TOPIC_TITLES=new Map(PUBLIC_TOPICS.map(({id,title})=>[id,title]));

function references(result){
  const sources=result.sources||result.topic?.sources||[];
  return sources.filter(source=>source && publicHref(source.href) && typeof source.title==='string')
    .map(source=>({title:source.title,url:new URL(source.href,PUBLIC_ROOT).href}));
}

function publicReply(result,history){
  if(result?.kind==='access'){
    return {status:'protected',reply:'I can explain the public record, but protected construction requires human-approved private review.',sources:[]};
  }
  if(result?.kind==='lesson'){
    const topic=result.topic;
    return {status:'answered',reply:result.conversation?.summary||topic.summary,
      topic:{id:topic.id,title:topic.title},evidence_class:topic.grade||'PUBLIC ACCOUNT',
      sources:references(result),
      next_question:result.conversation?.question||result.bridge?.question||topic.question};
  }
  if(result?.kind==='map'){
    const titles=new Map([...TOPIC_TITLES,...history.map(({id,title})=>[id,title])]);
    return {status:'clarify',reply:result.introduction||'I want to understand your question before choosing a lesson.',
      options:(result.options||[]).filter(id=>titles.has(id)).map(id=>({id,title:titles.get(id)}))};
  }
  return {status:'clarify',reply:result?.summary||result?.introduction||
    'I want to make sure I understand your question. Could you tell me a little more?'};
}

export function createTeacherSession(){
  const conversation=createOpenConversationKernel({resolve:teach,topics:TOPICS});
  return Object.freeze({
    ask(question){
      if(typeof question!=='string')throw new TypeError('Question must be plain text');
      return publicReply(conversation.ask(question),conversation.history());
    },
    choose(topicId){
      if(typeof topicId!=='string')throw new TypeError('Topic must be text');
      return publicReply(conversation.choose(topicId),conversation.history());
    },
    history:()=>conversation.history(),
  });
}
