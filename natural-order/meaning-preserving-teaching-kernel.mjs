// One public, source-constrained explanation layer shared across subjects.
// The entries below explain reviewed standard topic copy in ordinary language;
// they do not generate facts, judge evidence, or select a different lesson.
const PLAIN_LEADS=Object.freeze({
  'natural-order':'The Natural Order is the public V.A. account of how starting conditions shape what changes are possible and which effects may legitimately happen. It is a framework to examine against evidence, not a claim that every physical question has been settled.',
  'va-identity':'V.A. — The Shift examines whether a proposed action can acquire the right conditions to produce a real effect before that effect forms. Its public records describe particular designs and tests, each with limits you can inspect.',
  'teacher-purpose':'This Teacher helps you explore a question in ordinary language and follow public evidence. It offers a path for learning, not an answer to every possible question or access to private construction.',
  'about-terry':'Terry Snyder describes himself as an explorer who worked to discover and share the Natural Order. He asks this Teacher to be patient, explain clearly, welcome questions and put proof before power.',
  'about-frankie':'Frankie is a separate software companion in Terry’s V.A. work, not this public Teacher. Some of her functions have been tested under limited conditions; she is not connected to this public page.',
  'shared-purpose':'Terry wants people to have a fair chance to understand evidence and make their own informed choices. The Teacher helps examine what is known, uncertain or missing, without making the decision for you.',
  'ethical-reasoning':'Before calling a decision ethical, ask about honesty, harm, fairness, consent, dignity and transparency. The published example does not actually prove ethical approval or permission to act.',
  'true-zero':'True Zero is the starting ground in the public V.A. account, before a proposed action has permission to produce an effect. It is not simply the number zero or a reset button.',
  basin:'In Terry Snyder’s Natural Order account, the Elements Basin describes conditions that shape possible movement. Terry identifies it with dark matter, but that physical identification has not been independently established by the public evidence.',
  'new-k':'Corrected NEW K is the current mathematics described as the foundation for V.A. Older versions are not interchangeable with it, and the underlying construction is protected.',
  urk:'URK describes a formal way to check whether a proposed change meets its conditions before it can produce an effect. It can refuse or stop a change when conditions fail; that does not prove every physical application.',
  ahmr:'When conditions change, continuing is not automatic. This public framework examines whether a process may continue, must pause or must stop under its stated conditions.',
  consequence:'V.A. asks whether an unauthorized effect can be prevented from forming at all. A refusal message or computer log alone cannot prove that a real effect was prevented by every possible route.',
  proof:'An explanation is not proof. Examine the original observation, test conditions, controls, changed-condition runs and a way someone else can check the result. A simulated example proves only its own limited case.',
  pilot:'A pilot tells us only what its actual records show under the conditions tested. Some original records are not attached here, so a public link by itself does not reproduce every claimed result.',
  physical:'A software log cannot prove what happened in a physical apparatus. The public KCD work describes physical tests that would need independent instruments; it does not attach a completed new physical run.',
  safeguarding:'Protecting people requires meaningful permission, usable human intervention and evidence of what actually happened. Naming a human reviewer alone does not establish a safe result.',
  'repair-evidence':'A public image study found a repeated visual relationship through a specific sequence of changes. That limited observation does not establish the physical mechanism or every interpretation of the image.',
});

export function publicPlainLead(response){
  if(!response||response.kind!=='lesson'||!response.topic||typeof response.topic.id!=='string')return null;
  const topic=response.topic;
  const reviewed=Object.hasOwn(PLAIN_LEADS,topic.id)?PLAIN_LEADS[topic.id]:null;
  if(!reviewed)return null;
  // An explicitly routed visitor question can be narrower than the subject
  // summary even when that answer reused standard subject wording. Keep the
  // visitor's own intent in the primary public response.
  if(typeof response.originalQuestion==='string'&&response.originalQuestion.trim()&&!response.bridge)return null;
  // A direct, context-specific answer has its own bounded wording. Do not
  // substitute a general introduction or drop its evidence/source ceiling.
  if(typeof response.conversation?.summary==='string' &&
    response.conversation.summary.trim() && response.conversation.summary!==topic.summary)return null;
  return reviewed;
}
