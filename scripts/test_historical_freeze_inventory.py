#!/usr/bin/env python3
"""Isolated regression for private historical inventory; test bytes are fabricated."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from historical_freeze_inventory import check_inventory, seal
from validate_historical_carriers import validate_entry

PROGRAM = Path(__file__).with_name("historical_freeze_inventory.py")


def run(*args, expect_ok=True):
    r = subprocess.run([sys.executable, str(PROGRAM), *map(str, args)],
                       text=True, capture_output=True, check=False)
    if expect_ok and r.returncode:
        raise AssertionError(f"Expected CLI success, got {r.returncode}: {r.stderr}")
    if not expect_ok and r.returncode == 0:
        raise AssertionError("Expected fail-closed CLI rejection")
    return r


def main():
    with tempfile.TemporaryDirectory(prefix="synthetic-inventory-test-") as temp:
        base = Path(temp)
        root = base / "synthetic-originals"
        root.mkdir()
        (root / "layer-a").mkdir()
        (root / "layer-b").mkdir()
        first = root / "layer-a" / "test-freeze.bin"
        second = root / "layer-b" / "test-receipt.txt"
        first.write_bytes(b"SYNTHETIC IN-MEMORY FREEZE TEST, NOT A HISTORICAL SOURCE\n")
        second.write_bytes(b"SYNTHETIC RECEIPT TEST, NOT AN ACTUAL PILOT\n")
        # One exact private inventory. No source bytes or filesystem timestamps exported.
        inventory = base / "private-inventory.json"
        run("scan", "--root", root, "--out", inventory)
        data = json.loads(inventory.read_text(encoding="utf-8"))
        entries = check_inventory(data)
        assert len(entries) == 2
        assert data["entryCount"] == 2
        assert data["notAnOriginalFreezeDate"] is True
        assert data["notAnHistoricalProofOrPilotCount"] is True
        assert data["entryManifestSHA256"] == seal(entries)
        assert "PRIVATE" in data["classification"]
        assert all("modified" not in json.dumps(e).lower() for e in entries)
        assert "SYNTHETIC RECEIPT TEST" not in inventory.read_text(encoding="utf-8")
        assert all(not Path(e["relativePath"]).is_absolute() for e in entries)
        # Private inventory must be created with restrictive POSIX permissions.
        assert (inventory.stat().st_mode & 0o077) == 0
        run("verify", "--root", root, "--inventory", inventory)
        run("scan", "--root", root, "--out", inventory, expect_ok=False)
        run("scan", "--root", root, "--out", root / "do-not-write.json", expect_ok=False)
        run("scan", "--root", root, "--out", base / "max-bound.json",
            "--max-files", "1", expect_ok=False)
        # Selecting a source creates only an incomplete private release candidate.
        candidate = base / "private-candidate.json"
        run("select", "--root", root, "--inventory", inventory,
            "--relative-path", "layer-a/test-freeze.bin", "--out", candidate)
        selected = json.loads(candidate.read_text(encoding="utf-8"))
        assert selected["original"]["originalSHA256"] == entries[0]["sha256"]
        assert selected["original"]["originalFreezeDate"] is None
        assert selected["publication"]["releaseAuthorizationId"] is None
        assert "PRIVATE DRAFT" in selected["instructions"]
        assert (candidate.stat().st_mode & 0o077) == 0
        try:
            validate_entry(selected, root)
        except (ValueError, KeyError, TypeError):
            pass
        else:
            raise AssertionError("Unreleased incomplete candidate was admitted")
        run("select", "--root", root, "--inventory", inventory,
            "--relative-path", "layer-a/test-freeze.bin", "--out", candidate, expect_ok=False)
        # Detect file mutation even if a prior manifest still has a valid internal checksum.
        first.write_bytes(b"SYNTHETIC FILE TAMPER")
        run("verify", "--root", root, "--inventory", inventory, expect_ok=False)
        run("select", "--root", root, "--inventory", inventory,
            "--relative-path", "layer-a/test-freeze.bin", "--out", base / "bad-candidate.json",
            expect_ok=False)
        first.write_bytes(b"SYNTHETIC IN-MEMORY FREEZE TEST, NOT A HISTORICAL SOURCE\n")
        run("verify", "--root", root, "--inventory", inventory)
        # Detect integrity-corrupted private inventory.
        altered = json.loads(inventory.read_text(encoding="utf-8"))
        altered["entries"][0]["sha256"] = "0" * 64
        tampered = base / "tampered-inventory.json"
        tampered.write_text(json.dumps(altered), encoding="utf-8")
        run("verify", "--root", root, "--inventory", tampered, expect_ok=False)
        run("select", "--root", root, "--inventory", tampered,
            "--relative-path", "layer-a/test-freeze.bin", "--out", base / "bad2.json",
            expect_ok=False)
        # No symlink traversal, even when the link refers to a file inside the selected root.
        (root / "linked-original").symlink_to(first)
        run("scan", "--root", root, "--out", base / "symlink-inventory.json", expect_ok=False)
        (root / "linked-original").unlink()
        print("PASS: offline inventory with synthetic originals, stable hashing and private output permissions")
        print("PASS: modification, inventory tamper, unsafe output, overwrite, symlink, file cap and false promotion all refused")


if __name__ == "__main__":
    main()
