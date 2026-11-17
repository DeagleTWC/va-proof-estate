# AAR-facing public examination | Bounded synthetic seam

**Run:** `AAR-FACING-2026-11-17-SYN-001`  
**Date:** 17 November 2026  
**Evidence class:** LOCALLY OBSERVED SYNTHETIC FIXTURE; SCRIPT-VERIFIED ARCHIVE  
**Page:** `index.html` (English / Brazilian Portuguese)  
**Owners:** AAR — independent work of Adriana da Rocha; V.A. — independent computational foundation of Terry Snyder.

## 01 / Exact claim

A new, **independently authored public synthetic examiner** illustrates an admissibility corridor under an *illustrative rule invented for this examiner* (`EXAMINER-ILLUSTRATIVE-001/1.0`). In one in-process mock effect state, 20 specified case attempts produce their expected formal decisions and *observed local mock state* changes; 18 sequenced receipts have recomputable hashes and a linked chain; three permitted mock effects form exactly once; a retry duplicates no mock effect; synthetic refusal and injected-failure cases change no protected mock effect.

**This proves only the behavior of `examiner.py` on its declared local route.** It does not prove that Adria's protected AAR implementation ran, that the V.A. native True Zero/NEW K engine ran, that an external authorization or financial transfer was controlled, or that alternate routes in a real OS were closed. Independent third-party attestation has **not** been received for this new fixture.

## 02 / Public provenance and rights

- AAR — **Automatic Alignment Regulation** is an independent normative governance method and brand of **Adriana da Rocha**. Its own [official public overview](https://aarframework.github.io/aarframework/) describes institutionally accountable authority, admissibility and governance. All AAR proprietary implementation, rule parameters and patented/patent-pending material remain excluded here.
- V.A. — The Shift is a separate native computational foundation. This page examines a **proposed dimensional correspondence**, not an implemented weave.
- This examiner's limits (90 synthetic cost cents, 10 synthetic units, 20 capacity) are *independently invented test parameters*, **not attributed to AAR**. Neither the earlier controlled AAR source packet, prior private dry run, nor AAR's commercial brand assets are redistributed.
- AAR's name is used solely for factual attribution and context. No official AAR logo is used; the design is original and makes no claim of sponsorship, author approval, authorization to implement AAR or licensing. Author signoff of co-branding is not recorded.

See `DIMENSIONAL-CANDIDATE.md` for the exact scope of a proposed V.A. native mapping, and the [V.A. Estate proof standard](../proofs/EXAMINATION-STANDARD.md) for standing criteria.

## 03 / Frozen carrier table

| Item | Carrier | Standing |
|---|---|---|
| AAR as an independently authored method | [Official AAR overview](https://aarframework.github.io/aarframework/) | SOURCE-DECLARED; not imported into fixture |
| Synthetic rules and observed local behavior | `examiner.py`, `evidence/cases.json`, `evidence/effects.json` | LOCALLY OBSERVED |
| Frozen results | `evidence/result.json`, `evidence/manifest.json` | LOCALLY OBSERVED |
| Append-only-in-examiner receipt chain | `evidence/receipts.jsonl` | SCRIPT-VERIFIED; no third-party attestation |
| Hash, replay, negative mutation verification | `verify.py` | SCRIPT-VERIFIED |
| Native V.A. weave, full alternate-route coverage, customer effect | No original carrier attached | NOT SHOWN HERE |
| AAR endorsement, approved integration, native AAR run | No author approval attached | NOT ATTESTED |

## 04 / Reproduce without an API

Python 3.10+, standard library only. No internet connection, external model, private kernel, API key or service is needed.

```bash
cd aar-examination
python verify.py
python examiner.py --out my-reproduction
```

- `verify.py` checks exact SHA-256 hashes for every frozen file, deterministic rerun equality, every chain link and receipt digest, refusal non-effects, and a deliberately altered receipt to confirm mutation detection.
- `examiner.py --out DIR` reruns all 20 cases and writes fresh results, receipt chain and mock effect state. Identical inputs should produce identical bytes.
- The page's case explorer opens expected/observed decisions, reasons, before/after effect digests, and receipt IDs. Each output file is linked directly from the page.

## 05 / Negative controls and falsifiers

This local claim fails if any of the following occurs under the declared source and run: (i) a denied or held case changes the mock effect state, (ii) a retry creates a duplicate mock effect, (iii) a positive ALLOW case lacks its specified effect, (iv) an injected failure leaves a partially committed receipt or effect, (v) a receipt or frozen result is altered without a verifier failure, or (vi) same-input replay diverges.

An unexamined alternate route is **not** a passing route. A self-authored verifier is **not** an independent external observer. Local atomic copy-on-write staging is **not** proof of durable transactional atomicity.

## 06 / Owner-facing release boundary

This public-safe examiner was created for possible AAR-facing cooperation, without incorporating original controlled AAR packet bytes or protected implementation. Adria controls AAR scope and any permission to publish an AAR-endorsed proof or official branded graphic; the V.A. custodian controls native NEW K binding. A full end-to-end co-branded pilot requires a separately authorized, frozen native execution carrier with measured positive and negative effects, changed-condition re-resolution, alternate-route coverage, receipts, and an independent witness appropriate to the claim.

**Proof before power. Precise standing before broader claims.**
