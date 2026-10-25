#!/usr/bin/env python3
"""Synthetic ZIP-custody tampering regressions; contains no historical V.A. original bytes."""
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from verify_historical_v12_zip import verify_zip, digest, canonical

ROOT_NAME = "SYNTHETIC_BUILD_V1_2_NOT_HISTORICAL"


def encode(obj):
    return (json.dumps(obj, indent=2) + "\n").encode("utf-8")


def make_case(cid, index, previous):
    outcome = "EXECUTE" if index == 0 else "REFUSE"
    binds = outcome == "EXECUTE"
    dec = {"case_id": cid, "boundary_decision_id": "decision-" + cid,
           "boundary_outcome": outcome, "consequence_binds": binds}
    rec = {"case_id": cid, "receipt_id": "receipt-" + cid,
           "boundary_decision_id": dec["boundary_decision_id"],
           "boundary_outcome": outcome, "prev_receipt_hash": previous,
           "replay_determinant": digest(cid.encode("utf-8"))}
    rec["receipt_hash"] = digest(canonical(rec))
    rep = {"case_id": cid, "receipt_id": rec["receipt_id"],
           "replay_determinant": rec["replay_determinant"],
           "expected_boundary_outcome": outcome, "replayed_boundary_outcome": outcome,
           "replay_match": True}
    return dec, rec, rep


def originals():
    ids = ["synthetic-" + str(i) for i in range(8)]
    boundaries, receipts, replays = [], [], []
    previous = "GENESIS"
    for i, cid in enumerate(ids):
        d, r, v = make_case(cid, i, previous)
        previous = r["receipt_hash"]
        boundaries.append(d); receipts.append(r); replays.append(v)
    files = {
        "corridor_registry.json": encode({"corridor": "synthetic"}),
        "policy_registry.json": encode({"policy": "synthetic"}),
        "fixtures/fixture_set_v1.json": encode({"cases": [{"case_id": c} for c in ids]}),
        "outputs/boundary_results.json": encode(boundaries),
        "outputs/enforcement_receipts.json": encode(receipts),
        "outputs/replay_records.json": encode(replays),
        "reports/V1_2_certificate_verification_report.json":
            encode({"package_status": "PASS", "verifier_exit_code": 0, "tamper_test_exit_code": 0}),
        "verify_package.py": b"# inert synthetic test placeholder, not executable\n",
        "tamper_test.py": b"# inert synthetic test placeholder, not executable\n",
        "schemas/synthetic.json": encode({"kind": "fixture"})
    }
    mapping = {
        "corridor_registry_hash": "corridor_registry.json",
        "policy_registry_hash": "policy_registry.json",
        "hash_fixture_set": "fixtures/fixture_set_v1.json",
        "hash_boundary_results": "outputs/boundary_results.json",
        "hash_receipt_chain": "outputs/enforcement_receipts.json",
        "hash_replay_results": "outputs/replay_records.json",
        "hash_verification_report": "reports/V1_2_certificate_verification_report.json",
        "hash_verify_package_script": "verify_package.py",
        "hash_tamper_test_script": "tamper_test.py",
    }
    manifest = {k: digest(files[v]) for k, v in mapping.items()}
    schema_digest = {"synthetic.json": digest(files["schemas/synthetic.json"])}
    manifest["hash_schemas"] = digest(canonical(schema_digest))
    manifest["frozen_contract_version"] = "DEPLOY_BUILD_V1_2"
    files["manifest.json"] = encode(manifest)
    return files


def write_archive(path, files, duplicate=False):
    with ZipFile(path, "w", ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(ROOT_NAME + "/" + name, data)
        if duplicate:
            z.writestr(ROOT_NAME + "/manifest.json", files["manifest.json"])


def reject(path, desc):
    try:
        verify_zip(path)
    except (ValueError, KeyError, TypeError):
        return
    raise AssertionError("Fail-closed regression accepted " + desc)


def main():
    with tempfile.TemporaryDirectory(prefix="synthetic-v12-archive-") as d:
        temp = Path(d)
        files = originals()
        correct = temp / "synthetic-valid.zip"
        write_archive(correct, files)
        result = verify_zip(correct)
        assert result["caseCount"] == 8
        assert result["manifestEntryHashesChecked"] == 10
        assert result["receiptHashChainRecomputed"]
        assert result["observedRealWorldEffect"] is False
        assert result["independentWitnessAuthenticated"] is False
        checks = [
            ("tampered boundary source", "outputs/boundary_results.json",
             lambda f: f.update({"outputs/boundary_results.json": b'[]'})),
            ("tampered receipt source", "outputs/enforcement_receipts.json",
             lambda f: f.update({"outputs/enforcement_receipts.json": b'[]'})),
            ("tampered replay source", "outputs/replay_records.json",
             lambda f: f.update({"outputs/replay_records.json": b'[]'})),
            ("tampered original verification script", "verify_package.py",
             lambda f: f.update({"verify_package.py": b'changed script'})),
            ("tampered report", "reports/V1_2_certificate_verification_report.json",
             lambda f: f.update({"reports/V1_2_certificate_verification_report.json": b'{}'})),
            ("missing original receipt", "outputs/enforcement_receipts.json",
             lambda f: f.pop("outputs/enforcement_receipts.json")),
            ("unknown original contract", "manifest.json",
             lambda f: f.update({"manifest.json": encode({**json.loads(f["manifest.json"]), "frozen_contract_version": "V12"})})),
        ]
        for i, (label, unused, change) in enumerate(checks):
            altered = dict(files)
            change(altered)
            out = temp / f"bad-{i}.zip"
            write_archive(out, altered)
            reject(out, label)
        dup = temp / "duplicate.zip"
        from warnings import catch_warnings, simplefilter
        with catch_warnings():
            simplefilter("ignore", UserWarning)
            write_archive(dup, files, duplicate=True)
        reject(dup, "duplicate archive member")
        p = temp / "traversal.zip"
        with ZipFile(p, "w") as z:
            z.writestr(ROOT_NAME + "/../../escape.txt", b"synthetic")
        reject(p, "ZIP traversal")
        print("PASS: synthetic ZIP structural carrier and ten original hash entries")
        print("PASS: nine invalid source/receipt/replay/control/ZIP variants refused")
        print("PASS: zero native, real-world, customer-pilot or independent witness promotion")


if __name__ == "__main__":
    main()
