#!/usr/bin/env python3
"""Offline historical source fingerprint inventory. Never creates original freeze evidence."""
import argparse
import hashlib
import json
import os
import re
import stat
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "va-private-historical-inventory/1.0"
DIGEST = re.compile(r"^[0-9a-f]{64}$")
# Files in these generated/tool folders are not treated as historical source candidates.
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}
BLOCK = 1024 * 1024


def require(ok, why):
    if not ok:
        raise ValueError(why)


def hash_file(path):
    h = hashlib.sha256()
    with path.open("rb") as src:
        for block in iter(lambda: src.read(BLOCK), b""):
            h.update(block)
    return h.hexdigest()


def canonical_entries(entries):
    return json.dumps(entries, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def seal(entries):
    return hashlib.sha256(canonical_entries(entries)).hexdigest()


def source_root(root):
    path = Path(root).absolute()
    require(not path.is_symlink(), "Root cannot be a symlink")
    require(path.is_dir(), "Select an existing directory that you control")
    return path.resolve()


def output_path(path, root):
    p = Path(path).absolute()
    require(not p.is_symlink(), "Output must not be a symlink")
    require(not p.resolve().is_relative_to(root), "Keep private inventory OUTSIDE the scanned original directory")
    require(p.parent.is_dir(), "Output parent directory does not exist")
    return p


def source_entries(root, max_files=10000, max_file_bytes=0):
    root = source_root(root)
    require(isinstance(max_files, int) and max_files > 0, "max-files must be positive")
    require(isinstance(max_file_bytes, int) and max_file_bytes >= 0, "max-file-bytes must be nonnegative")
    entries = []
    skipped_dirs = set()
    for directory, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dpath = Path(directory)
        kept = []
        for name in sorted(dirs):
            candidate = dpath / name
            require(not candidate.is_symlink(), "Symlinked directory refused: " + candidate.relative_to(root).as_posix())
            if name in SKIP_DIRS:
                skipped_dirs.add(name)
            else:
                kept.append(name)
        dirs[:] = kept
        for name in sorted(files):
            full = dpath / name
            require(not full.is_symlink(), "Symlinked file refused: " + full.relative_to(root).as_posix())
            info = full.stat()
            require(stat.S_ISREG(info.st_mode), "Nonregular source refused")
            if max_file_bytes:
                require(info.st_size <= max_file_bytes, "File exceeds declared scan bound: " + full.name)
            require(len(entries) < max_files, "More files than --max-files limit; no partial output written")
            before = (info.st_size, info.st_mtime_ns)
            digest = hash_file(full)
            afterstat = full.stat()
            after = (afterstat.st_size, afterstat.st_mtime_ns)
            require(before == after, "Source changed while being hashed; retry the scan")
            entries.append({
                "relativePath": full.relative_to(root).as_posix(),
                "sizeBytes": info.st_size,
                "sha256": digest,
            })
    entries.sort(key=lambda e: e["relativePath"])
    require(len({x["relativePath"] for x in entries}) == len(entries), "Repeated source file path")
    return entries, sorted(skipped_dirs)


def scan_payload(root, max_files=10000, max_file_bytes=0):
    entries, skipped = source_entries(root, max_files, max_file_bytes)
    return {
        "schema": SCHEMA,
        "classification": "PRIVATE_LOCAL_WORKING_INVENTORY_DO_NOT_POST",
        "sourceMaterial": "User-selected local directory; no bytes uploaded",
        "generatedAtUTC": datetime.now(timezone.utc).isoformat(),
        "notAnOriginalFreezeDate": True,
        "notAnHistoricalProofOrPilotCount": True,
        "status": "UNREVIEWED_LOCAL_FILE_FINGERPRINTS",
        "excludedGeneratedDirectories": skipped,
        "entryCount": len(entries),
        "entryManifestSHA256": seal(entries),
        "entries": entries,
        "warning": "Paths and digests may be sensitive. This private inventory must never be published or treated as a pilot result, pre-existing freeze proof, witness result, or release authority.",
    }


def check_inventory(payload):
    require(isinstance(payload, dict) and payload.get("schema") == SCHEMA, "Invalid private inventory schema")
    require(payload.get("classification") == "PRIVATE_LOCAL_WORKING_INVENTORY_DO_NOT_POST", "Private watermark missing")
    require(payload.get("notAnOriginalFreezeDate") is True, "Generation date misrepresented")
    require(payload.get("notAnHistoricalProofOrPilotCount") is True, "Inventory count misrepresented as historical work")
    data = payload.get("entries")
    require(isinstance(data, list) and payload.get("entryCount") == len(data), "Inventory entry count mismatch")
    require(data == sorted(data, key=lambda x: x["relativePath"]), "Inventory order changed")
    require(seal(data) == payload.get("entryManifestSHA256"), "Inventory manifest checksum mismatch")
    seen = set()
    for item in data:
        p = item["relativePath"]
        require(isinstance(p, str) and p and not p.startswith("/") and
                not Path(p).is_absolute() and ".." not in Path(p).parts and
                "\\" not in p, "Invalid relative source path")
        require(p not in seen, "Duplicate source path")
        seen.add(p)
        require(isinstance(item["sizeBytes"], int) and item["sizeBytes"] >= 0, "Invalid source byte count")
        require(isinstance(item["sha256"], str) and DIGEST.fullmatch(item["sha256"]), "Invalid file digest")
    return data


def write_private_exclusive(path, payload):
    encoded = (json.dumps(payload, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(encoded)
            out.flush()
            os.fsync(out.fileno())
    except BaseException:
        try:
            path.unlink()
        except OSError:
            pass
        raise


def run_scan(args):
    root = source_root(args.root)
    destination = output_path(args.out, root)
    require(not destination.exists(), "Refusing overwrite of any prior inventory")
    payload = scan_payload(root, args.max_files, args.max_file_bytes)
    check_inventory(payload)
    write_private_exclusive(destination, payload)
    print("PRIVATE inventory saved locally; file contents were not copied or uploaded")
    print("Indexed local files:", len(payload["entries"]))
    print("Entry-manifest SHA-256:", payload["entryManifestSHA256"])
    print("No original freeze date, pilot execution or witness standing established")


def load_inventory(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_verify(args):
    root = source_root(args.root)
    payload = load_inventory(args.inventory)
    prior = check_inventory(payload)
    current, skipped = source_entries(root, args.max_files, args.max_file_bytes)
    require(prior == current, "Source changed: added/removed files, changed bytes or renamed paths")
    require(payload["excludedGeneratedDirectories"] == skipped, "Excluded folder set has changed")
    print("PASS: all currently accessible selected local file fingerprints match private inventory")
    print("This does not establish the original historic freeze date or operational proof")


def run_select(args):
    root = source_root(args.root)
    destination = output_path(args.out, root)
    require(not destination.exists(), "Refusing overwrite of a previous candidate")
    payload = load_inventory(args.inventory)
    entries = check_inventory(payload)
    matches = [x for x in entries if x["relativePath"] == args.relative_path]
    require(len(matches) == 1, "Selected path not present in inventory")
    entry = matches[0]
    path = (root / entry["relativePath"]).resolve()
    require(path.is_relative_to(root) and path.is_file() and not (root / entry["relativePath"]).is_symlink(),
            "Selected file missing or link-based")
    require(hash_file(path) == entry["sha256"] and path.stat().st_size == entry["sizeBytes"],
            "Selected original bytes have changed")
    template = Path(__file__).resolve().parents[1] / "proofs/historical/CARRIER-ENTRY-TEMPLATE.json"
    candidate = json.loads(template.read_text(encoding="utf-8"))
    require(candidate["schema"] == "va-historical-carrier-entry/1.0", "Template identity changed")
    candidate["original"]["originalSHA256"] = entry["sha256"]
    candidate["instructions"] = (
        "PRIVATE DRAFT ONLY — the source fingerprint is locally rechecked, NOT established as a "
        "historical freeze. Original ID, freeze date, pilot outcome, custody, permission and public "
        "extract remain unverified. DO NOT UPLOAD this candidate."
    )
    write_private_exclusive(destination, candidate)
    print("PRIVATE draft entry prepared from locally rechecked source SHA-256")
    print("NOT AN ADMITTED PUBLIC CARRIER. Confirm original freeze and all release rights separately.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    a = sub.add_parser("scan", help="Create one private fingerprint inventory, no uploads")
    a.add_argument("--root", required=True)
    a.add_argument("--out", required=True)
    a.add_argument("--max-files", type=int, default=10000)
    a.add_argument("--max-file-bytes", type=int, default=0)
    a.set_defaults(func=run_scan)
    a = sub.add_parser("verify", help="Recheck current selected files against a prior private inventory")
    a.add_argument("--inventory", required=True)
    a.add_argument("--root", required=True)
    a.add_argument("--max-files", type=int, default=10000)
    a.add_argument("--max-file-bytes", type=int, default=0)
    a.set_defaults(func=run_verify)
    a = sub.add_parser("select", help="Create an incomplete PRIVATE release candidate for an explicitly selected file")
    a.add_argument("--inventory", required=True)
    a.add_argument("--root", required=True)
    a.add_argument("--relative-path", required=True)
    a.add_argument("--out", required=True)
    a.set_defaults(func=run_select)
    args = parser.parse_args()
    try:
        args.func(args)
    except (ValueError, FileNotFoundError, OSError, KeyError, json.JSONDecodeError) as error:
        parser.exit(2, "REFUSED: " + str(error) + "\n")


if __name__ == "__main__":
    main()
