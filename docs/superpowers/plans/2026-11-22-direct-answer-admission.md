# Direct Answer Admission Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let a clear first-time visitor receive the relevant sourced Teacher answer immediately without weakening patient clarification or protected access.

**Architecture:** Keep the existing Human Interaction Kernel and public answer desk. The answer desk admits standalone public proof requests. Human Interaction admits a narrowly defined, real-world changed-authority finance inquiry when the source router already produces a compatible, single topic; Conversation Compatibility makes that response explicitly about settlement and evidence rather than a generic topic. Quick-start copy submits exactly what visitors see.

**Tech Stack:** Static browser ESM, Node built-in test runner, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-11-22-direct-answer-admission-design.md`

## Global Constraints

- Protected-access and source-specific public mathematical answers must never be weakened.
- No new network calls, external runtime, private materials, or additional teaching subjects.
- Maintain public source/evidence ceiling and real-world noncertification.
- Cache token `20261122-natural-order-28` across entry, stylesheet and module graph.

## Review Focus

1. A standalone proof question gets the public proof evidence explanation, while the same question after a prior lesson remains a contextual follow-up.
2. A clearly changed-authority payment question gets an immediate, truthful consequence explanation, including non-observation of actual settlement.
3. A mere “payment” or weak unrelated query stays in patient clarification, with no keyword-driven certainty.
4. A protected formula request containing the new trigger stays behind the private review gate.
5. The Proof shortcut's actual click directly shows the evidence route; the eleven existing subject exercises still function.

---

### Task 1: Direct first-question admission

**Files:**
- Modify: `natural-order/human-interaction-kernel.mjs`
- Modify: `natural-order/visitor-answer-desk.mjs`
- Modify: `natural-order/conversation-compatibility-kernel.mjs`
- Test: `natural-order/tests/human-interaction-kernel.test.mjs`
- Test: `natural-order/tests/visitor-answer-desk.test.mjs`
- Test: `natural-order/tests/open-conversation-kernel.test.mjs`
- Test: `natural-order/tests/conversation-compatibility-kernel.test.mjs`

**Interfaces:**
- Consumes `teach(question)` and its existing `{kind,topic,selection,bridge}` result, `createHumanInteractionKernel({resolve,topics})`, `reviewConversationCompatibility(question,candidate,{topics,priorLesson})`.
- Produces the existing kinds (`lesson`, `map`, `access`), no new public result type.

- [ ] **Step 1: Write failing tests** for exact public proof and changed-authority payment first-turn questions, with cited sources and the original question retained. Also pin contextual proof follow-up, ambiguity and protected variants.
- [ ] **Step 2: Verify RED** with `node --test natural-order/tests/{human-interaction-kernel,visitor-answer-desk,open-conversation-kernel,conversation-compatibility-kernel}.test.mjs`. Expected: at least one first-turn result wrong, with the older safety cases passing.
- [ ] **Step 3: Implement bounded admission** in the three modules, keeping existing source identity and preventing general inferred guesses from becoming answers.
- [ ] **Step 4: Verify GREEN** with the same targeted tests. Expected: all pass.
- [ ] **Step 5: Commit** these modules and tests to the isolated branch.

### Task 2: Published interface and release boundary

**Files:**
- Modify: `natural-order/index.html`, `natural-order/access.html`, `natural-order/app.mjs`, `natural-order/engine.mjs`, `natural-order/open-conversation-kernel.mjs`, `natural-order/visitor-answer-desk.mjs`, `natural-order/README.md`
- Test: `natural-order/tests/pages.test.mjs`, `natural-order/tests/app-interaction.test.mjs`

**Interfaces:**
- Consumes Task 1's unchanged result types. The public click handler submits `button.dataset.prompt` to the real `ask()` path.
- Produces a truthful Proof shortcut and consistent `20261122-natural-order-28` asset graph.

- [ ] **Step 1: Write failing browserless UI tests** for the Proof button's label/prompt contract and immediate relevant response to a payment question.
- [ ] **Step 2: Verify RED** with targeted page/app tests; expect button contract or first-turn lesson to fail.
- [ ] **Step 3: Align quick-start prompt** with its label, update the public-safe explanation and release version in entry/style/modules.
- [ ] **Step 4: Verify GREEN** with `node --test natural-order/tests/*.test.mjs` and `node natural-order/release-audit.mjs` plus `git diff --check`.
- [ ] **Step 5: Commit** UI, docs and version changes.

### Task 3: Final review and guarded publish

**Files:** None beyond Important corrections discovered in review.

- [ ] **Step 1:** Self-review the cumulative patch against the five Review Focus classes (no subagent dispatch under current delegation boundary).
- [ ] **Step 2:** Run the full 11-subject suite, public audit and diff check freshly.
- [ ] **Step 3:** Confirm current GitHub `main` baseline and construct only exact changed public files; verify `docs` and `natural-order` tree hashes match local git and unrelated trees remain unchanged.
- [ ] **Step 4:** Guarded fast-forward branch update, wait for public release and Pages deployment workflows to complete successfully.
- [ ] **Step 5:** Live smoke test Proof shortcut and payment question on the published site; report actual result, including any remaining gap.
