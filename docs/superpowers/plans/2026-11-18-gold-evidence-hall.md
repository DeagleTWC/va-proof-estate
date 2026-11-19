# V.A. Gold Evidence Hall Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a professional five-exhibit, source-bound, self-contained gold V.A. Evidence Hall to Deagle.

**Architecture:** Publish a static HTML page and focused CSS, backed by an inspectable JSON exhibit register. Reuse existing local original V.A. PDF carriers and the bounded VA-AD-001 synthetic fixture. Add minimally invasive homepage navigation; stage and verify changes on an isolated GitHub branch.

**Tech Stack:** Static HTML/CSS, JSON, Python 3 stdlib tests; GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-11-18-gold-evidence-hall-design.md`

## Global Constraints

- Official V.A. gold mark only; no invented branding.
- No Kamanaka outbound links in the new page; no protected KCD, substrate, or private kernels.
- Never imply that documentary DECLARED claims, local synthetic OBSERVED mock effects, and independent native reproduction are equivalent.
- Preserve current source hashes and historical records unchanged.

## Review Focus

1. User opens Hall without JavaScript: all five exhibits and evidence links must remain readable.
2. Narrow mobile screen: source text and metadata must wrap; no horizontal page overflow.
3. Missing or malformed evidence class: validator rejects unsupported promotion rather than silently displaying independent status.
4. A reviewer follows a local artifact link: its target must be a known repository path and never an external dependency.
5. A visitor interprets fixture results: the Hall must state that VA-AD-001 is an in-process mock, not native V.A. operation or an independent test.

---

### Task 1: Evidence register and integrity validator

**Files:** Create `proofs/EVIDENCE-HALL-REGISTER.json`; create `scripts/test_evidence_hall.py`.

**Interfaces:** Validator `validate_hall(repo_root: pathlib.Path) -> list[str]`; CLI exits nonzero if errors. Register contains five exhibit objects with `id`, `title`, `standing`, `scope`, `sources` (local `path` and `role`), `native_run_attached` false.

- [ ] Write test-first validator assertions for exact five exhibits, allowed status classes, restricted Kamanaka links, real local source paths, and bounded fixture label.
- [ ] Run red test against missing register.
- [ ] Create JSON register based on existing public documentation and existing local fixture; no third-party source code.
- [ ] Run green test, verify JSON and correct classification.

### Task 2: Five-exhibit gold page

**Files:** Create `evidence-hall.html`; create `evidence-hall.css`; extend validator tests.

**Interfaces:** All five exhibit IDs appear as native HTML `section` IDs; each section contains declared status and a local carrier reference; locally linked `va-gold-design.css` shared with site.

- [ ] Write failing tests for five visible HTML sections, every local carrier, official V.A. sigil, zero Kamanaka links, accessibility labels, and no native-run promotion.
- [ ] Run red test against missing page.
- [ ] Implement accessible static HTML and responsive CSS using the site's exact gold palette and existing logo geometry.
- [ ] Run green tests, visually inspect desktop/mobile if rendering is available.

### Task 3: Homepage integration and release

**Files:** Modify `index.html` minimally; publish the register, validator, page and CSS through a branch/PR.

**Interfaces:** Add one `evidence-hall.html` link to top navigation and a hero CTA; preserve every existing feature and link.

- [ ] Add failing homepage navigation assertions; verify expected red.
- [ ] Add link in existing navigation and hero CTA.
- [ ] Run green suite, validate links, compare remote branch file versions, and check full diff.
- [ ] Open PR, verify branch build/CI and merge only when verification allows.

