# The Natural Order — public teaching edition

This is a **static, dependency-free, public-source teaching experience** for the [V.A. Proof Estate](https://deagletwc.github.io/va-proof-estate/). It is not the private *Stewards Edition* and does not ship its originals, index, local Python server, or private teaching corpus.

## What visitors can do

- Ask a question or choose one of ten public subject routes.
- Read an accurate, brief public explanation with an evidence-class label.
- Follow direct links to the published source material.
- Examine the relationship in both directions, then vary one test condition.
- Learn the human-mediated process for seeking protected examination under an appropriate NDA.

The routing logic is deterministic, not an LLM. It does not silently invent open-world answers or send the visitor's input to a remote service. No input is stored locally or transmitted by this tool.

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

Only `index.html`, `access.html`, `styles.css`, `app.mjs`, `engine.mjs`, and `knowledge.mjs` are used by the teacher at runtime. The public PDF is a downloadable review template. `release-audit.mjs`, `README.md`, and the `tests/` directory are published transparency and review resources; GitHub Pages serves all tracked files, including tests, and none of them contains protected construction.

**Proof Before Power. Open Evidence. Protected Construction.**
