#!/usr/bin/env python3
"""Source-bound public math replay for Yang--Mills, ADG, fractions and P/NP.

Runs historical public-safe programs only in isolated temporary copies.
The output certifies reproducible finite evidence, not a native NEW K theorem.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile


REPO = Path(__file__).resolve().parents[1]
ADG = Path("research/admissibility-debt-geometry")
YANG = Path("research/yang-mills")
PNP = Path("research/p-versus-np")
EGYPTIAN = Path("math/egyptian-child")
ADG_ARCHIVE = "Snyder_Admissibility_Debt_Geometry_Source_Proofs_Witnesses_2026-11-11.zip"
ADG_ARCHIVE_SHA = "96683a83906d33bb1bbf37b4237f8c949e8624af620810e398c996c043ba8599"
ADG_SOURCE_SHA = "789779f75e72400ecb807019cb4c8a55cc5e08969cdcf2d5dc998621899efaa7"
YANG_LEDGER_SHA = "a6209231f4e5f7a14ea713c33910301c4fbfa194e89bb34355392d127cc24bc3"
YANG_ARCHIVED_SHA = "d2c99c3ac2026a1ffe2408c8c19d11c30dd60b45a9a3e6b19c4a51ffcde264e9"
YANG_REPLAY_SHA = "b08cc822ad22115648b14a05c3e6ddda387d8060aed66710a244fec3f0b8fe49"

YANG_FILES = [
    "verify_public_proof_chain.py",
    "URK_PROOF_CHAIN_STATUS.json",
    "03_REPRODUCIBILITY/verify_public_incidence.py",
    "03_REPRODUCIBILITY/STAGE72_MEDIATOR_LEDGER.json",
    "03_REPRODUCIBILITY/STAGE72_RESULTS.json",
    "03_REPRODUCIBILITY/STAGE79_ARCHIVED_RESULTS.json",
    "03_REPRODUCIBILITY/PUBLIC_REPLAY_RESULTS.json",
]
PNP_FILES = ["width_kernel_v3.py", "independent_verify_v3.py", "test_new_extension.py"]
EGYPTIAN_FILES = ["child_formula.mjs", "test_child_formula.mjs"]
SOURCE_FILES = (
    [str(ADG / ADG_ARCHIVE),
     str(ADG / "source/MATH_SOLUTIONS_original_unchanged.txt")] +
    [str(YANG / item) for item in YANG_FILES] +
    [str(YANG / "bridge-countermodel.py")] +
    [str(PNP / item) for item in PNP_FILES] +
    [str(EGYPTIAN / item) for item in EGYPTIAN_FILES]
)


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def run(args: list[str], cwd: Path) -> str:
    done = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if done.returncode:
        raise ValueError(f"public replay refused ({done.returncode}): {' '.join(args)}\n"
                         f"{(done.stdout + done.stderr)[-900:]}")
    return done.stdout + done.stderr


def copy_list(base: Path, target: Path, files: list[str]) -> None:
    for name in files:
        dest = target / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(base / name, dest)


def emit_json(path: Path, item: dict) -> None:
    path.write_text(json.dumps(item, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_adg_source_and_examples(repo: Path, work: Path,
                                   mirror: Path | None = None) -> dict:
    """Original archive stays immutable; LF mirror must match CRLF source exactly."""
    archive = repo / ADG / ADG_ARCHIVE
    if digest(archive.read_bytes()) != ADG_ARCHIVE_SHA:
        raise ValueError("ADG original ZIP SHA-256 mismatch")
    mirror = mirror or repo / ADG / "source/MATH_SOLUTIONS_original_unchanged.txt"
    with ZipFile(archive) as z:
        members = z.namelist()
        if not members or any(n.startswith("/") or ".." in Path(n).parts
                              or "\\" in n for n in members):
            raise ValueError("ADG original archive has an unsafe entry")
        original = z.read("source/MATH_SOLUTIONS_original_unchanged.txt")
        if digest(original) != ADG_SOURCE_SHA:
            raise ValueError("ADG frozen original source SHA-256 mismatch")
        if original.replace(b"\r\n", b"\n") != mirror.read_bytes():
            raise ValueError("ADG repository mirror differs beyond CRLF-to-LF normalization")
        with TemporaryDirectory() as temp:
            z.extractall(temp)
            verified = run([sys.executable,
                            str(Path(temp) / "reproducibility/verify_exact_output.py")],
                           cwd=Path(temp))
            if "PASS: source, contract, five exact rational examples, five certificates, five linked receipts, tamper rejection" not in verified:
                raise ValueError("ADG exact example gate did not report five linked receipts")
    return {
        "standing": "ORIGINAL_ZIP_CUSTODY_REPLAYED",
        "original_archive_sha256": ADG_ARCHIVE_SHA,
        "original_source_sha256": ADG_SOURCE_SHA,
        "repository_mirror_sha256": digest(mirror.read_bytes()),
        "repository_mirror_difference": "CRLF_TO_LF_ONLY",
        "exact_rational_witnesses": 5,
        "certificates": 5,
        "linked_receipts": 5,
        "negative_control": "REJECTED",
    }


def validate_yang_replay(result: dict) -> int:
    checks = result.get("checks")
    if (result.get("passed") != 14 or result.get("total") != 14 or
            not isinstance(checks, dict) or len(checks) != 14 or
            not all(value is True for value in checks.values()) or
            result.get("public_replay") is not True or
            "no continuum" not in result.get("scope", "")):
        raise ValueError("Yang-Mills expected all 14 finite incidence checks")
    return 14


def validate_egyptian_log(log: str) -> int:
    for item in ("# tests 4", "# pass 4", "# fail 0", "# skipped 0"):
        if re.search(r"(?m)^" + re.escape(item) + r"$", log) is None:
            raise ValueError("Egyptian public child needs four passing tests")
    return 4


def validate_pnp_report(result: dict) -> tuple[int, int]:
    if (result.get("independent_trace_replays") != 364
            or result.get("negative_controls_rejected") != 10
            or result.get("SAT") != 134 or result.get("UNSAT") != 230
            or result.get("historical_native_examinations_reexecuted") != 0
            or result.get("prior_v2_cases_reexecuted") != 0):
        raise ValueError("P-vs-NP requires 364 independent traces and 10 refusals")
    return 364, 10


def build_public_receipts(repo: Path, output: Path) -> dict:
    repo = repo.resolve()
    output = output.resolve()
    hashes = {}
    for name in SOURCE_FILES:
        source = repo / name
        if not source.is_file():
            raise ValueError(f"missing public math source: {name}")
        hashes[name] = digest(source.read_bytes())
    output.mkdir(parents=True, exist_ok=False)

    adg = verify_adg_source_and_examples(repo, output)
    emit_json(output / "adg-custody.json", adg)

    if hashes[str(YANG / "03_REPRODUCIBILITY/STAGE72_MEDIATOR_LEDGER.json")] != YANG_LEDGER_SHA:
        raise ValueError("Yang source mediator ledger changed")
    if hashes[str(YANG / "03_REPRODUCIBILITY/STAGE79_ARCHIVED_RESULTS.json")] != YANG_ARCHIVED_SHA:
        raise ValueError("Yang source Stage 79 recorded output changed")
    if hashes[str(YANG / "03_REPRODUCIBILITY/PUBLIC_REPLAY_RESULTS.json")] != YANG_REPLAY_SHA:
        raise ValueError("Yang archived public replay changed")
    with TemporaryDirectory() as temp:
        working = Path(temp)
        copy_list(repo / YANG, working, YANG_FILES)
        run([sys.executable, "verify_public_proof_chain.py"], working)
        generated = working / "03_REPRODUCIBILITY/PUBLIC_REPLAY_RESULTS.json"
        if generated.read_bytes() != (repo / YANG / "03_REPRODUCIBILITY/PUBLIC_REPLAY_RESULTS.json").read_bytes():
            raise ValueError("Yang archived replay is not byte-identical")
        yang = json.loads(generated.read_text())
        yang_count = validate_yang_replay(yang)
        (output / "yang-incidence.json").write_bytes(generated.read_bytes())

    bridge = run([sys.executable, str(repo / YANG / "bridge-countermodel.py")], repo)
    for line in ("n=2: local_rate=1, global_gap=0.5",
                 "n=10: local_rate=1, global_gap=0.1",
                 "n=1000: local_rate=1, global_gap=0.001"):
        if line not in bridge:
            raise ValueError("Yang spectral bridge countermodel missing expected limiting case")
    (output / "yang-bridge.log").write_text(bridge, encoding="utf-8")

    with TemporaryDirectory() as temp:
        working = Path(temp)
        copy_list(repo / EGYPTIAN, working, EGYPTIAN_FILES)
        egyptian_log = run(["node", "--test", "--test-reporter=tap",
                            "test_child_formula.mjs"], working)
    egyptian_count = validate_egyptian_log(egyptian_log)
    (output / "egyptian-tests.log").write_text(egyptian_log, encoding="utf-8")

    receipt_versions = []
    with TemporaryDirectory() as temp:
        for iteration in range(2):
            working = Path(temp) / f"pnp-{iteration}"
            copy_list(repo / PNP, working, PNP_FILES)
            run([sys.executable, "test_new_extension.py"], working)
            evidence = working / "evidence"
            report_bytes = (evidence / "new_test_report.json").read_bytes()
            receipt_bytes = (evidence / "new_receipts.json").read_bytes()
            report = json.loads(report_bytes)
            pnp_count, refusal_count = validate_pnp_report(report)
            receipts = json.loads(receipt_bytes)
            if len(receipts) != 364 or not all("receipt_sha256" in r for r in receipts):
                raise ValueError("P-vs-NP public receipt set incomplete")
            receipt_versions.append((report_bytes, receipt_bytes))
        if receipt_versions[0] != receipt_versions[1]:
            raise ValueError("P-vs-NP replay did not regenerate byte-identical receipts")
        (output / "pnp-new-receipts.json").write_bytes(receipt_versions[0][1])
        (output / "pnp-test-report.json").write_bytes(receipt_versions[0][0])

    counts = {
        "yang_incidence_checks": yang_count,
        "yang_bridge_cases": 3,
        "adg_exact_examples": adg["exact_rational_witnesses"],
        "egyptian_unit_tests": egyptian_count,
        "pnp_independent_traces": pnp_count,
        "pnp_adversarial_refusals": refusal_count,
        "total_public_observations":
            yang_count + 3 + adg["exact_rational_witnesses"] + egyptian_count
            + pnp_count + refusal_count,
    }
    summary = {
        "schema": "va.remaining-public-math-evidence-ci/v1",
        "standing": "PUBLIC_BOUND_EVIDENCE_ONLY",
        "native_newk_authenticated": False,
        "unrestricted_theorems_certified": False,
        "source_commit": os.environ.get("GITHUB_SHA"),
        "source_sha256": hashes,
        "counts": counts,
        "output_sha256": {name: digest((output / name).read_bytes()) for name in (
            "adg-custody.json", "yang-incidence.json", "yang-bridge.log",
            "egyptian-tests.log", "pnp-new-receipts.json", "pnp-test-report.json")},
    }
    emit_json(output / "audit-summary.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=REPO)
    args = parser.parse_args()
    result = build_public_receipts(args.repo_root, args.receipt_dir)
    print(f"Other public mathematical evidence: "
          f"{result['counts']['total_public_observations']} observations PASS; "
          f"seven review files in {args.receipt_dir}")
