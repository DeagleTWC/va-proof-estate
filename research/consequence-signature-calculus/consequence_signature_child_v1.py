#!/usr/bin/env python3
"""Public, exact-rational model child for the preserved CSC binding rule.

The declared finite viability corridor and derivative readings are inputs, not
measurements or claims of access to a sealed/native generator. No external
consequence is executed by this program.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


SOURCE_NAME = "Universal_Resolving_Structure_Consequence_Signature_Calculus_v1_2026-04-30.pdf"
SOURCE_SHA256 = "e17250eca29c37e708b131795f43431510e4ae8e49dafcaaa6fc92f48a766e61"
SCHEMA = "va.csc.exact-model-child.v1"
DERIVATIVES = ("reserve", "admissibility", "authority", "viability", "breach", "coherence")
READINGS = ("capacity", "burden", "admissibility", "authority", "breach", "coherence", "minimum_coherence")
KEYS = set(READINGS) | {"state_id", "restart_id", "viable_by_restart", "derivatives"}


def _as_rational(value: Any, name: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise TypeError(f"{name}: exact integer or rational string required (no floats)")
    if isinstance(value, str) and (not value or any(c in value for c in ".eE")):
        raise ValueError(f"{name}: use an exact integer or rational p/q")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f"{name}: invalid rational") from error


def _rational_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _source_check(source_pdf: Path) -> None:
    # A local path alias may be used for the original bytes; the hash is authoritative.
    try:
        actual = hashlib.sha256(source_pdf.read_bytes()).hexdigest()
    except OSError as error:
        raise ValueError("source PDF unavailable") from error
    if actual != SOURCE_SHA256:
        raise ValueError(f"source PDF hash mismatch: expected {SOURCE_SHA256}, found {actual}")


def _normalize(candidate: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(candidate, dict) or set(candidate) != KEYS:
        raise ValueError("candidate fields must match the published child schema exactly")
    normalized: dict[str, Any] = {}
    for key in ("state_id", "restart_id"):
        value = candidate[key]
        if not isinstance(value, str) or not value:
            raise ValueError(f"{key}: nonempty identifier required")
        normalized[key] = value
    corridor = candidate["viable_by_restart"]
    if not isinstance(corridor, dict) or not corridor:
        raise ValueError("viable_by_restart: nonempty finite mapping required")
    viable: dict[str, list[str]] = {}
    for restart, states in corridor.items():
        if not isinstance(restart, str) or not restart:
            raise ValueError("restart identifier must be a nonempty string")
        if not isinstance(states, list) or any(not isinstance(s, str) or not s for s in states):
            raise ValueError("viable states must be a list of nonempty identifiers")
        viable[restart] = sorted(set(states))
    normalized["viable_by_restart"] = dict(sorted(viable.items()))
    for key in READINGS:
        normalized[key] = _rational_text(_as_rational(candidate[key], key))
    derivatives = candidate["derivatives"]
    if not isinstance(derivatives, dict) or set(derivatives) != set(DERIVATIVES):
        raise ValueError("all six named derivative readings are required")
    normalized["derivatives"] = {
        key: _rational_text(_as_rational(derivatives[key], f"derivatives.{key}"))
        for key in DERIVATIVES
    }
    return normalized


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def generate(candidate: dict[str, Any], *, source_pdf: Path | str | None = None) -> dict[str, Any]:
    """Recompute the original binding conjunction and independent warning rule."""
    source = Path(source_pdf) if source_pdf is not None else Path(__file__).with_name(SOURCE_NAME)
    _source_check(source)
    data = _normalize(candidate)
    numeric = {key: Fraction(data[key]) for key in READINGS}
    remaining = numeric["capacity"] - numeric["burden"]
    viable = data["state_id"] in data["viable_by_restart"].get(data["restart_id"], [])
    invariants = {
        "capacity_and_admissibility": remaining >= 0 and numeric["admissibility"] >= 0,
        "standing": numeric["authority"] == 1,
        "viability": viable,
        "breach": numeric["breach"] == 0,
        "coherence": numeric["coherence"] >= numeric["minimum_coherence"],
    }
    binding = all(invariants.values())
    warning_causes = [
        name for name in DERIVATIVES
        if (Fraction(data["derivatives"][name]) > 0 if name == "breach"
            else Fraction(data["derivatives"][name]) < 0)
    ]
    warning = bool(warning_causes)
    standing = "REFUSE" if not binding else "PAUSE" if warning else "BIND"
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "source": {"file": SOURCE_NAME, "sha256": SOURCE_SHA256, "pages": 6},
        "scope": "finite-declared exact-rational model; not a native generator or external consequence certificate",
        "native_generator_authenticated": False,
        "input": data,
        "signature": {
            "remaining_capacity": _rational_text(remaining),
            "admissibility": data["admissibility"],
            "authority": data["authority"],
            "viability": viable,
            "breach": data["breach"],
            "restart": data["restart_id"],
            "coherence": data["coherence"],
        },
        "invariants": invariants,
        "bind_criterion_satisfied": binding,
        "warning": warning,
        "warning_causes": warning_causes,
        "standing": standing,
    }
    receipt["receipt_sha256"] = hashlib.sha256(_canonical_json(receipt)).hexdigest()
    return receipt


def verify_receipt(receipt: dict[str, Any], *, source_pdf: Path | str | None = None) -> bool:
    """Only exact regeneration under the preserved source can validate a receipt."""
    try:
        if not isinstance(receipt, dict) or not isinstance(receipt.get("input"), dict):
            return False
        return generate(receipt["input"], source_pdf=source_pdf) == receipt
    except (TypeError, ValueError, OSError):
        return False


def example_candidates() -> dict[str, dict[str, Any]]:
    """Positive, revoked-standing, and falling-reserve negative controls."""
    valid = {
        "state_id": "x0", "restart_id": "r0", "viable_by_restart": {"r0": ["x0", "x1"]},
        "capacity": "7/2", "burden": "2", "admissibility": "0", "authority": "1",
        "breach": "0", "coherence": "5/4", "minimum_coherence": "1",
        "derivatives": {key: "0" for key in DERIVATIVES},
    }
    refused = json.loads(json.dumps(valid))
    refused["authority"] = "0"
    paused = json.loads(json.dumps(valid))
    paused["derivatives"]["reserve"] = "-1/10"
    return {"bind": valid, "refuse": refused, "pause": paused}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--demo", action="store_true", help="write three deterministic exact receipts")
    group.add_argument("--verify", type=Path, help="replay a saved receipt")
    parser.add_argument("--receipt-dir", type=Path)
    parser.add_argument("--source-pdf", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.demo:
            if args.receipt_dir is None:
                parser.error("--demo requires --receipt-dir")
            receipts = {
                label: generate(candidate, source_pdf=args.source_pdf)
                for label, candidate in example_candidates().items()
            }
            args.receipt_dir.mkdir(parents=True, exist_ok=False)
            for label, receipt in receipts.items():
                path = args.receipt_dir / f"{label}-receipt.json"
                path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                print(f"{receipt['standing']} {receipt['receipt_sha256']} {path}")
        else:
            if args.receipt_dir is not None:
                parser.error("--verify does not accept --receipt-dir")
            receipt = json.loads(args.verify.read_text(encoding="utf-8"))
            if not verify_receipt(receipt, source_pdf=args.source_pdf):
                raise ValueError("receipt replay mismatch or source custody failure")
            print(f"VERIFIED {receipt['standing']} {receipt['receipt_sha256']}")
        return 0
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
