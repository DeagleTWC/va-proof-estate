# Visitor Evidence and Mathematics Answers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans, with test-driven development.

**Goal:** Give the Teacher direct, source-linked public answers for compliance versus custody, independent proof and pilot evidence, and indexed or unindexed mathematical questions.

**Architecture:** A finite public answer desk returns existing `kind:'lesson'` results with per-answer summary and source overrides. The existing intent, access and conversation layers retain control. The UI adds a voluntary mathematics inquiry email link shown only on mathematics answers.

**Tech Stack:** Static browser ES modules, Node built-in test runner, GitHub Pages, release audit.

**Spec:** `docs/superpowers/specs/2026-11-22-visitor-evidence-and-math-design.md`

## Global Constraints

- Protected access always precedes public answer lookup.
- Exactly eleven teaching kernels remain; named answer desks are not native V.A. kernels.
- Source links are public local paths and have independent evidence ceilings.
- No automatic email/network transmission of visitor questions.

## Review Focus

- Private requests with a public math name do not bypass protected access.
- A named open problem is not promoted to a solved theorem.
- Proof links are genuine routes but are not mislabeled as independent physical proof.
- A vague word like "proof" in an unrelated question does not hijack the lesson.
- A learner's question never leaves the page without a deliberate email action.

### Task 1: Public answer desk content

**Files:** Create `natural-order/visitor-answer-desk.mjs`, `natural-order/tests/visitor-answer-desk.test.mjs`.

**Interfaces:** `publicVisitorAnswer(question)` returns a public `kind:'lesson'` with `topic`, `conversation`, `sources`, `originalQuestion` or `null` for non-matches. The returned `topic` has the existing public topic fields.

- [ ] Write failing tests for compliance/custody, proof evidence, pilot path, named mathematics and unknown mathematics.
- [ ] Confirm missing-module failure.
- [ ] Implement finite answers with real source paths, status ceilings, and simple language.
- [ ] Verify targeted tests green.
- [ ] Commit answer desk and tests.

### Task 2: Router integration and access precedence

**Files:** Modify `natural-order/engine.mjs`, `natural-order/tests/engine.test.mjs`, `natural-order/tests/open-conversation-kernel.test.mjs`.

- [ ] Write failing integrated tests for the three LinkedIn examples and protected-shaped inquiries.
- [ ] Confirm RED; route answer-desk results only after protected access checks.
- [ ] Preserve old topic routes and user intention; verify targeted tests green.
- [ ] Commit integration and tests.

### Task 3: Source and inquiry presentation

**Files:** Modify `natural-order/app.mjs`, `natural-order/index.html`, `natural-order/tests/pages.test.mjs`, `natural-order/README.md`.

- [ ] Add failing DOM test for per-answer sources and the mathematics inquiry link, including hidden state on other lessons.
- [ ] Confirm RED, then render response-specific sources and opt-in mail draft, escaping the visitor question.
- [ ] Verify UI and integration tests green; commit.

### Task 4: Public release safety

**Files:** Modify `natural-order/release-audit.mjs`, cache-version imports/links, affected tests.

- [ ] Add new public files to the strict manifest; bump entry/import versions together.
- [ ] Run `node --test natural-order/tests/*.test.mjs`, `node natural-order/release-audit.mjs`, `git diff --check`.
- [ ] Confirm Frankie remains pinned off and no network is added; commit.
