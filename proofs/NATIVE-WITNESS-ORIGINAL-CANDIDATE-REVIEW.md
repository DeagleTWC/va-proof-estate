# Milestone 18 — Native witness admission: original source-seal gate

**Disposition: HOLD on admitting an independently witnessed native V.A. result to this public estate.** This is an evidence finding **about the candidates examined**, not a judgment that earlier real pilots never took place. The larger historical estate remains separately preserved.

## What was examined

This milestone recovered and inspected actual pre-existing, privately held source archives in three distinguishable classes:

| Original source category | Established source scope | Qualification outcome |
| --- | --- | --- |
| Historic local independent-verifier release | Two copies of an original archived release were compared; they are byte-identical. Its archived proof summary records bounded local test successes. | **SOURCE-CARRIER SEAL HOLD.** The original release-index checksum closure does not fully reconcile with actual member bytes and coverage. This is a custody/integrity defect, not an independently witnessed native run. Exact private source names, digest differences, and remediation details remain in the private custodian audit. |
| Public-safe boundary-interface pilot | Original packet, sample receipts, fixed expected responses and self-tests were identified. | **INTERFACE-LEVEL EVIDENCE ONLY.** A sample or a test of a boundary interface does not independently measure all possible native consequences. |
| External seam demonstrator | Original source contains external-formal-solver evidence and bounded example claims. | **DIFFERENT ENGINEERING OBJECT.** Results about a third-party solver or separate seam do not inherit independent native V.A. standing. |

No original private archive, internal source code, original ZIP fingerprint, personal customer identity or confidential third-party observation was copied into this public release. Two byte-identical copies of the same release **cannot** be counted as two separate witness reproductions. Original local case outcomes are retained in the private audit but have no automatic effect-standing promotion.

### Actual technical advancement

A new [read-only release-seal auditor](../scripts/audit_original_release_seal.py) tests **complete file-level SHA-256 closure** against the archive's own `RELEASE_HASHES.json` manifest. It refuses:
- incorrect expected digest for the original ZIP when supplied from separate custody;
- any registered source file whose current bytes disagree with its indexed SHA-256;
- any unindexed source member, including executable verifier or boundary code;
- declared-but-missing files, duplicate paths, traversal, unsafe member structure or malformed registry data.

The hash-index JSON file itself is excluded from its own inner index to avoid circular digests. A **separate, previously fixed whole-ZIP SHA-256** must be compared to authenticate an earlier archive identity; an internally rehashed substitute could otherwise look self-consistent.

The tool **does not** execute archived code, upload submitted archives, authorize source redistribution, establish original freeze chronology, authenticate an independent reviewer, or verify actual real-world effect or non-formation. A passing seal is only `INTERNAL_SOURCE_HASH_CLOSURE_PASS`, not a native consequence proof.

## Controlled local usage

```sh
python scripts/audit_original_release_seal.py \
  --archive "/private/original-frozen-release.zip" \
  --expected-archive-sha256 "<digest fixed in independent original custody>" \
  --out "/another-private-directory/release-seal-review.json"
```

The expected archive SHA is optional if no separate original fingerprint is available, but omission leaves its historical source identity **unanchored**. All report output can contain original names and digests; keep it private. The command exits **2** on invalid seal and **0** only when internal member checks close completely. It never modifies the archive.

The accompanying [synthetic adversarial tests](../scripts/test_audit_original_release_seal.py) cover altered registry hashes, incomplete source coverage, unlisted executable files, missing receipts, duplicate/traversal and a fully rehashed **replacement** that must still fail comparison with the separately fixed historical ZIP digest.

## Native independent-witness gate

A release-sealed artifact may advance to **independent native V.A. witness examination** only when the actual frozen native original, authorized bounded test, external measurement of permitted effect, independent measurement of refused **non-effect** across material routes, changed-condition replay, separate examiner identities and original results are all inspected.

The [independent observation qualification standard](INDEPENDENT-OBSERVATION-QUALIFICATION.md) governs the technical and human gate. The [historical original public-carrier register](historical/PUBLIC-CARRIER-REGISTER.json) governs separate release rights and exact public-extract digests.

**No qualified human independent native V.A. witness was added** by this milestone. This narrow present-publication result does not erase any earlier real pilot, engineering proof, local verifier or externally performed work that lies outside the specifically recovered objects.

**Operational qualification cannot be conferred by self-described filenames, passing local case counts, duplicated ZIPs or a simulated signed receipt. Preserve the originals, hold incomplete seals, and admit only the actual independently observed and authorized consequence.**
