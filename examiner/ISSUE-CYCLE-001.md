# Cycle 001: custodian-controlled fresh challenge issuance

**Operational status:** Issuance workflow implemented, pending the first external freeze. This procedure does not assert an independent examiner or native V.A. result.

## Applicant commitment

Run the freeze command in [Independent Challenge](INDEPENDENT-CHALLENGE.md) with the applicant's own controlled adapter. Publish ONLY the complete freeze.json as **plain JSON with no surrounding explanatory text** in a comment on [Cycle 001 issue #1](https://github.com/DeagleTWC/va-proof-estate/issues/1). Do not disclose the adapter source, proprietary math, passwords, customer records or private keys. Do not edit the published comment; an edited freeze cannot be admitted.

Copy the numeric comment ID from the end of its GitHub issuecomment identifier.

## Issuer authorization

A different custodian GitHub account opens [Issue Fresh External Challenge](https://github.com/DeagleTWC/va-proof-estate/actions/workflows/issue-fresh-challenge.yml) and selects Run workflow on main. Enter the freeze comment ID, family matrix/session, and a bounded round count.

The GitHub Actions job fetches the original comment and verifies its issue identity, unedited status, creation-before-issuance, freeze digest and issuer/account separation. The action then creates a fresh cryptographically random seed, suite digest and challenge nonce; records the source comment and run identity; uploads four immutable-for-the-run carriers; and posts the challenge reference back to issue #1.

The four archived files are freeze.json, challenge.json, issuance.json and comment-snapshot.json. Actions artifact retention is 90 days: download and independently preserve the originals before expiry.

Verify the downloaded packet locally using:

    python examiner/issue_cycle_challenge.py verify --dir /path/to/issuance

That local command checks internal bytes, hashes, author statements and relative ordering inside the saved record. It **does not remotely authenticate GitHub**: cross-check the actual public comment and Actions run. No participant adapter or protected V.A. construction executes on Deagle CI.

**Ceiling:** GitHub-anchored issuance only. It cannot establish independent examiner identity, actual physical effect, native V.A. operation, external route closure, certification, or access rights to either party's protected construction.
