# Historical Carrier Admission — Original Freeze Preservation

**Status:** Public release intake implemented; **no original historical run packet admitted in the current release register**. This number is not the number of past pilots, engineering layers, tests, freezes, or privately retained originals.

**Scope:** V.A. / The Shift historical pilot and freeze records that existed before the October 2026 public Proof Estate. No protected mathematics, substrate, proprietary implementation, KCD controlled source, client records, security credentials or unreleased works may enter this repository.

For a folder containing earlier pilot and freeze files, first use the [offline local fingerprint inventory](LOCAL-INVENTORY.md) to check unchanged source bytes without posting paths, protected originals or private candidates. This **precedes** release authorization and grants no evidence standing.

## Original record → public extract (two different objects)

The historical source object **keeps its original identifier, original freeze date, original SHA-256, original custodian and original execution/result record**. Do not generate a new historical timestamp, overwrite a freeze, or represent a later narrative as the original.

A newly authorized public extract receives **its own** release identity, publication date, SHA-256 and clearance boundary. It may omit non-disclosable internal fields while retaining enough material for the bounded public claim. It does **not** replace or modify the original frozen object.

## Controlling publication mission

The [public-interest evidence charter](../PUBLIC-INTEREST-PUBLICATION-CHARTER.md) requires the **maximum safely releasable, independently checkable results**, not automatic suppression of pilot outcomes for commercial secrecy. Candidate extracts should aim to preserve observable function, positive and negative cases, original receipts, changed conditions, independent review and limitations, while redacting specific hazardous construction and unauthorized third-party material. Each exact candidate must undergo recorded source custody, disclosure rights, privacy and public-harm review before publication. TMU historical pilot originals are **eligible for this process** when recovered, not blanket excluded or automatically authorized. The [private release review preflight](../../scripts/preflight_public_interest_release.py) verifies exact source/extract bytes and recorded approvals but cannot authenticate real rights or safety on its own.

## Release checklist

1. **Locate the actual original.** Verify the original build/freezed file or run packet, identifier, creation record, byte digest and custody. If any original field is unavailable, retain **NOT ESTABLISHED** for that field; do not guess.
2. **Confirm disclosure rights.** Obtain exact release authorization from every relevant custodian/owner or customer. No permission may be inferred from a public repo name or earlier test.
3. **Prepare a public-safe extract.** State the exact bounded observable claim, test scope, positive and negative observations where actually present, changed-condition identity, route limits and which raw records remain private.
4. **Keep original and extract separate.** Retain the unchanged private original. Generate and hash the *new* cleared public extract in `proofs/historical/carriers/<id>/`.
5. **Describe one source in a candidate entry.** Use [the blank JSON template](CARRIER-ENTRY-TEMPLATE.json). Fill the original's exact digest separately from the public extract's SHA-256, date and permission reference.
6. **Preflight locally**, before uploading any public file, with:

    `python scripts/validate_historical_carriers.py --candidate /path/to/entry.json --root /path/to/public-safe-staging-tree`

   The staging tree must preserve the repository-relative carrier paths. An incomplete template intentionally fails. This validation verifies file identities, paths and required metadata **only**, not a live effect or independent witness.
7. **Human custody gate:** Confirm the exact public bytes and consequences, negative controls, replay integrity, reviewer attribution, route limits, security/redaction and written release scope; attach a review disposition. If not cleared, do not publish.
8. **Admit only when released:** Add the approved entry to [the public register](PUBLIC-CARRIER-REGISTER.json) and the cleared extract(s) to the repository together. CI will reject missing bytes, modified hashes, absent clearance fields and unsupported status. Update the claim-to-carrier register only after an explicit independent proof review.

## Public standing and limits

- `SOURCE_RECORDED`: a release-cleared public source extract and preserved original identity are attached; no particular measured result is inferred.
- `PUBLIC_BOUNDED_OBSERVATION`: release-cleared direct observation, negative control and replay records are attached by their exact paths/digests. The reviewer still decides what those bytes demonstrate.
- `PUBLIC_INDEPENDENT_REPRODUCTION`: includes the above, plus distinct original reviewer packets and an explicitly documented independence adjudication. Two self-declared names or signing keys are not independent-person proof.

**No automated metadata check promotes any claim into native V12 or physical KCD standing.** Nothing in a public-submission workflow implies acceptance of a confidential customer disclosure. The register begins empty because no original historical run has been admitted to *this website*, not because historical pilot work has been absent.

## Read in sequence

[Historical evidence lineage](../HISTORICAL-EVIDENCE-INDEX.md) · [Version lineage](../VERSION-IDENTITY.md) · [Pilot release requirements](../PILOT-EVIDENCE-RELEASE.md) · [Original examination standard](../EXAMINATION-STANDARD.md) · [Carrier register](PUBLIC-CARRIER-REGISTER.json).
