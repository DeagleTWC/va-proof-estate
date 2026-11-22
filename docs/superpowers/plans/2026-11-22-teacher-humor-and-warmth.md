# Teacher Humor and Warmth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans, with test-driven development.

**Goal:** Add gentle, opt-in situational humor to the Teacher's public conversational behavior without displacing evidence or privacy safeguards.

**Architecture:** The existing `createOpenConversationKernel` recognizes two bounded warmth modes after complete-message access review and cognitive repair, but before ordinary lesson follow-ups. The existing map and lesson UI components present the response. No new model or service is introduced.

**Tech Stack:** Browser JavaScript ES modules, Node.js native tests, public release audit.

**Spec:** `docs/superpowers/specs/2026-11-22-teacher-humor-and-warmth-design.md`

## Global Constraints

- Preserve full-message access checks, the cognitive repair path, and the eleven teaching subjects.
- Do not joke about harm, suffering, protected information, or an unverified scientific claim.
- A humorous line is not evidence; original topic and sources remain visible in a continued lesson.

## Review Focus

- Short humor request should work without prior lesson and not fabricate a subject.
- In-context confusion should preserve prior lesson and field question.
- A new question with "lol" must not be mistaken for a request to joke.
- Serious or private inquiries outrank humor.
- Explicitly rejecting jokes should not trigger one.

### Task 1: Behavior and tests

**Files:** Modify `natural-order/open-conversation-kernel.mjs`, `natural-order/tests/open-conversation-kernel.test.mjs`, `natural-order/README.md`.

**Interfaces:** Existing `ask`, `choose`, `startTopic`, `reset`, `state` remain unchanged. Humor returns `kind:'lesson'` with bounded `conversation` when a lesson exists, or `kind:'map'` with no predetermined topic otherwise.

- [ ] Write failing tests for requested humor, self-confusion continuity, serious context, and privacy priority.
- [ ] Observe red assertions against existing conversation behavior.
- [ ] Implement minimal guarded warmth routing.
- [ ] Verify targeted and full public suites green.
- [ ] Commit behavior, tests and documentation.

### Task 2: Release boundary

**Files:** Modify `natural-order/app.mjs`, `natural-order/index.html`, `natural-order/access.html`, `natural-order/engine.mjs`, `natural-order/open-conversation-kernel.mjs`, and `natural-order/tests/pages.test.mjs` only as required for cache-coherent release URLs.

- [ ] Verify module-cache consistency with existing test.
- [ ] Run all public tests, release audit, and diff check.
- [ ] Confirm disabled Frankie gateway remains byte-pinned.
- [ ] Commit verified release changes.
