#!/usr/bin/env python3
"""Negative controls for public static asset byte identity and metadata."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_public_media_assets import ROOT, validate

INPUTS = ["index.html", "proof-estate-manifest.json",
          "favicon.png", "apple-touch-icon.png", "social-card-1200x630.jpg"]


class PublicMediaChecks(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="va-media-checks-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for path in INPUTS:
            shutil.copy2(ROOT / path, self.root / path)

    def test_current_public_assets(self):
        self.assertEqual(validate(self.root), [])

    def test_tampered_social_jpeg_is_rejected(self):
        path = self.root / "social-card-1200x630.jpg"
        data = path.read_bytes()
        path.write_bytes(data + b"tampered")
        self.assertTrue(any("SHA-256 differs" in x for x in validate(self.root)))

    def test_wrong_published_dimensions_are_rejected(self):
        path = self.root / "proof-estate-manifest.json"
        obj = json.loads(path.read_text(encoding="utf-8"))
        obj["socialPreview"]["sizePixels"] = [640, 480]
        path.write_text(json.dumps(obj), encoding="utf-8")
        self.assertTrue(any("dimensions" in x for x in validate(self.root)))

    def test_corrupted_favicon_is_rejected(self):
        (self.root / "favicon.png").write_bytes(b"not a png")
        self.assertTrue(any("Invalid PNG" in x for x in validate(self.root)))

    def test_missing_icon_is_rejected(self):
        (self.root / "apple-touch-icon.png").unlink()
        self.assertTrue(any("Missing public media asset" in x for x in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
