# Meaning-Preserving Teaching Kernel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give novice public Teacher visitors a short accurate answer first, keeping detailed evidence and source-specific meaning accessible.

**Architecture:** A dependency-free pure module selects pre-reviewed plain leads only for eligible standard lessons. The existing renderer shows it first, with the unchanged full account behind a native disclosure; the routing, eleven subjects and protected-access behavior are untouched.

**Tech Stack:** Native JavaScript modules, static HTML/CSS, Node test runner, existing GitHub Pages release.

**Spec:** `docs/superpowers/specs/2026-11-22-meaning-preserving-teaching-kernel-design.md`

## Global Constraints

- No new teaching subject or modification to the eleven exercises.
- No remote API, persistence, protected content, or new physical proof claim.
- Keep original question, evidence status, full summary, sources and review route.
- Bump all browser module/style references coherently from `20261122-natural-order-24` to `20261122-natural-order-25`.
- The companion Frankie gateway remains disabled.

## Review Focus

- A visitor asks “Explain simply” after a source-specific answer: keep the source-specific caveats visible, not a generic lesson.
- A named mathematical question or pilot evidence answer: MPTK must not replace precise status with generic text.
- A protected request: access path only, no short lesson.
- Eleven standard subjects: none is silently dropped or assigned another subject's copy.
- Browser disclosure: never hides the only evidence/source links or makes the full statement inaccessible.

---

### Task 1: Pure MPTK selection and teaching copy

**Files:**
- Create: `natural-order/meaning-preserving-teaching-kernel.mjs`
- Test: `natural-order/tests/meaning-preserving-teaching-kernel.test.mjs`

**Interfaces:**
- Consumes: existing `{kind:'lesson',topic,conversation?,originalQuestion?,sources?}` responses.
- Produces: `publicPlainLead(response): string | null`.

- [ ] **Step 1: Write failing tests** for natural-order, URK, Basin, eleven subject coverage, unrelated lesson, source-specific responses, malformed/nonlesson/protected requests. Assert output meaning and evidence ceiling rather than exact punctuation.
- [ ] **Step 2: Run RED** `node --test natural-order/tests/meaning-preserving-teaching-kernel.test.mjs` (missing module or unmet behavior).
- [ ] **Step 3: Implement the pure module** with frozen topic-id copy, source-specific guard and no I/O.
- [ ] **Step 4: Run GREEN** targeted and full public tests.
- [ ] **Step 5: Commit** `Teacher: add meaning-preserving public explanation kernel`.

### Task 2: Visible first answer, disclosure, release wiring

**Files:**
- Modify: `natural-order/index.html`, `natural-order/app.mjs`, `natural-order/styles.css`, `natural-order/README.md`, `natural-order/access.html`, `natural-order/engine.mjs`, `natural-order/open-conversation-kernel.mjs`, `natural-order/visitor-answer-desk.mjs`, `natural-order/release-audit.mjs`.
- Test: `natural-order/tests/pages.test.mjs`, `natural-order/tests/app-interaction.test.mjs`, `natural-order/tests/release.test.mjs`.

**Interfaces:**
- Consumes: `publicPlainLead(response)` from Task 1; full original lesson remains untouched.
- Produces: an accessible `#lesson-plain` paragraph and `#lesson-detail` native disclosure with original `#lesson-summary`.

- [ ] **Step 1: Write failing page/interaction tests** showing the new element IDs, new imported module and versioned graph, no broken sources; audit includes new public module/test.
- [ ] **Step 2: Run RED** targeted tests.
- [ ] **Step 3: Implement native disclosure**; show short lead when available, default expanded detail when not; preserve existing links/exercises and all grades.
- [ ] **Step 4: Bump v25 imports/styles**, document MPTK, update exact audit manifest.
- [ ] **Step 5: Run GREEN** full tests, `node natural-order/release-audit.mjs`, `git diff --check`.
- [ ] **Step 6: Commit** `Teacher: present simple first answers with full evidence available`.

### Task 3: Review and guarded publication

**Files:** No additional product files unless review uncovers a tested issue.

- [ ] **Step 1: Request one read-only whole-branch review** concentrating on original-source meaning, private access and disclosure.
- [ ] **Step 2: Fix Critical/Important issues test-first**, rerun complete suite and audit.
- [ ] **Step 3: Compare current remote head/subtrees** with local base; use a non-force, expected-SHA guarded publication keeping unrelated math commits.
- [ ] **Step 4: Verify GitHub Teacher public checks and Pages deployment** for published SHA before claiming the site live.
