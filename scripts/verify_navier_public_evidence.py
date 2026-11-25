#!/usr/bin/env python3
"""Recompute the four public Navier--Stokes evidence groups without changing sources.

This is a source-custody and finite-evidence verifier, not a theorem prover or
an authentication of private NEW K/URK code.  Its outputs are CI review
artifacts; a successful test run does not establish continuum regularity.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1] / "research" / "navier-stokes"

# Immutable baselines: historical Nov 8 / Nov 11 source assets plus the
# published Nov 21/24 public-safe child tests. Intentional updates require
# an explicit versioned review of these byte seals.
SOURCE_SHA256 = {
    "04_EVIDENCE_AND_TECHNICAL_SUPPLEMENTS/GEN_122_Mode_16_Step_Recorded_Output.json":
        "6330de1dfa73873f42b65c56dee1cabd7be5137f9c78a40317abef71b428c5a5",
    "04_EVIDENCE_AND_TECHNICAL_SUPPLEMENTS/GEN_250_Mode_16_Step_Recorded_Output.json":
        "8e4e6afb4df034eda02c795c67c01a029bed9877110ccaac0def7a8fdaf840de",
    "04_PUBLIC_COMPANION/urk_harmonic_edge_input.json":
        "9ed1612238f7685cdf250fe2e79191279d84974665c37120b52dccf8f1fa9692",
    "04_PUBLIC_COMPANION/urk_harmonic_edge_rates.py":
        "baad535857070231eabcadcbb13b5b44f365fee2568fb2cbf75a4eaf1ad167e8",
    "04_PUBLIC_COMPANION/urk_harmonic_edge_rates_example.json":
        "3be2cad99b8b66441b9ca62a3db7dfec53a59bc56201f8636556076282496258",
    "05_REPRODUCIBILITY/independent_midpoint_replay.py":
        "541d51c98b486d48f0240faa63d6ecca7821887a64efd33963d9e0c3d3e149b3",
    "05_REPRODUCIBILITY/original_edge_rate_input_unmodified.json":
        "9ed1612238f7685cdf250fe2e79191279d84974665c37120b52dccf8f1fa9692",
    "05_REPRODUCIBILITY/test_urk_movement_kernel_v1.py":
        "96ed878ab6fbf71a821c4f897393595783df06ff3a4c6524a749943ce47d22c5",
    "05_REPRODUCIBILITY/urk_movement_kernel_v1.py":
        "8ef5bd1cc9a653d64ac5372dc87c7c0e1c0000ae8901a6d1aac0f540472f0fca",
    "VERIFY_PUBLIC_EDGE_WITNESS.py":
        "e2b9ec5f7ebd78e732cfb75f66e2342de1c777e267a77ace45e6487188596f38",
    "refinement_countermodel.py":
        "fcda9ffd0d50408215e3c2d87f464253f2fba203c8cfac25b0b8b155873e4f1c",
    "test_refinement_countermodel.py":
        "232653165c856c938dd92210f1e0321982f17a8b55d573bcc99754ce0916885c",
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def validate_source_tree(root: Path) -> dict[str, str]:
    """Reject incomplete or changed candidates before running any mathematics."""
    present = {}
    for rel, expected in SOURCE_SHA256.items():
        source = root / rel
        if not source.is_file():
            raise ValueError(f"missing public Navier source: {rel}")
        actual = digest(source)
        if actual != expected:
            raise ValueError(f"SHA-256 mismatch for {rel}: {actual} != {expected}")
        present[rel] = actual
    return present


def validate_unittest_result(log: str, expected: int) -> int:
    """A zero-test or silently shortened suite must not count as a pass."""
    match = re.search(r"(?m)^Ran (\d+) tests? in [^\n]+", log)
    if not match or int(match.group(1)) != expected or not re.search(r"(?m)^OK\s*$", log):
        raise ValueError(f"expected {expected} successful unittest cases")
    return expected


def validate_edge_receipt(receipt: dict) -> int:
    checks = receipt.get("checks")
    if (receipt.get("passed") != 11 or receipt.get("total") != 11
            or not isinstance(checks, dict) or len(checks) != 11
            or not all(value is True for value in checks.values())
            or "no unrestricted NS proof" not in receipt.get("classification", "")):
        raise ValueError("expected 11 passing bounded edge checks")
    return 11


def validate_midpoint_receipt(receipt: dict) -> int:
    counts = receipt.get("counts", {})
    checks = receipt.get("checks")
    scope = receipt.get("scope", "")
    if (receipt.get("status") != "PASS" or
            counts != {"passed": 17, "failed": 0, "total": 17}
            or not isinstance(checks, list) or len(checks) != 17
            or not all(c.get("passed") is True for c in checks)
            or not scope.startswith("Independent finite-mode Galerkin midpoint reconstruction")
            or "not the original trajectory integrator" not in scope
            or not scope.endswith("or a continuum regularity proof")):
        raise ValueError("expected 17 checks with finite-only scope; scope promotion refused")
    return 17


def run_command(root: Path, *args: str) -> str:
    process = subprocess.run([sys.executable, *args], cwd=root, capture_output=True,
                             text=True, check=True)
    return process.stdout + process.stderr


def emit_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def build_public_receipts(root: Path, output_dir: Path) -> dict:
    """Create seven source-bound review files, or fail closed."""
    root = root.resolve()
    output_dir = output_dir.resolve()
    hashes = validate_source_tree(root)
    output_dir.mkdir(parents=True, exist_ok=False)

    edge_text = run_command(root, "VERIFY_PUBLIC_EDGE_WITNESS.py")
    edge = json.loads(edge_text)
    edge_count = validate_edge_receipt(edge)
    (output_dir / "edge.json").write_text(edge_text, encoding="utf-8")

    movement_log = run_command(root, "-m", "unittest", "discover",
                               "-s", "05_REPRODUCIBILITY",
                               "-p", "test_urk_movement_kernel_v1.py", "-v")
    movement_count = validate_unittest_result(movement_log, 19)
    (output_dir / "movement-tests.log").write_text(movement_log, encoding="utf-8")

    refinement_log = run_command(root, "-m", "unittest", "-v",
                                 "test_refinement_countermodel.py")
    refinement_count = validate_unittest_result(refinement_log, 4)
    (output_dir / "refinement-tests.log").write_text(refinement_log, encoding="utf-8")

    run_command(root, "05_REPRODUCIBILITY/independent_midpoint_replay.py",
                "--output", str(output_dir / "midpoint.json"))
    midpoint = json.loads((output_dir / "midpoint.json").read_text())
    midpoint_count = validate_midpoint_receipt(midpoint)

    movement_receipt = run_command(root, "05_REPRODUCIBILITY/urk_movement_kernel_v1.py",
                                   "--demo")
    again = run_command(root, "05_REPRODUCIBILITY/urk_movement_kernel_v1.py", "--demo")
    if movement_receipt != again:
        raise ValueError("exact movement receipt failed byte-identical replay")
    movement = json.loads(movement_receipt)
    if (movement.get("standing") != "RUN" or
            movement.get("scope") != "FINITE_GALERKIN_IDENTITY" or
            movement.get("unrestricted_proof") is not False or
            movement.get("native_parent_authenticated") is not False or
            movement.get("energy_balance_residual") != "0"):
        raise ValueError("movement receipt failed exact finite-scope standing")
    receipt_path = output_dir / "movement-receipt.json"
    receipt_path.write_text(movement_receipt, encoding="utf-8")
    replay_line = run_command(root, "05_REPRODUCIBILITY/urk_movement_kernel_v1.py",
                              "--verify", str(receipt_path))
    if f"REPLAY VERIFIED {movement['receipt_sha256']}" not in replay_line:
        raise ValueError("movement receipt was not independently replayed")

    emit_json(output_dir / "source-sha256.json", hashes)
    checks = {
        "edge": edge_count, "movement": movement_count,
        "refinement": refinement_count, "midpoint": midpoint_count,
        "passed": edge_count + movement_count + refinement_count + midpoint_count,
        "total": 51,
    }
    summary = {
        "schema": "va.ns.public-source-evidence-ci/v1",
        "standing": "FINITE_PUBLIC_EVIDENCE_ONLY",
        "native_generator_authenticated": False,
        "unrestricted_regularity_certified": False,
        "source_commit": os.environ.get("GITHUB_SHA"),
        "source_sha256": hashes,
        "checks": checks,
        "receipt_sha256": {name: digest(output_dir / name) for name in (
            "edge.json", "midpoint.json", "movement-receipt.json",
            "movement-tests.log", "refinement-tests.log", "source-sha256.json",
        )},
    }
    emit_json(output_dir / "audit-summary.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt-dir", type=Path, required=True)
    arguments = parser.parse_args()
    result = build_public_receipts(ROOT, arguments.receipt_dir)
    print(f"Navier public source replay: {result['checks']['passed']}/"
          f"{result['checks']['total']} checks PASS; "
          f"receipt directory {arguments.receipt_dir}")
