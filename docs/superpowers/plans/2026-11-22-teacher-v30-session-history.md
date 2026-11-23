# Teacher V30 Session History Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore a recently visited public lesson without replaying the visitor's wording.

**Architecture:** Extend the existing temporary open-conversation state with up to three public lesson snapshots and a history-selection map. Add one public UI shortcut to ask for that map. Keep the access gate and source-bearing lesson results unchanged.

**Tech Stack:** Dependency-free browser ECMAScript modules, HTML and Node test runner.

**Spec:** `docs/superpowers/specs/2026-11-22-teacher-v30-session-history-design.md`

## Global Constraints

- No network, storage, credentials, private construction or Frankie runtime changes.
- Protected requests outrank all history commands. No unoffered choice succeeds.
- Do not turn the finite public tutor into a purported general reasoning engine.
- Preserve exact published public sources and field questions.

## Review Focus

- History with no previous lesson: patient map, no invented topic.
- More than three distinct lessons: oldest forgotten, latest three selectable.
- Repeated topic: one entry, most recently visited first.
- Private request during history selection: access response and history cleared.
- Invalid history choice: cannot disclose any different or unoffered lesson.

---

### Task 1: Conversation history

**Files:**
- Modify: `natural-order/open-conversation-kernel.mjs`
- Test: `natural-order/tests/open-conversation-kernel.test.mjs`

**Interfaces:**
- Add `history()` returning up to three `{id,title}` public descriptors.
- `ask('What have we covered?')` returns a map of cached topic IDs.
- `choose(topicId)` restores only an offered history lesson with its sources and original question.

- [ ] Write tests for history listing, choosing, restored follow-ups, eviction, resets, protected access and unoffered choice.
- [ ] Run focused tests and verify they fail for missing history.
- [ ] Implement minimal session-only state.
- [ ] Run focused tests and verify they pass.

### Task 2: Visitor shortcut and public release

**Files:**
- Modify: `natural-order/index.html`, `natural-order/app.mjs`, `natural-order/README.md` and cache-version import consumers.
- Test: `natural-order/tests/app-interaction.test.mjs` and relevant page/release tests.

**Interfaces:**
- `#history-button` invokes `interaction.ask('What have we covered?')` through the same renderer.
- Disabled when `interaction.history().length===0`.

- [ ] Write real UI-boundary test for button, history options, restored source and disabled state.
- [ ] Verify the new test fails.
- [ ] Add the button and handler without transmitting any text; bump public cache version to V30.
- [ ] Verify the focused and full test suites.
- [ ] Run `node natural-order/release-audit.mjs` and `git diff --check`.
- [ ] Review exact public tree and publish through the existing guarded GitHub release procedure only if all checks pass.
