# Cognitive Reasoning Kernel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task, using test-driven development.

**Goal:** Add a public-safe, bounded reasoning check and a humble repair path to the existing Teacher conversation.

**Architecture:** A new focused module checks each admitted turn against correction and certainty boundaries. The open-conversation coordinator invokes it after the access check, retains conversation context where appropriate, and presents repair through the existing clarification panel.

**Tech Stack:** Browser-native JavaScript modules, Node.js built-in test runner, existing release audit.

**Spec:** `docs/superpowers/specs/2026-11-22-cognitive-reasoning-kernel-design.md`

## Global Constraints

- No network, persistence, protected material, or automatic Frankie access.
- No invention of certainty or proof from an apparent reversed interpretation.
- An explicit visitor correction outranks a prior lesson; a new question outranks correction-only handling.

## Review Focus

- Corrective language embedded in a genuine new question should not be swallowed.
- Broad words such as "wrong" should not misclassify a diagnostic inquiry.
- Protected correction-shaped requests must fail closed.
- Repaired conversations must clear old lesson state before the next inquiry.
- A prior field example should preserve its actual visitor wording.

### Task 1: Review kernel

**Files:** Create `natural-order/cognitive-reasoning-kernel.mjs`, `natural-order/tests/cognitive-reasoning-kernel.test.mjs`.

**Interfaces:** `reviewCognitiveTurn(question, {admission, priorQuestion})` returns `mode: 'continue' | 'clarify' | 'repair' | 'protected'` and a `response` for repair.

- [ ] Write test cases for a correction-only turn, genuine question, inferred lesson, and protected request.
- [ ] Run targeted tests; verify failure due to missing module.
- [ ] Implement bounded pure review function and patient repair copy.
- [ ] Run targeted tests; verify green.

### Task 2: Conversation integration

**Files:** Modify `natural-order/open-conversation-kernel.mjs`, `natural-order/tests/open-conversation-kernel.test.mjs`, `natural-order/README.md`.

**Interfaces:** The existing `ask`, `choose`, `startTopic`, `reset`, `state` API remains unchanged. Repair displays `kind:'map'` with original visitor question and no predetermined options.

- [ ] Write integration tests for correction, reset, explicit replacement, and access precedence.
- [ ] Verify tests fail before routing change.
- [ ] Wire the review after access admission and before follow-up interpretation; reset stale intent when repairing.
- [ ] Run targeted tests; verify green.

### Task 3: Public release checks

**Files:** Update import version only if needed for cache coherence; no private gateway changes.

- [ ] Run `node --test natural-order/tests/*.test.mjs`.
- [ ] Run `node natural-order/release-audit.mjs` and `git diff --check`.
- [ ] Inspect changes for unsafe content; commit the bounded change.
