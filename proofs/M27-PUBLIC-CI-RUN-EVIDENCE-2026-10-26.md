# Deagle V.A. — source-bound public CI observation

**Observed:** October 26, 2026. **Evidence class:** completed GitHub Actions run and original downloaded public-test artifact. **Scientific standing:** M27 **HOLD**, M28 **NOT OPEN**. This is an independent rerun *in GitHub's CI environment of public synthetic tests*, **not** an independent native V.A. consequence measurement or qualified human witness.

## Original GitHub run and archive identity

- Workflow: [Public Proof Integrity, run #131](https://github.com/DeagleTWC/va-proof-estate/actions/runs/40367447420), push to `main`; recorded result **Success**.
- Repository commit checked out inside the original archived run: `75cbf29843363f021ef519611bd326ae05b5ca6c`.
- Workflow job: `verify-public-carriers`; completed successfully.
- GitHub artifact ID: `12671366188`; filename `va-public-proof-ci-40367447420-1.zip`; reported size **2,996 bytes**.
- GitHub artifact SHA-256, independently checked against downloaded ZIP bytes: `fca4990a33241a5413ff0e4a82b7d734dbe5d1a673afc876fce58e57a35d6b8d`.
- The ZIP format tested without errors and contained exactly **8** distinct public CI record files. The artifact uses a GitHub Actions retention period of **90 days**, so availability of its original download after expiry must not be assumed.
- Recorded execution environment: **Python 3.11.17**; configured test Node **v20.20.2**. These versions describe the *public-test runner*, not native V.A. substrate.
- Earlier [run #130](https://github.com/DeagleTWC/va-proof-estate/actions/runs/40356781918) also independently reports success for the integration commit `4405dbdb169274a06e912d899c06b74fdb9e54f9`; it did not yet generate the new archive.

## Recovered original recorded outputs

| Original ZIP member | Grounded observation |
| --- | --- |
| `run-identity.txt` | Commit `75cbf29843363f021ef519611bd326ae05b5ca6c`, run ID `40367447420`, attempt `1` |
| `m27-synthetic-tests.log` | `Ran 39 tests` followed by `OK`; public synthetic-only fixture coverage |
| `va-origin-register.log` | Source inventory gate `ok: true`; **36** eligible references, **3** non-assimilated, **10** recovery lanes |
| `va-origin-adversarial-tests.log` | `controlCount: 14`, including the baseline consistency control plus **13** synthetic negative controls, all rejected as expected |
| `public-source-sha256.txt` | Six original public-source digests pinned to the checked-out commit |
| `standing-ceiling.json` | `nativeVAEvidence`, `externalEffectsQualified`, `independentWitnessQualified`, `M27Completed`, `M28Authorized`, `publicationAuthorized` are all `false` |
| `python-version.txt` / `node-version.txt` | `Python 3.11.17` / `v20.20.2` |

Source SHA-256 values in the runner's original log:

```text
d4aae0d2b1419d69dd8b94f798f176af807b1ba556e4bd5069693e78f4bf17ac  scripts/preflight_m27_target_readback.py
b13a41109bc3e6ec8f2ba0b1109b7018522e46bba8d823e3e5c6b20e4caa6867  scripts/test_preflight_m27_target_readback.py
efdd767114c1015a3cd17bba7689e621f0f17d08d931856c5452aa5275d6c5da  scripts/verify_va_original_capability_recovery.mjs
d4d9b1dae760589edd8a8b881875527840dfc3cd24c40fc242bba92b1d79b86b  scripts/test_va_original_capability_recovery.mjs
acaada55b2482206ae6777db445971d026be5accbbc3900f0a0dc8371a70bc5b  proofs/VA-ORIGINAL-CAPABILITY-RECOVERY.json
ce91621441ccd1b8fea4a6cbaadec3fdbb3e8cda476522a94659d65b494b8227  proofs/END-TO-END-ESTATE-REGISTER.json
```

## Admissibility and limits

The outcome is **verified CI execution of bounded public tests at the identified source commit**. GitHub Actions runner execution is not a disinterested independent scientist, a real native system's effect witness, an independently authenticated apparatus, rights approval, or proof of live operational safety. Local synthetic checks are not promoted by being rerun in CI. The artifact's retained source digests and this record also do not certify all other CI steps' human or physical proof content.

The original public-test ZIP was downloaded and its SHA-256 and archived contents were checked. This report is a reproducible identity and output index, not a replacement for the original downloadable archive. Any later GitHub run is a *separate* original with its own commit, ID and digest.

**M27 acceptance still requires** authentic, independently acquired permitted-effect and refused-non-effect protected-target observations from one frozen authorized native V.A. consequence route; bound original receipts; qualified observer/custody; route accounting; and safe exact-byte release review. **M27 HOLD. M28 NOT OPEN.** This record is not a new scientific milestone.
