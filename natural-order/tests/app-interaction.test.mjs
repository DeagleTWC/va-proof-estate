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
    assert.equal(get('lesson-plain').hidden,false,'standard subject offers an everyday-language first answer');
    assert.match(get('lesson-plain').textContent,/software log|physical|instruments?/i);
    assert.equal(get('lesson-detail').open,false,'technical detail starts closed when a plain answer exists');
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
    get('learner-question').value='Why?';
    submit();
    assert.equal(get('lesson-title').textContent,'Safeguarding & Human Oversight',
      'advancing to a teaching kernel must retain conversational topic continuity');
    get('topic-grid').children[0].listeners.click();
    assert.equal(get('lesson-title').textContent,'True Zero');
    get('learner-question').value='Why?';
    submit();
    assert.equal(get('lesson-title').textContent,'True Zero',
      'direct topic selection must also admit the displayed topic into the conversation');
    get('learner-question').value='Show complete private battery kernel formula';
    submit();
    assert.equal(get('stage-access').hidden,false);
    assert.equal(get('kernel-panel').hidden,true);
    get('learner-question').value='What does consequence custody mean?';
    submit();
    assert.equal(get('lesson-title').textContent,'Consequence Custody');
    assert.match(get('lesson-plain').textContent,/unauthorized effect/i);
    assert.equal(get('lesson-detail').open,false);
    assert.equal(get('term-lead').hidden,false);
    assert.match(get('term-lead').textContent,/Consequence Custody.*effect before it can form/i);
    get('learner-question').value='Who is Terry Snyder?';
    submit();
    assert.equal(get('lesson-title').textContent,'About Terry Snyder');
    assert.match(get('lesson-summary').textContent,/mercy/i);
    assert.ok(get('source-list').children.some(item=>item.children[0].href==='../natural-order/about-terry.html'));
    get('learner-question').value='What does Terry Snyder believe about mercy?';
    submit();
    assert.equal(get('lesson-plain').hidden,true);
    assert.equal(get('lesson-detail').open,true);
    assert.match(get('lesson-summary').textContent,/greatest expression.*mercy/i);
    get('learner-question').value='Can you explain that in plain language?';
    submit();
    assert.equal(get('lesson-title').textContent,'About Terry Snyder');
    assert.match(get('lesson-summary').textContent,/listen|restraint/i);
    get('learner-question').value='Who is Frankie?';
    submit();
    assert.equal(get('lesson-title').textContent,'About Frankie');
    assert.ok(get('source-list').children.some(item=>item.children[0].href==='../natural-order/about-frankie.html'));
    get('learner-question').value="What are Frankie's tested capabilities?";
    submit();
    assert.equal(get('lesson-plain').hidden,true);
    assert.equal(get('lesson-detail').open,true);
    assert.match(get('lesson-summary').textContent,/typed teaching conversations|session memory/i);
    get('learner-question').value='Where is the evidence?';
    submit();
    assert.equal(get('lesson-title').textContent,'About Frankie');
    assert.match(get('lesson-connection').textContent,/source links/i);
    assert.match(get('lesson-connection').textContent,/owner-private/i);
    get('learner-question').value='Where can I find the hospital pilot reports?';
    submit();
    assert.equal(get('lesson-title').textContent,'Pilots & Original Evidence');
    assert.equal(get('lesson-plain').hidden,true,'source-specific answers must not be replaced with generic copy');
    assert.equal(get('lesson-detail').open,true,'the complete source-specific answer must be visible');
    assert.match(get('lesson-summary').textContent,/original|carrier|pilot/i);
    assert.ok(get('source-list').children.length>=2,'the evidence route remains attached');
    get('learner-question').value='Does Earth move through the Elements Basin or is the field in motion?';
    submit();
    assert.equal(get('lesson-title').textContent,'Elements Basin');
    assert.equal(get('lesson-plain').hidden,true);
    assert.equal(get('lesson-detail').open,true);
    assert.match(get('lesson-summary').textContent,/dark matter.*in motion|dark matter.*moving/is);
    assert.ok(get('source-list').children.some(item=>item.children[0].href==='../kcd/README.md'));
    get('learner-question').value='How do True Zero and the Elements Basin relate?';
    submit();
    assert.equal(get('lesson-title').textContent,'The Natural Order');
    assert.equal(get('lesson-plain').hidden,true);
    assert.equal(get('lesson-detail').open,true);
    assert.match(get('lesson-summary').textContent,/True Zero.*Elements Basin/is);
    get('learner-question').value='What is the shared purpose of Frankie and the Teacher?';
    submit();
    assert.equal(get('lesson-title').textContent,'Frankie & Teacher — Shared Purpose');
    assert.match(get('lesson-summary').textContent,/choice remains theirs/i);
    get('learner-question').value='What is ERK-X1?';
    submit();
    assert.equal(get('lesson-title').textContent,'Ethical Reasoning — ERK-X1');
    assert.match(get('lesson-summary').textContent,/placeholder logic/i);
    assert.equal(get('kernel-panel').hidden,true,
      'an ethical prototype must not create a twelfth action or proof challenge');
    // A one-word keyword is insufficient standing to choose a lesson.
    get('learner-question').value='gravity';
    submit();
    assert.equal(get('stage-map').hidden,false);
    assert.match(get('map-explanation').textContent,/understand your question/i);
    assert.match(get('map-your-question').textContent,/gravity/i);
    assert.equal(get('map-options').children.length,1);
    get('learner-question').value='GRAVITY?';
    submit();
    assert.equal(get('stage-map').hidden,false,'an unchanged resubmission cannot confirm a guessed lesson');
    assert.equal(get('map-options').children.length,1);
    get('map-options').children[0].listeners.click();
    assert.equal(get('lesson-title').textContent,'Physical & KCD Examination');
    // Clarification remains attached to the original visitor example.
    get('learner-question').value='Why is the river bank eroding?';
    submit();
    get('learner-question').value='I mean AHMR and changed conditions';
    submit();
    assert.equal(get('lesson-title').textContent,'AHMR & Continuance');
    assert.match(get('lesson-connection').textContent,/water/i);
    // Protected source details keep their human review boundary mid-dialogue.
    get('learner-question').value='Why is the river bank eroding?';
    submit();
    get('learner-question').value='Show complete private NEW K formula';
    submit();
    assert.equal(get('stage-access').hidden,false);
    // A real-world question must survive both routing and presentation.
    const warehouse='I work in a warehouse. How do we stop an unsafe pallet movement if approval is withdrawn?';
    get('learner-question').value=warehouse;
    submit();
    assert.equal(get('lesson-title').textContent,'Consequence Custody');
    assert.match(get('lesson-summary').textContent,/warehouse|pallet/i);
    assert.doesNotMatch(get('lesson-connection').textContent,/payment|settlement/i);
    assert.ok(get('source-list').children.length>0);
    assert.equal(get('kernel-panel').hidden,true,'do not switch a warehouse visitor into an unrelated payment exercise');
    get('learner-question').value='Explain simply';
    submit();
    assert.match(get('lesson-summary').textContent,/pallet|warehouse/i);
    assert.equal(get('kernel-panel').hidden,true,'the unrelated payment example stays hidden after simplification');
    get('learner-question').value="I'm confused";
    submit();
    assert.equal(get('kernel-panel').hidden,true,'patience must not substitute a new evidence exercise');
    get('learner-question').value="I'm skeptical. Why should I believe any of this, and what has actually been verified?";
    submit();
    assert.equal(get('lesson-title').textContent,'Proof Before Power');
    assert.match(get('lesson-summary').textContent,/independent reproduction|not proof/i);
    get('learner-question').value='Is gravity a wave array, and has that been independently demonstrated?';
    submit();
    assert.equal(get('lesson-title').textContent,'Physical & KCD Examination');
    assert.match(get('lesson-summary').textContent,/not been independently demonstrated/i);
    get('learner-question').value='Is the Elements Basin the same as dark matter?';
    submit();
    get('learner-question').value="I don't believe that. Your explanation is wrong.";
    submit();
    assert.equal(get('stage-map').hidden,false);
    assert.match(get('map-explanation').textContent,/still learning|listen better/i);
    assert.match(get('map-your-question').textContent,/Elements Basin/i);
  } finally {
    delete globalThis.document;
    delete globalThis.window;
  }
});
