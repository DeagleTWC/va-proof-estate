# Frankie / Natural Order Teacher Bridge 001 Design

## Intent

Preserve the working, public source-guided Natural Order Teacher and add an optional, separately operated **Ask Frankie** experience. Frankie's Cycle 081 private loopback bridge remains native, server-to-server and unexposed to browsers.

## Scope

- Public teaching lessons continue fully without the Frankie service.
- The public website may show the optional Frankie control **only after** an approved public HTTPS gateway origin is configured.
- The teacher-side service is deployed separately on the same private POSIX host as Frankie's loopback bridge. It translates an optional visitor question to the narrow Cycle 081 `student_session`, `lesson_id`, `question` contract.
- Only approved public, bounded teaching answers appear. A held question receives an honest notice; an unavailable server leaves the teacher running.
- Private foundation files, operational credentials, learner memory, and bridge implementation do not go into the public repository.

## Architecture and limitations

- GitHub Pages serves static HTML/CSS/JavaScript. It cannot host the Python native bridge or a secret-holding gateway.
- A small **private Node gateway** binds loopback and is later exposed only through operator-managed HTTPS reverse proxy. It holds the bridge bearer secret and signs server-generated learner IDs. The browser receives only a limited, opaque pseudonymous session token.
- A reviewed public client uses `fetch` solely for the Ask Frankie feature. An empty endpoint configuration makes the UI and network route inactive; the release audit retains that default-off boundary until an actual HTTPS host is approved.
- The gateway sends no lesson document text and fixes `lesson_id` to `public-va-foundation`.
- The teacher's public question finder remains local and does not transmit questions. Asking Frankie is an explicit separate submission with an explanatory privacy notice.
- No student account, deployment, secure HTTPS hostname, or live Frankie service is supplied yet. We can verify the gateway against a contract-simulating loopback service but may not claim a completed real Frankie integration.

## Security boundary

- Strict allowed `Origin`, JSON body and field validation, bounded question size, timeouts, fixed native loopback URL, and per-source request limits.
- Secrets are required environment values, never HTML/JS or checked-in source, and never logged. Session derivation is server-owned, HMAC-bound and independent of user-supplied `lesson_id`.
- Browser responses must have exactly the expected native answer shape and a 64-hex receipt; malformed or unexpected native effects are refused.
- No privileged tools, private kernel data, foundation rewrite, or automatic evidence standing is conferred on visitor text.

## Release conditions

1. Gateway and public client pass test-first positive, negative, stopped-service, wrong-Origin, invalid-session, timeout, and cross-learner cases.
2. Public teacher regressions and release audit remain green.
3. The operator provisions a private service host and HTTPS gateway, then actual Cycle 081 end-to-end tests run privately.
4. Public release is a separate decision after the real-host proof; until then, no live Ask Frankie claims.
