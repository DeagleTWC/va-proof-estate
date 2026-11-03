/* V.A. | Proof in Motion — public source-bound visitor examination.
   No kernel execution, effect simulation, telemetry or source promotion. */
(() => {
  'use strict';

  const ROOT = document.body.dataset.root || '';
  const REGISTER_PATH = 'proofs/CLAIM-TO-CARRIER.json';
  const PROOF_STANDARD = 'proofs/EXAMINATION-STANDARD.md';
  const WEBSITE = 'https://deagletwc.github.io/va-proof-estate/';
  const SCENARIOS = Object.freeze([
    {
      id: 'standing', number: '01', title: 'Standing holds',
      description: 'Before the boundary', claimId: 'VA-N01',
      question: 'What should the examination require before protected consequence is permitted?',
      expected: 'bind',
      prediction: 'Conditional admission may be established only with actual, present standing and a bounded observed consequence.',
      falsifier: 'A protected effect forms despite loss or absence of a load-bearing standing condition.',
      boundary: 'Present standing is declared; original executable native consequence observations are not attached here.',
      shareTitle: 'Can you establish standing before consequence?',
      page: 'challenge/standing.html'
    },
    {
      id: 'authority', number: '02', title: 'Authority removed',
      description: 'A non-formation challenge', claimId: 'VA-N02',
      question: 'What should happen to protected consequence after a load-bearing authority condition is withdrawn?',
      expected: 'no-bind',
      prediction: 'The declared requirement is REFUSE / NO-BIND, supported by measurements of the consequence boundary—not only a decision label.',
      falsifier: 'Any declared reachable route forms the protected effect after the required authority or standing is removed.',
      boundary: 'The native refusal/no-effect receipt and instrumented consequence packet are not attached here.',
      shareTitle: 'Can you prove what did not form?',
      page: 'challenge/authority.html'
    },
    {
      id: 'alternate', number: '03', title: 'Alternate route',
      description: 'Close the bypass', claimId: 'VA-P02',
      question: 'If a forbidden consequence might form through another route, what must the physical examination establish?',
      expected: 'no-bind',
      prediction: 'All declared reachable routes within the fixed observation boundary must be examined for forbidden effects under the negative control.',
      falsifier: 'A prohibited physical effect is detected through an unexamined or supposedly closed route, or the instruments cannot cover the claimed boundary.',
      boundary: 'An independently instrumented physical negative-control run is not attached in the current public release.',
      shareTitle: 'Did the forbidden consequence find another path?',
      page: 'challenge/alternate-route.html'
    }
  ]);
  const EXPECTATIONS = Object.freeze([
    {value:'bind',label:'Conditional formation may be permitted'},
    {value:'no-bind',label:'Protected consequence must not form'},
    {value:'unknown',label:'Released evidence cannot establish an actual result'}
  ]);
  const registerURL = ROOT + REGISTER_PATH;
  const app = document.getElementById('cc-app');
  const initial = document.body.dataset.scenario || 'authority';
  const state = {current:SCENARIOS.some(s=>s.id===initial)?initial:'authority',
                 predicted:null, revealed:false, register:null, registerHash:null,
                 loading:true, error:null, message:'', examinerMode:false};

  function safe(x) {
    return String(x === undefined || x === null ? '' : x)
      .replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }
  function localPath(path) {
    return typeof path === 'string' && !path.includes('..') &&
      /^(?:proofs|challenges|examiner)\/[A-Za-z0-9/_\-.#]+$/.test(path) ? ROOT + path : null;
  }
  function getScenario(id) {return SCENARIOS.find(s=>s.id===id) || SCENARIOS[1];}
  function getRecord(id) {return state.register?.entries.find(x=>x.id===id) || null;}
  function hex(buf) {return [...new Uint8Array(buf)].map(x=>x.toString(16).padStart(2,'0')).join('');}
  async function getSHA256(data) {
    if (!globalThis.crypto?.subtle) return null;
    return hex(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(data)));
  }

  /* Pure constructor; source records remain verbatim at their public standing. */
  function buildPassport(record, sourceHash, scenario, prediction, published) {
    return {
      schemaVersion:'VA-PUBLIC-CHALLENGE-PASSPORT-1.0',
      recordType:'VISITOR_GENERATED_EXAMINATION_NOT_NATIVE_PROOF',
      claimPromotion:false,
      site:'V.A. — The Proof Estate',
      publicReference:WEBSITE + scenario.page,
      generatedAt:new Date().toISOString(),
      generatedLocally:true,
      sourceRegister:{
        path:REGISTER_PATH, url:WEBSITE + REGISTER_PATH,
        exactBytesSHA256:sourceHash || 'NOT VERIFIED IN THIS BROWSER',
        published:published || 'UNSPECIFIED'
      },
      challenge:{
        scenarioId:scenario.id, claimId:scenario.claimId,
        question:scenario.question,
        visitorPrediction:prediction || 'NOT SELECTED',
        declaredExaminationExpectation:scenario.prediction,
        proposedFalsificationQuestion:scenario.falsifier,
        expectedResultIsNotObservedResult:true
      },
      publicClaimCarrier:{
        id:record.id, class:record.class, standing:record.standing,
        nativeVAEvidence:record.nativeVAEvidence === true,
        carrier:record.carrier || null, source:record.source || null,
        sourceTextCarrier:record.sourceTextCarrier || null,
        sourcePdfSHA256:record.sourcePdfSHA256 || null,
        scope:record.scope || null, sourceScope:record.sourceScope || null
      },
      evidenceBoundary:{
        observedNativeEffect:'NOT ATTACHED HERE',
        independentlyReproducedNativeEffect:'NOT ATTACHED HERE',
        scenarioEvidenceGap:scenario.boundary,
        conclusion:'This passport is a locally generated navigation and examination record, not a signed V.A. receipt, independent witness, native system run, or physical result.'
      },
      verification:'Hash the exact public claim-register bytes and compare to sourceRegister.exactBytesSHA256. Check the claim ID and fields against the linked source. A matching hash establishes byte identity, not scientific truth or independent reproduction.'
    };
  }
  function buttonLabel(choice) {return EXPECTATIONS.find(p=>p.value===choice)?.label || 'No prediction selected';}
  function statusBadge(record) {
    const standing = record?.standing || 'NOT AVAILABLE';
    return '<span class="cc-status '+(standing==='OBSERVED'?'observed':'')+'">'+safe(standing)+'</span>';
  }
  function linkToSource(record) {
    const source = localPath(record?.sourceTextCarrier || record?.source || '');
    return source?'<a class="cc-link" href="'+safe(source)+'">Read the original published source</a>':
      '<span class="cc-secondary">Exact public source link not supplied</span>';
  }
  function cardLane(id, caption) {
    const record = getRecord(id);
    if (!record) return '<article class="cc-evidence"><h3>'+safe(caption)+'</h3><p>Source entry unavailable.</p></article>';
    return '<article class="cc-evidence"><h3>'+safe(caption)+'</h3><p>'+statusBadge(record)+'</p>'+
      '<p><strong>'+safe(record.id)+' · '+safe(record.class)+'</strong></p>'+
      '<p>'+safe(record.scope)+'</p></article>';
  }
  const orb = '<svg class="cc-orbit" viewBox="0 0 320 220" aria-hidden="true" focusable="false">'+
    '<g class="cc-orbit-spin"><circle class="cc-orbit-ring" cx="160" cy="110" r="95" stroke-width=".7"/>'+
    '<circle class="cc-orbit-ring" cx="160" cy="110" r="74" stroke-width="1"/>'+
    '<circle class="cc-orbit-ring" cx="160" cy="110" r="52" stroke-width=".65"/>'+
    '<circle cx="160" cy="15" r="4" fill="#e6b66e"/><circle cx="234" cy="110" r="2.8" fill="#e6b66e"/></g>'+
    '<path class="cc-orbit-light" d="M48 110H272M160 0V220" stroke-dasharray="3 7"/>'+
    '<circle class="cc-orbit-core" cx="160" cy="110" r="7"/>'+
    '<path d="M126 88 144 126 160 91 176 126 194 88M141 141 160 103 179 141" fill="none" stroke="#f3cb80" stroke-width="2.3"/></svg>';

  function render() {
    if (!app) return;
    if (state.loading) {app.innerHTML='<div class="cc-note" role="status">Loading the original public claim register…</div>';return;}
    if (state.error) {
      app.innerHTML='<div class="cc-error" role="alert"><strong>Source-bound examination unavailable.</strong> '+
        safe(state.error)+'. No result is displayed without its current register. '+
        '<a class="cc-link" href="'+safe(registerURL)+'">Open the public claim-to-carrier register</a>.</div>';
      return;
    }
    const scenario=getScenario(state.current),record=getRecord(scenario.claimId);
    if (!record) {state.error='The required claim is missing';render();return;}
    const sourceHash=state.registerHash || 'NOT VERIFIED IN THIS BROWSER';
    const buttons=SCENARIOS.map(s=>'<button type="button" class="cc-choice" data-case="'+s.id+'" aria-pressed="'+(s.id===scenario.id)+'">'+
      '<span class="cc-number">EXAMINATION '+s.number+'</span><strong>'+safe(s.title)+'</strong>'+
      '<small>'+safe(s.description)+'</small></button>').join('');
    const options=EXPECTATIONS.map(p=>'<button type="button" class="cc-option" data-prediction="'+p.value+'" aria-pressed="'+(p.value===state.predicted)+'">'+
      '<span class="cc-dot" aria-hidden="true"></span>'+safe(p.label)+'</button>').join('');
    const expectedMatch=state.predicted===scenario.expected;
    const reveal = state.revealed?
      '<div class="cc-reveal" id="cc-reveal" tabindex="-1" aria-live="polite">'+
      '<span class="cc-kicker">EXAMINATION / EXPECTED BEHAVIOR</span><h3>'+safe(scenario.prediction)+'</h3>'+
      '<p>'+(expectedMatch?'Your prediction matches the declared examination expectation.':
      'Your selection opens a valid question, but the declared test requirement is different from that prediction.')+'</p>'+
      '<p><strong>Actual native outcome:</strong> NOT ESTABLISHED BY THIS PUBLIC ENTRY. '+safe(scenario.boundary)+'</p>'+
      '<p><strong>What would falsify this bounded claim?</strong> '+safe(scenario.falsifier)+'</p>'+
      '<p class="cc-source-note">'+statusBadge(record)+' '+safe(record.id)+' / '+safe(record.class)+
      ' · This badge describes public record standing, not your prediction.</p></div>':'';
    document.body.classList.toggle('cc-examiner-mode',state.examinerMode);
    app.innerHTML=
      '<div class="cc-view-switch" role="group" aria-label="Reading mode">'+
      '<button type="button" class="cc-view-button" data-mode="visitor" aria-pressed="'+(!state.examinerMode)+'">Visual examination</button>'+
      '<button type="button" class="cc-view-button" data-mode="examiner" aria-pressed="'+state.examinerMode+'">Examiner mode · exact record</button></div>'+
      (state.examinerMode?
      '<section class="cc-section cc-examiner-detail"><div class="cc-heading"><h2>Original register entry</h2>'+
      '<p>Exact source JSON fields. No generated native result.</p></div>'+
      '<pre class="cc-raw-record" tabindex="0">'+safe(JSON.stringify(record,null,2))+'</pre></section>':'')+
      '<section class="cc-section" aria-labelledby="cc-select-title"><div class="cc-heading"><div>'+
      '<div class="cc-kicker">01 / Select a condition</div><h2 id="cc-select-title">Choose your challenge.</h2></div>'+
      '<p>No score or artificial proof animation. Each choice points to an identified public record.</p></div>'+
      '<div class="cc-grid">'+buttons+'</div></section>'+
      '<section class="cc-section" aria-labelledby="cc-question-title"><div class="cc-heading"><div>'+
      '<div class="cc-kicker">02 / Examine the boundary</div><h2 id="cc-question-title">Make a prediction.</h2></div>'+
      '<p>Predict the required behavior of the declared test—not an unobserved real-world result.</p></div>'+
      '<div class="cc-inquiry"><div class="cc-panel"><span class="cc-disc">'+safe(record.id)+
      ' · '+safe(record.class)+'</span><h3 class="cc-question">'+safe(scenario.question)+'</h3>'+
      '<div class="cc-options" role="group" aria-label="Choose a test prediction">'+options+'</div>'+
      '<div class="cc-actions"><button class="cc-action" id="cc-reveal-button" type="button" '+
      (state.predicted?'':'disabled')+'>Reveal the evidence requirement</button></div></div>'+
      '<div class="cc-panel cc-context" data-choice="'+safe(state.predicted||'unknown')+'">'+orb+
      '<small>Standing → admissibility → consequence custody</small>'+
      '<p>Visual examination map. Not a V.A. runtime visualization or observed effect.</p></div></div>'+
      reveal+'</section>'+
      '<section class="cc-section" aria-labelledby="cc-proof-title"><div class="cc-heading"><div>'+
      '<div class="cc-kicker">03 / Claim-to-carrier</div><h2 id="cc-proof-title">Follow the original record.</h2></div>'+
      '<p>For this challenge, the published entry has its own class, standing and limits.</p></div>'+
      '<div class="cc-panel"><p>'+statusBadge(record)+' &nbsp; <strong>'+safe(record.id)+'</strong> / '+safe(record.class)+'</p>'+
      '<p>'+safe(record.scope)+'</p><p class="cc-secondary">Original native run carrier: <strong>'+
      (record.carrier?safe(record.carrier):'NOT ATTACHED HERE')+'</strong></p>'+
      '<p class="cc-secondary">Source designation: '+safe(record.sourceScope || record.source || 'See public register')+'</p>'+
      '<p class="cc-digest">Public source register SHA-256: '+safe(sourceHash)+'</p>'+
      (record.sourcePdfSHA256?'<p class="cc-digest">Source PDF identity (from register): '+safe(record.sourcePdfSHA256)+'</p>':'')+
      '<div class="cc-links">'+linkToSource(record)+
      '<a class="cc-link" href="'+safe(registerURL)+'">Full claim register</a>'+
      '<a class="cc-link" href="'+safe(ROOT+PROOF_STANDARD)+'">Seven-part examination standard</a>'+
      '</div></div></section>'+
      '<section class="cc-section" aria-labelledby="cc-gallery-title"><div class="cc-heading"><div>'+
      '<div class="cc-kicker">04 / Three independent questions</div><h2 id="cc-gallery-title">Formation. Non-formation. Change.</h2></div>'+
      '<p>Different proof obligations; none inherits another claim’s evidence class.</p></div>'+
      '<div class="cc-evidence-grid">'+cardLane('VA-N01','Positive standing')+
      cardLane('VA-N02','Non-formation')+cardLane('VA-N03','Changed conditions')+'</div>'+
      '<p class="cc-secondary" style="margin-top:14px">The public register also contains one observed synthetic fixture (VA-AD-001). It is not a native V.A. run or a physical result. There is no independently reproduced native run attached to this release.</p></section>'+
      '<section class="cc-section" aria-labelledby="cc-share-title"><div class="cc-heading"><div>'+
      '<div class="cc-kicker">05 / Pass the challenge forward</div><h2 id="cc-share-title">One question. One evidence trail.</h2></div>'+
      '<p>Share the source-linked question, not a fabricated performance result.</p></div>'+
      '<div class="cc-panel"><div class="cc-export">'+
      '<button class="cc-action" type="button" id="cc-share">Share challenge</button>'+
      '<button class="cc-action alt" type="button" id="cc-copy">Copy permanent link</button>'+
      '<button class="cc-action alt" type="button" id="cc-image">Download gold challenge card (PNG)</button>'+
      '<button class="cc-action alt" type="button" id="cc-passport">Export source-linked Proof Passport (JSON)</button>'+
      '</div><p class="cc-toast" id="cc-toast" role="status" aria-live="polite">'+safe(state.message)+'</p>'+
      '<p class="cc-secondary">The share card is generated locally in your browser. The Proof Passport records this visitor examination, the original public source hash and the declared evidence ceiling; it is not a cryptographic signature or a native receipt.</p>'+
      '<div class="cc-links"><a class="cc-link" href="'+safe(ROOT+'reviewer-route.html')+'">Start independent review</a>'+
      '<a class="cc-link" href="'+safe(ROOT+'examiner/INDEPENDENT-CHALLENGE.md')+'">Read the fresh-challenge protocol</a>'+
      '<a class="cc-link" href="https://github.com/DeagleTWC/va-proof-estate/issues/1">Submit a bounded public challenge</a></div></div></section>';

    app.querySelectorAll('[data-mode]').forEach(button=>button.addEventListener('click',()=>{
      state.examinerMode=button.dataset.mode==='examiner';state.message='';render();
    }));
    app.querySelectorAll('[data-case]').forEach(button=>button.addEventListener('click',()=>{
      state.current=button.dataset.case;state.predicted=null;state.revealed=false;state.message='';
      // Keep this document URL fixed so its relative sources and links remain valid.
      // The share action uses the selected scenario's own permanent URL.
      render();
    }));
    app.querySelectorAll('[data-prediction]').forEach(button=>button.addEventListener('click',()=>{
      state.predicted=button.dataset.prediction;state.revealed=false;state.message='';render();
    }));
    app.querySelector('#cc-reveal-button').addEventListener('click',()=>{
      if (!state.predicted) return;
      state.revealed=true;render();
      app.querySelector('#cc-reveal')?.focus();
    });
    app.querySelector('#cc-share').addEventListener('click',()=>shareChallenge(scenario));
    app.querySelector('#cc-copy').addEventListener('click',()=>copyChallenge(scenario));
    app.querySelector('#cc-image').addEventListener('click',()=>downloadCard(scenario,record));
    app.querySelector('#cc-passport').addEventListener('click',()=>downloadPassport(scenario,record));
  }

  function shareURL(scenario) {return WEBSITE+scenario.page;}
  function toast(message) {
    state.message=message;
    const el=document.getElementById('cc-toast');if(el)el.textContent=message;
  }
  async function copyChallenge(scenario) {
    const url=shareURL(scenario);
    try {
      if (navigator.clipboard?.writeText) {await navigator.clipboard.writeText(url);toast('Permanent challenge link copied.');return;}
      const input=document.createElement('textarea');input.value=url;input.setAttribute('readonly','');input.style.position='fixed';input.style.opacity='0';
      document.body.appendChild(input);input.select();
      const ok=document.execCommand('copy');input.remove();
      toast(ok?'Permanent challenge link copied.':'Copy unavailable. Use this link: '+url);
    } catch (_) {toast('Copy unavailable. Use this link: '+url);}
  }
  async function shareChallenge(scenario) {
    const payload={title:'V.A. | '+scenario.shareTitle,
      text:scenario.question+' Examine the public claim record and its evidence standing.',
      url:shareURL(scenario)};
    if(navigator.share){try{await navigator.share(payload);toast('Share sheet opened for the source-linked challenge.');return;}
      catch(e){if(e.name==='AbortError')return;}}
    await copyChallenge(scenario);
  }

  function downloadBlob(name,blob) {
    const url=URL.createObjectURL(blob),link=document.createElement('a');
    link.href=url;link.download=name;document.body.appendChild(link);link.click();link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),30000);
  }
  function downloadPassport(scenario,record) {
    const passport=buildPassport(record,state.registerHash,scenario,state.predicted,state.register.published);
    downloadBlob('VA-'+scenario.id+'-proof-passport.json',new Blob([JSON.stringify(passport,null,2)+'\n'],{type:'application/json'}));
    toast('Public Proof Passport saved locally. No site upload or native result asserted.');
  }
  function wrapText(ctx,text,x,y,maxWidth,lineHeight,maxLines) {
    const words=text.split(/\s+/);let line='',count=0;
    for(const word of words){
      const sample=line?line+' '+word:word;
      if(ctx.measureText(sample).width>maxWidth&&line){
        ctx.fillText(line,x,y);y+=lineHeight;line=word;count++;
        if(count>=maxLines-1)break;
      }else line=sample;
    }
    if(line&&count<maxLines)ctx.fillText(line,x,y);
  }
  function downloadCard(scenario,record) {
    const canvas=document.createElement('canvas');
    canvas.width=1200;canvas.height=630;
    const c=canvas.getContext('2d');
    if(!c){toast('PNG export is unavailable in this browser.');return;}
    const bg=c.createLinearGradient(0,0,1200,630);bg.addColorStop(0,'#080807');bg.addColorStop(.65,'#191108');bg.addColorStop(1,'#24180e');
    c.fillStyle=bg;c.fillRect(0,0,1200,630);
    const glow=c.createRadialGradient(948,275,10,948,275,375);
    glow.addColorStop(0,'rgba(191,128,43,.23)');glow.addColorStop(1,'rgba(191,128,43,0)');
    c.fillStyle=glow;c.fillRect(0,0,1200,630);
    c.strokeStyle='rgba(224,173,87,.28)';c.lineWidth=1;
    for(const r of [120,181,239,302]){c.beginPath();c.arc(956,304,r,0,Math.PI*2);c.stroke();}
    c.beginPath();c.moveTo(956,50);c.lineTo(956,560);c.stroke();
    c.beginPath();c.moveTo(705,304);c.lineTo(1190,304);c.stroke();
    c.strokeStyle='#ecc179';c.lineWidth=5;c.beginPath();
    c.moveTo(890,256);c.lineTo(917,330);c.lineTo(956,269);c.lineTo(995,330);c.lineTo(1023,256);c.stroke();
    c.beginPath();c.moveTo(927,364);c.lineTo(956,294);c.lineTo(985,364);c.stroke();
    c.strokeStyle='#916a34';c.strokeRect(27,27,1146,576);
    c.fillStyle='#edc180';c.font='700 19px Arial,sans-serif';c.fillText('V.A. / PROOF BEFORE POWER',74,101);
    c.fillStyle='#f5e4c7';c.font='58px Georgia,serif';c.fillText('The Consequence',74,189);c.fillText('Challenge',74,250);
    c.fillStyle='#e5b46f';c.font='700 24px Arial,sans-serif';c.fillText(scenario.number+' / '+scenario.title.toUpperCase(),74,321);
    c.fillStyle='#e8d8c0';c.font='24px Arial,sans-serif';
    wrapText(c,scenario.question,74,374,620,36,3);
    c.fillStyle='#c3ac88';c.font='700 16px Arial,sans-serif';
    c.fillText('CLAIM '+record.id+' · PUBLIC STANDING: '+record.standing,74,532);
    c.fillText('Source-linked examination · Not a native execution result',74,563);
    canvas.toBlob(blob=>{
      if(blob){downloadBlob('VA-'+scenario.id+'-challenge-card.png',blob);toast('Gold challenge card saved locally.');}
      else toast('PNG export is unavailable in this browser.');
    },'image/png');
  }
  async function init() {
    render();
    try {
      const response=await fetch(registerURL,{cache:'no-store'});
      if(!response.ok)throw Error('The public claim register returned HTTP '+response.status);
      const raw=await response.text(),parsed=JSON.parse(raw);
      if(parsed.schema!=='va-proof-register/1.0'||!Array.isArray(parsed.entries))throw Error('Unexpected public register format');
      for(const scenario of SCENARIOS){
        const record=parsed.entries.find(entry=>entry.id===scenario.claimId);
        if(!record||typeof record.standing!=='string'||typeof record.scope!=='string')throw Error('Required claim '+scenario.claimId+' missing from public register');
      }
      state.register=parsed;
      try {state.registerHash=await getSHA256(raw);}catch(_){state.registerHash=null;}
      state.loading=false;render();
    } catch(e) {state.loading=false;state.error=e.message||'Unknown source error';render();}
  }
  init();
})();