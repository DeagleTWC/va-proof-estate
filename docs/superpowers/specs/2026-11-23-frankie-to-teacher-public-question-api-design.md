# Frankie → Teacher Public Question API

## Purpose

Frankie needs a live way to ask the Natural Order Teacher questions without a human at the keyboard. The Teacher is currently a static source-linked site with a deterministic public interaction kernel; it does not host an HTTP API. Build a separate, read-only API adapter over that same public code. Frankie remains a separate system and keeps custody of her own reasoning, private documents and actions.

## Hosting decision

The chosen first deployment architecture is **a loopback-only HTTP service on the same host as Frankie**, using `127.0.0.1` and a distinct local port. This reuses existing infrastructure, needs no new public port, cloud account or paid service, and keeps Teacher's web site independent. This turn builds and locally verifies the distributable code; installing it on Frankie's private host and wiring her own runtime require a separately verified host-side handoff. No public HTTPS endpoint is asserted to exist until such deployment.

Other routes considered: an additional public serverless API (new hosting, authentication and billing decisions), or a fixed static JSON answer catalog on Pages (not a live conversational API). The local service preserves session continuity without those tradeoffs.

## Contract

- Node.js 24, built-in modules only. Standalone `teacher-question-api` directory in the public Proof Estate repository; no dependency on private Frankie files or secrets.
- Bind only `127.0.0.1`. Refuse browser Origins, unexpected Host headers, non-JSON/malformed input, oversized input, and unknown routes. Never enable CORS. No logs of questions or answers.
- `POST /v1/teacher/session` creates a random opaque, memory-only session ID.
- `POST /v1/teacher/ask` accepts `{session_id, question}` and returns a public lesson, gentle clarification/options, or a protected refusal. Questions are at most 300 plain-text characters.
- `POST /v1/teacher/choose` accepts `{session_id, topic_id}` and selects only the active public options. It must not bypass the protected-access boundary.
- `POST /v1/teacher/close` deletes a session. Sessions expire after one hour and the in-memory table is capped at 64 sessions.
- Every answered lesson includes the actual publicly sourced explanation, the evidence class as labeled in the public record, validated public URLs, and the next learning question. No claimed general certainty, unsupported source, private construction or network lookup.
- The Teacher's existing `createOpenConversationKernel` provides in-session follow-ups and topic history; protected inquiries clear that history.
- The source references are constrained by the existing `publicHref` rule. The API never executes instructions contained in a question.

## Out of scope

- No changes to Frankie’s assembly, cloud server, files, email, storage scanning or learning scheduler.
- No new public endpoint on GitHub Pages. Do not repurpose the disabled Teacher→Frankie browser gateway.
- No generative model, external search, private knowledge access or physical/mathematical certification.

## Acceptance

Local HTTP tests demonstrate answers with real public references; contextual follow-up; option selection; refusal and history clear on protected requests; invalid session/body/Host/Origin rejection; session closing/expiry; loopback binding. The full public Teacher tests and release audit remain green. Publication of source code must not be described as deployment to Frankie's private host.
