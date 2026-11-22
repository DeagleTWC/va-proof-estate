// Public Definition Conversion Kernel: language assistance, not the protected
// mathematical resolving kernel. Each conversion keeps the named V.A. term,
// provides a bounded everyday explanation, and points to its public record.
const define=(term,short,explanation,href,title,aliases=[])=>({
  term,short,explanation,aliases,source:{href,title},
});
export const DEFINITIONS=Object.freeze([
  define('V.A.','the system called The Shift',
    'V.A. — The Shift is the name of the system and proof estate described by Terry Snyder. The public record presents its proposed foundation and bounded engineering evidence; each application must be examined at its documented scope.',
    '../foundation.html','V.A. foundation',['V.A. — The Shift']),
  define('True Zero','the foundational ground before an action has standing',
    'In V.A. terminology, True Zero is the starting condition rather than an ordinary numeral, an empty register, or a point already moving. Its mathematical construction is not disclosed in this public teacher.',
    '../foundation.html','True Zero foundation'),
  define('Elements Basin','the conditions shaping which movements are possible',
    'In the Natural Order account, the Elements Basin is identified with what people call dark matter and is itself described as moving, not as a stationary background. Natural Order water refers to a named element, not H2O. A horizon limits local access or observation; that is not evidence of deletion or destruction. Gravity as a wave array is under examination. The public KCD design holds a protected interior while surrounding field relations change, but its software receipts do not prove that physical or astrophysical interpretation.',
    '../foundation.html','Elements Basin explanation'),
  define('Corrected NEW K','the current resolving mathematics identified in V.A.',
    'The public mathematical index distinguishes corrected NEW K from earlier K expressions. Historical equations are not assumed equivalent to the operative protected construction.',
    '../research/mathematics/INDEX.json','Public mathematical release index',['NEW K']),
  define('Universal Resolving Kernel','the framework for checking whether a transition has standing',
    'URK is the name used in the public formal account for lawful states, admissible transitions and continued standing. Public descriptions are distinct from protected native implementation.',
    '../foundation.html','Universal Resolving Kernel overview',['URK']),
  define('AHMR','a named continuance constraint in the public V.A. account',
    'AHMR distinguishes permitted progression, threshold-preserved continuity, review conditions and stop conditions. Its exact technical scope belongs to its versioned source record.',
    '../foundation.html','AHMR public explanation'),
  define('Lawful Continuance','rechecking whether movement remains admissible as conditions change',
    'An earlier approval or feasible state does not automatically confer continuing standing after capacity, authority or governing conditions have changed.',
    '../proofs/CONTINUATION-CHECKPOINT-2026-10-26.md','Continuance checkpoint',['lawful continuation']),
  define('Consequence Custody','the claimed custody of an effect before it can form',
    'The relevant test is whether an inadmissible consequence actually failed to form, including through alternate routes. A logged refusal or later warning alone does not establish that outcome.',
    '../consequence-aperture.html','Consequence aperture'),
  define('Standing','the conditions under which a movement may legitimately proceed',
    'Standing means more than a proposed operation or a message of approval. An examiner has to identify the governing conditions and the effect they actually support.',
    '../proofs/EXAMINATION-STANDARD.md','Public examination standard'),
  define('Admissibility','whether a candidate meets its required conditions',
    'The public account separates a candidate that can be described or simulated from one that may be admitted to a protected outcome under the current conditions.',
    '../foundation.html','Public admissibility account',['admissible']),
  define('Invariant','a condition that a claimed operation must preserve',
    'An invariant is a stated requirement that must remain true across the bounded transitions being examined. The exact invariant and evidence of preservation must be specified.',
    '../proofs/EXAMINATION-STANDARD.md','Examination of invariants',['invariants']),
  define('Kernelization','examining movement through a defined resolving boundary',
    'Within the V.A. account, kernelization means relating a candidate movement to its conditions of standing and continuation. The public teacher does not expose the protected kernel mechanism.',
    '../foundation.html','V.A. foundation',['kernelize','kernelized']),
  define('Proof Before Power','establish the relevant evidence before enabling a consequential effect',
    'For a bounded claim, examiners identify its original carrier, conditions, positive and negative controls, changed-condition replay and alternate routes. A slogan is not itself a proof.',
    '../proofs/EXAMINATION-STANDARD.md','Public proof standard'),
  define('Witness','an observable record of what actually happened',
    'A witness can be a specific trace, measurement or native carrier. Its identity, independence and scope determine what it supports; a model-generated description is not the same evidence.',
    '../proofs/EXAMINATION-STANDARD.md','Original-witness requirements',['witnesses']),
  define('Negative Control','a test in which the claimed effect should not form',
    'A negative control deliberately removes a required condition, so a measured refusal or absence of effect can challenge the claimed boundary.',
    '../proofs/EXAMINATION-STANDARD.md','Negative-control review',['negative controls']),
  define('Alternate Route','another path capable of reaching the same consequence',
    'Testing one blocked route is incomplete when a queue, retry or separate actuator can still produce the effect through another route.',
    '../proofs/EXAMINATION-STANDARD.md','Alternate-route examination',['alternate routes']),
  define('Replay','repeat the examination with identified inputs and conditions',
    'Replay asks whether the original carrier, input state and changed conditions permit another examiner to reproduce the specific claimed observation.',
    '../proofs/EXAMINATION-STANDARD.md','Replay criteria'),
].map(row=>Object.freeze({...row,aliases:Object.freeze(row.aliases),source:Object.freeze(row.source)})));

const escaped=value=>value.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
const findMatches=text=>{
  if(typeof text!=='string'||text.length>5000)return [];
  const hits=[];
  for(const entry of DEFINITIONS){
    let earliest=null;
    for(const phrase of [entry.term,...entry.aliases]){
      const pattern=new RegExp(`(^|[^a-zA-Z0-9])(${escaped(phrase)})(?![a-zA-Z0-9])`,'i');
      const found=pattern.exec(text);
      if(found){
        const index=found.index+found[1].length;
        if(!earliest||index<earliest.index||index===earliest.index&&phrase.length>earliest.length)
          earliest={entry,index,length:found[2].length};
      }
    }
    if(earliest)hits.push(earliest);
  }
  return hits.sort((a,b)=>a.index-b.index||b.length-a.length).filter((hit,i,arr)=>
    !arr.some((prior,j)=>j<i&&prior.index<=hit.index&&prior.index+prior.length>hit.index));
};

export function definitionsForLesson(text){return findMatches(text).map(hit=>hit.entry);}

export function convertTermDefinitions(text,{explained=new Set()}={}){
  if(typeof text!=='string')return '';
  const hits=findMatches(text);
  let result='',cursor=0;
  for(const hit of hits){
    const first=!explained.has(hit.entry.term);
    result+=text.slice(cursor,hit.index)+text.slice(hit.index,hit.index+hit.length)+(first?` (${hit.entry.short})`:'');
    explained.add(hit.entry.term);
    cursor=hit.index+hit.length;
  }
  return result+text.slice(cursor);
}
