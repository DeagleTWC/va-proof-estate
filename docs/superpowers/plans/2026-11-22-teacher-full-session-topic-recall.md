# Teacher V31 Full Session Topic Recall Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep every distinct cited public lesson from the current Teacher visit available for explicit topic recall.

**Architecture:** Extend the existing bounded, in-memory open-conversation layer by removing its numerical history truncation while retaining de-duplication and public access checks. The existing visible menu uses `history()` to render topics; add a regression test for more than three selections and update documentation/cache version.

**Tech Stack:** Static ES modules, Node.js built-in test runner, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-11-22-teacher-full-session-topic-recall-design.md`

## Global Constraints

- Public source-bound lessons only; no protected knowledge or native Frankie integration.
- In-page memory only; never persist or transmit visitor questions.
- Preserve original cited lesson and question, newest-first topic order, and existing public access/reset boundaries.

## Review Focus

1. Fourth/fifth distinct lesson: both remain offered after review (Task 1 test).
2. Duplicate topic after revisit: only one entry and it becomes newest (Task 1 test).
3. Oldest lesson selection: exact earlier question and sources survive (Task 1 test).
4. Protected question: full history clears (existing protected/reset test, Task 1 suite).
5. Visible menu: maps all public history choices without conflating profiles or general clarifications (Task 2 test).

---

### Task 1: Remove the History Truncation

**Files:**
- Modify: `natural-order/tests/open-conversation-kernel.test.mjs`
- Modify: `natural-order/open-conversation-kernel.mjs`

**Interfaces:**
- Consumes: `createOpenConversationKernel({resolve,topics})` with `history()`, `ask()` and `choose()`.
- Produces: history of all distinct public cited topics, most recent first.

- [ ] **Step 1: Write the failing test** for at least five distinct public topics, checking an earliest topic remains in `history()` and the history menu, source preservation after `choose()`, and deduplication after revisit. Replace the old three-topic eviction expectation.
- [ ] **Step 2: Run** `node --test natural-order/tests/open-conversation-kernel.test.mjs`. **Expected:** new recall test FAIL from the three-topic cap.
- [ ] **Step 3: Remove only the numerical `.slice(0,3)` truncation** in `record()`; preserve all filtering, access and reset checks.
- [ ] **Step 4: Run** `node --test natural-order/tests/open-conversation-kernel.test.mjs`. **Expected:** all PASS.
- [ ] **Step 5: Run** `node --test natural-order/tests/*.test.mjs`. **Expected:** all PASS.
- [ ] **Step 6: Commit** the kernel and its tests.

### Task 2: Public UI and Release Documentation

**Files:**
- Modify: `natural-order/tests/app-interaction.test.mjs`
- Modify: `natural-order/README.md`
- Modify: `natural-order/index.html`, `natural-order/app.mjs`, `natural-order/open-conversation-kernel.mjs`, `natural-order/engine.mjs`, `natural-order/visitor-answer-desk.mjs`, `natural-order/access.html` (cache version)

**Interfaces:**
- Consumes: unlimited `history()` from Task 1.
- Produces: the existing “Review earlier topics” menu offering every public recalled subject.

- [ ] **Step 1: Add UI integration assertions** for a fourth historical public topic and returning to the earliest cited lesson.
- [ ] **Step 2: Run** `node --test natural-order/tests/app-interaction.test.mjs`. **Expected:** new assertions exercise full history; fail against a three-topic kernel (already proven RED in Task 1).
- [ ] **Step 3: Update** README from “three” to “every distinct public subject in this visit” and bump the public asset version to `20261122-natural-order-31` consistently.
- [ ] **Step 4: Run** the complete test suite, `node natural-order/release-audit.mjs`, and `git diff --check`. **Expected:** 0 failures, audit passed, clean diff.
- [ ] **Step 5: Commit** UI regression, public documentation and cache references.

After local verification and guarded GitHub publication, confirm both the public checks and Pages deployment succeed, then smoke-test the history menu on the live Teacher.
