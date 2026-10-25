# Deagle external examination — Review Cycle 001

**Status: OPEN FOR INDEPENDENT CANDIDATES. No third-party examination, execution or witness standing is established merely by opening this cycle.**

## Examination invitation

DeagleTWC invites an independent engineer to submit a bounded adapter of their own engineering work to a prospective **freshly seeded local interface examination**. Every participant retains their protected internals. Deagle does not supply protected V.A. construction, does not run untrusted uploaded code, and does not present a passed toy interface as native execution.

The narrow proposition examined is whether an externally engineered adapter returns the expected bounded decisions under changed authority, stale evidence, substitutions, repeated requests and alternate declared routes. It does **not** test actual real-world non-formation of a consequence.

## Sequence

1. The participant freezes an exact local source-file identity, revision, SHA-256 and commitment nonce using the public "independent_challenge.py freeze" command. The source remains private and under the participant's custody.
2. The participant preserves the commitment in a dated, independently viewable issue/comment or other out-of-band witness record **before** challenge issuance. The tool does not independently authenticate chronology.
3. A challenge issuer distinct from the participant runs "independent_challenge.py issue" after observing the freeze. The generated challenge binds an unpredictable seed, nonce, suite fingerprint and previous commitment.
4. Two genuinely distinct examiners, using their own authorized access to the identical frozen source, run the same challenge separately and retain unmodified reports. Merely creating two personas or keys does not meet independent witnessing.
5. Each examiner signs their own record with a locally held private RSA key; the published packet includes the corresponding **public** keys only.
6. Collect the ten permitted carriers in one directory. Do not upload the source artifact or private signing keys.
7. Run the read-only verifier. Out-of-band verification of reviewer independence, chronology, custody and actual real-world effects remains separately required.
8. A human examiner assigns any higher standing after inspecting genuine originals; this verifier cannot grant native V.A. or physical performance claims.

## Ten-carrier local reviewer packet

    freeze.json
    challenge.json
    left-report.json
    left-record.json
    left-signature.json
    left-public.pem
    right-report.json
    right-record.json
    right-signature.json
    right-public.pem

Execute:

    python examiner/external_witness_admission.py /path/to/review-packet --out /path/to/local-admission.json

The validator checks mandatory file identity, signatures and original report consistency. It does not execute submitted code. Unexpected file types, incomplete data, altered signatures and altered challenge identities fail closed. Other material in the directory is **not** reviewed by the tool.

## Admission ceiling

- Missing or mismatched freeze, challenge, report, signature or public key: REFUSE.
- Valid ten-carrier structure and signatures: LOCAL_DATA_AND_SIGNATURE_VALID_ONLY.
- Two distinct signing keys and different declared examiner names: **not proof of two independent people**.
- Genuine independent examiner reproduction: separate, attributable examiner identities and locally retained originals still required.
- Native V.A. or physical KCD standing: cannot be inherited from this synthetic interface packet. Requires separately frozen native/physical objects and real consequence-bearing witness measurements.

Negative controls, failures and disagreements must be retained, not rewritten into passes.

No synthetic result can automatically change the native V.A. or KCD registers. Custodian release clearance is required before making any actual external evidence public. Do not post private IP, corrected mathematical construction, customer information, credentials, actuator instructions or unreleased implementation details.

Related: [frozen challenge](INDEPENDENT-CHALLENGE.md) | [examiner source](external_witness_admission.py) | [public intake](../.github/ISSUE_TEMPLATE/external-independent-examination.md) | [proof standard](../proofs/EXAMINATION-STANDARD.md).
