/* Browser-level public website verification: no native V.A. run, private kernels,
   third-party inputs, external challenge submission or protected data. */
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {readFile, mkdtemp, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {chromium} from 'playwright';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const port=19386;
const base='http://127.0.0.1:'+port;
const server=spawn('python3',['-m','http.server',String(port),'--bind','127.0.0.1'],{
  cwd:root,stdio:['ignore','ignore','pipe']
});
let browser,dir,errors=[];
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const waitForServer=async()=>{
  for(let i=0;i<50;i++){
    try{const response=await fetch(base+'/consequence-challenge.html');if(response.ok)return;}catch(_){}
    if(server.exitCode!==null)break;
    await sleep(125);
  }
  throw new Error('Local read-only site preview server did not start');
};
const pageErrors=page=>page.on('pageerror',e=>errors.push(e.message));
const expectedDigest=async()=>createHash('sha256')
 .update(await readFile(join(root,'proofs/CLAIM-TO-CARRIER.json'))).digest('hex');

try{
  await waitForServer();
  dir=await mkdtemp(join(tmpdir(),'va-public-challenge-'));
  browser=await chromium.launch({headless:true,args:['--no-sandbox']});
  const context=await browser.newContext({
    viewport:{width:1280,height:800},reducedMotion:'reduce',
    acceptDownloads:true
  });
  const page=await context.newPage();
  pageErrors(page);
  let r=await page.goto(base+'/consequence-challenge.html',{waitUntil:'networkidle'});
  assert.equal(r.status(),200);
  await page.locator('.cc-choice').first().waitFor();
  assert.equal(await page.locator('.cc-choice').count(),3);
  assert.equal(await page.locator('.cc-option').count(),3);
  assert.equal(await page.locator('.cc-evidence').count(),3);
  assert.ok((await page.locator('#cc-app').innerText()).includes('VA-N02'));
  assert.ok(!(await page.locator('#cc-app').innerText()).includes('Source-bound examination unavailable'));

  // Keyboard: switching an examination or prediction must retain focus.
  await page.locator('[data-case="standing"]').focus();
  await page.keyboard.press('Enter');
  assert.equal(await page.evaluate(()=>document.activeElement?.getAttribute('data-case')),'standing');
  assert.equal(await page.locator('[data-case="standing"]').getAttribute('aria-pressed'),'true');
  await page.locator('[data-case="authority"]').click();
  await page.locator('[data-prediction="no-bind"]').focus();
  await page.keyboard.press('Enter');
  assert.equal(await page.evaluate(()=>document.activeElement?.getAttribute('data-prediction')),'no-bind');
  assert.equal(await page.locator('[data-prediction="no-bind"]').getAttribute('aria-pressed'),'true');
  await page.locator('#cc-reveal-button').click();
  await page.locator('#cc-reveal').waitFor();
  assert.match(await page.locator('#cc-reveal').innerText(),/NOT ESTABLISHED BY THIS PUBLIC ENTRY/);
  assert.match(await page.locator('#cc-reveal').innerText(),/falsify/i);
  assert.ok(await page.locator('#cc-reveal a[href="#cc-share-title"]').count()===1);
  await page.locator('[data-mode="examiner"]').click();
  assert.equal(await page.locator('[data-mode="examiner"]').getAttribute('aria-pressed'),'true');
  const source=await page.locator('.cc-raw-record').textContent();
  assert.equal(JSON.parse(source).id,'VA-N02');
  assert.equal(JSON.parse(source).standing,'DECLARED');
  assert.equal(await page.evaluate(()=>document.activeElement?.getAttribute('data-mode')),'examiner');

  // Browser download 1: verifiable source-bound JSON Passport, not a native receipt.
  const passEvent=page.waitForEvent('download');
  await page.locator('#cc-passport').click();
  const passDownload=await passEvent;
  assert.equal(passDownload.suggestedFilename(),'VA-authority-proof-passport.json');
  const passPath=join(dir,'passport.json');
  await passDownload.saveAs(passPath);
  const passport=JSON.parse(await readFile(passPath,'utf8'));
  assert.equal(passport.schemaVersion,'VA-PUBLIC-CHALLENGE-PASSPORT-1.0');
  assert.equal(passport.recordType,'VISITOR_GENERATED_EXAMINATION_NOT_NATIVE_PROOF');
  assert.equal(passport.claimPromotion,false);
  assert.equal(passport.publicClaimCarrier.id,'VA-N02');
  assert.equal(passport.publicClaimCarrier.standing,'DECLARED');
  assert.equal(passport.publicClaimCarrier.nativeVAEvidence,false);
  assert.equal(passport.challenge.visitorPrediction,'no-bind');
  assert.equal(passport.sourceRegister.exactBytesSHA256,await expectedDigest());
  assert.equal(passport.evidenceBoundary.observedNativeEffect,'NOT ATTACHED HERE');
  assert.equal(passport.evidenceBoundary.independentlyReproducedNativeEffect,'NOT ATTACHED HERE');
  assert.equal(passport.publicReference,'https://deagletwc.github.io/va-proof-estate/challenge/authority.html');

  // Browser download 2: real canvas PNG file, not merely a button.
  const pngEvent=page.waitForEvent('download');
  await page.locator('#cc-image').click();
  const pngDownload=await pngEvent;
  assert.equal(pngDownload.suggestedFilename(),'VA-authority-challenge-card.png');
  const pngPath=join(dir,'challenge.png');
  await pngDownload.saveAs(pngPath);
  const png=await readFile(pngPath);
  assert.equal(png.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
  assert.equal(png.readUInt32BE(16),1200);
  assert.equal(png.readUInt32BE(20),630);
  assert.ok(png.length>10000,'Gold canvas preview must not be empty');

  // Browser-generated copy link (and native share fallback when unavailable).
  await context.grantPermissions(['clipboard-read','clipboard-write'],{origin:base});
  await page.locator('#cc-copy').click();
  const copied=await page.evaluate(()=>navigator.clipboard.readText());
  assert.equal(copied,'https://deagletwc.github.io/va-proof-estate/challenge/authority.html');

  // No overflow on narrow screens; mobile is an actual chromium viewport.
  for(const width of [760,390,360,320]){
    await page.setViewportSize({width,height:780});
    const sizes=await page.evaluate(()=>({
      client:document.documentElement.clientWidth,
      scroll:document.documentElement.scrollWidth,
      columns:getComputedStyle(document.querySelector('.cc-grid')).gridTemplateColumns.split(' ').length,
      revealText:getComputedStyle(document.querySelector('.cc-reveal')).fontSize
    }));
    assert.ok(sizes.scroll<=sizes.client+2,
      'Horizontal overflow at viewport '+width+': '+JSON.stringify(sizes));
    if(width<=760)assert.equal(sizes.columns,1,'Challenge cards must stack on mobile');
    assert.ok(sizes.revealText);
  }
  assert.equal(await page.locator('.cc-orbit-spin').evaluate(el=>getComputedStyle(el).animationName),'none',
    'Reduced-motion request must disable rotating rings');

  // Three permanent nested pages: correct source resolution and share preview metadata.
  for(const [name,id,image] of [
    ['standing','VA-N01','standing'],
    ['authority','VA-N02','authority'],
    ['alternate-route','VA-P02','alternate-route']
  ]){
    const response=await page.goto(base+'/challenge/'+name+'.html',{waitUntil:'networkidle'});
    assert.equal(response.status(),200);
    await page.locator('.cc-choice').first().waitFor();
    assert.match(await page.locator('.cc-panel').first().innerText(),new RegExp(id));
    assert.equal(await page.locator('[data-case="'+(name==='alternate-route'?'alternate':name)+'"]').getAttribute('aria-pressed'),'true');
    const src=await page.locator('.cc-links a').first().getAttribute('href');
    assert.ok(src.startsWith('../proofs/'),'Nested page must keep source links at root');
    const parsed=new URL(src,page.url());
    assert.ok(parsed.pathname.startsWith('/proofs/'),'No /challenge/proofs/ misrouting');
    const og=await page.locator('meta[property="og:image"]').getAttribute('content');
    assert.equal(og,'https://deagletwc.github.io/va-proof-estate/challenge/'+image+'-1200x630.png');
    const imageResponse=await page.request.get(base+'/challenge/'+image+'-1200x630.png');
    assert.equal(imageResponse.status(),200,'Nested gold preview must load');
    const imageBytes=await imageResponse.body();
    assert.equal(imageBytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
  }
  assert.deepEqual(errors,[],'No JavaScript runtime exceptions');
  console.log('PASS: real Chromium 320–1280px, keyboard focus, examiner mode, JSON/PNG downloads, source identity, clipboard fallback, unique social assets and 3 permanent pages');
}finally{
  if(browser)await browser.close();
  if(dir)await rm(dir,{recursive:true,force:true});
  server.kill('SIGTERM');
}
