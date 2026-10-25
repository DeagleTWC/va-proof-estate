# Milestone 19 — Original-preserving release-seal derivative and immutable custody lineage

**Result:** A **new, separately identified private review derivative** has been constructed from an actual recovered historical release ZIP. Unlike a retrospective alteration of an original, its exact original source contents remain unchanged and the new member index closes completely.

**The original historical source remains at HOLD.** The new carrier qualifies only its **own internal member hashes**, not any production deployment, native V.A. effect, human witness or original historical freeze.

## Distinct original and derivative objects

| Examined property | Original April-labelled historical source | Newly made review derivative |
| --- | --- | --- |
| Stored copies | Two matching historical originals, retained without mutation | New separate derivative only |
| Total archive files | 57 | 58, including new provenance and replacement index |
| Original source-file payloads | 56 | **Same 56 original files, byte-identical** |
| Member hashes recorded | 55 | **57** (56 source files plus new custody-provenance record) |
| Recorded member hashes matching source | 54 | **57/57** |
| Previously unindexed member | 1 | **0** |
| Original mismatch | 1 | Not silently changed; preserved in historical defect record |
| Evidentiary status | **HOLD — historical seal incomplete** | **PASS — new private member-index closure only** |

The new derivative retains each original source-file payload. Only the **release hash index** is recalculated for the derivative, and one explicit **`CUSTODY_REISSUE_PROVENANCE.json`** member is added. Recompression and these additions give the derivative a distinct whole-ZIP identity. No archived source was executed, no historical operation was replayed, and the original freeze's record remains unchanged.

The new provenance explicitly identifies the archived source (by private original SHA-256), previous index, original seal HOLD and changed member roles. The original and derivative whole-archive SHA-256 values remain in a **separate private audit**, outside this public repository. The previously recovered local proof-suite results are preserved in the original; this review operation neither repeats nor cancels them.

## Examiner reproducibility without publishing construction

The new [read-only archive reissue utility](../scripts/reissue_original_seal_for_review.py) creates the same *kind* of private review derivative for any authorized archive using `RELEASE_HASHES.json`. It:

1. Requires a separately fixed SHA-256 of the unchanged original. This prevents an attacker from substituting another archive and merely recomputing a self-consistent index.
2. Rejects missing, already fully sealed, malformed, encrypted, symlinked, duplicated or traversal-bearing sources as appropriate; refuses output overwrite or output beside the historic original.
3. Reads, never executes, all original source data; independently detects missing and mismatched member hash entries.
4. Retains every source member **byte-for-byte at the uncompressed payload level**, writes a new provenance record and complete new per-member SHA-256 index in a **separate, new private ZIP**.
5. Reopens the derived ZIP, verifies its entire index and original-source byte equality, and rechecks that the historical original SHA-256 still matches.

Run locally:

```sh
python scripts/reissue_original_seal_for_review.py \
  --original "/original-custody/unchanged-historic-release.zip" \
  --expected-original-sha256 "<SHA-256 from a separately preserved earlier custody record>" \
  --out "/separate-private-review/new-review-derivative.zip" \
  --edition 2026-10-25
```

The command **must not** publish the private ZIP or credentials. It does not import archived runtime source, modify original bytes, validate effect observations or grant release rights. The [older release-seal auditor](../scripts/audit_original_release_seal.py) can separately verify the new archive's current member hash closure. Its **historical authenticity still depends on the original externally fixed source fingerprint**.

The [synthetic adversarial suite](../scripts/test_reissue_original_seal_for_review.py) refuses tampered originals, overwrite, source substitution, same-folder output, duplicate paths, invalid editions, traversal and needless reissuing of an already complete source. Synthetic fixtures do not become prior original pilots.

## Independent human and consequence work remains distinct

The additional historical evidence search did not authenticate an independent native V.A. public-original witness packet with all required effect observations and release consent. This **does not erase previous pilots or their protected private original records**. It means no such packet has been newly admitted by this specific public milestone.

The next substantive operational gate is to examine a **separate, actually frozen native V.A. execution object** with effect-bearing action, refusal, material governing-condition change, route inventory, independently measured consequences and genuine qualified human examiners. Its original receipts, replay, observer credentials and public release permissions must remain bound to exact source identities. Use the [independent observation standard](INDEPENDENT-OBSERVATION-QUALIFICATION.md) and [original carrier release gate](historical/ADMISSION-GUIDE.md).

**Two independently established things are now recorded:** the original's historically incomplete seal remains HOLD, and a newly created custody derivative has 57/57 matching source-member hashes. Neither one is falsely represented as proof of live independent native V.A. operation.

**Preserve the original. Distinguish the derivative. Qualify the consequence independently.**
