/* Real browser Stage A test: local draft, real SHA-256 of originals, falsifiable negative input. */
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {mkdtemp,readFile,rm} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {tmpdir} from 'node:os';
import {join,resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from 'playwright';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const port=19593,base='http://127.0.0.1:'+port;
const server=spawn('python3',['-m','http.server',String(port),'--bind','127.0.0.1'],{cwd:root,stdio:'ignore'});
let browser,dir;const sleep=x=>new Promise(r=>setTimeout(r,x));
const file=(name,contents)=>({name,mimeType:'text/plain',buffer:Buffer.from(contents)});
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
try{
 for(let tries=0;tries<60;tries++){try{if((await fetch(base+'/consequence-aperture.html')).ok)break}catch(_){await sleep(120)}}
 dir=await mkdtemp(join(tmpdir(),'va-aperture-'));
 browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1280,height:800},acceptDownloads:true,reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 let response=await page.goto(base+'/consequence-aperture.html',{waitUntil:'networkidle'});
 assert.equal(response.status(),200);
 assert.match(await page.locator('h1').innerText(),/Consequence\s*Aperture/);
 assert.match(await page.locator('.ap-ceiling').innerText(),/not connected/i);
 await page.locator('[name=claimant]').fill('applicant-1');
 await page.locator('[name=artifact_sha256]').fill('a'.repeat(64));
 await page.locator('[name=protected_effect]').fill('Protected electric lamp effect');
 await page.locator('[name=scope]').fill('Sandbox simulated fixture instrument');
 await page.locator('[name=routes]').fill('Primary route\nAlternate route');
 const dl=page.waitForEvent('download');await page.locator('#ap-request-form button').click();
 const saved=await dl;assert.equal(saved.suggestedFilename(),'va-aperture-challenge-request.json');
 const filePath=join(dir,'request.json');await saved.saveAs(filePath);
 const draft=JSON.parse(await readFile(filePath,'utf8'));
 assert.equal(draft.status,'DRAFT_UNISSUED');
 assert.equal(draft.native_execution_occurred,false);
 assert.equal(draft.independent_reproduction_established,false);
 assert.equal(draft.boundary.alternate_routes.length,2);
 // Exact original-byte verification must be based on real browser file digest.
 const names=['pos-sensor.txt','pos-receipt.txt','neg-sensor.txt','neg-receipt.txt','change-sensor.txt','change-receipt.txt','replay-sensor.txt','replay-receipt.txt','witness.txt'];
 const originals=names.map(n=>file(n,'SYNTHETIC-TEST-ONLY: '+n));
 const packet={schema:'VA-APERTURE-1',packet_id:'SYNTHETIC-TEST',standing:'DECLARED_ONLY',
 freeze:{artifact_id:'toy',owner_id:'applicant',artifact_sha256:'b'.repeat(64),frozen_at:'2026-11-03T10:00:00Z',anchor:'https://example.test/freeze'},
 challenge:{id:'question',examiner_id:'examiner',issued_at:'2026-11-03T10:01:00Z',condition_summary:'Previously unknown changed condition'},
 boundary:{protected_effect:'toy light',observation_scope:'not an actual instrument',alternate_routes:['main','alternate']},
 controls:[['POSITIVE','pos','base',true],['NEGATIVE','neg','revoked',false],['CHANGED','change','different',true],['REPLAY','replay','base',false]].map(([kind,prefix,condition_id,measured_effect])=>({kind,condition_id,measured_effect,measurement_file:prefix+'-sensor.txt',receipt_file:prefix+'-receipt.txt'})),
 witness:{id:'test-witness',statement_file:'witness.txt'},
 originals:originals.map(x=>({file:x.name,sha256:hash(x.buffer)}))};
 await page.locator('#ap-packet').setInputFiles({name:'packet.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(packet))});
 await page.locator('#ap-originals').setInputFiles(originals);
 await page.locator('#ap-verify-form button').click();
 await page.locator('#ap-result[data-status=pass]').waitFor();
 assert.match(await page.locator('#ap-result').innerText(),/9 submitted original files/);
 assert.match(await page.locator('#ap-result').innerText(),/DECLARED_ONLY/);
 assert.ok(!(await page.locator('#ap-result').innerText()).includes('independently reproduced'));
 // True falsification must not be converted into a PASS: the checker accepts contradictory measurement claims for later independent review.
 const changed=originals.map(x=>({...x,buffer:Buffer.from(x.buffer)}));
 changed[2].buffer=Buffer.from('tampered external reading');
 await page.locator('#ap-originals').setInputFiles(changed);
 await page.locator('#ap-verify-form button').click();
 await page.locator('#ap-result[data-status=fail]').waitFor();
 assert.match(await page.locator('#ap-result').innerText(),/SHA-256 mismatch: neg-sensor.txt/);
 await page.setViewportSize({width:320,height:730});
 await page.waitForTimeout(150);
 const overflow=await page.evaluate(()=>({documentWidth:document.documentElement.scrollWidth,viewport:innerWidth}));
 assert.ok(overflow.documentWidth<=overflow.viewport+2,'320px overflow: '+JSON.stringify(overflow));
 assert.deepEqual(errors,[]);
 console.log('Consequence Aperture real browser, download, hash, tamper, 320px: PASS');
}finally{if(browser)await browser.close();if(dir)await rm(dir,{recursive:true,force:true});server.kill('SIGTERM')}
