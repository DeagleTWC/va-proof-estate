# Milestone 17 — Original independently authored review harness recovered and source verified

**Source outcome:** The actual historic **Independent PyJWT Review Package v1.0** ZIP was recovered from the Library and examined as data. It contains the original July same-object review PDF and DOCX, its independently authored Python harness, and both machine-readable result files. The source files were **not reconstructed**, invented, or substituted with new demonstration test data.

**This closes a concrete evidentiary gap left by Milestone 16.** That milestone examined two genuine review PDFs but could not access the particular underlying original harness/results cited in the same-object differential report. The original package is now recovered. It remains in private custody pending disclosure clearance.

## Exact original-source correspondence

| Historical source member | Source-byte result | What the original recorded |
| --- | --- | --- |
| Original July 20 review PDF | **Byte-identical** to the separate original PDF recovered in M16 | Same-object PyJWT differential review and **PARTIAL QUALIFICATION** of bounded Python release-claim examiner |
| Independently authored Python review harness | **SHA-256 matches the value in the historic review report** | Six bounded test functions covering release-claim families C001–C005 (C005 has two checks) |
| PyJWT 2.13.0 stored result JSON | **SHA-256 matches the historic report** | **Six saved PASS** results |
| PyJWT 2.12.1 stored result JSON | **SHA-256 matches the historic report** | **Six saved FAIL** results on corresponding cases |
| Original DOCX review | Source bytes located in the same unchanged archive | Companion review document; does not enlarge the claim |

The specific file digests of the three documented technical source objects are in the [machine-readable review source register](HISTORICAL-DIFFERENTIAL-SOURCE-REGISTER.json). The original ZIP digest and unreleased document digests remain with the original custodian; the original contents have **not** been copied onto this public site.

The six bounded technical cases describe distinct software release behaviors for PyJWT, **not six V.A. customer runs or independent physical consequences**. The baseline failures and fixed-version passes are values **recorded in the recovered original result files**. Their original SHA-256 values agree exactly with the source report. Matching a saved outcome to a previously recorded report is meaningful provenance but does **not** recreate the original execution event.

## Scope and reviewer credit

This evidence now permits precise historic credit for **a documented, independent-style, same-object comparative review of a third-party Python library** and its recovered original reproducibility carriers.

The earlier [reviewer-submission assessment](HISTORICAL-EXTERNAL-REVIEW-ORIGINALS.md) concluded **HOLD** regarding the evidence formation of the submitted reviewer carrier. The later, separately described same-object differential review recorded a **bounded five-claim technical PASS** and **PARTIAL qualification** for Python release-claim evaluation. The originals establish that these two determinations were documented; the M17 archive recovers the separately authored test and result sources named by the latter. The reports' July 20 date labels do not alone authenticate their event ordering.

None of this means an outside examiner reproduced native V.A. Nor does a report's word **independent** identify or authenticate an unrelated human observer: signature, identity, affiliation, method, original environment and actual re-execution remain separate.

## Source-only independent examiner

A new [read-only original-review ZIP checker](../scripts/verify_historical_pyjwt_differential_original.py) accepts the **actual** private archive and compares exact bytes of the three source files with the digests already named in the historic July review. It refuses missing/duplicated archive entries, unsafe ZIP paths, changed original Python or result files, switched version labels, mismatched test IDs and absent fail-before/pass-after *recorded* outcomes. It can optionally compare the archived PDF byte-for-byte with a separately held prior source PDF:

```sh
python scripts/verify_historical_pyjwt_differential_original.py \
  --zip "/private/Independent_PyJWT_Review_Package_v1.0.zip" \
  --prior-review-pdf "/private/Independent_Technical_Review_PyJWT_2.13.0_and_Reviewer_Comparison_v1.0.pdf" \
  --out "/another-private-directory/review-original-audit.json"
```

This local examiner **never imports or executes the archived Python harness**, installs a dependency, calls a production system, or accesses the network. A successful result is **`ORIGINAL_REVIEW_PACKAGE_MEMBERS_MATCH_REPORTED_HASHES`**, *not* a newly run software test. The original reported import paths and saved environment fields are historic strings, not attested runtime provenance.

The public [synthetic negative tests](../scripts/test_historical_pyjwt_differential_original.py) test forged and mismatched original carriers. Their synthetic records must not be counted as independent reviewers or historic original runs.

## Actual native V.A. independent-witness admission remains separate

The [Milestone 15 witness standard](INDEPENDENT-OBSERVATION-QUALIFICATION.md) requires a **frozen native original**, authorized source custody, independent actual effect/non-effect measurement, material-condition challenge, original receipts and independently authenticated reviewers. These PyJWT originals cannot satisfy that native requirement, regardless of the quality of the third-party software review.

**Current public status:** source-hash-bound historic external review records **verified**; independently witnessed native V.A. public carrier **not established/attached**. No unsupported customer, pilot count, source rights or physical proof has been promoted. The [historical public original-carrier register](historical/PUBLIC-CARRIER-REGISTER.json) remains an admission control, not a census of historic work.

**Next controlled examination:** source-safe actual re-execution of the independently authored PyJWT review against exact original dependencies *if authorized and environmental provenance can be fixed*, while independently seeking a real native V.A. third-party original witness/external consequence carrier for a different evidence lane.
