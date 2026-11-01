#!/usr/bin/env python3
"""Verify public release identity, retained checksum lineage, and format separation.

This does not evaluate the protected True Zero/NEW-K mathematical substrate.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEX_SHA = re.compile(r"^[a-f0-9]{64}$")


def validate(root=ROOT):
    root = Path(root)
    errors = []

    def load(path):
        try:
            return (root / path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"Unreadable {path}: {exc}")
            return ""

    try:
        manifest = json.loads(load("proof-estate-manifest.json"))
    except (ValueError, TypeError) as exc:
        return [f"Invalid release manifest JSON: {exc}"]
    version = manifest.get("release")
    edition = manifest.get("edition")
    declared_sha = manifest.get("mainFileSHA256", "")
    html = load("index.html")
    if not HEX_SHA.fullmatch(str(declared_sha)):
        errors.append("Current website SHA-256 is absent or invalid")
    if hashlib.sha256(html.encode("utf-8")).hexdigest() != declared_sha:
        errors.append("Website source differs from manifest byte digest")

    if manifest.get("versionDisambiguation", {}).get("publicationRelease") != version:
        errors.append("Manifest versionDisambiguation publication release is stale")
    if manifest.get("versionDisambiguation", {}).get("publicationEdition") != edition:
        errors.append("Manifest publication edition is stale")

    for needle in (
        f"PUBLIC-SAFE · V{version}",
        f"Edition {edition}",
        f"{version} / edition {edition}",
        f"bounded entries · edition {edition}",
        f"V.A. Public Proof Estate v{version}",
        f"V.A. — The Proof Estate v{version}",
        f"V.A. Proof Estate v{version}",
    ):
        if needle not in html:
            errors.append(f"Public homepage/export lacks current release identity: {needle}")

    for path, needle in (
        ("foundation.html", f"WEBSITE RELEASE {version}"),
        ("README.md", f"website release {version} / edition {edition}"),
        ("proofs/VERSION-IDENTITY.md", f"release {version} / edition {edition}"),
        ("proofs/MILESTONE-LEDGER.md", f"website release {version} / edition {edition}"),
    ):
        if needle not in load(path):
            errors.append(f"{path} lacks current release identity: {needle}")

    history = manifest.get("releaseHistory", [])
    previous = manifest.get("previousWebsiteRelease", {})
    if not isinstance(history, list) or not history:
        errors.append("Retained website release history absent")
    else:
        if len({record.get("release") for record in history}) != len(history):
            errors.append("Release history duplicates a version")
        for record in history:
            if not HEX_SHA.fullmatch(str(record.get("mainFileSHA256", ""))):
                errors.append(f"Invalid retained release checksum: {record.get('release')}")
            if record.get("release") == version:
                errors.append("Current release must not duplicate an archived release")
        recent = history[-1]
        for key, value in (
            ("release", recent.get("release")),
            ("edition", recent.get("edition")),
            ("mainFileSHA256", recent.get("mainFileSHA256")),
        ):
            if previous.get(key) != value:
                errors.append(f"Previous release is inconsistent with retained history: {key}")
        if previous.get("preservedInGitHistory") is not True:
            errors.append("No declared preservation of previous release")

    if manifest.get("versionDisambiguation", {}).get("challengePacketSchema") != (
        "VA-CHALLENGE-2.0 (stable format; distinct from website release)"
    ):
        errors.append("Challenge schema and website release identity conflated")
    if "schemaVersion:'VA-CHALLENGE-2.0'" not in html:
        errors.append("Old challenge schema was incorrectly changed or removed")
    if manifest.get("systemVersionReference", {}).get("designation") != "V12":
        errors.append("Native V.A. system version was accidentally changed")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for p in problems:
            print("RELEASE ERROR:", p)
        raise SystemExit(1)
    print("PASS: public release, checksum lineage, format identity and native-version separation")
