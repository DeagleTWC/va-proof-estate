#!/usr/bin/env python3
"""Adversarial tests for the public hub's native-source-lineage boundary."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_native_source_lineage import ROOT, validate


REFERENCE_TEST_BLOB = "007f260076ceacab0ebb5a2de7525f97eb0af6e2"


class NativeSourceLineageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for name in (
            "index.html",
            "foundation.html",
            "end-to-end.html",
            "proof-estate-manifest.json",
            "proofs/VA-ORIGINAL-CAPABILITY-RECOVERY.json",
        ):
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, destination)

    def validate(self):
        return validate(self.root, reference_fingerprints=frozenset({REFERENCE_TEST_BLOB}))

    def test_current_hub_passes(self):
        self.assertEqual(self.validate()["reference_module_matches"], 0)

    def test_rejects_old_k_operating_floor_on_current_page(self):
        page = self.root / "end-to-end.html"
        original = page.read_text(encoding="utf-8")
        self.assertIn("NEW corrected K", original)
        page.write_text(original.replace("NEW corrected K", "old K", 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "NEW K|old K"):
            self.validate()

    def test_rejects_html_encoded_old_k_even_with_new_k_elsewhere(self):
        page = self.root / "end-to-end.html"
        original = page.read_text(encoding="utf-8")
        self.assertIn("The current V.A. computational foundation is NEW corrected K", original)
        tampered = original.replace(
            "The current V.A. computational foundation is NEW corrected K",
            "The current V.A. computational foundation is old&nbsp;K",
            1,
        )
        page.write_text(tampered, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "old K"):
            self.validate()

    def test_rejects_old_k_manifest_substitution(self):
        path = self.root / "proof-estate-manifest.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        record["publicReviewerRoute"]["primaryFoundation"] = "old K"
        path.write_text(json.dumps(record), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "foundation"):
            self.validate()

    def test_rejects_exact_reference_module_bytes(self):
        (self.root / "copied_module.py").write_bytes(b"synthetic-shared-reference")
        with self.assertRaisesRegex(ValueError, "byte-matched reference"):
            self.validate()

    def test_rejects_symlinked_python_source(self):
        (self.root / "bytes.data").write_bytes(b"synthetic-shared-reference")
        (self.root / "native.py").symlink_to("bytes.data")
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.validate()

    def test_rejects_outside_source_promoted_as_native(self):
        path = self.root / "proofs/VA-ORIGINAL-CAPABILITY-RECOVERY.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["sourceReferences"][0]["nativeVAEvidence"] = True
        path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "outside source"):
            self.validate()

    def test_allows_unrelated_source_and_historical_math(self):
        (self.root / "unrelated.py").write_text("print('local')\n", encoding="utf-8")
        math_archive = self.root / "research/mathematics/legacy.md"
        math_archive.parent.mkdir(parents=True)
        math_archive.write_text("Historical old K discussion stays original.\n", encoding="utf-8")
        self.assertEqual(self.validate()["reference_module_matches"], 0)


if __name__ == "__main__":
    unittest.main()
