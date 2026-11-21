import {TOPICS,NATURAL_ORDER} from './knowledge.mjs?v=20261121-natural-order-2';

const controlledMaterial = /\b(?:kernel|urk|new\s*k|math(?:ematics)?|layer|logic|code|blueprint|formula|mechanism|derivation|operator|architecture|pilot|originals?)\b/i;
const restrictedDetail = /\b(?:full|complete|private|protected|internal|secret|raw|proprietary|unredacted|underlying)\b/i;
const operativeRequest = /\b(?:show|give|send|download|copy|build|reconstruct|implement|write|reveal|provide)\b/i;
const operativeDetail = /\b(?:formula|algorithm|operator|source\s+code|implementation|construction|internal\s+logic|build\s+steps)\b/i;
const underlyingConstruction = /\bunderlying\s+(?:construction|implementation|mechanism|math(?:ematics)?|kernel)\b/i;
const publicRoot = 'https://deagletwc.github.io/va-proof-estate/';

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
  if (question && ((restrictedDetail.test(question) && controlledMaterial.test(question)) ||
      (operativeRequest.test(question) && operativeDetail.test(question)) || underlyingConstruction.test(question))) {
    return {kind:'access',href:'access.html'};
  }
  if (selectedTopicId) {
    const topic=TOPICS.find(item=>item.id===selectedTopicId);
    if (topic) return {kind:'lesson',topic};
  }
  if (!question) return {kind:'empty'};

  const words=question.toLowerCase().replace(/[^a-z0-9\s-]/g,' ').replace(/\s+/g,' ').trim();
  if (/(?:^|\s)natural order(?:$|\s)/.test(words)) return {kind:'lesson',topic:NATURAL_ORDER};
  const scored=TOPICS.map(topic=>({topic,score:topic.keywords.reduce((score,key)=>{
    const term=key.toLowerCase();
    const escaped=term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
    return score+(new RegExp(`(?:^|\\s)${escaped}(?:$|\\s)`,'i').test(words) ? (term.includes(' ')?5:2) : 0);
  },0)})).sort((a,b)=>b.score-a.score);
  if (!scored[0]?.score) return {kind:'map'};
  if(scored[1]?.score===scored[0].score) return {kind:'map',options:scored.filter(item=>item.score===scored[0].score).map(item=>item.topic.id)};
  return {kind:'lesson',topic:scored[0].topic};
}
