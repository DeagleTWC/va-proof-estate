# Human Interaction Kernel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the public Natural Order Teacher patient, intent-respecting clarification before uncertain lesson selection.

**Architecture:** A pure, browser-local stateful `createHumanInteractionKernel` wraps existing `teach()` without replacing its protection checks. The browser UI renders clarification in the existing learning stage, then returns to the documented lesson after a visitor's choice or clearer question.

**Tech Stack:** Browser ES modules, Node built-in tests, existing public release audit.

**Spec:** `docs/superpowers/specs/2026-11-22-human-interaction-kernel-design.md`

## Global Constraints

- No LLM, storage, network, private-source release, or fabricated claims.
- Preserve existing public routes, field bridges, and reviewed protected navigation.
- Eleven teaching subjects and definition conversion stay intact.

## Review Focus

- A vague single-keyword question should not be silently assigned to its highest-scoring subject.
- A direct public subject request should work without a needless follow-up.
- A private request should reach human NDA review even after ambiguous dialogue.
- An unexpected selected topic should not bypass the unresolved question.
- A follow-up and a changed textarea should not overwrite the original question attached to a chosen field lesson.

---

### Task 1: Deterministic interaction state and test coverage

**Files:** Create `natural-order/human-interaction-kernel.mjs`; create `natural-order/tests/human-interaction-kernel.test.mjs`; modify `natural-order/engine.mjs` only to identify inferred keyword results.

**Interfaces:** `createHumanInteractionKernel({resolve,topics})` returns `{ask(question), choose(topicId), reset()}`. `ask()` and `choose()` return existing `lesson`/`access`/`empty` results or a `map` with a patient `introduction` and optional `options`.

- [ ] Step 1: Add tests for explicit route, ambiguity, inferred route, original question preservation, follow-up, privacy refusal, invalid choice, and reset.
- [ ] Step 2: Run `node --test natural-order/tests/human-interaction-kernel.test.mjs` and observe expected RED.
- [ ] Step 3: Implement minimal browser-local interaction module and `selection:'inferred'` metadata on the score-only router return.
- [ ] Step 4: Re-run focused test, then full suite, confirm GREEN.
- [ ] Step 5: Commit Task 1.

### Task 2: Wire the interaction kernel into the public Teacher

**Files:** Modify `natural-order/app.mjs`, `natural-order/index.html`, `natural-order/access.html`, `natural-order/release-audit.mjs`, and `natural-order/tests/app-interaction.test.mjs`; bump release URLs together.

**Interfaces:** `app.mjs` calls `interaction.ask()` for text and `interaction.choose()` for offered options; direct topic navigation resets any pending interaction.

- [ ] Step 1: Write a UI test for patient clarification with original question, selecting offered option, and protected request during clarification.
- [ ] Step 2: Run focused UI test and observe expected RED.
- [ ] Step 3: Wire module, accessible clarification copy, source-safe rendering, manifest, and versioned URLs.
- [ ] Step 4: Run `node --test natural-order/tests/*.test.mjs` and `node natural-order/release-audit.mjs`; confirm GREEN.
- [ ] Step 5: Commit Task 2; review full branch before any publication.
