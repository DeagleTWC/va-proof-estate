/* V.A. Consequence Aperture release/standing/source custody tests. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {Script} from 'node:vm';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>readFileSync(resolve(root,p),'utf8');
const home=read('index.html'),html=read('consequence-aperture.html'),css=read('consequence-aperture.css'),js=read('consequence-aperture.js');
const manifest=JSON.parse(read('proof-estate-manifest.json'));
assert.doesNotThrow(()=>new Script(js,{filename:'consequence-aperture.js'}));
assert.ok(html.includes('id="ap-request-form"')&&html.includes('id="ap-verify-form"'));
assert.ok(html.includes('name="viewport"')&&html.includes('href="va-gold-design.css"'));
assert.ok(html.includes('<main id="main">')&&html.includes('aria-live="polite"'));
assert.ok(html.includes('No predetermined')&&html.includes('DRAFT · NO EXECUTION'));
assert.ok(html.includes('Instrumented effect: not attached here'));
assert.ok(css.includes('@media(max-width:600px)')&&css.includes('prefers-reduced-motion:reduce'));
assert.equal(css.split('{').length,css.split('}').length,'CSS syntax braces');
assert.ok(js.includes('crypto.subtle.digest')&&js.includes('SHA-256'));
assert.ok(js.includes('measured_effect')&&js.includes('DECLARED_ONLY'));
assert.ok(!js.includes('actual = expected')&&!js.includes('status = "PASS"'));
for(const banned of ['sendBeacon(', 'localStorage.', 'sessionStorage.', 'XMLHttpRequest(', 'indexedDB.', 'fetch(']){
 assert.ok(!js.includes(banned),'Unexpected remote tracking/upload pattern: '+banned)
}
for(const p of ['index.html','consequence-challenge.html','reviewer-route.html','README.md']){
 assert.ok(read(p).includes('consequence-aperture.html'),'Aperture not visible from '+p);
}
assert.equal(manifest.release,'2.7');
assert.equal(manifest.consequenceAperture.nativeExecutionConnected,false);
assert.equal(manifest.consequenceAperture.independentNativeReproductionAttached,false);
assert.equal(manifest.consequenceAperture.existingClaimToCarrierRegisterUnchanged,true);
assert.equal(manifest.nativeRuntimeReceiptsAttached,0);
assert.equal(manifest.independentlyReproducedRunsAttached,0);
assert.equal(manifest.instrumentedPhysicalRunsAttached,0);
assert.equal(createHash('sha256').update(Buffer.from(home,'utf8')).digest('hex'),manifest.mainFileSHA256);
assert.ok(read('aperture/README.md').includes('DECLARED_ONLY'));
console.log('Consequence Aperture static/manifest/source integrity: PASS');
