import {TOPICS} from './knowledge.mjs?v=20261122-natural-order-25';

// Finite answers about the *public* record. This is a source navigator, not a
// general mathematical solver, proof validator, or private source index.
const source=(title,href)=>({title,href});
const mathSources=Object.freeze([
  source('Public mathematics and ongoing research','../mathematics.html'),
  source('Mathematics publication and status register','../research/mathematics/PUBLICATION-STATUS.md'),
  source('Machine-readable mathematics index','../research/mathematics/INDEX.json'),
  source('Mathematics independent-review crosswalk','../research/mathematics/REVIEW-CROSSWALK.md'),
]);

const custodyTopic=Object.freeze({
  id:'custody-compliance',number:'00',title:'Compliance and Native Consequence Custody',
  kicker:'Before power, not an after-the-fact compliance layer',grade:'PUBLIC ENGINEERING ACCOUNT',
  summary:'Human oversight and compliance can review, supervise or record activity. V.A. describes a different native consequence-custody objective: before power or consequential formation, proposed movement must have lawful standing under the governing conditions. Kernelization is presented as the way to make impermissible consequences non-forming, not as an extra policy check or post-event log.',
  connection:'Terry’s underwriting distinction is that the custody system itself is the proposed underwritable autonomous system. Bonding, insurance and underwriting concern the consequences that can actually form when a button is pressed; a technical design or published record is not, by itself, an insurer’s approval or guarantee.',
  question:'Which original, independently observable positive and negative controls, changed-condition runs, bypass tests and replay receipts would establish this custody boundary?',
  sources:[source('V.A. native foundation','../foundation.html'),
    source('Proof Before Power — examination requirements','../proofs/EXAMINATION-STANDARD.md'),
    source('Public claim-to-carrier evidence','../proofs/CLAIM-TO-CARRIER.json'),
    source('Evidence Hall — scope and witnessed status','../evidence-hall.html')],
});

const mathTopic=Object.freeze({
  id:'math-public',number:'00',title:'Mathematics — Public Answers and Ongoing Work',
  kicker:'The knowledge belongs to everyone; each answer has a scope',grade:'PUBLIC RESEARCH INDEX',
  summary:'The public mathematics section indexes source-preserved mathematical work, finite witnesses, proposed answers and ongoing examinations. It does not establish that every mathematical question has been solved, and a missing public link does not mean no one is working on the question.',
  connection:'We can examine the published version, assumptions, proof steps, bounded witnesses and remaining obligations. Protected native construction is not in this public Teacher.',
  question:'If your exact question is not answered here, you may send a voluntary message asking where its answer or current work can be found.',
  sources:mathSources,
});

const namedMath=Object.freeze([
  {
    terms:/\bp\s*[-–—]?\s*(?:vs\.?|versus|v\.?)\s*[-–—]?\s*np\b|\bp\s*(?:=|≠|!=)\s*np\b/i,
    summary:'The public P-versus-NP record includes bounded Boolean and source-custody examinations, including Native Examination 91 and a later author-proposed decision formulation. An unrestricted P-versus-NP resolution is not established by those public records.',
    sources:[source('P versus NP — public examination','../p-versus-np.html'),
      source('Examination 91 — scope and checks','../research/p-versus-np/EXAMINATION-91-PUBLIC-STATUS.md'),
      source('Later proposed native decision answer','../research/p-versus-np/PROPOSED-ANSWER-URK-DECISION-AND-PROOFS-2026-11-13.md')],
  },
  {
    terms:/\bnavier[-\s–—]*stokes\b/i,
    summary:'The published Navier–Stokes work provides bounded Fourier/harmonic-edge tests, preserved sources and formula-to-proof material. An unrestricted three-dimensional regularity theorem is not authenticated by the linked public companion.',
    sources:[source('Navier–Stokes research examination','../navier-stokes.html'),
      source('Exact public proof-chain status','../research/navier-stokes/URK_PROOF_CHAIN_STATUS_v1.1.json')],
  },
  {
    terms:/\byang[-\s–—]*mills\b/i,
    summary:'The Yang–Mills public research includes exact finite SU(2) constructions and bounded checks. A proposed continuum answer is under examination; an unrestricted continuum mass-gap result is not established by the linked public status.',
    sources:[source('Yang–Mills research examination','../yang-mills.html'),
      source('Yang–Mills public proof-chain status','../research/yang-mills/URK_PROOF_CHAIN_STATUS.json')],
  },
  {
    terms:/\briemann\s+hypothesis\b/i,
    summary:'The Riemann Hypothesis has a named public research track, but a complete authorized original proof carrier and its examination record are not yet linked or mirrored in this repository’s mathematics index. That is a publication-status statement, not a global verdict on the question.',
    sources:[source('Mathematics publication status','../research/mathematics/PUBLICATION-STATUS.md'),
      source('Research publication coverage','../research-publication.html')],
  },
  {
    terms:/\berd[őoö]s[-\s–—]*straus\b|\begyptian\s+(?:unit\s+)?fractions?\b/i,
    summary:'The public Egyptian-unit-fractions child witness gives exact formulas on a bounded set of residue classes, with unresolved corridors beyond those formulas. It is not an unrestricted resolution of the Erdős–Straus conjecture.',
    sources:[source('Egyptian fractions — interactive bounded witness','../math/egyptian-child/index.html'),
      source('Original child proof and limitations','../math/egyptian-child/PROOF.md')],
  },
  {
    terms:/\badmissibility[-\s–—]*debt\s+geometry\b/i,
    summary:'Admissibility–Debt Geometry has published conditional model theorems, exact rational witnesses and a public release manifest. This does not independently establish the model in unrestricted real-world operation or claim external peer review.',
    sources:[source('Admissibility–Debt Geometry examination','../admissibility-debt-geometry.html'),
      source('Exact public release and status manifest','../research/admissibility-debt-geometry/PUBLIC_RELEASE_MANIFEST.json')],
  },
  {
    terms:/\bgrid[-\s–—]*k1\b/i,
    summary:'GRID-K1 includes finite single-commodity network and conditional model theorems with synthetic proof receipts. The public release does not claim physical-grid deployment, certified cascade prevention or independent third-party review.',
    sources:[source('GRID-K1 infrastructure continuity geometry','../grid-k1-infrastructure-continuity.html'),
      source('GRID-K1 public release manifest','../research/grid-k1/PUBLIC_RELEASE_MANIFEST.json')],
  },
  {
    terms:/\bconsequence\s+signature\s+calculus\b/i,
    summary:'Consequence Signature Calculus has a public original mathematical formalization and source-custody manifest. Its published standing is a formal model, not an independently established unrestricted physical theorem.',
    sources:[source('Consequence Signature Calculus formalization','../consequence-signature-calculus.html'),
      source('Original formalization public release manifest','../research/consequence-signature-calculus/PUBLIC_RELEASE_MANIFEST.json')],
  },
]);

export const hasNamedPublicMathematics=input=>namedMath.some(item=>item.terms.test(String(input??'')));

const complianceQuestion=question=>/\b(?:compliance|human[- ]in[- ]the[- ]loop|human oversight|regulatory)\b/i.test(question) &&
  /\b(?:v\.?\s*a\.?|custody|autonom\w*|underwrit\w*|insur\w*|bond\w*)\b/i.test(question) ||
  /\b(?:custody\s+systems?|autonom\w+)\b.{0,90}\b(?:underwrit\w*|insur\w*|bond\w*)\b/i.test(question);
const pilotQuestion=question=>!/\b(?:airport|aircraft|airplane|airline|aviation|flight|runway|pilot\s+(?:light|holes?))\b/i.test(question) &&
  /\b(?:verify|reproduce|examine|find|where|show|inspect)\b/i.test(question) &&
  /\bpilots?\b/i.test(question) &&
  (/\b(?:v\.?\s*a\.?|natural order|proof estate|historical|hospital|seam|your)\b/i.test(question) ||
    /\bpilots?\s+(?:records?|reports?|evidence|tests?|runs?|carriers?)\b/i.test(question));
const evidenceQuestion=question=>!/^\s*what\s+is\s+proof\s+before\s+power\b/i.test(question) &&
  !/^(?:where\s+is\s+the\s+evidence|where(?:'s| is)\s+the\s+proof)[?.!\s]*$/i.test(question) &&
  (/\b(?:where|show|find|inspect|verify|reproduce|independent(?:ly)?)\b.{0,130}\b(?:proof|evidence|claim|reproducible|reproduced|source|sources)\b/i.test(question) ||
    /\b(?:what|where)(?:'s| is)\s+the\s+(?:independent\s+|reproducible\s+)?(?:proof|evidence)\b/i.test(question));
const generalMathQuestion=question=>/\b(?:math(?:ematics|ematical)?|theorem|conjecture|equation|number theory|whole numbers?|integers?|prime numbers?|mathematical answer|solved problem)\b/i.test(question);
// Only route a physical-science question here when the visitor anchors it to
// the Natural Order account. Generic cosmology belongs to ordinary enquiry.
const basinQuestion=question=>(/\belements\s+basin\b/i.test(question) &&
    /\b(?:dark matter|field|earth|gravity|wave array|horizon|water)\b/i.test(question)) ||
  // "natural order of ..." is ordinary descriptive English, not a claim
  // that the visitor is asking about Terry's named Natural Order project.
  (/\bnatural\s+order\b(?!\s+of\b)/i.test(question) &&
    (/\b(?:dark matter|horizon|gravity.{0,35}wave array)\b/i.test(question) ||
      /\bnatural\s+order\s+water\b/i.test(question)));

function lesson(topic,question,{summary=topic.summary,connection=topic.connection,sources=topic.sources}={}){
  return {kind:'lesson',topic,originalQuestion:question,sources,
    conversation:{summary,connection,question:topic.question}};
}

export function publicVisitorAnswer(input){
  const question=String(input??'').trim().slice(0,800);
  if(!question)return null;
  if(complianceQuestion(question))return lesson(custodyTopic,question);
  const named=namedMath.find(item=>item.terms.test(question));
  if(named)return lesson(mathTopic,question,{summary:named.summary,
    connection:'The links identify the published result and its current scope. Check the original hypotheses and source before treating a proposed or bounded result as a general theorem.',
    sources:[...named.sources,...mathSources]});
  if(basinQuestion(question)){
    const basin=TOPICS.find(item=>item.id==='basin');
    const waterOrHorizon=/\b(?:water|horizon)\b/i.test(question);
    return lesson(basin,question,{summary:waterOrHorizon
      ? `${basin.summary} Natural Order water names a Basin element, not H2O. A horizon is an access or observation boundary, not evidence of deletion or destruction. Claims of transfer, re-encoding or conservation need explicit accounting and independent physical measurement; the public KCD software does not establish a black-hole or cosmological consequence.`
      : basin.summary});
  }
  const proof=TOPICS.find(item=>item.id==='proof');
  const pilot=TOPICS.find(item=>item.id==='pilot');
  if(pilotQuestion(question))return lesson(pilot,question,{
    summary:'The public estate has historical pilot accounts and a release procedure, but original January pilot run carriers are not attached to this repository. These links alone cannot independently replay a specific claimed native pilot. Evidence must be checked at its exact recorded scope, not treated as unrestricted independent reproduction.',
    connection:'Begin with the pilot evidence release and historical crosswalk. Compare run identity, original witness, changed-condition controls and replay receipts. To examine originals that are not publicly attached, use the authorized reviewer route and its lawful disclosure boundaries.',
    sources:[source('Public pilot evidence release','../proofs/PILOT-EVIDENCE-RELEASE.md'),
      source('Historical evidence index','../proofs/HISTORICAL-EVIDENCE-INDEX.md'),
      source('Historical pilot-to-carrier crosswalk','../proofs/HISTORICAL-PILOT-CARRIER-CROSSWALK.md'),
      source('Independent examination route','../reviewer-route.html'),
      source('Evidence Hall — status and limits','../evidence-hall.html')],
  });
  if(evidenceQuestion(question))return lesson(proof,question,{
    summary:'Independent proof requires more than an assertion, an index or a refusal receipt. Begin with original bounded records, positive and negative controls, changed-condition runs, alternate-route checks, independent observation and replay. The public materials must be read at their exact evidenced scope.',
    connection:'Here are the public Proof Estate, pilot, claim-to-carrier and reviewer paths. The linked documents let you examine what is declared, observed and independently reproduced; a link alone does not upgrade a claim into physical proof.',
    sources:[source('Evidence Hall — claim and witness scope','../evidence-hall.html'),
      source('Independent examination standard','../proofs/EXAMINATION-STANDARD.md'),
      source('Public pilot evidence release','../proofs/PILOT-EVIDENCE-RELEASE.md'),
      source('Historical evidence index','../proofs/HISTORICAL-EVIDENCE-INDEX.md'),
      source('Public claim-to-carrier register','../proofs/CLAIM-TO-CARRIER.json'),
      source('Examiner route and repository sources','../reviewer-route.html')],
  });
  if(generalMathQuestion(question)&&!/(?:\bnew\s+k\b|\burk\b|\btrue\s+zero\b)/i.test(question)){
    return lesson(mathTopic,question,{summary:'I cannot locate a published answer to your exact question with this finite public question matcher. That is not a search of every published record: the mathematics register contains additional indexed research and ongoing work. Absence here does not prove the question is globally unsolved or that nobody is examining it.',
      connection:'Please check the mathematics publication register and current research. If the answer is not clear there, you can voluntarily ask where this specific answer or active examination can be found.',
      sources:mathSources});
  }
  return null;
}
