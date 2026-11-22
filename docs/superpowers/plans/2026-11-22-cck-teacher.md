# Conversation Compatibility Kernel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stop the public Teacher from substituting generic or unrelated replies for clear visitor intentions, using one bounded compatibility gate.

**Architecture:** A pure `reviewConversationCompatibility(question,candidate,{topics})` inspects a human-intent candidate and returns either that exact candidate or a public, source-bound answer for the three observed failures. `exerciseFitsConversation(result)` prevents a field-specific answer from displaying an unrelated generic lesson exercise. The existing cognitive-repair recognizer admits one natural disagreement variant, and the open-conversation kernel resets pending clarification when a compatible direct answer replaces it.

**Tech Stack:** Browser-native ES modules, Node.js built-in test runner, static GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-11-22-conversation-compatibility-kernel-design.md`

## Global Constraints

- No remote language model, analytics, user-text transmission, or persistent memory.
- All protected requests retain human review priority; no private source files enter the public release.
- Exact public evidence ceilings and existing eleven learning subjects remain unchanged.
- Version all live imports together, and admit new public files through the strict release audit.

## Review Focus

- A warehouse question that also asks for private kernel construction must stay in the protected route (Task 1).
- A question about a real emergency or specific machine must not receive operational safety certification (Task 1).
- A skeptical user asking about a named mathematical theorem must retain the named math evidence status, not be redirected to generic proof (Task 1).
- A correction containing a new substantive question must route that question and not be swallowed by warmth (Task 2).
- The visitor's first question remains intact after a compatible lesson and the next two follow-ups (Task 2).

---

### Task 1: Pure Compatibility Decision

**Files:**
- Create: `natural-order/conversation-compatibility-kernel.mjs`
- Create: `natural-order/tests/conversation-compatibility-kernel.test.mjs`
- Modify: `natural-order/release-audit.mjs`

**Interfaces:**
- Consumes: public `TOPICS`, existing `kind:'map'|'lesson'|'access'|'empty'` candidates.
- Produces: `reviewConversationCompatibility(question,candidate,{topics})` returning an unchanged candidate or a public `kind:'lesson'` with `originalQuestion`, `conversation`, sources from its topic, and `compatibility:{fieldBound:boolean}`; `exerciseFitsConversation(result)` returning a boolean.

- [ ] Write tests: `warehouse/pallet` with withdrawn approval gives `consequence` and a warehouse-specific no-certification answer; skepticism gives public proof status and sources; gravity-wave-array evidence gives an explicit not-independently-established statement; protected or named-math candidates never change; generic maps and lessons pass unchanged; field-bound exercises are rejected.
- [ ] Run `node --test natural-order/tests/conversation-compatibility-kernel.test.mjs` and observe RED for missing interface.
- [ ] Implement the smallest public compatibility kernel with no external APIs, preserving original input and the exact topics' source links.
- [ ] Add only its new module and test to `PUBLIC_FILES`; run targeted test and `node --test natural-order/tests/*.test.mjs` plus `node natural-order/release-audit.mjs` GREEN.
- [ ] Commit the pure kernel and tests.

### Task 2: Interaction, Repair and Presentation

**Files:**
- Modify: `natural-order/open-conversation-kernel.mjs`
- Modify: `natural-order/cognitive-reasoning-kernel.mjs`
- Modify: `natural-order/app.mjs`
- Modify: `natural-order/tests/open-conversation-kernel.test.mjs`
- Modify: `natural-order/tests/cognitive-reasoning-kernel.test.mjs`
- Modify: `natural-order/tests/app-interaction.test.mjs`
- Modify: `natural-order/tests/pages.test.mjs`
- Modify: `natural-order/README.md`
- Modify: versioned live imports in `natural-order/{access.html,index.html,engine.mjs,visitor-answer-desk.mjs,open-conversation-kernel.mjs,app.mjs}`.

**Interfaces:**
- Consumes: Task 1's `reviewConversationCompatibility` and `exerciseFitsConversation`.
- Produces: a source-bound compatible visible answer and preserved conversation context with unrelated exercises suppressed; human-sounding disagreement response.

- [ ] Write failing conversation tests for the four observed live inputs, safe follow-ups, pending-choice reset, serious/protected requests and an explicit replacement question. Write app integration test showing real answer text, source links and a hidden unrelated exercise.
- [ ] Run targeted tests; observe RED from the old routing/repair/presentation.
- [ ] Integrate the compatibility decision after human-intent routing and before recording a public answer; clear stale pending state when replaced. Expand narrowly the cognitive-repair phrase pattern. Suppress the unrelated field-bound exercise in the app, leaving the bank unchanged.
- [ ] Bump all shared runtime cache tokens from `20261122-natural-order-25` to `20261122-natural-order-26`; update graph assertions and document the bounded new kernel.
- [ ] Run full `node --test natural-order/tests/*.test.mjs`, `node natural-order/release-audit.mjs` and `git diff --check` GREEN.
- [ ] Commit the integration and tests.

### Task 3: Release Verification and Publication

**Files:** No extra product files required.

**Interfaces:** Consumes Tasks 1–2; publishes reviewed public files without altering unrelated research trees.

- [ ] Self-review the whole diff against the spec and five review-focus inputs; fix only observed Important/Critical findings by RED→GREEN tests.
- [ ] Run fresh complete tests and public audit; compare local public subtrees to remote main and preserve unrelated remote changes.
- [ ] Publish a non-force guarded fast-forward commit after approval already granted by Terry's explicit “make it happen” and prior publication request.
- [ ] Verify main SHA, public release checks and Pages deployment. Report exact outcome and limitations.
