# Frankie Teacher Bridge 001 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare the Natural Order Teacher for optional Frankie Cycle 081 teaching, with a private server gateway and no public deployment until hosting is verified.

**Architecture:** Public UI is configured off by default. A separately packaged private gateway translates student requests into the fixed local Cycle 081 server contract. Both components are tested with an isolated local contract stub.

**Tech Stack:** Existing static HTML/CSS and Node ESM browser code; standalone Node 24 HTTP/crypto, built-in `node:test`.

**Spec:** `docs/superpowers/specs/2026-11-22-frankie-teacher-bridge-design.md`

## Global Constraints

- Never put a secret, private assembly, or operating endpoint into public GitHub Pages files.
- The public teacher and its 11-topic source map keep working with Frankie absent.
- No unverified public integration claim; private hosted service is not available yet.
- Cycle 081 accepts only `student_session`, `lesson_id`, `question`; `lesson_id` is server-fixed as `public-va-foundation`.
- Public release audit must enforce a disabled configuration until a separately authorized HTTPS host is ready.

## Review Focus

- Malformed native responses must not become trusted lessons: gateway test for incorrect `act` and receipt.
- A browser-origin or session mismatch must be refused: gateway test for wrong Origin and tampered token.
- Outage and slow native responses must not affect local lessons: gateway/client tests for 503/timeout and fallback.
- User text must never become HTML: client test checks `textContent` instead of `innerHTML`.
- The staged public code must not create a live remote request by default: release audit and source test.

---

### Task 1: Private teacher-side gateway

**Files:** Private scratch `teacher-gateway/server.mjs`; `teacher-gateway/test/server.test.mjs`; private README.

**Interfaces:** `createGateway({bridgeUrl, bridgeSecret, sessionSecret, allowedOrigin, fetchImpl, clock})` returns an HTTP server; POST `/api/teacher/session` generates a signed opaque token, POST `/api/teacher/ask` verifies token and forwards the narrow native request.

- [ ] Write tests for session issuance, authenticated happy path, wrong Origin, bad question, tampered session, native refusal/rollback, malformed reply, and timeout.
- [ ] Run tests and observe expected missing-implementation failures.
- [ ] Implement minimal gateway with fixed server-owned IDs, strict CORS, no secret exposure, request limits and failure mapping.
- [ ] Run all gateway tests; confirm no external outbound call except native loopback.
- [ ] Package privately; preserve any existing Drive artifacts.

### Task 2: Optional public client and teaching interface

**Files:** `natural-order/frankie-client.mjs`; `natural-order/tests/frankie-client.test.mjs`; modify `natural-order/app.mjs`, `index.html`, `styles.css`, `release-audit.mjs`, affected release tests.

**Interfaces:** `initFrankie({gatewayUrl, fetchImpl, sessionStore, elements})` leaves UI absent when URL empty; when enabled, opens a separate consent-aware question form and calls the private HTTPS gateway (never native loopback).

- [ ] Write client tests for disabled state, optional student request, safe text rendering, rejected/failed requests, and retention of the normal lesson.
- [ ] Run tests and observe missing-implementation failures.
- [ ] Implement client and UI markup, minimal styling and a default-disabled gateway URL.
- [ ] Update audit to admit exactly the scoped client request code while pinning the empty endpoint configuration.
- [ ] Run the full public tests and release audit.

### Task 3: Integration record and verification

**Files:** `natural-order/README.md`, private gateway README and test fixtures.

- [ ] Run gateway-to-stub request and browser-client tests, noting that these do not prove real native Cycle 081 runtime connectivity.
- [ ] Run `node --test natural-order/tests/*.test.mjs` and `node natural-order/release-audit.mjs`.
- [ ] Run `git diff --check` and review public files for secrets/private paths.
- [ ] Keep the HTTPS deployment and button enablement pending an actual host and user authorization.
