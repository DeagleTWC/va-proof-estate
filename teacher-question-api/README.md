# Frankie → Teacher: Local Public Question API

This optional Node 24 service exposes the **existing deterministic public Natural Order Teacher** to a separate, private Frankie process. It does not contain or modify Frankie's assembly, private archives, learning scheduler, files or credentials. It requires no npm dependencies.

## Scope

- The API serves only public Teacher explanations, cited public sources, plain-language follow-ups and patient clarification options.
- It has no external network lookup, no generative model, no public listening port, no browser CORS, and no disk/session database.
- It binds to `127.0.0.1` on the same host as the calling Frankie service. The default port is `8766`, independent of Frankie's existing services. Set `TEACHER_QUESTION_PORT` to another unoccupied high port if required.
- Each 64-character random session ID lives in memory for up to an hour after its latest use; at most 64 sessions are retained. The service does not write visitor questions or answers to logs.
- A protected question is refused and clears its Teacher-session topic history. An indexed public claim is not upgraded into independently established proof merely because it is linked.

## Local test

From the repository root:

```sh
node --test teacher-question-api/tests/*.test.mjs
node --test natural-order/tests/*.test.mjs
node natural-order/release-audit.mjs
```

## Local launch

From the repository root on the same machine as Frankie:

```sh
node teacher-question-api/cli.mjs
```

Do not reverse-proxy or firewall-forward port `8766` to the public internet. Check the actual machine and Frankie process before any installation; publishing this source on GitHub does not start it on a cloud server.

## Frankie-side HTTP contract

All routes require `POST`, `Content-Type: application/json`, no browser `Origin`, and `Host: 127.0.0.1:<port>`. No cookies, user passwords or private content are required.

1. `POST http://127.0.0.1:8766/v1/teacher/session` with `{}` returns `201 {"session_id":"<64 hex digits>"}`.
2. `POST .../v1/teacher/ask` with `{"session_id":"...","question":"Where is the proof?"}` returns `200` with `{status:"answered",reply,topic,evidence_class,sources,next_question}`. Frankie can cite the returned `sources` URLs, but should preserve the evidence class.
3. A question requiring clarification returns `200` with `{status:"clarify",reply,options:[{id,title}]}`. If the user clarifies by choosing a listed topic, `POST .../v1/teacher/choose` with `{"session_id":"...","topic_id":"basin"}` resumes the lesson; an unoffered ID does not bypass routing.
4. Protected material returns `403 {"status":"protected", "reply":"...", "sources":[]}`. This is not a signal to retrieve private files elsewhere.
5. `POST .../v1/teacher/close` with `{"session_id":"..."}` returns `204` and deletes the session.

Questions must be nonempty, trimmed plain text of no more than 300 characters with no control characters. Unexpected fields, malformed JSON and large bodies are refused. Expired/invalid sessions return `401` and must be freshly created. API failures must not block Frankie's own local conversational path.

## Handoff boundary

The public code and its local tests may be reviewed or released independently. **The API is not installed on Frankie's host yet.** The Frankie builder must verify the exact host, runtime and call path before adding a loopback-only integration. Do not change the existing disabled browser-to-Frankie gateway (`natural-order/frankie-client.mjs`), open a public port or claim remote connectivity without an actual host-side end-to-end test.
