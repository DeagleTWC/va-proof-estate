/* V.A. Consequence Aperture — data-only public workbench.
   No native runtime, no guessed outcomes, no server transmission, no status promotion. */
(()=>{'use strict';
const $=id=>document.getElementById(id);
const HEX=/^[0-9a-f]{64}$/i, KINDS=['POSITIVE','NEGATIVE','CHANGED','REPLAY'], STATUS='DECLARED_ONLY';
const clean=v=>typeof v==='string'&&v.trim().length>0;
const time=v=>typeof v==='string'&&Number.isFinite(Date.parse(v))&&/Z$|[+-][0-9]{2}:[0-9]{2}$/.test(v);
const download=(name,body)=>{const u=URL.createObjectURL(new Blob([JSON.stringify(body,null,2)+'\n'],{type:'application/json'}));const a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1000)};
const sha=async bytes=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(b=>b.toString(16).padStart(2,'0')).join('');
$('ap-request-form').addEventListener('submit',event=>{event.preventDefault();const f=new FormData(event.currentTarget);
 const routes=String(f.get('routes')).split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
 if(!routes.length){$('ap-draft-status').textContent='Declare at least one reachable route.';return;}
 const draft={schema:'VA-APERTURE-REQUEST-1',status:'DRAFT_UNISSUED',created_at:new Date().toISOString(),applicant:String(f.get('claimant')).trim(),
 freeze:{artifact_sha256:String(f.get('artifact_sha256')).toLowerCase(),standing:'DECLARED_BY_APPLICANT_UNANCHORED'},
 boundary:{protected_effect:String(f.get('protected_effect')).trim(),observation_scope:String(f.get('scope')).trim(),alternate_routes:routes},
 examiner_obligations:['Freeze before separate examiner challenge','Measure positive and negative effects','Change a load-bearing condition','Replay the frozen base condition','Preserve separate measurement, receipt and witness originals'],
 native_execution_occurred:false,independent_reproduction_established:false,production_authorized:false};
 download('va-aperture-challenge-request.json',draft);
 $('ap-draft-status').textContent='Unissued request downloaded. It is not a freeze, proof, or execution receipt.'});
const require=(condition,message,errors)=>{if(!condition)errors.push(message)};
const nameOK=s=>clean(s)&&s.length<160&&/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(s)&&s!=='.'&&s!=='..';
function structure(p,errors){
 require(p&&typeof p==='object'&&!Array.isArray(p),'Packet must be a JSON object.',errors);if(!p||typeof p!=='object')return;
 require(p.schema==='VA-APERTURE-1','Unrecognized packet schema.',errors);
 require(p.standing==='DECLARED_ONLY','Self-submitted packets cannot declare observed or independently reproduced standing.',errors);
 require(clean(p.packet_id),'Missing packet ID.',errors);
 const f=p.freeze||{},c=p.challenge||{},b=p.boundary||{},w=p.witness||{};
 require(clean(f.artifact_id)&&clean(f.owner_id)&&HEX.test(f.artifact_sha256||''),'Freeze needs artifact ID, owner ID and SHA-256.',errors);
 require(time(f.frozen_at)&&time(c.issued_at)&&Date.parse(f.frozen_at)<Date.parse(c.issued_at),'Declared freeze must precede challenge issuance.',errors);
 require(clean(f.anchor)&&/^https:\/\//.test(f.anchor),'Freeze requires a separate HTTPS chronology anchor (not independently checked).',errors);
 require(clean(c.id)&&clean(c.examiner_id)&&clean(c.condition_summary),'Challenge needs ID, examiner ID and condition summary.',errors);
 require(c.examiner_id!==f.owner_id,'Examiner ID must differ from applicant ID (identity not authenticated).',errors);
 require(clean(b.protected_effect)&&clean(b.observation_scope)&&Array.isArray(b.alternate_routes)&&b.alternate_routes.length>0&&b.alternate_routes.every(clean),'Protected effect, observation scope and route inventory required.',errors);
 require(clean(w.id)&&w.id!==f.owner_id&&nameOK(w.statement_file),'Witness declaration and original statement file required.',errors);
 require(Array.isArray(p.originals)&&p.originals.length>0,'Original file manifest required.',errors);
 const originals=new Map();
 if(Array.isArray(p.originals))for(const o of p.originals){
  if(!o||!nameOK(o.file)||!HEX.test(o.sha256||'')){errors.push('Invalid original manifest entry.');continue}
  if(originals.has(o.file))errors.push('Duplicate original: '+o.file);
  originals.set(o.file,o.sha256.toLowerCase());
 }
 require(originals.has(w.statement_file),'Witness statement must be in originals manifest.',errors);
 require(Array.isArray(p.controls)&&p.controls.length===4,'Exactly four independently described controls required.',errors);
 const runs=new Map(),used=new Set();if(Array.isArray(p.controls))for(const r of p.controls){
  if(!r||!KINDS.includes(r.kind)||runs.has(r.kind)){errors.push('Invalid or duplicate control kind.');continue}
  runs.set(r.kind,r);
  require(clean(r.condition_id),'Condition ID missing for '+r.kind,errors);
  require(typeof r.measured_effect==='boolean','Measured-effect observation is required for '+r.kind,errors);
  for(const fld of ['measurement_file','receipt_file']){
   require(nameOK(r[fld])&&originals.has(r[fld]),r.kind+' '+fld+' requires named original.',errors);
   if(nameOK(r[fld])){if(used.has(r[fld]))errors.push('Original reused across control roles: '+r[fld]);used.add(r[fld])}
  }
  require(r.measurement_file!==r.receipt_file,r.kind+' receipt cannot be its own measurement.',errors);
 }
 for(const kind of KINDS)require(runs.has(kind),'Missing '+kind+' control.',errors);
 if(runs.has('POSITIVE')&&runs.has('REPLAY'))require(runs.get('REPLAY').condition_id===runs.get('POSITIVE').condition_id,'Replay must use frozen baseline condition.',errors);
 if(runs.has('CHANGED')&&runs.has('POSITIVE'))require(runs.get('CHANGED').condition_id!==runs.get('POSITIVE').condition_id,'Changed control must change condition ID.',errors);
 require(p.claimed_proven!==true&&p.native_certified!==true&&p.independent_reproduced!==true,'Packet cannot self-certify native or independent proof.',errors);
 return originals;
}
async function inspect(event){event.preventDefault();const panel=$('ap-result');panel.dataset.status='';panel.replaceChildren();
 const heading=document.createElement('strong'),list=document.createElement('ul');panel.append(heading,list);
 const add=s=>{const li=document.createElement('li');li.textContent=s;list.appendChild(li)};
 const errors=[];let p;let raw;
 try{raw=await $('ap-packet').files[0].arrayBuffer();if(raw.byteLength>1024*1024)throw Error('Packet exceeds 1 MB.');p=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(raw))}
 catch(e){heading.textContent='PRECHECK FAILED';panel.dataset.status='fail';add('Packet unreadable: '+e.message);return}
 const originals=structure(p,errors),selected=new Map();
 for(const file of $('ap-originals').files){if(selected.has(file.name))errors.push('Duplicate attached filename: '+file.name);selected.set(file.name,file)}
 if(originals){for(const [name,digest]of originals){const file=selected.get(name);if(!file){errors.push('Missing exact original: '+name);continue}
 if(file.size>16*1024*1024){errors.push('File exceeds 16 MB browser preflight limit: '+name);continue}
 try{if(await sha(await file.arrayBuffer())!==digest)errors.push('SHA-256 mismatch: '+name)}catch(e){errors.push('Hash failed: '+name)}
 }
 for(const name of selected.keys())if(!originals.has(name))errors.push('Unlisted attached file: '+name);
 }
 heading.textContent=errors.length?'PRECHECK FAILED':'STRUCTURE AND ORIGINAL BYTES MATCH';
 panel.dataset.status=errors.length?'fail':'pass';
 if(errors.length)errors.forEach(add);
 else{add('SHA-256 matches all '+originals.size+' submitted original files.');add('Four control roles and declared condition relationships are structurally complete.');add('Packet SHA-256: '+await sha(raw));}
 add('Standing remains '+STATUS+'. No examiner identity, chronology, sensor calibration, actual effect or native V.A. execution was authenticated.');
}
$('ap-verify-form').addEventListener('submit',inspect);
})();