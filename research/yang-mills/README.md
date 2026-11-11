# Yang–Mills — proposed answer, exact intermediate proofs, and open examination

Author: Terry Allen Snyder (V.A. / URK research lineage)  
Release date: 11 November 2026  
Public record: https://deagletwc.github.io/va-proof-estate/yang-mills.html

This is a **publicly released, author-proposed affirmative answer**, with exact finite-lattice SU(2) results, sourced mathematical derivations, and reproducible bounded checks. The mathematical and numerical carriers in this release **do not establish the unrestricted four-dimensional quantum Yang–Mills existence and positive mass-gap theorem**, and do not assert recognition by a prize committee.

## Files

- `Snyder_Yang_Mills_Proposed_Answer_and_Proofs_2026-11-11.pdf`: public-reader manuscript with equations and proof sketches.
- `.md`, `.html`: exact same manuscript content in editable and web form.
- `02_SOURCE_PROOFS/`: unchanged original mathematical stage notes (Stages 49, 53, 54, 69, 70, 71, 72, 73, 78, 79). These are historical documents with their own dated claims, not independent certification of every theorem.
- `03_REPRODUCIBILITY/`: exact Stage 72 ledger/results, preserved Stage 79 results, original Stage 79 verifier (needs unreleased parent archives) and a standalone public Python verifier.
- `STAGE_LINEAGE_INDEX.csv`: chronological source index, not a proof certificate.
- `PUBLIC_RELEASE_MANIFEST.json`, `SHA256SUMS.txt`: custody and exact file checksums.

## Replay

Run with Python 3 and no third-party packages:

```
cd 03_REPRODUCIBILITY
python verify_public_incidence.py
```

The public verifier reconstructs 12 graph/source checks and 2 file-identity checks and asserts 14/14; these are **new public bounded checks**. The original Stage 79 verifier previously passed 14/14 against the archived parent ZIPs; original check labels differ. Do **not** treat either count as proving Wilson-measure covariance decay or a physical spectral gap.

The original private URK generators and nested master archives are not distributed by this public package. The public ledger is finite combinatorial graph data, not a native computational kernel.

## Assessment boundary

The source proof of the coarea and covariance identities, and the arithmetic and graph evidence, can be examined separately. The full positive continuum gap requires additional mathematically established hypotheses, including nontrivial continuum reconstruction and uniform physical correlation decay for the reconstructed theory. These are identified as *not proved in this package*. A proof gap is not repaired by a checksum or by the working Navier–Stokes-specialized harmonic edge-rate generator.

Independent readers are invited to point to precise equations, propose counterexamples, supply missing derivations or reproduce the bounded calculations. GitHub issues: https://github.com/DeagleTWC/va-proof-estate/issues
