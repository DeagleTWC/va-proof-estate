# Deagle Mathematics — Admissibility–Debt Geometry

**Author:** Terry Allen Snyder · V.A. / Deagle  
**Dated public research record:** 11 November 2026 · Version 1.0

This release formalizes the author's original `MATH SOLUTIONS.txt` and preserves it byte-for-byte in `source/`. The manuscript states the mathematical model, exact theorems and proofs, precise conditions, and worked examples. The original source and the formalization are separate and traceable through the crosswalk.

The exact-rational example scripts use Python's standard library and are public-safe reference calculations—not a claim to reproduce a protected URK generator. The general theorems are proved in the manuscript; the five example-specific certificates and five linked receipts record the exact worked calculations.

## Reproduction

From the extracted folder, run:

```
python reproducibility/verify_exact_output.py
```

This performs read-only verification of source identity, preparation contract, five exact rational witnesses, certificates, receipt chain, and a tamper negative control. To generate a *new*, separately identified run, use `python reproducibility/run_exact_examples.py` in a copy; do not overwrite this release's original output.

## Mathematical scope

The mathematical claims are the stated conditional model theorems. Physical collapse, unconditional Lyapunov stability, signal-noise performance, and any application to a specific physical system require further corresponding hypotheses. The author's original statements are preserved unchanged.

## Custody

`PUBLIC_RELEASE_MANIFEST.json` and `SHA256SUMS.txt` bind the released PDF, evidence ZIP, and source. The release is offered for mathematical examination through the Deagle Proof Estate.
