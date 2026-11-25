#!/usr/bin/env python3
"""Verify the frozen public-safe New K Hodge lattice child, without native GEN.

This is an exact, source-bound Fermat-quintic software audit. It does not
authenticate a protected generator or prove unrestricted Hodge.
"""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARCHIVE = ROOT / "research/hodge/NEWK_HODGE_LATTICE_CLOSURE_CHILD_V1_2026-11-25.zip"
ARCHIVE_SHA256 = "ee0d52bbe2cb5498c2aafc1e578e266dec5f4d72d614f05f2fe753bf320cb1e4"
EXPECTED_TESTS = 39
FROZEN_RECEIPTS = {
    "carry": ("newk_lattice_closure_v1", "CARRY", 0),
    "reexamine": ("newk_lattice_changed_v1", "REEXAMINE", 2),
    "refuse": ("newk_lattice_wrong_anchor_v1", "REFUSE", 3),
}


class VerificationError(Exception):
    """An asserted public witness failed a required check."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def checked_zip_extract(archive: Path, destination: Path) -> None:
    with ZipFile(archive) as source:
        for info in source.infolist():
            member = PurePosixPath(info.filename)
            mode = info.external_attr >> 16
            require(
                not member.is_absolute()
                and ".." not in member.parts
                and member.parts[:1] == ("HISTORY_KERNEL_V1",)
                and not stat.S_ISLNK(mode),
                "unsafe ZIP member: " + info.filename,
            )
        source.extractall(destination)


def run(command: list[str], cwd: Path, expected_exit: int, label: str) -> str:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    require(
        result.returncode == expected_exit,
        f"{label} exit {result.returncode}, expected {expected_exit}: "
        + (result.stdout + result.stderr)[-1800:],
    )
    return result.stdout + result.stderr


def verify(archive: Path) -> None:
    require(archive.is_file(), "archive not found: " + str(archive))
    require(sha256_file(archive) == ARCHIVE_SHA256, "archive SHA-256 mismatch")

    with TemporaryDirectory(prefix="hodge-public-proof-") as temp:
        temporary = Path(temp)
        checked_zip_extract(archive, temporary)
        child = temporary / "HISTORY_KERNEL_V1"
        manifest = read_json(child / "NEWK_LATTICE_CLOSURE_MANIFEST.json")
        public_manifest = ROOT / "research/hodge/NEWK_LATTICE_CLOSURE_MANIFEST.json"
        if public_manifest.exists():
            require(read_json(public_manifest) == manifest, "published manifest differs from frozen ZIP")

        require(manifest["generated_geometric_planes"] == 1875, "plane count changed")
        require(manifest["galois_orbit_count"] == 480, "orbit count changed")
        require(manifest["gram_dimension"] == 401, "Gram dimension changed")
        require(manifest["determinant_modulus"] == 1009, "modulus changed")
        require(manifest["determinant_residue"] == 437, "Gram determinant changed")
        require(manifest["unrestricted_hodge_proof_established_by_this_child"] is False,
                "unrestricted status silently changed")
        require(manifest["protected_gen1056_authenticated"] is False,
                "protected GEN status silently changed")

        test_output = run(
            [sys.executable, "-m", "unittest", "discover", "-p", "test_*.py"],
            child, 0, "39-test regression",
        )
        require(re.search(r"Ran 39 tests\b", test_output) is not None and
                re.search(r"^OK$", test_output, re.MULTILINE) is not None,
                "expected 39 passing tests were not observed")

        source_sha = manifest["source_sha256"]
        ledger_sha = manifest["identifier_ledger_sha256"]
        for case, (frozen_name, gate, exit_code) in FROZEN_RECEIPTS.items():
            prefix = temporary / ("replayed_" + case)
            trusted_ledger = "0" * 64 if case == "refuse" else ledger_sha
            flags = [
                "--trusted-source-sha", source_sha,
                "--trusted-ledger-sha", trusted_ledger,
                "--output-prefix", str(prefix),
            ]
            run_flags = list(flags)
            if case == "reexamine":
                run_flags.extend(["--conditions-json", "newk_lattice_changed_conditions.json"])
            output = run(
                [sys.executable, "lattice_closure_cli.py", "run", *run_flags],
                child, exit_code, case + " gate",
            )
            require("LATTICE_GATE " + gate in output, case + " gate output mismatch")

            issued = read_json(Path(str(prefix) + "_receipt.json"))
            frozen = read_json(child / (frozen_name + "_receipt.json"))
            require(issued == frozen, case + " receipt differs from frozen witness")
            require(issued["sha256"] == manifest["receipt_sha256"][case],
                    case + " receipt commitment mismatch")

            exact = read_json(Path(str(prefix) + "_exact_evidence.json"))
            frozen_exact = read_json(child / (frozen_name + "_exact_evidence.json"))
            require(exact == frozen_exact, case + " exact evidence differs from frozen witness")

            replay_output = run(
                [sys.executable, "lattice_closure_cli.py", "replay", *flags],
                child, 0, case + " replay",
            )
            require("LATTICE_REPLAY_OK" in replay_output, case + " replay failed")

        print("HODGE_PUBLIC_AUDIT PASS 39/39 CARRY=0 REEXAMINE=2 REFUSE=3 REPLAYS=3/3")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    args = parser.parse_args()
    try:
        verify(args.archive)
    except (VerificationError, OSError, ValueError, KeyError, RuntimeError) as exc:
        print("HODGE_PUBLIC_AUDIT REFUSE: " + str(exc), file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
