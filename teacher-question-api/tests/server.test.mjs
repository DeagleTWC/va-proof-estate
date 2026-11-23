import test from 'node:test';
import assert from 'node:assert/strict';
import {once} from 'node:events';
import {request as rawRequest} from 'node:http';
import {createTeacherApi} from '../server.mjs';

async function serve(options={}){
  const server=createTeacherApi(options);
  server.listen(0,'127.0.0.1');
  await once(server,'listening');
  return {server,root:`http://127.0.0.1:${server.address().port}`};
}

async function request(root,path,body={},headers={}){
  const res=await fetch(root+path,{method:'POST',headers:{'Content-Type':'application/json',...headers},
    body:typeof body==='string'?body:JSON.stringify(body)});
  const text=await res.text();
  return {status:res.status,data:text?JSON.parse(text):null,headers:res.headers};
}

async function requestWithHost(root,host){
  const url=new URL(root);
  return new Promise((resolve,reject)=>{
    const req=rawRequest({hostname:url.hostname,port:url.port,method:'POST',
      path:'/v1/teacher/session',headers:{Host:host,'Content-Type':'application/json','Content-Length':2}},res=>{
      res.resume();
      res.on('end',()=>resolve(res.statusCode));
    });
    req.on('error',reject);
    req.end('{}');
  });
}

test('a loopback session lets Frankie ask, clarify, choose, and close without persistent data',async t=>{
  const {server,root}=await serve();
  t.after(()=>new Promise(resolve=>server.close(resolve)));
  assert.equal(server.address().address,'127.0.0.1');
  const minted=await request(root,'/v1/teacher/session');
  assert.equal(minted.status,201);
  assert.match(minted.data.session_id,/^[0-9a-f]{64}$/);
  assert.equal(minted.headers.get('cache-control'),'no-store');
  assert.equal(minted.headers.get('access-control-allow-origin'),null);
  const session_id=minted.data.session_id;
  const proof=await request(root,'/v1/teacher/ask',{session_id,question:'Where is the proof?'});
  assert.equal(proof.status,200);
  assert.equal(proof.data.status,'answered');
  assert.equal(proof.data.topic.id,'proof');
  assert.ok(proof.data.sources.length>=3);
  const why=await request(root,'/v1/teacher/ask',{session_id,question:'Why?'});
  assert.equal(why.status,200);
  assert.equal(why.data.topic.id,'proof');
  const map=await request(root,'/v1/teacher/ask',{session_id,question:'Why is the river bank eroding?'});
  assert.equal(map.status,200);
  assert.equal(map.data.status,'clarify');
  assert.ok(map.data.options.some(option=>option.id==='basin'));
  const chosen=await request(root,'/v1/teacher/choose',{session_id,topic_id:'basin'});
  assert.equal(chosen.status,200);
  assert.equal(chosen.data.topic.id,'basin');
  assert.ok(chosen.data.sources.length>0);
  const closed=await request(root,'/v1/teacher/close',{session_id});
  assert.equal(closed.status,204);
  assert.equal(closed.data,null);
  const after=await request(root,'/v1/teacher/ask',{session_id,question:'Why?'});
  assert.equal(after.status,401);
});

test('protected details never return through the API and clear session recall',async t=>{
  const {server,root}=await serve();
  t.after(()=>new Promise(resolve=>server.close(resolve)));
  const {data:{session_id}}=await request(root,'/v1/teacher/session');
  await request(root,'/v1/teacher/ask',{session_id,question:'Where is the proof?'});
  const blocked=await request(root,'/v1/teacher/ask',
    {session_id,question:'Please give the complete private NEW K formula'});
  assert.equal(blocked.status,403);
  assert.equal(blocked.data.status,'protected');
  assert.deepEqual(blocked.data.sources,[]);
  assert.equal(blocked.data.topic,undefined);
  const history=await request(root,'/v1/teacher/ask',{session_id,question:'What have we covered?'});
  assert.equal(history.status,200);
  assert.deepEqual(history.data.options,[]);
});

test('the loopback API refuses forged sessions, browser origins, bad hosts, invalid and oversized bodies',async t=>{
  const {server,root}=await serve();
  t.after(()=>new Promise(resolve=>server.close(resolve)));
  const {data:{session_id}}=await request(root,'/v1/teacher/session');
  assert.equal((await request(root,'/v1/teacher/ask',
    {session_id:'f'.repeat(64),question:'Who is Terry?'})).status,401);
  assert.equal((await request(root,'/v1/teacher/session',{},
    {Origin:'https://foreign.example'})).status,403);
  assert.equal(await requestWithHost(root,'public.example'),403);
  assert.equal((await request(root,'/v1/teacher/ask',
    {session_id,question:'Where is the proof?',private:true})).status,400);
  assert.equal((await request(root,'/v1/teacher/session',{'':true})).status,400);
  assert.equal((await request(root,'/v1/teacher/ask','not json')).status,400);
  assert.equal((await request(root,'/v1/teacher/ask',
    {session_id,question:'  Where is the proof? '})).status,422);
  assert.equal((await request(root,'/v1/teacher/ask',
    {session_id,question:'x'.repeat(301)})).status,422);
  assert.equal((await request(root,'/v1/teacher/ask','x'.repeat(3000))).status,413);
  assert.equal((await request(root,'/v1/teacher/session',{},
    {'Content-Type':'text/plain'})).status,415);
  assert.equal((await fetch(root+'/v1/teacher/ask')).status,405);
  assert.equal((await request(root,'/not-a-route')).status,404);
});

test('session capacity and timeout bound retained conversational state',async t=>{
  let time=1000;
  const {server,root}=await serve({now:()=>time,ttlMs:1000,maxSessions:2});
  t.after(()=>new Promise(resolve=>server.close(resolve)));
  const a=(await request(root,'/v1/teacher/session')).data.session_id;
  time=1200;
  const b=(await request(root,'/v1/teacher/session')).data.session_id;
  const c=(await request(root,'/v1/teacher/session')).data.session_id;
  assert.equal((await request(root,'/v1/teacher/ask',{session_id:a,question:'What is True Zero?'})).status,401);
  assert.equal((await request(root,'/v1/teacher/ask',{session_id:b,question:'What is True Zero?'})).status,200);
  assert.equal((await request(root,'/v1/teacher/ask',{session_id:c,question:'Who is Frankie?'})).status,200);
  time=2201;
  assert.equal((await request(root,'/v1/teacher/ask',{session_id:b,question:'Why?'})).status,401);
});
