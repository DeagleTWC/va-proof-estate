# Milestone 16 — Source-authenticated historic third-party review originals

**Result:** **Two original, dated, public-safe-labelled technical-review PDFs were retrieved from the Library and fingerprinted from actual bytes under private custody.** This adds historical *review practice* evidence. It does **not** supply a missing independent witness of native V.A., authorize publication of those PDFs, or verify the underlying test harness by merely reading a document.

The [public candidate register](HISTORICAL-REVIEW-ORIGINAL-REGISTER.json) preserves each report's distinct object and disposition. Exact original PDF digests and the PDFs themselves remain in the private custody ledger; **“public-safe” on a document header is not proof of authorization to redistribute it**.

## Two authentic documents, two different evidentiary questions

| Original report | Dated in document | Scope actually reviewed | Recorded conclusion | What this milestone independently confirmed |
| --- | --- | --- | --- | --- |
| **IQR-ITR-001-v1.0** (8 pages) | July 20, 2026 | Qualification of a third party's **submitted review carrier** for five PyJWT 2.13.0 security-behavior claims | **HOLD — qualification not established by that submitted carrier.** Original package did not independently bind saved output to exact source, command, runtime and test state. | Actual original PDF present; exact bytes, size, header and SHA-256 fingerprint recorded privately; original disposition examined. |
| **ITR-PYJWT-2130-INDEPENDENT-v1.0** (5 pages) | July 20, 2026 | **Separately described same-object** PyJWT 2.13.0 test against 2.12.1 vulnerable baseline and comparison with the submitted five-claim reviewer | Document reports **PASS** on the five bounded release claims and **PARTIAL QUALIFICATION** for bounded Python release-claim review. | Actual original PDF present; exact bytes, size, header and SHA-256 fingerprint recorded privately; described scope and disposition examined. |

Both source documents display **July 20, 2026**. This evidence does not authenticate a precise event ordering or separately witnessed creation chronology. The dispositions are **not a contradiction** that can be resolved by ignoring one: the first grades the completeness of the *original submitted review carrier*, and the second describes additional same-object differential analysis of the underlying *PyJWT release claims* and consequently a **narrower conditional reviewer finding**. They must be cited with their proper objects, not collapsed into an unbounded PASS.

The second report names an independently authored reproduction harness and JSON test results with their SHA-256 values. **Those separately named source files have not been recovered and re-executed in this milestone.** The original PDF therefore establishes the existence and precise text of a recorded review, not freshly reproduced PyJWT differential behavior or a qualified reviewer of native V.A.

## Private original verification

The [read-only original-PDF verifier](../scripts/verify_historical_external_review_originals.py) checks the exact original bytes against a separately retained private source SHA-256, validates PDF framing and size, and enforces one HOLDER-review object and one independent same-object differential-review object. It also prevents changed source names, mistaken release rights, false native V.A. reviewer promotion and under-specified dates from being accepted as valid.

For an authorized custodian:

```sh
python scripts/verify_historical_external_review_originals.py \
  --root "/private/review-pdfs" \
  --manifest "/private/review-original-identities.json" \
  --out "/private/private-byte-audit.json"
```

The private manifest follows `va-private-original-review-document-check/1.0` and uses `releaseAuthorization: false`, `independentNativeVAWitnessAuthenticated: false`, and `independentDifferentialHarnessReproducedInThisAudit: false`. Each document entry binds an exact `reviewId`, `reviewClass`, expected byte count and `source: {path,sha256}`. The main output is **`ORIGINAL_REVIEW_PDF_BYTES_MATCH_PRIVATE_MANIFEST_ONLY`**. This tool does not execute any PDF JavaScript, private verifier or network resource.

The [synthetic negative tests](../scripts/test_historical_external_review_originals.py) prove that a changed source digest, swapped PDF, fake release approval, reviewer-scope inflation or substituted non-PDF original is refused. They do not pretend to be independent real-world pilot observations.

## Actual qualification and publication gate

Before these historical reviewer results can be published as source-carrier proof: authenticate ownership and redistribution permission for the exact original PDF or extract, preserve its original digest privately and give the *authorized public extract* a separate new digest, establish original report attribution and qualification, retrieve any test harness and raw output needed to reproduce the technical result, retain failures and limitations, and issue a bounded disposition.

For **native V.A. independent consequence evidence**, this third-party PyJWT review is **not a substitute**: obtain a frozen native original, externally sensed permitted and refused effects, changed-condition and route controls, independently verified actual people/measurements, authenticated receipts and explicit customer release authority under the [Milestone 15 standard](INDEPENDENT-OBSERVATION-QUALIFICATION.md).

The [historic public-carrier register](historical/PUBLIC-CARRIER-REGISTER.json) remains empty for separately approved original pilot run packets. That is a publication status, **not** a finding of zero historical pilots.

## Examiner credit

The estate can accurately distinguish and credit: (a) historic examination of an external engineering submission, (b) independently authored same-object differential review as **recorded in the original report**, and (c) a separate as-yet-unadmitted independent native V.A. witness examination. Source fingerprints establish the first-level authenticity of these **report documents**; they are not test truth, signed human identity, or unlimited competence qualification.

**Credit the exact work demonstrated. Do not invent stronger standing from a PDF header, checksum, or self-declaration.**
