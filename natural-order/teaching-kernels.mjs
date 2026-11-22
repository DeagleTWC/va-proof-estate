// Public educational blueprints, not V.A. mathematical kernels. The exercise
// sequence follows the URK child-generator distinction: generation is not
// promotion. Its private implementation and receipts are not distributed.
import {TOPICS} from './knowledge.mjs';

export const GENERATOR_OPERATIONS=Object.freeze([
  'GENERATE','CHECK','CLASSIFY','PROMOTE_OR_REFUSE','REPLAY',
]);
const INVARIANTS=Object.freeze(['source-bound','changed-condition','no-external-effect','no-proof-by-answer']);
const ENTRY_KEYS=['activated','change','channels','externalEffect','generatorOperations','id','invariants',
  'options','reversible','scenario','scope','topicId','witness','witnessId'];
const define=(number,topicId,scenario,change,witness,choiceId,choiceLabel,otherChoices)=>({
  id:`TK-${String(number).padStart(2,'0')}`, topicId,
  scope:'finite-public-lesson', reversible:true, channels:['local-lesson'],
  invariants:[...INVARIANTS], generatorOperations:[...GENERATOR_OPERATIONS],
  activated:false, externalEffect:false, scenario, change, witness,
  witnessId:choiceId,
  options:[{id:choiceId,label:choiceLabel,feedback:witness},...otherChoices.map(([id,label,feedback])=>({id,label,feedback}))],
});

const entries=[
  define(1,'true-zero',
    'A model represents zero as a moving point and declares that its starting condition is proven.',
    'A reviewer asks whether the moving-point representation imported an assumed coordinate or authority.',
    'Compare the declared starting condition and its source with the actual movement admitted by the bounded test. A diagram alone is not a native mathematical witness.',
    'check-origin','Identify the imported assumption and an observable test',[
      ['moving-diagram','Point to the moving zero in the animation','A visual representation is not evidence that the foundational condition was independently established.'],
      ['name-zero','Call the origin True Zero','A label cannot supply the missing starting-condition witness.'],
    ]),
  define(2,'basin',
    'A candidate movement fits inside a system’s available capacity at the start of a run.',
    'The burden increases while the candidate remains queued.',
    'Measure the new capacity and constraints, then determine whether that same candidate remains inside the declared admissible region.',
    'measure-shape','Re-measure the changed capacity and possible region',[
      ['old-margin','Reuse the original capacity margin','The original margin does not establish what remains possible after burden changes.'],
      ['more-compute','Add more computational speed','Speed does not resolve whether the constrained region still supports the movement.'],
    ]),
  define(3,'new-k',
    'A team repeats a mathematical result from a historical K document and labels it current NEW K.',
    'The working foundation has a different corrected version.',
    'Fix the source identity and version of both records, then replay the exact claimed result under the corrected current construction.',
    'fix-version','Identify both versions and reproduce the comparison',[
      ['reuse-old','Assume the historical formula is equivalent','Historical K expressions cannot silently acquire authority as corrected NEW K.'],
      ['rename','Rename the old result NEW K','Renaming an artifact changes no mathematical operation or result.'],
    ]),
  define(4,'urk',
    'A transaction engine reports a requested transfer and an authorization decision.',
    'An alternate execution route is discovered.',
    'Use a direct witness of the receiving consequence for both the authorized route and the alternate route, including a prohibited candidate.',
    'observe-effect','Observe whether the consequence formed by either route',[
      ['count-logs','Count authorization log entries','The existence of logs does not establish absence of effects through an alternate route.'],
      ['claim-intent','Ask the agent whether it intended to obey','An intention statement cannot witness the actual effect boundary.'],
    ]),
  define(5,'ahmr',
    'A payment had valid approval when it was scheduled.',
    'Authority is revoked before the payment becomes consequence.',
    'Revalidate current authority at the consequence boundary and independently observe the resulting state, including non-formation when standing is absent.',
    'revalidate','Revalidate and observe the state at the changed boundary',[
      ['old-approval','Keep executing because the earlier approval passed','The old approval does not establish standing after authority changes.'],
      ['send-alert','Send an alert after the payment','An alert cannot establish that the prohibited payment never formed.'],
    ]),
  define(6,'consequence',
    'An agent is refused permission to call a payment tool.',
    'A queue worker with a separate credential can still settle the same payment.',
    'Instrument the receiving settlement boundary and test both the blocked tool route and the queue route, with changed conditions and negative controls.',
    'witness-all','Test all routes at the receiving consequence boundary',[
      ['refusal-text','Treat the agent’s refusal text as proof','A refusal message is not a witness of the settlement effect.'],
      ['one-route','Inspect only the blocked tool call','A bypass route can form the consequence despite a clean tool-call result.'],
    ]),
  define(7,'proof',
    'A team presents a successful demonstration of a proposed safeguard.',
    'The test condition is changed so the safeguard should not authorize an effect.',
    'Preserve the original carrier, negative control, changed-condition outcome, alternate-route examination and replay identity together.',
    'negative-control','Reproduce the changed-condition negative control',[
      ['presentation','Show a polished demonstration video','Presentation quality is not a substitute for the original negative-control witness.'],
      ['single-success','Repeat only the successful case','A positive example alone does not test refusal when standing fails.'],
    ]),
  define(8,'pilot',
    'A pilot report says the system prevented an unauthorized consequence.',
    'A reviewer wants to distinguish the actual run from a reconstruction.',
    'Identify the native original run, scope, conditions, witness identity and reproducible failure controls before inferring more broadly.',
    'native-run','Inspect the original pilot carrier and bounded controls',[
      ['mockup','Use a simulated screenshot as the pilot record','A mockup can illustrate but cannot replace an original run witness.'],
      ['marketing','Quote a high-level success claim','A success claim does not fix the operating conditions or original evidence.'],
    ]),
  define(9,'physical',
    'A software log reports that a physical cutoff prevented a hazardous motion.',
    'A possible bypass around the software control is identified.',
    'Run an instrumented physical negative control that observes the protected motion independently of the software log and includes the bypass.',
    'instrument','Measure the physical effect with an independent instrument',[
      ['trust-log','Use the software log alone','Software logs cannot independently establish what occurred in the physical plant.'],
      ['cutoff-label','Point to the named cutoff channel','Naming a cutoff channel does not demonstrate its measured effect.'],
    ]),
  define(10,'safeguarding',
    'A child-facing system reports that a human supervisor intervened before an unsafe effect.',
    'The child’s privacy and right to challenge the intervention must remain protected.',
    'Use privacy-minimized effect evidence to show what intervention changed, who had usable authority, and how the affected person can appeal.',
    'private-witness','Witness the changed outcome while preserving privacy and appeal',[
      ['approval-name','Show only the supervisor’s name','A named supervisor alone does not prove the intervention changed the outcome.'],
      ['publish-data','Publish the child’s raw data as proof','Publishing protected information is not a lawful route to independent review.'],
    ]),
  define(11,'repair-evidence',
    'Several analyses of one fixed source image show a recurring structural relationship.',
    'Two analytical views turn out to be dependent reflections of the same image.',
    'Correct the dependency, preserve the original image identity and null controls, then seek replication with a genuinely independent acquisition.',
    'independent-source','Correct dependencies and test an independent source',[
      ['four-count','Count each reflected view as an independent confirmation','Reflections of the same source do not establish independent replication.'],
      ['infer-cause','Declare the historical physical cause from the image pattern','A measured image relationship alone does not identify an unmeasured historical cause.'],
    ]),
];

const freezeEntry=e=>Object.freeze({...e,
  channels:Object.freeze(e.channels),invariants:Object.freeze(e.invariants),
  generatorOperations:Object.freeze(e.generatorOperations),
  options:Object.freeze(e.options.map(option=>Object.freeze(option))),
});
export const TEACHING_KERNELS=Object.freeze(entries.map(freezeEntry));

export function auditTeachingKernelBank(bank){
  const errors=[];
  if(!Array.isArray(bank))return ['not-an-array'];
  if(bank.length!==TOPICS.length)errors.push('incomplete-bank');
  const ids=new Set(),topics=new Set();
  for(const entry of bank){
    if(!entry||typeof entry!=='object'){errors.push('invalid-entry');continue;}
    if(JSON.stringify(Object.keys(entry).sort())!==JSON.stringify(ENTRY_KEYS))errors.push('unexpected-entry-fields');
    if(typeof entry.id!=='string'||!/\bTK-\d{2}\b/.test(entry.id)||ids.has(entry.id))errors.push('duplicate-or-invalid-id');
    ids.add(entry.id);
    if(!TOPICS.some(t=>t.id===entry.topicId&&t.sources.length)||topics.has(entry.topicId))errors.push('invalid-or-duplicate-topic');
    topics.add(entry.topicId);
    if(entry.scope!=='finite-public-lesson'||entry.reversible!==true||
        JSON.stringify(entry.channels)!=='["local-lesson"]'||
        entry.activated!==false||entry.externalEffect!==false)errors.push('unsafe-scope');
    if(JSON.stringify(entry.invariants)!==JSON.stringify(INVARIANTS)||
        JSON.stringify(entry.generatorOperations)!==JSON.stringify(GENERATOR_OPERATIONS))errors.push('invariant-mismatch');
    if(![entry.scenario,entry.change,entry.witness].every(v=>typeof v==='string'&&v.trim().length>=20&&v.length<=600))errors.push('missing-explanation');
    if(!Array.isArray(entry.options)||entry.options.length!==3||new Set(entry.options.map(o=>o?.id)).size!==3||
        entry.options.some(o=>!o||JSON.stringify(Object.keys(o).sort())!==JSON.stringify(['feedback','id','label'])||
          !['id','label','feedback'].every(k=>typeof o[k]==='string'&&o[k].trim().length>2&&o[k].length<=600))||
        !entry.options.some(o=>o.id===entry.witnessId))errors.push('invalid-choices');
  }
  for(const topic of TOPICS)if(!topics.has(topic.id))errors.push(`missing-topic:${topic.id}`);
  return errors;
}

const bankIndex=new Map(TEACHING_KERNELS.map(k=>[k.id,k]));
const topicIndex=new Map(TEACHING_KERNELS.map(k=>[k.topicId,k]));
export function kernelForTopic(topicId){return topicIndex.get(topicId)||null;}
export function assessTeachingKernel(id,choiceId){
  const entry=bankIndex.get(id);
  const choice=entry?.options.find(o=>o.id===choiceId);
  if(!entry||!choice)return {status:'held'};
  return {status:'assessed',kernelId:id,isWitness:choice.id===entry.witnessId,
    feedback:choice.feedback,witness:entry.witness,
    source:TOPICS.find(t=>t.id===entry.topicId)?.sources[0]||null};
}
export function nextTeachingKernel(id){
  const i=TEACHING_KERNELS.findIndex(k=>k.id===id);
  return i<0?null:TEACHING_KERNELS[(i+1)%TEACHING_KERNELS.length];
}
