# Frankie to Teacher Public Question API Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Provide a loopback-only, session-aware, public-read-only HTTP API so Frankie's builder can connect to the Teacher's existing knowledge and interaction kernel.

**Architecture:** Adapt actual `teach` and `createOpenConversationKernel` outputs into an explicitly small JSON response shape, then expose those via a separate Node HTTP service. All URL validation uses the existing `publicHref` rule. Native Frankie is not included or modified.

**Tech Stack:** Node 24 ESM, `node:http`, `node:crypto`, built-in `node:test`, public Teacher ES modules.

**Spec:** `docs/superpowers/specs/2026-11-23-frankie-to-teacher-public-question-api-design.md`

## Global Constraints

- Only already-cleared public Teacher data. No private Frankie documents, secrets, or automatic web retrieval.
- Service binds to `127.0.0.1` only; no public listening port, CORS or external account.
- Session IDs are random and memory-only; 1-hour expiry, 64-session cap, no persistence or user-question logging.
- Protected inquiries return a refusal without evidence/source leakage and clear existing history.
- Never claim live cloud deployment until separately verified on the actual host.

## Review Focus

1. Protected payload buried inside public-looking text must be refused (Task 1 test).
2. `Why?` in the same session must retain the correct previous public lesson and links (Task 1 test).
3. Unoffered topic IDs must not open another lesson (Task 1 test).
4. Forged session, browser Origin and nonlocal Host must be rejected at the HTTP boundary (Task 2 test).
5. Malformed/large JSON, expired session and table cap must fail closed without logging or forwarding (Task 2 test).

---

### Task 1: Public Response Adapter

**Files:** Create `teacher-question-api/teacher.mjs`; test `teacher-question-api/tests/teacher.test.mjs`.

**Interfaces:** `createTeacherSession()` returns `{ask(question), choose(topicId), history()}`; responses are `{status, reply, topic?, evidence_class?, next_question?, sources?, options?}` with `status` one of `answered`, `clarify`, `protected`.

- [ ] Write tests first for public proof lesson, actual source URLs, short follow-up, clarification, protected request and unoffered choice.
- [ ] Run `node --test teacher-question-api/tests/teacher.test.mjs`; expect missing module failure.
- [ ] Implement the adapter using the existing Teacher engine, no mock knowledge or invented text.
- [ ] Run its tests; expect all green.
- [ ] Commit adapter and tests.

### Task 2: Loopback HTTP Interface and Handoff

**Files:** Create `teacher-question-api/server.mjs`, `teacher-question-api/cli.mjs`, `teacher-question-api/tests/server.test.mjs`, `teacher-question-api/README.md`.

**Interfaces:** `createTeacherApi({now,ttlMs,maxSessions})` returns an unstarted HTTP Server. CLI starts on `127.0.0.1` using `TEACHER_QUESTION_PORT` (default 8766). Endpoints exactly as spec.

- [ ] Write real HTTP tests for session/ask/choose/close, body/Host/Origin violations, expiry and bounded session capacity.
- [ ] Run `node --test teacher-question-api/tests/server.test.mjs`; observe RED for missing implementation.
- [ ] Implement strict JSON parsing, in-memory sessions, loopback requirement and response mapping; CLI separate from library import.
- [ ] Run HTTP tests and all adapter tests; expect green.
- [ ] Write the operator README with example Frankie-side calls, no private credentials or unsafe commands.
- [ ] Run `node --test teacher-question-api/tests/*.test.mjs`, `node --test natural-order/tests/*.test.mjs`, `node natural-order/release-audit.mjs`, `git diff --check`.
- [ ] Commit code, tests and public-safe docs. Self-review security and publication scope.

After committed source has passed audit, publish only through a guarded GitHub update if the public branch still matches its verified baseline. Do not deploy to Frankie’s machine without the host handoff.
