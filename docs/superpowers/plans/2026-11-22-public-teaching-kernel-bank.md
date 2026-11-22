# Public Teaching Kernel Bank Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a versioned, source-bound bank of eleven executable public learning exercises and a voluntary feedback route in the existing Natural Order Teacher.

**Architecture:** Pure data and admission/assessment functions in `natural-order/teaching-kernels.mjs` drive a new optional UI inside the existing source teacher. No backend, persistence, telemetry, private math or Frankie activation.

**Source correction:** The supplied mega text is blueprint-only. Implementation must follow the inspected URK generator/Frankie Cycle 049 native-candidate lineage as a public-safe educational derivative, with no protected generation code, no historical K substituted for corrected NEW K, and no claim that a classroom answer is an operative admission. A separate public Definition Conversion Kernel supports first-use everyday explanations and source-linked expansion.

**Tech Stack:** browser ES modules, Node 24 built-in test runner, existing GitHub Pages/CSS.

**Spec:** `docs/superpowers/specs/2026-11-22-public-teaching-kernel-bank-design.md`

## Global Constraints

- Existing ordinary source teacher and routes remain independent of Frankie.
- No unauthorized effects, hidden analytics, credentials or private mathematics in public files.
- `connect-src 'none'` stays in the shipped Content Security Policy.
- Every exercise is admitted to finite public educational scope, requires no student identity, and links only to an existing public source.
- All data is rendered using DOM-safe text nodes.

## Review Focus

1. Unknown exercise or choice must not invent an assessment; cover in Task 1.
2. Malformed/excessive private-looking kernel metadata must fail admission; cover in Task 1.
3. Every public subject and source must remain reachable without a loop or unanswered page; cover in Task 1 and Task 2.
4. Student markup and missing-input behavior must not become HTML or a submission; cover in Task 2.
5. Offline networking and protected route must remain unchanged; cover in Task 3.

---

### Task 1: Bank and bounded evaluator

**Files:** Create `natural-order/teaching-kernels.mjs`, `natural-order/tests/teaching-kernels.test.mjs`.

**Interfaces:** `TEACHING_KERNELS`, `auditTeachingKernelBank(entries)`, `kernelForTopic(topicId)`, `assessTeachingKernel(id,choiceId)`.

- [ ] Write failing tests: eleven known topic bindings, finite/admissible entries, exact source links, correct/wrong answer explanations, no mutation, refusal for unknown IDs.
- [ ] Run `node --test natural-order/tests/teaching-kernels.test.mjs` and observe expected failures.
- [ ] Implement pure bank and admissions/evaluator functions; inspect safety invariants for each entry.
- [ ] Run bank tests, then all Natural Order tests.
- [ ] Commit Task 1.

### Task 2: Integrated teaching experience

**Files:** Modify `natural-order/index.html`, `natural-order/app.mjs`, `natural-order/styles.css`, `natural-order/tests/app-interaction.test.mjs` and `natural-order/tests/pages.test.mjs`.

**Interfaces:** Read-only bank data/evaluator from Task 1. Existing `teach`, public source routing, private NDA path, and Frankie default-off remain intact.

- [ ] Add failing UI tests: topic exercise, choice feedback, next exercise, no silent submission or dynamic HTML, voluntary feedback.
- [ ] Verify RED against current DOM.
- [ ] Build an exercise panel that opens on demand, exposes accessible choice controls and next-kernel progression, and updates feedback through `textContent`.
- [ ] Run DOM/browser smoke tests and full suite.
- [ ] Commit Task 2.

### Task 3: Public release custody

**Files:** Modify `natural-order/release-audit.mjs`, `natural-order/README.md`, cache-bust references in `index.html`, `access.html`, `app.mjs`, `engine.mjs`, and affected release tests.

- [ ] Write failing release audit test for missing/unapproved bank asset and broken version references.
- [ ] Confirm RED.
- [ ] Update manifest and same-version imports, retain no-connect CSP and disabled Frankie boundary.
- [ ] Run `node --test natural-order/tests/*.test.mjs`, `node natural-order/release-audit.mjs`, `git diff --check`.
- [ ] Commit and prepare public branch for reviewed release; publish only after verification.
