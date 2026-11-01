#!/usr/bin/env python3
"""Static public safety-surface negative controls."""
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_static_public_safety import ROOT, PUBLIC_PAGES, validate


class StaticSafetySurfaceTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="va-public-safety-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for name in PUBLIC_PAGES:
            shutil.copy2(ROOT / name, self.root / name)

    def inject(self, text):
        index = self.root / "index.html"
        content = index.read_text(encoding="utf-8")
        index.write_text(content.replace("</body>", text + "\n</body>", 1), encoding="utf-8")

    def test_public_pages_use_no_outbound_runtime(self):
        self.assertEqual(validate(self.root), [])

    def test_external_script_rejected(self):
        self.inject('<script src="https://third.example/track.js"></script>')
        self.assertTrue(any("externally loaded script" in e for e in validate(self.root)))

    def test_fetch_rejected(self):
        self.inject('<script>fetch("https://third.example/upload", {method:"POST"})</script>')
        self.assertTrue(any("outbound runtime primitive" in e for e in validate(self.root)))

    def test_telemetry_rejected(self):
        self.inject('<script>navigator.sendBeacon("https://third.example", "x")</script>')
        self.assertTrue(any("outbound runtime primitive" in e for e in validate(self.root)))

    def test_hidden_form_upload_rejected(self):
        self.inject('<form method="post" action="https://third.example/submit"></form>')
        self.assertTrue(any("network submission" in e for e in validate(self.root)))

    def test_iframe_rejected(self):
        self.inject('<iframe src="https://third.example"></iframe>')
        self.assertTrue(any("embedded active content" in e for e in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
