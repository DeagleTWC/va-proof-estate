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

The public access page requests nonconfidential inquiries via an existing GitHub issues route. Terry has not yet supplied a general-public NDA or a designated email address for signed agreements; the app does not invent either. When both are approved, the correct NDA download and email handoff can be added following review. Existing signed bilateral NDAs must not be used as a public template.

## Preview locally

From the repository root: `python3 -m http.server 8765`, then visit `http://localhost:8765/natural-order/`.

## Tests and release audit

From the repository root:

```sh
node --test natural-order/tests/*.test.mjs
node natural-order/release-audit.mjs
```

Only `index.html`, `access.html`, `styles.css`, `app.mjs`, `engine.mjs`, `knowledge.mjs`, `release-audit.mjs`, and `README.md` need to ship. Test files are development records and not part of the deploy directory.

**Proof Before Power. Open Evidence. Protected Construction.**
