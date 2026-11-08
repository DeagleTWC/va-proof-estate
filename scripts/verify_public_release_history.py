#!/usr/bin/env python3
"""Recompute published website checksums from pinned Git source commits.

Only publication byte identity is tested. This does not establish native V.A.
runtime execution, physical consequence, or protected True Zero/NEW-K mathematics.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA1 = re.compile(r"^[a-f0-9]{40}$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")


def validate(root=ROOT):
    root = Path(root).resolve()
    problems = []
    try:
        manifest = json.loads((root / "proof-estate-manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"Cannot read publication manifest: {exc}"]

    history = manifest.get("releaseHistory", [])
    items = []
    if not isinstance(history, list):
        problems.append("Release history is not a list")
        history = []
    items.extend((x.get("release"), x.get("indexSourceCommit"), x.get("mainFileSHA256"))
                 for x in history if isinstance(x, dict))
    items.append((manifest.get("release"), manifest.get("currentIndexSourceCommit"),
                  manifest.get("mainFileSHA256")))
    for version, commit, expected in items:
        if not isinstance(commit, str) or not SHA1.fullmatch(commit):
            problems.append(f"Missing/invalid pinned source commit for {version}")
            continue
        if not isinstance(expected, str) or not SHA256.fullmatch(expected):
            problems.append(f"Missing/invalid SHA-256 for {version}")
            continue
        try:
            raw = subprocess.run(["git", "show", f"{commit}:index.html"], cwd=root,
                                 capture_output=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError) as exc:
            problems.append(f"Unable to read Git source for {version}: {exc}")
            continue
        measured = hashlib.sha256(raw).hexdigest()
        if measured != expected:
            problems.append(f"Historic source digest mismatch for {version}: {measured}")
    try:
        current = hashlib.sha256((root / "index.html").read_bytes()).hexdigest()
        if current != manifest.get("currentSiteIndexSHA256", manifest.get("mainFileSHA256")):
            problems.append("Current website source differs from current publication digest")
    except OSError as exc:
        problems.append(f"Missing current index: {exc}")
    prior = manifest.get("previousWebsiteRelease", {})
    if history and (
        prior.get("indexSourceCommit") != history[-1].get("indexSourceCommit")
        or prior.get("mainFileSHA256") != history[-1].get("mainFileSHA256")
    ):
        problems.append("Previous release does not match latest archived original")
    return problems


if __name__ == "__main__":
    errors = validate()
    if errors:
        for error in errors:
            print("RELEASE CHAIN FAILURE:", error)
        raise SystemExit(1)
    print("PASS: all archived and current publication digests recomputed from original pinned Git commits")
