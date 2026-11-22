import test from 'node:test';
import assert from 'node:assert/strict';
import {DEFINITIONS,definitionsForLesson,convertTermDefinitions} from '../definition-kernel.mjs';

test('every definition has one original term, plain meaning, explanation and public source',()=>{
  assert.ok(DEFINITIONS.length>=12);
  for(const term of DEFINITIONS){
    assert.ok(typeof term.term==='string'&&term.term.length>=2);
    assert.ok([term.short,term.explanation].every(x=>typeof x==='string'&&x.length>15));
    assert.match(term.source.href,/^\.\.\/[a-z0-9/-]+(?:\.html|\.md|\.json)$/i);
    assert.equal(typeof term.source.title,'string');
  }
});

test('defines first use in public prose while keeping original technical terminology',()=>{
  const result=convertTermDefinitions('True Zero and the Elements Basin begin the study. True Zero is not moving.');
  assert.match(result,/True Zero \(/);
  assert.match(result,/Elements Basin \(/);
  assert.equal((result.match(/True Zero \(/g)||[]).length,1);
  assert.match(result,/True Zero is not moving\./);
});

test('a lesson can mark a heading term explained and define later terms only once',()=>{
  const explained=new Set(['Consequence Custody']);
  const summary=convertTermDefinitions('Consequence Custody requires standing and standing may change.',{explained});
  assert.doesNotMatch(summary,/Consequence Custody \(/);
  assert.equal((summary.match(/standing \(/gi)||[]).length,1);
  assert.ok(explained.has('Standing'));
});

test('returns expandable sourced definitions, without spurious private or unknown terms',()=>{
  const definitions=definitionsForLesson('Corrected NEW K and Lawful Continuance refer to V.A. A nonsense term does not.');
  assert.deepEqual(definitions.map(x=>x.term),['Corrected NEW K','Lawful Continuance','V.A.']);
  assert.equal(definitionsForLesson('The common apple fell.').length,0);
});

test('untrusted text stays data and never produces HTML or network requests',()=>{
  const converted=convertTermDefinitions('True Zero <script>alert(1)</script>');
  assert.match(converted,/\<script\>/);
  assert.doesNotMatch(converted,/<a href=/);
});
