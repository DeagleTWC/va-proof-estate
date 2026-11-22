# The Natural Order — public teaching edition

This is a **static, dependency-free, public-source teaching experience** for the [V.A. Proof Estate](https://deagletwc.github.io/va-proof-estate/). It is not the private *Stewards Edition* and does not ship its originals, index, local Python server, or private teaching corpus.

## What visitors can do

- Ask a question or choose one of eleven public subject routes.
- Bring an example from energy storage, health care, water engineering, transportation, automation, or finance; choose among bounded examination paths that keep the original question in view.
- Read an accurate, brief public explanation with an evidence-class label.
- Follow direct links to the published source material.
- Examine the relationship in both directions, then vary one test condition.
- Learn the human-mediated process for seeking protected examination under an appropriate NDA.

The routing logic is deterministic, not an LLM. It does not silently invent open-world answers or send the visitor's input to a remote service. No input is stored locally or transmitted by this public source finder.

## Frankie Cycle 081 — prepared optional companion

The reviewed public client contains an optional **Ask Frankie** panel and safe answer renderer, but the companion is **disabled in this public release** (`FRANKIE_GATEWAY_URL=''`). Its default-off state and exact client bytes are pinned in `release-audit.mjs`. There is no public gateway address, private bearer secret, or Frankie runtime in this repository.

When a separately hosted HTTPS teacher gateway is approved, visitors will explicitly open an **Ask Frankie** question form. Sending from that form is different from using the local teaching navigator: it sends only the visitor's chosen question and an opaque, pseudonymous student token. The teacher gateway fixes the public lesson identifier, communicates privately with Frankie Cycle 081's native loopback bridge, and returns only a bounded public lesson and receipt hash. Held or unavailable answers never replace source links.

**This is an integration staging milestone, not evidence that the public connection is live.** The operator still needs a separately hosted POSIX runtime, public HTTPS terminator and the real Cycle 081 end-to-end test before enabling it. The companion and the public teacher can then be upgraded in separate versioned cycles.

## Boundary and legal handoff

**All files inside this directory are public once pushed to GitHub.** `knowledge.mjs` contains only hand-curated public-facing summaries and links. There is no public import path to internal kernels or private data.

The public access page provides the approved, blank `VA_Universal_Bounded_Review_MNDA.pdf` and directs signed returns to `canarybird0618@gmail.com`. It is a reusable mutual review form, based on a newly generalized agreement rather than an existing signed bilateral NDA. The PDF alone grants no access to protected material: Terry must countersign and approve a specifically bounded Exhibit A. The PDF is pinned by SHA-256 in `release-audit.mjs` so an unexpected substitution fails the audit.

## Preview locally

From the repository root: `python3 -m http.server 8765`, then visit `http://localhost:8765/natural-order/`.

## Tests and release audit

From the repository root:

```sh
node --test natural-order/tests/*.test.mjs
node natural-order/release-audit.mjs
```

The teacher's runtime modules are `index.html`, `styles.css`, `app.mjs`, `engine.mjs`, `knowledge.mjs` and the gated `frankie-client.mjs`. The public PDF is a downloadable review template. `release-audit.mjs`, `README.md`, and the `tests/` directory are published transparency and review resources; GitHub Pages serves all tracked files, including tests, and none of them contains protected construction.

**Proof Before Power. Open Evidence. Protected Construction.**
