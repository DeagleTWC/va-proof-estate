import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const file = name => readFile(new URL(`../${name}`,import.meta.url),'utf8');

test('main public teaching page has a complete accessible learning route', async () => {
  const html=await file('index.html');
  for (const id of ['learning-form','topic-grid','lesson-stage','source-list','reflect-form','access-route','replay-question']) {
    assert.match(html,new RegExp(`id="${id}"`));
  }
  assert.match(html,/aria-live="polite"/);
  assert.match(html,/Do not enter personal or confidential information/i);
  assert.match(html,/Proof Before Power/);
  assert.match(html,/app\.mjs/);
  assert.match(html, /id="lesson-stage"[^>]*tabindex="-1"/);
  assert.match(html, /id="teach-submit"[^>]*disabled/);
  assert.doesNotMatch(html, /name="question"/);
  assert.match(html, /class="brand-mark"[^>]*><img src="\.\.\/favicon\.png"/);
});

test('protected route offers approved universal NDA, signed return email and personal walkthrough', async () => {
  const html=await file('access.html');
  assert.match(html,/NDA/);
  assert.match(html,/sign/i);
  assert.match(html,/email/i);
  assert.match(html,/Terry/);
  assert.match(html,/personal walkthrough/i);
  assert.match(html,/href="VA_Universal_Bounded_Review_MNDA\.pdf"/);
  assert.match(html,/mailto:canarybird0618@gmail\.com/);
  assert.doesNotMatch(html,/mailto:undefined|mailto:YOUR_EMAIL|github\.com\/DeagleTWC\/va-proof-estate\/issues\/new/i);
  assert.match(html,/do not post (confidential|protected)/i);
  assert.match(html,/class="brand-mark"[^>]*><img src="\.\.\/favicon\.png"/);
});

test('public repair evidence page shows reproducible receipts, precise claim boundary and NDA route', async () => {
  const html=await file('repair-evidence.html');
  assert.match(html,/Redundant Structural Information Field/i);
  assert.match(html,/Electromagnetically Resonant Image Field/i);
  assert.match(html,/1500\s*[×x]\s*430/i);
  assert.match(html,/caafe063a3848c59edbdd4763b930186d751915fc63faa6032e7dafa5b40c0e9/);
  for (const value of ['0.151','0.299','0.431','0.725','0.678','0.713','0.633']) assert.ok(html.includes(value),value);
  assert.match(html,/independent photographic replication.*not established/is);
  assert.match(html,/physical mechanism.*unresolved/is);
  assert.match(html,/source (?:JPEG|image).*not included/is);
  assert.match(html,/href="access\.html"/);
});

test('public app uses DOM-safe content insertion and no remote API', async () => {
  const js=await file('app.mjs');
  assert.match(js,/textContent/);
  assert.doesNotMatch(js,/innerHTML\s*=/);
  assert.doesNotMatch(js,/fetch\s*\(|localStorage|sessionStorage|XMLHttpRequest/i);
  assert.match(js,/teach-submit.*disabled\s*=\s*false/);
  assert.match(js,/prefers-reduced-motion/);
});

test('responsive polish includes reduced motion, keyboard focus and mobile handling', async () => {
  const css=await file('styles.css');
  assert.match(css,/@media\s*\(max-width:\s*\d+px\)/);
  assert.match(css, /prefers-reduced-motion/);
  assert.match(css,/:focus-visible/);
});
