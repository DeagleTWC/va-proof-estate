# Classical Navier–Stokes — open mathematical source and bounded reproducibility

Author: Terry Allen Snyder  
Public release date: 2026-11-08  

## Mathematical manuscript

`Snyder_Classical_Navier_Stokes_Proof_Extract_11pp.pdf` is **exactly the original rendered pages 5–15** of the original 80-page correlated proof reader. Those pages form **Part A, classical formulation and proof sequence**, with unchanged printed theorem numbers, equations, and mathematical statements. The original 80-page source reader is not published as part of this public-safe classical release because it includes separate native mathematics.

`ORIGINAL_PART_II_CLASSICAL_TEX_EXCERPT.tex` is an exact-text extraction of the manuscript's original *Part II* LaTeX source, excluding native Part I and constructed Part III. It is a partial source with original cross-references and is provided for reading/source comparison; it is **not** claimed to compile independently.

This release does not supply a native NEW K / URK kernel, operators, generators, or protected construction.

## Conventional numerical reproduction

The file `05_REPRODUCIBILITY/independent_midpoint_replay.py` reconstructs **finite** 122- and 250-mode periodic Fourier-Galerkin examples and compares against the 16-step saved endpoint records. The results are **bounded computational evidence**, not a proof of unrestricted global regularity or an original URK implementation.

From the extracted release directory:

```bash
python -m pip install -r 05_REPRODUCIBILITY/requirements-replay.txt
python 05_REPRODUCIBILITY/independent_midpoint_replay.py --output independent_replay_result.json
```

The saved comparisons and six-mode seed are included verbatim from the November 8 repaired referee archive. The original protected generator and native proof sources are deliberately omitted.

## Examination and standing

Review the complete stated hypotheses, definitions, equations, and proofs against the original mathematical manuscript. Reviewers should cite the specific theorem or equation and provide derivations or counterexamples when reporting an alleged defect. This is an author-produced open artifact, with an independent-review invitation; neither Clay recognition nor journal acceptance nor third-party certification is claimed.

Hashes in `SHA256SUMS.txt` cover the exact released files. Bibliographic DOI: **not assigned**.
