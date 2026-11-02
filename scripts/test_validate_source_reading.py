"""Source reader negative-control tests."""
from pathlib import Path
import tempfile
import shutil
import unittest
from validate_source_reading import ROOT, validate

class ReaderTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(prefix="va-reader-")
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        for n in ("source-reading.html","foundation.html","reviewer-route.html"):
            shutil.copy2(ROOT/n,self.root/n)
        for n in ROOT.rglob("*"):
            if n.is_file() and n.suffix in (".md",".json") and n.is_relative_to(ROOT):
                rel=n.relative_to(ROOT)
                target=self.root/rel
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text("fixture",encoding="utf-8")
        shutil.copy2(ROOT/"index.html",self.root/"index.html")
        shutil.copy2(ROOT/"end-to-end.html",self.root/"end-to-end.html")

    def test_current_reader(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_original_is_detected(self):
        (self.root/"proofs/CLAIM-TO-CARRIER.json").unlink()
        self.assertTrue(any("missing or unsafe" in e for e in validate(self.root)))

    def test_skip_navigation_required(self):
        p=self.root/"foundation.html"
        s=p.read_text(encoding="utf-8")
        p.write_text(s.replace('href="#main">Skip to main content','href="#invalid">Skip to main content'),encoding="utf-8")
        self.assertTrue(any("keyboard skip" in e for e in validate(self.root)))

if __name__=="__main__":
    unittest.main()
