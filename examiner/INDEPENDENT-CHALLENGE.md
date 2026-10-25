# Frozen external challenge and two-key local re-examination

**Public-safe synthetic interface test. No native V.A. execution, hardware effect, or protected construction.** This examination improves on known-seed sample adapters: the participant first records an artifact fingerprint; an examiner **then issues a fresh challenge**; separate examiners can preserve and cryptographically sign their own reports. This does not, by itself, authenticate chronology, people, separate machines, or an external effect.

Python 3.11 and OpenSSL command-line are required. Run only trusted third-party adapters in your own protected environment. Deagle CI never runs uploaded outside executables.

## Protocol

1. **Participant freezes one executable source file** and records its SHA-256. Retain source privately, circulate only the JSON commitment before the new challenge. Example:

    python examiner/independent_challenge.py freeze --artifact examiner/example_layer.py --participant "Engineer A" --revision "rev1" --out freeze.json

2. **Independent examiner issues an unpredictable challenge only after receipt of the freeze.** Record issuance through a separately verifiable channel if chronology is material.

    python examiner/independent_challenge.py issue --freeze freeze.json --family matrix --rounds 2 --out challenge.json

   Families: matrix (nine synthetic cases per cohort), session (27 persistent-process synthetic events per cohort). The challenge embeds the frozen hash, seed, nonce and regenerated suite fingerprint.

3. **Two separate examiners run the same frozen artifact and challenge** on their own trusted machines. Each keeps an original report and examination record. The executed command must explicitly reference the pinned artifact file.

    python examiner/independent_challenge.py run --freeze freeze.json --challenge challenge.json --artifact examiner/example_layer.py --examiner "Examiner One" --report one.json --record one-record.json --adapter python examiner/example_layer.py

   Repeat for Examiner Two as `two.json` and `two-record.json`. This binds the declared source *file*, not hidden dependencies, runtime effects or hardware.

4. **Sign each record under a different local private RSA key.** Never upload a private key.

    openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out one-private.pem
    openssl pkey -in one-private.pem -pubout -out one-public.pem
    python examiner/independent_challenge.py sign --freeze freeze.json --challenge challenge.json --report one.json --record one-record.json --private-key one-private.pem --public-key one-public.pem --out one-signature.json
    python examiner/independent_challenge.py verify --freeze freeze.json --challenge challenge.json --report one.json --record one-record.json --signature one-signature.json --public-key one-public.pem --artifact examiner/example_layer.py

   Examiner Two signs their own record with their own different private key and publishes the corresponding public key.

5. **Compare both signed records.** The tool refuses mismatched challenge identities, source digests, unsupported evidence status changes, contradictory oracle results, forged signatures, identical declared examiner names or reused keys.

    python examiner/independent_challenge.py compare --freeze freeze.json --challenge challenge.json --left-report one.json --left-record one-record.json --left-signature one-signature.json --left-public-key one-public.pem --right-report two.json --right-record two-record.json --right-signature two-signature.json --right-public-key two-public.pem --out cross-examination.json

## Proof standing and release

Passing this interface examination does not prove live V.A., actual negative physical formation, production fitness, route closure, a scientific category, or independent third-party identity. Signed records prove possession of a cryptographic key, **not** that the key owner is the declared examiner. Publication and freeze ordering also require external custody or separately corroborated records. Two accounts and two keys can belong to one person.

An external examiner seeking stronger standing must separately retain the exact artifact, provenance, release clearance, genuine instrument/telemetry observations, negative controls, changed-condition behavior, receipts, independent environment identity and replay. A public issue may refer to release-cleared bounded observations; **do not publish private substrate, protected mathematics, secret keys, confidential operational evidence or executable uploads**.

[External examiner intake](https://github.com/DeagleTWC/va-proof-estate/issues/new?template=external-independent-examination.md).
