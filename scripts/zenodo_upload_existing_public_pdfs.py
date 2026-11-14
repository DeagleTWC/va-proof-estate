#!/usr/bin/env python3
"""Upload the two already-public mathematical manuscripts to their EXISTING Zenodo drafts.
Does not create records or publish. Verification prevents substituting other files.
"""
import hashlib
import os
import pathlib
import sys
import requests

API = "https://zenodo.org/api"
ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGETS = {
    "grid-k1": (
        24194644,
        "research/grid-k1/Snyder_GRID_K1_Infrastructure_Continuity_Formal_Proofs_2026-11-11.pdf",
        "57ae364ba9ddc398ac8b8b02c19ad04ed0ec2c1b3478d28d642e677412308ddc",
        320368,
        "GRID-K1",
    ),
    "adg": (
        24194875,
        "research/admissibility-debt-geometry/Snyder_Admissibility_Debt_Geometry_Formal_Proofs_2026-11-11.pdf",
        "d5efe3dd89c8a7cca5e097292a8276df7884383d7ec0154a81f7d9b5ebe81e57",
        302294,
        "Admissibility",
    ),
}

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in TARGETS:
        raise SystemExit("Select one of: grid-k1 or adg")
    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        raise SystemExit("Missing ZENODO_TOKEN; no upload attempted")

    target_id, file_rel, expected_sha, expected_size, title_word = TARGETS[sys.argv[1]]
    path = ROOT / file_rel
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    if len(data) != expected_size or sha != expected_sha:
        raise SystemExit("Source bytes failed frozen release-manifest SHA-256/size; upload ABORTED.")

    sess = requests.Session()
    sess.headers.update({
        "Authorization": "Bearer " + token,
        "User-Agent": "VA-Proof-Estate-Zenodo-Transfer/1.0 (+https://github.com/DeagleTWC/va-proof-estate)",
    })
    resp = sess.get(f"{API}/deposit/depositions/{target_id}", timeout=45)
    resp.raise_for_status()
    draft = resp.json()
    title = draft.get("metadata", {}).get("title", "")
    if title_word.lower() not in title.lower():
        raise SystemExit(f"Wrong record title for target {target_id}; upload ABORTED.")
    if draft.get("submitted") or draft.get("state") in ("done", "published", "submitted"):
        raise SystemExit("Deposit is already published; do not alter it.")
    existing = draft.get("files") or []
    name = path.name
    previous = [f for f in existing if f.get("filename", f.get("key", f.get("name"))) == name]
    if previous:
        print("Already listed in draft:", name)
    else:
        bucket = draft.get("links", {}).get("bucket", "")
        if not bucket.startswith("https://zenodo.org/api/files/"):
            raise SystemExit("Missing authenticated Zenodo file-bucket URL.")
        result = sess.put(
            f"{bucket}/{name}",
            data=data,
            headers={"Content-Type": "application/pdf"},
            timeout=120,
        )
        if result.status_code not in (200, 201):
            print("Upload HTTP status:", result.status_code, result.text[:600])
            raise SystemExit("Zenodo rejected file PUT.")
        file_result = result.json()
        if int(file_result.get("size", -1)) != len(data):
            raise SystemExit("Zenodo uploaded byte count mismatch; STOP.")
        print("Uploaded", file_result.get("key"), file_result.get("size"), "bytes")

    verified = sess.get(f"{API}/deposit/depositions/{target_id}/files", timeout=45)
    verified.raise_for_status()
    files = verified.json()
    hits = [f for f in files if f.get("filename", f.get("key", f.get("name"))) == name]
    if not hits:
        raise SystemExit("Uploaded PDF absent from Zenodo file listing.")
    found = hits[0]
    remote_bytes = found.get("filesize", found.get("size"))
    if int(remote_bytes) != expected_size:
        raise SystemExit("Zenodo file size differs from original.")
    remote_checksum = str(found.get("checksum", "")).split(":")[-1]
    if remote_checksum and remote_checksum != hashlib.md5(data).hexdigest():
        raise SystemExit("Zenodo remote file checksum differs from original.")
    print("UPLOAD VERIFIED: draft", target_id)
    print("File:", name)
    print("Size:", expected_size, "SHA-256:", sha)
    print("Draft URL:", f"https://zenodo.org/uploads/{target_id}")
    print("Publication deliberately not triggered here; verify copyright settings in Zenodo UI.")

if __name__ == "__main__":
    main()
