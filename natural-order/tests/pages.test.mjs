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
