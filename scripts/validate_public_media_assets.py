#!/usr/bin/env python3
"""Verify public images, site-icon identities and published social preview metadata.

Checks published static asset bytes only, never protected mathematics or runtime.
"""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPG_MAGIC = b"\xff\xd8"
SOF_MARKERS = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
ALLOWED_MEDIA = {"favicon.png", "apple-touch-icon.png", "social-card-1200x630.jpg"}


def jpeg_dimensions(content):
    if not content.startswith(JPG_MAGIC):
        raise ValueError("JPEG file signature missing")
    idx = 2
    while idx + 4 <= len(content):
        if content[idx] != 0xFF:
            idx += 1
            continue
        while idx < len(content) and content[idx] == 0xFF:
            idx += 1
        if idx >= len(content):
            break
        marker = content[idx]
        idx += 1
        if marker in {0xD8, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if marker in {0xD9, 0xDA}:
            break
        if idx + 2 > len(content):
            break
        length = int.from_bytes(content[idx:idx + 2], "big")
        if length < 2 or idx + length > len(content):
            raise ValueError("Invalid JPEG segment length")
        if marker in SOF_MARKERS:
            if length < 7:
                raise ValueError("Incomplete JPEG frame header")
            height, width = struct.unpack(">HH", content[idx + 3:idx + 7])
            if not height or not width:
                raise ValueError("Invalid JPEG dimensions")
            return width, height
        idx += length
    raise ValueError("No JPEG image frame dimensions found")


def validate(root=ROOT):
    root = Path(root)
    errors = []
    try:
        manifest = json.loads((root / "proof-estate-manifest.json").read_text(encoding="utf-8"))
        html = (root / "index.html").read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        return [f"Cannot inspect public media declarations: {exc}"]

    social = manifest.get("socialPreview", {})
    path = social.get("path")
    if path != "social-card-1200x630.jpg" or social.get("mimeType") != "image/jpeg":
        errors.append("Social media preview path/type differs from declared public image")
    if social.get("sizePixels") != [1200, 630]:
        errors.append("Declared preview dimensions drifted from published 1200x630 design")
    icons = manifest.get("siteIcons")
    if icons != ["favicon.png", "apple-touch-icon.png"]:
        errors.append("Site icon identities are missing or altered")

    for filename in ALLOWED_MEDIA:
        try:
            data = (root / filename).read_bytes()
        except OSError as exc:
            errors.append(f"Missing public media asset {filename}: {exc}")
            continue
        if filename.endswith(".png"):
            if len(data) < 24 or not data.startswith(PNG_MAGIC) or data[12:16] != b"IHDR":
                errors.append(f"Invalid PNG structure: {filename}")
                continue
            width, height = struct.unpack(">II", data[16:24])
            if not width or not height:
                errors.append(f"Invalid PNG dimensions: {filename}")
        else:
            sha = hashlib.sha256(data).hexdigest()
            if sha != social.get("sha256"):
                errors.append("Published social preview SHA-256 differs from actual JPEG bytes")
            try:
                measured = jpeg_dimensions(data)
                if list(measured) != social.get("sizePixels"):
                    errors.append(f"Social preview image dimensions differ: {measured}")
            except ValueError as exc:
                errors.append(f"Invalid public JPEG: {exc}")

    if social.get("path") not in ALLOWED_MEDIA:
        errors.append("Social preview references a file outside the fixed public media inventory")
    for declared in icons if isinstance(icons, list) else []:
        if declared not in ALLOWED_MEDIA:
            errors.append(f"Unreviewed icon path: {declared}")
    if "social-card-1200x630.jpg" not in html:
        errors.append("Public site does not reference its declared social preview")
    if "favicon.png" not in html:
        errors.append("Public site does not reference the site favicon")
    return errors


if __name__ == "__main__":
    failures = validate()
    for error in failures:
        print("PUBLIC MEDIA ERROR:", error)
    if failures:
        raise SystemExit(1)
    print("PASS: original public social-card hash, JPEG dimensions, PNG icons and declared media names")
