import {createTeacherApi} from './server.mjs';

const rawPort=process.env.TEACHER_QUESTION_PORT||'8766';
const port=Number(rawPort);
if(!/^\d{1,5}$/.test(rawPort)||!Number.isSafeInteger(port)||port<1024||port>65535){
  throw new RangeError('TEACHER_QUESTION_PORT must be between 1024 and 65535');
}

const server=createTeacherApi();
server.listen(port,'127.0.0.1',()=>{
  process.stdout.write(`Teacher public question API listening on 127.0.0.1:${port}\n`);
});
server.on('error',error=>{
  process.stderr.write(`Teacher public question API could not start: ${error.code||'unavailable'}\n`);
  process.exitCode=1;
});
for(const signal of ['SIGINT','SIGTERM']){
  process.on(signal,()=>server.close(()=>{process.exitCode=0;}));
}
