#!/usr/bin/env python3
"""Deterministically reconcile the public classical-only research ZIP with its hosted manifest.

No private source or native NEW K / URK material is read or published.
This script runs only on the already public research/navier-stokes files.
"""
from __future__ import annotations
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "research" / "navier-stokes"
MANIFEST = FOLDER / "PUBLIC_RELEASE_MANIFEST.json"
PUBLIC_ZIP = FOLDER / "Deagle_Navier_Stokes_Classical_Public_2026-11-08.zip"
ARTICLE = ROOT / "navier-stokes.html"
INDEX = ROOT / "research" / "mathematics" / "INDEX.json"

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def dump(o: dict) -> bytes:
    return (json.dumps(o, indent=2, ensure_ascii=False) + "\n").encode("utf-8")

def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    old_digest = manifest["published_zip_sha256"]
    assert re.fullmatch("[0-9a-f]{64}", old_digest), "Expected previous archive checksum"
    assert manifest["release_page_selection"].startswith("Original correlated PDF pages 5"), "Expected classical-only scope"
    required = dict(manifest["files"])
    citation = (FOLDER / "CITATION.cff").read_bytes()
    required["CITATION.cff"] = {"sha256": sha256(citation), "bytes": len(citation)}
    for rel, evidence in required.items():
        assert "native" not in rel.lower() and "URK" not in rel.upper(), rel
        fp = FOLDER / rel
        assert fp.is_file(), f"Missing public-source file: {rel}"
        data = fp.read_bytes()
        assert sha256(data) == evidence["sha256"] and len(data) == evidence["bytes"], f"Unmatched evidence: {rel}"

    embedded = json.loads(json.dumps(manifest))
    embedded["files"] = required
    embedded["published_zip_sha256"] = None
    embedded["published_zip_git_blob_sha1"] = None
    embedded["archive_digest_location"] = "Published website PUBLIC_RELEASE_MANIFEST.json (self-hash is intentionally excluded from the ZIP to avoid circular references)"
    embedded["publication_status"] = manifest["publication_status"]

    members = sorted(set(required) | {"PUBLIC_RELEASE_MANIFEST.json", "SHA256SUMS.txt"})
    with zipfile.ZipFile(PUBLIC_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in members:
            payload = dump(embedded) if rel == "PUBLIC_RELEASE_MANIFEST.json" else (FOLDER / rel).read_bytes()
            meta = zipfile.ZipInfo(rel, date_time=(2026, 11, 8, 0, 0, 0))
            meta.compress_type = zipfile.ZIP_DEFLATED
            meta.external_attr = (0o644 << 16)
            z.writestr(meta, payload, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    actual = PUBLIC_ZIP.read_bytes()
    digest = sha256(actual)
    blob_sha1 = hashlib.sha1(b"blob " + str(len(actual)).encode() + b"\0" + actual).hexdigest()
    manifest["files"] = required
    manifest["published_zip_sha256"] = digest
    manifest["published_zip_git_blob_sha1"] = blob_sha1
    manifest["archive_digest_location"] = "Public site manifest only; the ZIP's embedded manifest sets published_zip_sha256 to null to avoid a circular checksum."
    MANIFEST.write_bytes(dump(manifest))

    html = ARTICLE.read_text(encoding="utf-8")
    assert html.count(old_digest) == 1, "Expected one exact prior ZIP digest in article"
    ARTICLE.write_text(html.replace(old_digest, digest), encoding="utf-8")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    entry = next(x for x in index["entries"] if x["id"] == "navier-stokes-2026-11-08")
    assert entry["supporting_archive_sha256"] == old_digest, "Expected matching prior register digest"
    entry["supporting_archive_sha256"] = digest
    INDEX.write_bytes(dump(index))

    with zipfile.ZipFile(PUBLIC_ZIP) as z:
        assert set(z.namelist()) == set(members), "Published member set mismatch"
        assert json.loads(z.read("PUBLIC_RELEASE_MANIFEST.json"))["publication_status"] == manifest["publication_status"]
        for rel, e in required.items():
            data = z.read(rel)
            assert sha256(data) == e["sha256"], f"Archive member mismatch: {rel}"
    assert digest == sha256(PUBLIC_ZIP.read_bytes()), "Archive digest mismatch"
    assert digest in ARTICLE.read_text(encoding="utf-8"), "Article digest mismatch"
    print(f"PASS: reconciled {len(members)} safe public files; ZIP SHA-256={digest}; Git blob SHA-1={blob_sha1}")

if __name__ == "__main__":
    main()
