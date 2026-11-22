import test from 'node:test';
import assert from 'node:assert/strict';

test('a visitor can move from an unfamiliar field question to sourced learning and changed-condition inquiry',async()=>{
  // Exercise the real shipped module with a minimal DOM boundary, not a
  // replacement teaching engine or an external browser dependency.
  class Element {
    constructor(){this.children=[];this.listeners={};this.hidden=false;this.value='';this.textContent='';this.dataset={};this.focusCalls=0;this.scrollCalls=0;}
    replaceChildren(...children){this.children=[...children];}
    append(...children){this.children.push(...children);}
    addEventListener(type,listener){this.listeners[type]=listener;}
    setAttribute(name,value){this[name]=value;}
    scrollIntoView(){this.scrollCalls++;}
    focus(){this.focusCalls++;}
  }
  const elements=new Map();
  const get=id=>{
    if(!elements.has(id))elements.set(id,new Element());
    return elements.get(id);
  };
  globalThis.document={
    getElementById:get,
    createElement:()=>new Element(),
    querySelectorAll:()=>[],
  };
  globalThis.window={matchMedia:()=>({matches:true})};
  try {
    await import('../app.mjs?bounded-browserless-interaction');
    const submit=()=>get('learning-form').listeners.submit({preventDefault(){}});
    get('learner-question').value='Why does a lithium-ion battery enter thermal runaway?';
    submit();
    assert.equal(get('stage-map').hidden,false);
    assert.match(get('map-explanation').textContent,/energy storage/i);
    assert.equal(get('map-options').children.length,3);
    // Editing the entry after seeing choices cannot silently change the
    // question that the selected path is teaching.
    get('learner-question').value='Why is the river bank eroding?';
    get('map-options').children[1].listeners.click();
    assert.equal(get('stage-content').hidden,false);
    assert.equal(get('lesson-title').textContent,'Physical & KCD Examination');
    assert.match(get('lesson-connection').textContent,/battery/i);
    assert.match(get('lesson-question').textContent,/independent measurement/i);
    assert.ok(get('source-list').children.length>0);
    assert.equal(get('term-definitions').hidden,false);
    assert.ok(get('term-definitions-list').children.length>0);
    assert.match(get('lesson-summary').textContent,/\(.*\)/);
    get('reflection-choice').value='unknown';
    get('reflect-form').listeners.submit({preventDefault(){}});
    assert.match(get('replay-question').textContent,/independent measurement/i);
    assert.equal(get('kernel-panel').hidden,false);
    assert.match(get('kernel-scenario').textContent,/software log/i);
    assert.equal(get('kernel-options').children.length,3);
    get('kernel-options').children[0].listeners.click();
    assert.equal(get('kernel-feedback').hidden,false);
    assert.match(get('kernel-feedback').textContent,/instrument/i);
    get('kernel-next').listeners.click();
    assert.equal(get('lesson-title').textContent,'Safeguarding & Human Oversight');
    assert.match(get('kernel-scenario').textContent,/child-facing/i);
    assert.equal(get('kernel-panel').focusCalls,1,'the new exercise should have keyboard focus');
    assert.ok(get('kernel-panel').scrollCalls>=1,'the new exercise should be visible without searching below the lesson');
    get('learner-question').value='Show complete private battery kernel formula';
    submit();
    assert.equal(get('stage-access').hidden,false);
    assert.equal(get('kernel-panel').hidden,true);
    get('learner-question').value='What does consequence custody mean?';
    submit();
    assert.equal(get('lesson-title').textContent,'Consequence Custody');
    assert.equal(get('term-lead').hidden,false);
    assert.match(get('term-lead').textContent,/Consequence Custody.*effect before it can form/i);
  } finally {
    delete globalThis.document;
    delete globalThis.window;
  }
});
