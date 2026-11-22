// Release boundary: no hosted HTTPS gateway is authorized yet.
// This must remain empty in public deployment until a separately reviewed
// host, exact Origin and real Frankie end-to-end test are established.
export const FRANKIE_GATEWAY_URL='';

const SESSION_KEY='va-frankie-student-session';
const TOKEN=/^[0-9a-f]{64}\.[0-9a-f]{64}$/;
const RECEIPT=/^[0-9a-f]{64}$/;
const NATIVE_ACTS=new Set(['teacher_lesson','teacher_followup','teacher_transfer_assessed','public_reference','public_knowledge']);

function validUrl(url){
  let parsed;
  try{parsed=new URL(url);}catch{throw new Error('Frankie gateway requires an HTTPS origin');}
  if(parsed.protocol!=='https:'||parsed.pathname!=='/'||parsed.search||parsed.hash||
    parsed.username||parsed.password)throw new Error('Frankie gateway requires a bare HTTPS origin');
  return parsed.origin;
}

export function initFrankie({
  gatewayUrl=FRANKIE_GATEWAY_URL,
  elements,
  getSuggestedQuestion=()=>'',
  fetchImpl=globalThis.fetch,
  storage,
  requestTimeoutMs=8000,
}={}){
  if(!elements?.panel)throw new Error('Missing optional Frankie panel');
  if(!gatewayUrl){
    elements.panel.hidden=true;
    return {enabled:false};
  }
  const origin=validUrl(gatewayUrl);
  if(!Number.isFinite(requestTimeoutMs)||requestTimeoutMs<50||requestTimeoutMs>15000)throw new Error('Invalid teacher request timeout');
  const {panel,toggle,form,question,send,answer,notice,receipt}=elements;
  if([toggle,form,question,send,answer,notice,receipt].some(item=>!item))throw new Error('Incomplete Frankie panel');
  panel.hidden=false;
  form.hidden=true;
  answer.textContent='';
  receipt.textContent='';
  let busy=false;
  let inMemoryToken=null;
  const sessionStore=()=>{
    try{return storage??globalThis.sessionStorage;}catch{return null;}
  };
  const readToken=()=>{
    try{return sessionStore()?.getItem(SESSION_KEY)||inMemoryToken;}catch{return inMemoryToken;}
  };
  const saveToken=token=>{
    inMemoryToken=token;
    try{sessionStore()?.setItem(SESSION_KEY,token);}catch{/* memory-only teaching session */}
  };
  const clearToken=()=>{
    inMemoryToken=null;
    try{
      const store=sessionStore();
      if(store?.removeItem)store.removeItem(SESSION_KEY);
      else store?.setItem(SESSION_KEY,'');
    }catch{/* memory-only teaching session */}
  };

  toggle.addEventListener('click',()=>{
    form.hidden=!form.hidden;
    if(!form.hidden){
      if(!question.value)question.value=getSuggestedQuestion();
      question.focus();
    }
  });
  form.addEventListener('submit',async event=>{
    event.preventDefault();
    if(busy)return;
    const submitted=question.value;
    answer.textContent='';
    receipt.textContent='';
    if(typeof submitted!=='string'||!submitted.trim()||submitted!==submitted.trim()||submitted.length>300||
       /[\u0000-\u001f\u007f]/.test(submitted)){
      notice.textContent='Please enter one plain-text question (up to 300 characters, without extra spaces).';
      return;
    }
    busy=true;
    send.disabled=true;
    notice.textContent='Asking Frankie through the separate teaching service…';
    try{
      let session_token=readToken();
      for(let retry=0;retry<2;retry++){
        if(!TOKEN.test(session_token||'')){
          const minted=await fetchImpl(`${origin}/api/teacher/session`,{
            method:'POST',headers:{'Content-Type':'application/json'},
            body:'{}',cache:'no-store',credentials:'omit',mode:'cors',
            signal:AbortSignal.timeout(requestTimeoutMs),
          });
          if(minted.status!==201)throw new Error('unavailable');
          session_token=(await minted.json()).session_token;
          if(typeof session_token!=='string'||!TOKEN.test(session_token))throw new Error('bad session');
          saveToken(session_token);
        }
        const result=await fetchImpl(`${origin}/api/teacher/ask`,{
          method:'POST',headers:{'Content-Type':'application/json'},
          body:JSON.stringify({session_token,question:submitted}),
          cache:'no-store',credentials:'omit',mode:'cors',
          signal:AbortSignal.timeout(requestTimeoutMs),
        });
        if(result.status===403 && retry===0){
          clearToken();
          session_token=null;
          continue;
        }
        if(result.status===422){
          notice.textContent='Frankie is holding that question. The public teacher and its source paths remain available.';
        }else if(result.status===200){
          const content=await result.json();
          if(content?.status!=='answered'||!NATIVE_ACTS.has(content.act)||
            typeof content.reply!=='string'||content.reply.length<1||content.reply.length>5000||
            typeof content.receipt_hash!=='string'||!RECEIPT.test(content.receipt_hash)){
            throw new Error('unexpected answer');
          }
          answer.textContent=content.reply;
          receipt.textContent=`Receipt: ${content.receipt_hash}`;
          notice.textContent='Frankie answered within her current public teaching scope. Examine the original sources for evidence.';
        }else{
          notice.textContent='Frankie is not available for that request. The public teacher remains available.';
        }
        break;
      }
    }catch{
      notice.textContent='Frankie could not answer just now. The public teacher remains available.';
    }finally{
      busy=false;
      send.disabled=false;
    }
  });
  return {enabled:true};
}
