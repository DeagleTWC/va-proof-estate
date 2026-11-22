import test from 'node:test';
import assert from 'node:assert/strict';
import {initFrankie} from '../frankie-client.mjs';

class Element {
  constructor(){this.hidden=true;this.disabled=false;this.value='';this.textContent='';this.listeners={};}
  addEventListener(name,fn){this.listeners[name]=fn;}
  focus(){}
}
function fixture(){
  const nodes=Object.fromEntries(['panel','toggle','form','question','send','answer','notice','receipt'].map(key=>[key,new Element()]));
  const store=new Map();
  const storage={getItem:key=>store.get(key)||null,setItem:(key,value)=>store.set(key,value)};
  return {nodes,storage,store};
}
const hash='c'.repeat(64);
const session=`${'a'.repeat(64)}.${'b'.repeat(64)}`;
const reply={status:'answered',act:'teacher_lesson',reply:'A public, source-bounded lesson.',receipt_hash:hash};
const gateway='https://classroom.example';

test('unconfigured Frankie remains hidden with no network or browser storage access',()=>{
  const {nodes}=fixture();
  const result=initFrankie({gatewayUrl:'',elements:nodes,fetchImpl:()=>{throw new Error('network invoked');},storage:{getItem(){throw new Error('storage invoked');}}});
  assert.equal(result.enabled,false);
  assert.equal(nodes.panel.hidden,true);
  assert.equal(nodes.toggle.listeners.click,undefined);
});

test('the button opens a private-send form without transmitting the current lesson',()=>{
  const {nodes,storage}=fixture();
  let requests=0;
  initFrankie({gatewayUrl:gateway,elements:nodes,storage,fetchImpl:()=>{requests++;},getSuggestedQuestion:()=> 'Teach me about True Zero'});
  assert.equal(nodes.panel.hidden,false);
  assert.equal(nodes.form.hidden,true);
  nodes.toggle.listeners.click();
  assert.equal(nodes.form.hidden,false);
  assert.equal(nodes.question.value,'Teach me about True Zero');
  assert.equal(requests,0);
});

test('sends only the student question and gateway-issued session to the HTTPS gateway',async()=>{
  const {nodes,storage,store}=fixture();
  const calls=[];
  const fetchImpl=async(url,init)=>{
    calls.push({url,init,body:JSON.parse(init.body)});
    return calls.length===1?new Response(JSON.stringify({session_token:session}),{status:201}):
      new Response(JSON.stringify(reply),{status:200});
  };
  initFrankie({gatewayUrl:gateway,elements:nodes,storage,fetchImpl,getSuggestedQuestion:()=> 'Teach me about True Zero'});
  nodes.toggle.listeners.click();
  nodes.question.value='Teach me about True Zero';
  await nodes.form.listeners.submit({preventDefault(){}});
  assert.equal(calls.length,2);
  assert.equal(calls[0].url,`${gateway}/api/teacher/session`);
  assert.deepEqual(calls[0].body,{});
  assert.equal(calls[1].url,`${gateway}/api/teacher/ask`);
  assert.deepEqual(calls[1].body,{session_token:session,question:'Teach me about True Zero'});
  assert.equal(store.get('va-frankie-student-session'),session);
  assert.equal(nodes.answer.textContent,reply.reply);
  assert.equal(nodes.receipt.textContent,`Receipt: ${hash}`);
});

test('continues a prior session without minting a different native learner',async()=>{
  const {nodes,storage,store}=fixture();
  store.set('va-frankie-student-session',session);
  const calls=[];
  initFrankie({gatewayUrl:gateway,elements:nodes,storage,fetchImpl:async(url,init)=>{
    calls.push({url,body:JSON.parse(init.body)});
    return new Response(JSON.stringify(reply),{status:200});
  }});
  nodes.question.value='Why do you say that?';
  await nodes.form.listeners.submit({preventDefault(){}});
  assert.equal(calls.length,1);
  assert.equal(calls[0].body.session_token,session);
  assert.equal(calls[0].body.question,'Why do you say that?');
});

test('renders every admitted Cycle 081 teaching act with its native receipt',async()=>{
  for(const act of ['teacher_lesson','teacher_followup','teacher_transfer_assessed','public_reference','public_knowledge']){
    const {nodes,storage,store}=fixture();
    store.set('va-frankie-student-session',session);
    initFrankie({gatewayUrl:gateway,elements:nodes,storage,fetchImpl:async()=>
      new Response(JSON.stringify({...reply,act}),{status:200})});
    nodes.question.value='Why do you say that?';
    await nodes.form.listeners.submit({preventDefault(){}});
    assert.equal(nodes.answer.textContent,reply.reply,`valid native act: ${act}`);
    assert.equal(nodes.receipt.textContent,`Receipt: ${hash}`);
  }
});

test('native holds and outages never display invented answers or disable ordinary lessons',async()=>{
  for(const status of [422,503]){
    const {nodes,storage}=fixture();
    initFrankie({gatewayUrl:gateway,elements:nodes,storage,fetchImpl:async(url)=>{
      if(url.endsWith('/session'))return new Response(JSON.stringify({session_token:session}),{status:201});
      return new Response(JSON.stringify({status:'held'}),{status});
    }});
    nodes.question.value='Unknown question';
    await nodes.form.listeners.submit({preventDefault(){}});
    assert.equal(nodes.answer.textContent,'');
    assert.match(nodes.notice.textContent,/public teacher/i);
    assert.equal(nodes.send.disabled,false);
  }
});

test('malicious HTML and unexpected acts are never injected into the document',async()=>{
  const {nodes,storage}=fixture();
  initFrankie({gatewayUrl:gateway,elements:nodes,storage,fetchImpl:async(url)=>{
    if(url.endsWith('/session'))return new Response(JSON.stringify({session_token:session}),{status:201});
    return new Response(JSON.stringify({...reply,act:'unexpected'}),{status:200});
  }});
  nodes.question.value='<img src=x onerror=alert(1)>';
  await nodes.form.listeners.submit({preventDefault(){}});
  assert.equal(nodes.answer.textContent,'');
  assert.match(nodes.notice.textContent,/public teacher/i);
});

test('a legitimate answer containing HTML markup is shown literally, not interpreted',async()=>{
  const {nodes,storage}=fixture();
  const literal='<img src=x onerror=alert(1)> is an example string';
  initFrankie({gatewayUrl:gateway,elements:nodes,storage,fetchImpl:async url=>
    new Response(JSON.stringify(url.endsWith('/session')?{session_token:session}:{...reply,reply:literal}),{
      status:url.endsWith('/session')?201:200,
    })});
  nodes.question.value='Teach me about True Zero';
  await nodes.form.listeners.submit({preventDefault(){}});
  assert.equal(nodes.answer.textContent,literal);
});

test('a 403 after secret rotation clears the stale token and mints a new session once',async()=>{
  const {nodes,storage,store}=fixture();
  const stale=`${'f'.repeat(64)}.${'a'.repeat(64)}`;
  store.set('va-frankie-student-session',stale);
  const calls=[];
  initFrankie({gatewayUrl:gateway,elements:nodes,storage,fetchImpl:async(url,init)=>{
    calls.push({url,body:JSON.parse(init.body)});
    if(url.endsWith('/session'))return new Response(JSON.stringify({session_token:session}),{status:201});
    return new Response(JSON.stringify(init.body.includes(stale)?{status:'refused'}:reply),{
      status:init.body.includes(stale)?403:200,
    });
  }});
  nodes.question.value='Teach me about True Zero';
  await nodes.form.listeners.submit({preventDefault(){}});
  assert.deepEqual(calls.map(x=>x.url.split('/').at(-1)),['ask','session','ask']);
  assert.equal(nodes.answer.textContent,reply.reply);
  assert.equal(store.get('va-frankie-student-session'),session);
});

test('an unresponsive gateway cannot leave the student send button stuck',async()=>{
  const {nodes,storage,store}=fixture();
  store.set('va-frankie-student-session',session);
  initFrankie({gatewayUrl:gateway,elements:nodes,storage,requestTimeoutMs:60,fetchImpl:async(_url,init)=>
    new Promise((_,reject)=>init.signal.addEventListener('abort',()=>reject(new Error('timeout')),{once:true}))});
  nodes.question.value='Teach me about True Zero';
  // AbortSignal.timeout() uses an unref'd timer in Node. Keep this test alive
  // with a bounded, referenced deadline while the simulated gateway stalls.
  let deadline;
  try {
    await Promise.race([
      nodes.form.listeners.submit({preventDefault(){}}),
      new Promise((_,reject)=>{deadline=setTimeout(()=>reject(new Error('gateway timeout did not settle')),1000);}),
    ]);
  } finally {
    clearTimeout(deadline);
  }
  assert.equal(nodes.send.disabled,false);
  assert.match(nodes.notice.textContent,/public teacher/i);
});

test('disabled client never reads browser storage, even if the getter is unavailable',()=>{
  const {nodes}=fixture();
  const result=initFrankie({gatewayUrl:'',elements:nodes,storage:undefined});
  assert.equal(result.enabled,false);
});

test('rejects plain HTTP and endpoint paths on production configuration',()=>{
  const {nodes,storage}=fixture();
  assert.throws(()=>initFrankie({gatewayUrl:'http://server.example',elements:nodes,storage}),/HTTPS/);
  assert.throws(()=>initFrankie({gatewayUrl:'https://server.example/secret',elements:nodes,storage}),/HTTPS/);
});
