'use strict';
// Local, zero-network browser synthetic examiner. Not V.A. native implementation.
const $ = id => document.getElementById(id);
const clone = v => JSON.parse(JSON.stringify(v));
const DEFAULT = JSON.parse($('initialWorkflow').textContent);
let workflow = clone(DEFAULT);
let report = null;
let lastResponses = null;
let lastSource = '';
let revision = 0;
function invalidateEvidence(note){
 revision += 1;
 report = null; lastResponses = null; lastSource = '';
 $('summary').replaceChildren();
 $('resultsTable').replaceChildren();
 $('downloadReportBtn').disabled = true;
 $('downloadResponseBtn').disabled = true;
 if(note) msg('Changed conditions: apply your edits, then run the examination again. Previous results cleared.');
}
function setReport(r){ report=r; $('downloadReportBtn').disabled=false; $('downloadResponseBtn').disabled=!lastResponses; }

const keys = [
  ['authority_active','authority'],['evidence_fresh','fresh'],
  ['capacity_evidence_consistent','consistent'],['local_veto','veto'],
  ['jurisdiction_valid','jurisdiction'],['timebase_valid','timebase']
];
function positiveInt(v, label){const n=Number(v);if(!Number.isSafeInteger(n)||n<1)throw Error(`${label} must be a positive whole number`);return n;}
function nonnegInt(v,label){const n=Number(v);if(!Number.isSafeInteger(n)||n<0)throw Error(`${label} must be a nonnegative whole number`);return n;}
function state(){return {allocated:Object.fromEntries(workflow.sites.map(s=>[s.id,0])),water:Object.fromEntries(workflow.sites.map(s=>[s.id,0])),remaining:workflow.total_obligation,consumed:new Set()};}
function snapshot(st){return {allocated:clone(st.allocated),water:clone(st.water),remaining:st.remaining,total_bound:workflow.total_obligation-st.remaining};}
function oracle(e,site,st){
 const c=e.conditions;const reasons=[];
 if(!c.authority_active)reasons.push('authority revoked');
 if(!c.evidence_fresh)reasons.push('stale evidence');
 if(!c.capacity_evidence_consistent)reasons.push('contradictory capacity');
 if(c.local_veto)reasons.push('local veto');
 if(!c.jurisdiction_valid)reasons.push('invalid jurisdiction');
 if(!c.timebase_valid)reasons.push('invalid timebase');
 if(st.consumed.has(e.candidate_id))reasons.push('repeated candidate');
 if(e.units>st.remaining)reasons.push('unallocated obligation insufficient');
 if(st.allocated[e.site]+e.units>site.capacity)reasons.push('site capacity exceeded');
 if(st.water[e.site]+e.units*site.water_per_unit>site.water_budget)reasons.push('water budget exceeded');
 return reasons;
}
function validate(w){
 if(w.schema!=='va-zero-x-workflow/1.0')throw Error('Expected a va-zero-x-workflow/1.0 JSON file');
 if(!w.identity || !w.identity.protected_effect)throw Error('Protected effect is required');
 if(!Array.isArray(w.sites)||!w.sites.length||!Array.isArray(w.events)||!w.events.length||!Array.isArray(w.routes)||!w.routes.length)throw Error('Provide sites, routes and events');
 if(new Set(w.sites.map(s=>s.id)).size!==w.sites.length)throw Error('Duplicate site IDs');
 if(new Set(w.routes).size!==w.routes.length)throw Error('Duplicate routes');
 positiveInt(w.total_obligation,'Total obligation');
 for(const s of w.sites){for(const k of ['capacity','water_budget','water_per_unit'])nonnegInt(s[k],`${s.id} ${k}`);}
 const seen=new Set();
 for(const e of w.events){
  if(seen.has(e.id)||!e.id)throw Error('Duplicate or missing event ID');seen.add(e.id);
  if(!w.sites.find(s=>s.id===e.site) || !w.routes.includes(e.route))throw Error('Unknown site or route in '+e.id);
  positiveInt(e.units,e.id+' units');if(!e.candidate_id)throw Error('Missing candidate in '+e.id);
  const s=w.sites.find(s=>s.id===e.site);if(!Number.isSafeInteger(e.units*s.water_per_unit))throw Error('Water arithmetic exceeds safe integer range in '+e.id);
  for(const [key] of keys)if(typeof e.conditions?.[key]!=='boolean')throw Error('Missing condition '+key+' in '+e.id);
 }
}
function referenceResponses(){
 const st=state();const sites=Object.fromEntries(workflow.sites.map(s=>[s.id,s]));const r=[];
 for(const e of workflow.events){
  const ok=oracle(e,sites[e.site],st).length===0;
  if(ok){st.allocated[e.site]+=e.units;st.water[e.site]+=e.units*sites[e.site].water_per_unit;st.remaining-=e.units;st.consumed.add(e.candidate_id);}
  r.push({id:e.id,decision:ok?'BIND':'NO_BIND',effect_request:ok?{site:e.site,units:e.units}:null});
 }return r;
}
function evaluate(responses, source){
 validate(workflow);
 if(!Array.isArray(responses)||responses.length!==workflow.events.length)throw Error(`Expected ${workflow.events.length} responses, found ${responses?.length??'none'}`);
 const st=state();const sites=Object.fromEntries(workflow.sites.map(s=>[s.id,s]));const rows=[];
 for(let i=0;i<workflow.events.length;i++){
  const e=workflow.events[i],r=responses[i];
  if(r?.id!==e.id)throw Error(`Response identity mismatch at ${e.id}`);
  if(!['BIND','NO_BIND'].includes(r.decision))throw Error('Unknown decision at '+e.id);
  const before=snapshot(st), reasons=oracle(e,sites[e.site],st), expect=reasons.length?'NO_BIND':'BIND';let faults=[];
  const eff=r.effect_request;
  if(eff!==null && eff!==undefined){
    if(!eff||!sites[eff.site]||!Number.isSafeInteger(eff.units)||eff.units<=0)throw Error('Invalid effect request at '+e.id);
    if(!Number.isSafeInteger(eff.units*sites[eff.site].water_per_unit))throw Error('Effect arithmetic exceeds safe integer range at '+e.id);
    st.allocated[eff.site]+=eff.units;st.water[eff.site]+=eff.units*sites[eff.site].water_per_unit;st.remaining-=eff.units;
    if(r.decision==='BIND')st.consumed.add(e.candidate_id);
  }
  if(r.decision!==expect)faults.push('Decision contradicts conditions');
  if(expect==='BIND' && (!eff||eff.site!==e.site||eff.units!==e.units))faults.push('Required admitted effect missing or different');
  if(expect==='NO_BIND'&&eff)faults.push('Unauthorized mock effect occurred');
  if(r.decision==='NO_BIND'&&eff)faults.push('Refusal recorded, but mock effect occurred');
  if(st.remaining<0)faults.push('Duplicated or extra workload');
  for(const s of workflow.sites)if(st.allocated[s.id]>s.capacity||st.water[s.id]>s.water_budget)faults.push('Site capacity or water limit breached');
  if(Object.values(st.allocated).reduce((a,b)=>a+b,0)+st.remaining!==workflow.total_obligation)faults.push('Workload conservation failed');
  const after=snapshot(st);
  rows.push({id:e.id,site:e.site,route:e.route,candidate_id:e.candidate_id,expected:expect,decision:r.decision,
    effect_request:eff??null,unmet_conditions:reasons,mock_before:before,mock_after:after,
    verdict:faults.length?'FAIL':'PASS',findings:[...new Set(faults)]});
 }
 const fails=rows.filter(x=>x.verdict==='FAIL');
 return {schema:'va-zero-x-browser-report/1.0',evidence_class:'SYNTHETIC_MOCK_EFFECT_ONLY',
    response_source:source,native_va_proof:'NOT_ESTABLISHED',independent_effect_witness:'NOT_ESTABLISHED',
    workflow:clone(workflow),case_count:rows.length,passing_events:rows.length-fails.length,failing_events:fails.length,
    final_mock_state:snapshot(st),events:rows,overall:fails.length?'SYNTHETIC_PROTOCOL_FAIL':'SYNTHETIC_PROTOCOL_PASS',
    note:'Browser reference or imported decisions tested against a local MOCK effect state. No protected V.A. kernel, independent observed physical effect or operational endorsement.'};
}
function download(name,obj){
 const data=typeof obj==='string'?obj:JSON.stringify(obj,null,2)+'\n';
 const url=URL.createObjectURL(new Blob([data],{type:'application/json;charset=utf-8'}));
 const a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),5000);
}
function msg(t, bad=false){const s=$('actionStatus');s.textContent=t;s.className=bad?'status bad':'status good';}
function saveTop(){
 workflow.identity.name=$('wfName').value.trim();workflow.identity.owner=$('wfOwner').value.trim();
 workflow.identity.protected_effect=$('wfEffect').value.trim();
 workflow.total_obligation=positiveInt($('wfTotal').value,'Total obligation');
 validate(workflow);
}
function loadTop(){
 $('wfName').value=workflow.identity.name||'';$('wfEffect').value=workflow.identity.protected_effect||'';
 $('wfOwner').value=workflow.identity.owner||'';$('wfTotal').value=workflow.total_obligation;
 $('eventSelect').replaceChildren(...workflow.events.map(e=>new Option(`${e.id} — ${e.note||e.site+' '+e.route}`,e.id)));
 $('editSite').replaceChildren(...workflow.sites.map(s=>new Option(s.id,s.id)));
 $('editRoute').replaceChildren(...workflow.routes.map(s=>new Option(s,s)));
 editEvent();renderSiteEditor();
}
function selected(){return workflow.events.find(e=>e.id===$('eventSelect').value)}
function editEvent(){const e=selected();if(!e)return;
 $('editSite').value=e.site;$('editRoute').value=e.route;$('editUnits').value=e.units;
 for(const [key,id] of keys)$(id).checked=e.conditions[key];
}
function applyEvent(){invalidateEvidence(false);const e=selected();if(!e)throw Error('Select a test event');
 e.site=$('editSite').value;e.route=$('editRoute').value;e.units=positiveInt($('editUnits').value,'Proposed units');
 for(const [key,id] of keys)e.conditions[key]=$(id).checked;
 validate(workflow);msg(`Updated ${e.id}. Run the safe example to see its effect.`);
}
function renderSiteEditor(){
 const root=$('siteEditor');root.replaceChildren();
 for(const title of ['Site','Capacity','Water limit','Water per unit']){const e=document.createElement('div');e.className='site-head';e.textContent=title;root.appendChild(e);}
 for(const s of workflow.sites){const name=document.createElement('div');name.textContent=s.id;name.style.paddingTop='12px';root.appendChild(name);
  for(const key of ['capacity','water_budget','water_per_unit']){const input=document.createElement('input');input.type='number';input.min='0';input.step='1';input.value=s[key];input.dataset.site=s.id;input.dataset.key=key;input.setAttribute('aria-label',s.id+' '+key);root.appendChild(input);}
 }
}
function applySites(){invalidateEvidence(false);for(const x of $('siteEditor').querySelectorAll('input')){
 const s=workflow.sites.find(s=>s.id===x.dataset.site);s[x.dataset.key]=nonnegInt(x.value,x.dataset.site+' '+x.dataset.key);
 }validate(workflow);msg('Facility limits updated. Run the example again.');}
function renderResults(r){
 const summary=$('summary');summary.replaceChildren();
 for(const [value,label] of [[r.passing_events+' / '+r.case_count,'Synthetic cases passed'],[r.failing_events,'Cases with findings'],[r.final_mock_state.total_bound,'Mock workload allocated'],[r.final_mock_state.remaining,'Workload still accounted for']]){
  const d=document.createElement('div');d.className='stat';
  const n=document.createElement('strong');n.textContent=value;const t=document.createElement('span');t.textContent=label;
  d.append(n,t);summary.appendChild(d);
 }
 const root=$('resultsTable');root.replaceChildren();const table=document.createElement('table');
 const head=document.createElement('thead');const hr=document.createElement('tr');
 for(const h of ['Event / route','Site / units','Expected','Returned','Actual mock effect','Verdict / why']){const th=document.createElement('th');th.textContent=h;hr.appendChild(th);}head.appendChild(hr);table.appendChild(head);
 const body=document.createElement('tbody');
 for(const row of r.events){const tr=document.createElement('tr');
  const e=r.workflow.events.find(e=>e.id===row.id);
  const cells=[`${row.id} · ${row.route}`,`${row.site} · ${e.units}`,row.expected,row.decision,
    row.effect_request?`${row.effect_request.units} units to ${row.effect_request.site}`:'None',
    row.verdict+(row.findings.length?' — '+row.findings.join('; '):(row.unmet_conditions.length?' — blocked: '+row.unmet_conditions.join(', '):' — admitted mock effect'))];
  cells.forEach((v,i)=>{const td=document.createElement('td');td.textContent=v;if(i===5)td.className=row.verdict==='PASS'?'good':'bad';tr.appendChild(td);});body.appendChild(tr);
 }table.appendChild(body);root.appendChild(table);
 const note=document.createElement('p');note.className='small';note.textContent=`${r.response_source} • ${r.overall} • NATIVE V.A. PROOF: NOT ESTABLISHED. These are simulated after-state observations, not actual hardware effects.`;root.prepend(note);
}
async function readFile(input){const f=input.files?.[0];if(!f)return null;if(f.size>2000000)throw Error('JSON file exceeds 2 MB. Use the offline adapter for larger test sets.');const data=await f.text();return JSON.parse(data);}
async function importWorkflow(){try{const obj=await readFile($('workflowFile'));if(!obj)return;validate(obj);workflow=clone(obj);invalidateEvidence(false);loadTop();msg('Your workflow scenario loaded. Review its conditions and run the safe example.');}catch(e){msg(e.message,true)}finally{$('workflowFile').value=''}}
async function importResponses(){try{saveTop();const responses=await readFile($('responsesFile'));if(!responses)return;invalidateEvidence(false);lastResponses=clone(responses);lastSource='import';setReport(evaluate(responses,'EXAMINER_IMPORTED_RESPONSES_UNAUTHENTICATED'));renderResults(report);msg('Imported response comparison complete. Check every case and its evidence boundary.');}catch(e){msg(e.message,true)}finally{$('responsesFile').value=''}}
function guard(fn){return ()=>{try{fn()}catch(e){msg(e.message,true);console.error(e)}}}
function guide(){return `ZERO-X PUBLIC EXAMINER QUICK GUIDE

1. Open the V.A. ZERO-X public website or local index.html.
2. Describe one consequential workflow and its total obligation.
3. Run the included synthetic case, then edit authority, capacity, veto, or route conditions and run again.
4. Save your own workflow and JSON response template.
5. To examine your own system, import only non-sensitive, bounded response JSON. Each response needs an event id, BIND/NO_BIND decision, and optional mock effect request.
6. The browser will show a synthetic before/after mock state and label any disallowed effect; it does not operate your technology.
7. For real local executable adapters use the separate public Bring Your Own Workflow examiner at:
   https://github.com/DeagleTWC/va-proof-estate/tree/main/examiner/
8. The 10–100-year horizon selection describes proposed input sizes only. There are no native V.A. long-horizon results on this page.
9. Do not enter private code, customer data, secrets, live equipment instructions, or protected native construction.
10. Independent native V.A. execution requires a separately authorized handoff and original evidence.

No proof of native V.A. formation, physical effects, or CEOS/ZERO execution is conferred by this browser demo.
OPEN EVIDENCE. PROTECTED CONSTRUCTION. PROOF BEFORE POWER.
`;}
$('runDemoBtn').addEventListener('click',guard(()=>{saveTop();invalidateEvidence(false);lastResponses=referenceResponses();lastSource='sample';setReport(evaluate(lastResponses,'INCLUDED_CONVENTIONAL_SAMPLE_NOT_VA'));renderResults(report);msg('Synthetic example completed. Inspect case-by-case results; this is not a native V.A. execution.');}));
$('loadWorkflowBtn').addEventListener('click',()=>$('workflowFile').click());$('loadResponsesBtn').addEventListener('click',()=>$('responsesFile').click());
$('workflowFile').addEventListener('change',importWorkflow);$('responsesFile').addEventListener('change',importResponses);
$('downloadWorkflowBtn').addEventListener('click',guard(()=>{saveTop();download('MY_ZERO_X_WORKFLOW.json',workflow);msg('Saved editable workflow JSON.');}));
$('downloadReportBtn').addEventListener('click',guard(()=>{if(!report)throw Error('Run a test or import your responses first');download('MY_ZERO_X_EXAMINATION_REPORT.json',report);msg('Saved the synthetic evidence report.');}));
$('downloadResponseBtn').addEventListener('click',guard(()=>{if(!lastResponses)throw Error('Run the safe example or import responses first');download('ZERO_X_EXAMPLE_RESPONSES.json',lastResponses);msg('Saved responses for examination.');}));
$('templateBtn').addEventListener('click',guard(()=>{saveTop();download('MY_RESPONSES_TEMPLATE.json',workflow.events.map(e=>({id:e.id,decision:'NO_BIND',effect_request:null})));msg('Template saved. Fill this with your actual bounded workflow responses.');}));
$('downloadGuideBtn').addEventListener('click',()=>download('ZERO_X_PUBLIC_QUICK_GUIDE.txt',guide()));
$('eventSelect').addEventListener('change',editEvent);
$('saveEventBtn').addEventListener('click',guard(()=>{saveTop();applyEvent()}));
$('addEventBtn').addEventListener('click',guard(()=>{saveTop();invalidateEvidence(false);const prev=selected()||workflow.events.at(-1);const e=clone(prev);e.id='MY-'+String(workflow.events.length+1).padStart(3,'0');e.candidate_id='new-candidate-'+e.id;e.note='Independent examiner added case';workflow.events.push(e);loadTop();$('eventSelect').value=e.id;editEvent();msg('New independent test added. Change its conditions and apply.');}));
$('restoreBtn').addEventListener('click',()=>{workflow=clone(DEFAULT);invalidateEvidence(false);loadTop();msg('Original synthetic scenario restored.');});
$('saveSitesBtn').addEventListener('click',guard(()=>{saveTop();applySites()}));
$('horizon').addEventListener('change',()=>{$('horizonText').textContent=`${$('horizon').value} synthetic years selected. The 10–100 year generator produces input cases only, not 10–100 years of native outcomes.`;});
loadTop();

// A downloaded report must never describe any unexamined post-run field edits.
const watchedIds = ['wfName','wfEffect','wfOwner','wfTotal','editSite','editRoute','editUnits',
 'authority','fresh','consistent','veto','jurisdiction','timebase'];
for(const id of watchedIds) $(id).addEventListener('input', ()=>invalidateEvidence(true));
$('siteEditor').addEventListener('input', (e)=>{if(e.target?.matches('input'))invalidateEvidence(true);});
$('downloadReportBtn').disabled=true;
$('downloadResponseBtn').disabled=true;