# Milestone 12 — Historical source bytes independently cross-checked

**Source verification:** 2026-10-25. The public review estate now provides exact immutable-source links to three real historical public receipt/result files, plus a **byte-verified original July public proof-path PDF identity**. This work does not restart any earlier pilot or assert that these source records are the original freeze from which every past run was produced.

## What was actually verified

1. **Original public Proof Path v2 PDF, July 2026.** Its *actual 71,495 original PDF bytes* were retrieved from the Library and independently hashed. SHA-256 was **`dd5a626e4ed5efafb49e70e987f61f151e220d793e35b96c55b05e59dc426ca6`**, matching the checksum already recorded in [SOURCE-ESTATE.md](SOURCE-ESTATE.md). The PDF remains in source custody, not copied to this GitHub repository; its [public-safe extracted transcript](sources/shift-public-proof-path-v2-extracted.md) is already present. The document provides the six bounded earlier repository inspection routes; it does not independently establish the execution of native V.A. V12 or actual customer pilot results.
2. **Elyria One Proof receipt:** [unchanged receipt file in its original repository](https://github.com/Kamanaka5502/elyria-one-proof/blob/7ef8c424ca95d0bf55b18b9d13aa79e4ac29a058/receipts/demo-valid-001_receipt.json). One source receipt with an execution-boundary decision; the source's included timestamp reads 2026-04-30. This is a recorded local decision, **not an external effect measurement**.
3. **Authority Revocation Witness:** [original public result record](https://github.com/Kamanaka5502/authority-revocation-witness/blob/620324048ff1b067af6602d50d3016adcaed3747/authority_receipt.json), five bounded source results including revoked and divergent conditions. Their stored match flags and status labels describe the test record; they are **not** an independently measured real-world consequence.
4. **Scope Expiry Gate:** [original public result record](https://github.com/Kamanaka5502/scope-expiry-gate/blob/d0acaa0b4dee8cc26b357ce0e26c57f2d989da34/scope_receipt.json), five bounded source results including expiry and divergent conditions. These are distinct from the April proof build and current native V12.

For each original public JSON source, the [byte-identity manifest](HISTORICAL-SOURCE-BYTE-VERIFICATION.json) retains the exact original repository, 40-character commit identity, path, Git blob SHA-1, independently computed UTF-8 full-source SHA-256, byte count and bounded scope. The manifest links rather than republishes original source, respecting source ownership, attribution and custody. **Eleven indexed receipt/result entries are not eleven historical pilots or eleven independently witnessed V.A. runs.**

## What remains in original private custody

The April 2026 **Deploy Build V1.2 Final Production Proof Package ZIP** was found as a historical email attachment. Prior documentary records describe eight verification cases and tamper/replay controls. But the original ZIP bytes have **not been extracted or independently re-executed here**, and the original ZIP has not been cleared for publication. April–May launch ZIPs, controlled customer pilot packets, any original live-run receipts and private independent-witness records likewise remain separate.

No older engineering review may be promoted to the **current V12 native evidence register** on the strength of a filename, copied figure, asserted customer pilot, or decision-only receipt. The [historical carrier admission register](historical/PUBLIC-CARRIER-REGISTER.json) has **zero separately cleared and attached historical run packets in this GitHub release**. That figure says nothing about how many actual pilots or freezes were performed.

## Recheck original public source bytes

Use the [fail-closed historical source checker](../scripts/validate_historical_source_bytes.py) from a local checkout:

```sh
python scripts/validate_historical_source_bytes.py
python scripts/validate_historical_source_bytes.py --fetch-originals
```

The first command checks schema and source-identity constraints without network access; the second reads the *exact pinned public-source revisions* and confirms each source SHA-256 and Git blob identity. Its web fetch is **read-only** and never runs the downloaded code or treats its decision labels as independently observed effect.

Passing these checks establishes precisely: **the publicly referenced bytes are the recorded public source bytes at the pinned commit**, not the original frozen native build, an authenticated observer, or proof of non-formation across unexamined consequence routes.

## Next original operational-carrier gate

Once the custodian can access the authentic V1.2 ZIP or an original release-cleared historical pilot packet, preserve original hash, freeze chronology, full original outcome/replay and rights; independently repeat the exact claim where authorized; then follow [the release admission gate](historical/ADMISSION-GUIDE.md). Do not manufacture an original from this source manifest.

**Function available for examination; protected construction remains protected.**
