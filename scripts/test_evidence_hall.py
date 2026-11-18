"""Public-safe Hall contract tests; no private runtime or network access."""

import json
import pathlib
import shutil
import tempfile
import unittest
from html.parser import HTMLParser

from validate_evidence_hall import validate_hall


ROOT = pathlib.Path(__file__).resolve().parents[1]


class HallParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = {}
        self.hrefs = []
        self.sigil = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("data-exhibit"):
            self.sections[attrs["data-exhibit"]] = attrs.get("data-standing")
        if tag == "a" and "href" in attrs:
            self.hrefs.append(attrs["href"])
        if tag == "svg" and attrs.get("aria-label") == "Official V.A. mark":
            self.sigil = True


class EvidenceHallTests(unittest.TestCase):
    def test_hall_contains_five_source_bound_exhibits(self):
        register = json.loads((ROOT / "proofs/EVIDENCE-HALL-REGISTER.json").read_text())
        parser = HallParser()
        html = (ROOT / "evidence-hall.html").read_text()
        parser.feed(html)
        self.assertEqual(len(register["exhibits"]), 5)
        self.assertEqual(set(parser.sections), {item["id"] for item in register["exhibits"]})
        self.assertTrue(all(v == "DECLARED" for v in parser.sections.values()))
        self.assertTrue(parser.sigil)
        self.assertIn("va-gold-design.css", html)
        self.assertIn("VA-AD-001", html)
        self.assertIn("in-process mock", html)
        self.assertIn("not native V.A.", html)
        self.assertIn("INDEPENDENTLY REPRODUCED", html)
        for item in register["exhibits"]:
            for source in item["sources"]:
                self.assertIn(source["path"], parser.hrefs)
        self.assertTrue(all(not h.startswith(("http:", "https:", "//")) for h in parser.hrefs))

    def test_homepage_exposes_gold_hall_in_navigation_and_hero(self):
        home = (ROOT / "index.html").read_text()
        nav = home.split('<nav class="navlinks"', 1)[1].split("</nav>", 1)[0]
        hero = home.split('<section class="hero"', 1)[1].split("</section>", 1)[0]
        self.assertIn('href="evidence-hall.html"', nav)
        self.assertIn('href="evidence-hall.html"', hero)

    def test_validator_rejects_unwarranted_independent_promotion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self._copy_fixture(root)
            register_path = root / "proofs/EVIDENCE-HALL-REGISTER.json"
            data = json.loads(register_path.read_text())
            data["exhibits"][0]["standing"] = "INDEPENDENTLY REPRODUCED"
            register_path.write_text(json.dumps(data))
            errors = validate_hall(root)
            self.assertTrue(any("unqualified evidence" in e for e in errors), errors)

    def test_validator_rejects_external_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self._copy_fixture(root)
            register_path = root / "proofs/EVIDENCE-HALL-REGISTER.json"
            data = json.loads(register_path.read_text())
            data["exhibits"][1]["sources"][0]["path"] = "https://example.org/source"
            register_path.write_text(json.dumps(data))
            errors = validate_hall(root)
            self.assertTrue(any("nonlocal source" in e for e in errors), errors)

    def test_validator_accepts_complete_local_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self._copy_fixture(root)
            self.assertEqual(validate_hall(root), [])

    def test_validator_refuses_incorrect_recorded_mock_effect(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self._copy_fixture(root)
            path = root / "proofs/VA-AD-001/local-fixture-report.json"
            report = json.loads(path.read_text())
            report["cases"][2]["observed_mock_effect"] = True
            path.write_text(json.dumps(report))
            self.assertTrue(any("recorded mock observation mismatch" in e for e in validate_hall(root)))

    @staticmethod
    def _copy_fixture(root):
        for path in ["proofs/EVIDENCE-HALL-REGISTER.json", "evidence-hall.html", "evidence-hall.css", "va-gold-design.css"]:
            dest = root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            if (ROOT / path).exists():
                shutil.copyfile(ROOT / path, dest)
            else:
                dest.write_text("")
        data = json.loads((root / "proofs/EVIDENCE-HALL-REGISTER.json").read_text())
        for item in data["exhibits"]:
            for source in item["sources"]:
                dest = root / source["path"]
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text("fixture source")
        for field in ("record", "runner", "verifier"):
            dest = root / data["fixture"][field]
            dest.parent.mkdir(parents=True, exist_ok=True)
            source = ROOT / data["fixture"][field]
            if source.exists():
                shutil.copyfile(source, dest)
            else:
                dest.write_text("fixture source")


if __name__ == "__main__":
    unittest.main()
