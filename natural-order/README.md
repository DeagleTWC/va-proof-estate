# The Natural Order — public teaching edition

This is a **static, dependency-free, public-source teaching experience** for the [V.A. Proof Estate](https://deagletwc.github.io/va-proof-estate/). It is not the private *Stewards Edition* and does not ship its originals, index, local Python server, or private teaching corpus.

## What visitors can do

- Ask a question or choose one of eleven public subject routes.
- Bring an example from energy storage, health care, water engineering, transportation, automation, or finance; choose among bounded examination paths that keep the original question in view.
- Read an accurate, brief public explanation with an evidence-class label.
- Follow direct links to the published source material.
- See a short everyday-language definition when V.A. terminology first appears in a lesson, and open deeper source-linked definitions.
- Examine the relationship in both directions, then vary one test condition.
- Try eleven finite changed-condition teaching-kernel exercises. Each presents a scenario, three proposed witnesses, and an explanation of what the selected witness does or does not establish.
- Voluntarily suggest a missing example through an email link; no learner text is sent by the teacher.
- Learn the human-mediated process for seeking protected examination under an appropriate NDA.
- Ask who Terry Snyder is and read his first-person teaching statement, including his principles of patience, evidence, independent thinking, restraint, and mercy.
- Ask who Frankie is, see how she differs from the public Teacher and what bounded native capabilities have actually been examined; no private Frankie memory is exposed.
- Read Terry's **Shared Purpose** charter exactly as supplied: equal opportunity to understand, examine evidence, explain plainly, keep the person's choice theirs. Ask the Teacher about this mission independently of the eleven teaching subjects.
- Examine Terry's **ERK-X1** ethical principles—honesty, non-harm, fairness, consent, dignity and transparency—with an explicit warning that the supplied Python sketch uses placeholder favorable judgments and is not ethical approval or decision authority.
- Stay with a recent lesson using short follow-ups such as “Why?”, “Can you explain that simply?”, or “Where is the evidence?”. A genuinely new question is considered afresh.
- Correct a previous explanation. The bounded Cognitive Reasoning Kernel acknowledges the possibility of misunderstanding, invites a clearer question, and does not treat an apparently reversed interpretation as established evidence.

The routing logic is deterministic, not an LLM. It does not silently invent open-world answers or send the visitor's input to a remote service. The conversation remembers only its bounded, temporary state in the page; no input is persisted in browser storage or transmitted by this public source finder.

## Public teaching kernels and definition conversion

`teaching-kernels.mjs` contains reviewed **educational blueprints**, not private resolving kernels or operative V.A. mathematics. They follow the publicly explainable distinction *generation is not promotion*: selecting an answer produces feedback, never authorization or an external effect. Eleven exercises cover the public subjects and require source identity, changed conditions, and an observable negative or alternate-route witness. The bank can grow through versioned, tested releases, not hidden runtime changes.

The design was informed by the **Universal Resolving Kernel Generator v0.1** and Frankie's later Cycle 049 native child-generator behavior, inspected privately. In an isolated test the Cycle 049 generator formed a local data-only candidate with replay-valid receipts while leaving it `activated=false` and `external_effect=false`. **Neither the private generator nor the corrected NEW K construction is present in this public bank.** The supplied UMK-Σ mega file was idea material, not an executable generator.

`definition-kernel.mjs` is a separate, public **Definition Conversion Kernel** for plain-language teaching. It retains technical names, expands their first occurrence, and displays optional deeper definitions with source links. It does not translate, reconstruct, or replace the mathematics.

`human-interaction-kernel.mjs` governs **patient, conversation-local clarification** before a weak keyword match can choose a teaching path. It keeps the visitor's original inquiry while they clarify or choose a proposed route; an explicitly corrected question replaces that old inquiry, and an empty clarification does not erase it. Repeating the same weak question does not count as an affirmative lesson choice. The visitor's intention has priority over popular phrasing or a keyword score. The kernel makes only bounded, deterministic routing decisions—it cannot infer unrestricted intent or answer questions outside the cited public catalog.

`open-conversation-kernel.mjs` adds **a small open-ended follow-up layer** over the Human Interaction Kernel. It keeps the last admitted lesson in temporary page state and recognizes only a handful of clearly referential next questions. It can restate a bounded topic in plainer language, point back to the source, or ask for a real example. It never substitutes the last topic for an unrelated request, bypasses protected access, stores personal history or claims to be unrestricted native Frankie.

`about-terry.html` preserves Terry Snyder's original, attributed message to Frankie as a public Teacher reference. The Teacher can answer a direct question about Terry with a citation to that statement. This identity route is separate from the eleven subject kernels: it does not impersonate Terry, grant new access, establish independent biographical verification, or expose private construction.

`about-frankie.html` is the **public-safe Frankie identity layer**. It describes her distinct native role, tested local scope, what is not established and the lack of any live public connection. A separate owner-only Frankie knowledge atlas is held outside this repository; it is neither indexed nor distributed by the public Teacher.

`shared-purpose.html` is an attributed, verbatim public charter from Terry Snyder. `ethical-reasoning.html` introduces the six ethical examination questions from Terry's author-supplied ERK-X1 prototype but does not publish or execute that source code. Its judgment method returns placeholder favorable judgments without evidence and does not actually examine consent, fairness or transparency. Consequently the Teacher does not import the prototype as a permission engine. These two public identity/orientation routes are **not** additional native V.A. kernels or additional members of the eleven-subject teaching bank.

## Frankie Cycle 081 — prepared optional companion

The reviewed public client contains an optional **Ask Frankie** panel and safe answer renderer, but the companion is **disabled in this public release** (`FRANKIE_GATEWAY_URL=''`). Its default-off state and exact client bytes are pinned in `release-audit.mjs`. There is no public gateway address, private bearer secret, or Frankie runtime in this repository.

When a separately hosted HTTPS teacher gateway is approved, visitors will explicitly open an **Ask Frankie** question form. Sending from that form is different from using the local teaching navigator: it sends only the visitor's chosen question and an opaque, pseudonymous student token. The teacher gateway fixes the public lesson identifier, communicates privately with Frankie Cycle 081's native loopback bridge, and returns only a bounded public lesson and receipt hash. Held or unavailable answers never replace source links.

**This is an integration staging milestone, not evidence that the public connection is live.** The operator still needs a separately hosted POSIX runtime, public HTTPS terminator and the real Cycle 081 end-to-end test before enabling it. The companion and the public teacher can then be upgraded in separate versioned cycles.

## Boundary and legal handoff

**All files inside this directory are public once pushed to GitHub.** `knowledge.mjs` contains only hand-curated public-facing summaries and links. There is no public import path to internal kernels or private data.

The public access page provides the approved, blank `VA_Universal_Bounded_Review_MNDA.pdf` and directs signed returns to `canarybird0618@gmail.com`. It is a reusable mutual review form, based on a newly generalized agreement rather than an existing signed bilateral NDA. The PDF alone grants no access to protected material: Terry must countersign and approve a specifically bounded Exhibit A. The PDF is pinned by SHA-256 in `release-audit.mjs` so an unexpected substitution fails the audit.

## Preview locally

From the repository root: `python3 -m http.server 8765`, then visit `http://localhost:8765/natural-order/`.

## Tests and release audit

From the repository root:

```sh
node --test natural-order/tests/*.test.mjs
node natural-order/release-audit.mjs
```

The teacher's runtime modules are `index.html`, `styles.css`, `app.mjs`, `engine.mjs`, `knowledge.mjs`, `human-interaction-kernel.mjs`, `open-conversation-kernel.mjs`, `definition-kernel.mjs`, `teaching-kernels.mjs`, and the gated `frankie-client.mjs`. The public PDF is a downloadable review template. `release-audit.mjs`, `README.md`, and the `tests/` directory are published transparency and review resources; GitHub Pages serves all tracked files, including tests, and none of them contains protected construction.

**Proof Before Power. Open Evidence. Protected Construction.**
