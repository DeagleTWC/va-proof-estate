#!/usr/bin/env python3
"""Check public GitHub carriers and declared limits; never infer native proof."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def verify():
    manifest = read_json("proof-estate-manifest.json")
    index = ROOT / manifest["mainFile"]
    current_sha = hashlib.sha256(index.read_bytes()).hexdigest()
    assert current_sha == manifest["mainFileSHA256"], (
        f"Website release checksum mismatch: {current_sha}"
    )

    register = read_json("proofs/CLAIM-TO-CARRIER.json")
    assert register["canonicalRepository"] == "DeagleTWC/va-proof-estate"
    entries = register["entries"]
    ids = [r["id"] for r in entries]
    assert len(ids) == len(set(ids)), "Duplicate claim ID"
    assert "VA-AD-001" in ids
    assert all(r["standing"] in (
        "DECLARED", "OBSERVED", "INDEPENDENTLY REPRODUCED"
    ) for r in entries)

    for record in entries:
        carrier = record.get("carrier")
        if carrier is not None:
            path = ROOT / carrier.split("#", 1)[0]
            assert path.is_file(), f"Missing registered carrier: {carrier}"
        assert record.get("nativeVAEvidence") is False or (
            record["standing"] != "DECLARED" and carrier is not None
        ), f"Native evidence cannot promote without an attached carrier: {record['id']}"
        if record["class"] == "challenge-specification":
            assert record["standing"] == "DECLARED"

    fixture = next(r for r in entries if r["id"] == "VA-AD-001")
    assert fixture["class"] == "synthetic-fixture"
    assert fixture["standing"] == "OBSERVED"
    assert fixture["nativeVAEvidence"] is False
    assert (ROOT / fixture["record"]).is_file()
    fixture_file_sha = hashlib.sha256(
        (ROOT / fixture["carrier"]).read_bytes()
    ).hexdigest()
    fixture_manifest = next(
        x for x in manifest["publicExaminerFixtures"] if x["id"] == "VA-AD-001"
    )
    assert fixture_manifest["sourceSHA256"] == fixture_file_sha

    native_carriers = [
        e for e in entries if e.get("nativeVAEvidence")
        and e["standing"] in ("OBSERVED", "INDEPENDENTLY REPRODUCED")
    ]
    assert manifest["nativeRuntimeReceiptsAttached"] <= len(native_carriers)
    assert manifest["publicEvidenceStatus"] == "DECLARED" or native_carriers, (
        "Native public status promoted without a native carrier"
    )
    print(f"PASS: {len(entries)} registered objects, checksum, carriers and standing ceilings")
    print(f"PUBLIC NATIVE RECEIPTS IN MANIFEST: {manifest['nativeRuntimeReceiptsAttached']}")


if __name__ == "__main__":
    verify()
