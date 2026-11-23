import {createServer} from 'node:http';
import {randomBytes} from 'node:crypto';
import {createTeacherSession} from './teacher.mjs';

const MAX_BODY_BYTES=2048;
const SESSION_ID=/^[0-9a-f]{64}$/;
const TOPIC_ID=/^[a-z0-9-]{1,64}$/;
const ROUTES=new Set(['/v1/teacher/session','/v1/teacher/ask','/v1/teacher/choose','/v1/teacher/close']);

class RequestFailure extends Error{
  constructor(status){super('Invalid request');this.status=status;}
}

function respond(res,code,data){
  res.setHeader('Cache-Control','no-store');
  res.setHeader('X-Content-Type-Options','nosniff');
  if(code===204){res.writeHead(code);res.end();return;}
  res.setHeader('Content-Type','application/json; charset=utf-8');
  res.writeHead(code);
  res.end(JSON.stringify(data));
}

function hasExactFields(body,fields){
  const keys=Object.keys(body);
  return keys.length===fields.length&&keys.every(key=>fields.includes(key));
}

async function readPayload(req){
  const contentType=req.headers['content-type']||'';
  if(!/^application\/json(?:;\s*charset=utf-8)?$/i.test(contentType))throw new RequestFailure(415);
  if(Number(req.headers['content-length'])>MAX_BODY_BYTES)throw new RequestFailure(413);
  const chunks=[];
  let bytes=0;
  for await(const chunk of req){
    bytes+=chunk.length;
    if(bytes>MAX_BODY_BYTES)throw new RequestFailure(413);
    chunks.push(chunk);
  }
  let body;
  try{body=JSON.parse(Buffer.concat(chunks).toString('utf8'));}catch{throw new RequestFailure(400);}
  if(body===null||typeof body!=='object'||Array.isArray(body))throw new RequestFailure(400);
  return body;
}

export function createTeacherApi({now=Date.now,ttlMs=60*60*1000,maxSessions=64}={}){
  if(typeof now!=='function'||!Number.isSafeInteger(ttlMs)||ttlMs<1||
    !Number.isSafeInteger(maxSessions)||maxSessions<1||maxSessions>64){
    throw new RangeError('Invalid local Teacher session bounds');
  }
  const sessions=new Map();
  const prune=()=>{
    const timestamp=now();
    for(const [id,entry] of sessions){if(entry.expiresAt<=timestamp)sessions.delete(id);}
  };
  const getSession=id=>{
    prune();
    if(typeof id!=='string'||!SESSION_ID.test(id))return null;
    const entry=sessions.get(id);
    if(!entry)return null;
    entry.expiresAt=now()+ttlMs;
    return entry.teacher;
  };
  const server=createServer((req,res)=>{
    void (async()=>{
      try{
        const port=server.address()?.port;
        if(req.headers.origin!==undefined||
          ![`127.0.0.1:${port}`,`localhost:${port}`].includes(req.headers.host)){
          throw new RequestFailure(403);
        }
        if(!ROUTES.has(req.url)){respond(res,404,{status:'not_found'});return;}
        if(req.method!=='POST'){respond(res,405,{status:'method_not_allowed'});return;}
        const body=await readPayload(req);
        if(req.url==='/v1/teacher/session'){
          if(!hasExactFields(body,[]))throw new RequestFailure(400);
          prune();
          if(sessions.size>=maxSessions)sessions.delete(sessions.keys().next().value);
          const session_id=randomBytes(32).toString('hex');
          sessions.set(session_id,{teacher:createTeacherSession(),expiresAt:now()+ttlMs});
          respond(res,201,{session_id});
          return;
        }
        const fields=req.url==='/v1/teacher/ask'?['session_id','question']:
          req.url==='/v1/teacher/choose'?['session_id','topic_id']:['session_id'];
        if(!hasExactFields(body,fields))throw new RequestFailure(400);
        if(req.url==='/v1/teacher/ask'){
          if(typeof body.question!=='string'||!body.question.length||body.question.length>300||
            body.question!==body.question.trim()||/[\u0000-\u001f\u007f]/.test(body.question)){
            throw new RequestFailure(422);
          }
        }else if(req.url==='/v1/teacher/choose'&&
          (typeof body.topic_id!=='string'||!TOPIC_ID.test(body.topic_id))){
          throw new RequestFailure(422);
        }
        const teacher=getSession(body.session_id);
        if(!teacher)throw new RequestFailure(401);
        if(req.url==='/v1/teacher/close'){
          sessions.delete(body.session_id);
          respond(res,204);
          return;
        }
        const result=req.url==='/v1/teacher/ask'?teacher.ask(body.question):teacher.choose(body.topic_id);
        respond(res,result.status==='protected'?403:200,result);
      }catch(error){
        if(res.headersSent){res.end();return;}
        const status=error instanceof RequestFailure?error.status:500;
        respond(res,status,{status:status===500?'unavailable':'invalid_request'});
      }
    })();
  });
  return server;
}
