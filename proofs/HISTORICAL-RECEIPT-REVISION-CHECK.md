# Historical receipt revision identity — synthetic examiner aid

**Review class:** Public-safe checker specification and synthetic regression controls; **not** a new scientific milestone or native consequence measurement.

The [existing historical run-lineage examiner](../scripts/verify_historical_run_lineage.py) evaluates internally consistent archived case/receipt/closeout fields and detects a repeated run ID across revisions. This distinct read-only control examines a narrower provenance question: *did original receipt source bytes change while their receipt identifier was reused?*

## Method and bounded result

Use [`check_historical_receipt_revision.py`](../scripts/check_historical_receipt_revision.py) against two authorized, unchanged, private connected-environment ZIP originals. It reads but never executes source members. It requires a matching declared run ID, three captured decision classes, three distinct captured receipt identifiers per version, and safe archive and unambiguous JSON structure. For each receipt pair it distinguishes:

- Identical serialized bytes versus changed original serialized bytes.
- Reused receipt IDs, timestamps, opaque state-hash strings and opaque signature labels.
- Changed bytes under a reused ID (`provenanceReviewRequired: true`), which must be reconciled with original revision chronology and the actual signature scheme before attributing historical identity or freeze standing.

A changed receipt **does not alone demonstrate incorrect execution or improper alteration**. A stable signature-like string **does not authenticate** the changed source bytes, historical signing event, key owner, examiner independence or separately measured external effect. The tool never opens scientific M28, changes M27 source qualifications or authorizes publication.

Private-only example:

```sh
python3 scripts/check_historical_receipt_revision.py \
  --connected-v1 /private/connected_environment_executed_v1.zip \
  --connected-v2 /private/connected_environment_executed_v2.zip \
  --out /private/new-private-revision-review.json
```

The private report includes source hashes and must not be committed, attached to a public issue or uploaded to the Proof Estate without exact-byte permission and the [publication charter](PUBLIC-INTEREST-PUBLICATION-CHARTER.md)'s rights, privacy, custody and safety gates.

Regression tests in [`test_historical_receipt_revision.py`](../scripts/test_historical_receipt_revision.py) generate synthetic local ZIPs and check changed/reused identity, unchanged receipt bytes, freshly assigned identifiers, nonmatching run ID, capture/receipt mismatch, duplicate receipt IDs, duplicate JSON keys and unsafe archive member paths. Passing controls establish this **examiner's behavior**, not historic native V.A. operation, a qualified external observer or a physical measurement.

**Scientific continuity:** This tooling can advance documentation and independent source examinations while specific evidence questions remain under review. It must not be interpreted as a project-wide stop, a new pilot, or a new milestone.
