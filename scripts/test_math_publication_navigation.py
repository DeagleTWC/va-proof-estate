"""Public math navigation should lead to its latest exact Hodge carriers.

This checks reader-visible publication routes, not the mathematical theorem.
"""

from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
CURRENT_ZIP = "research/hodge/NEWK_HODGE_LATTICE_CLOSURE_CHILD_V1_2026-11-25.zip"
CURRENT_FORMAL = "research/hodge/NEWK_LATTICE_CLOSURE_FORMAL_2026-11-25.md"
CURRENT_RECIPE = "research/hodge/HODGE_LATTICE_PUBLIC_REPRODUCTION_RECIPE_2026-11-25.md"
CURRENT_CI = "https://github.com/DeagleTWC/va-proof-estate/actions/workflows/hodge-public-evidence.yml"


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def _hrefs(html_or_markdown: str) -> list[str]:
    return re.findall(r'href="([^"]+)"', html_or_markdown)


class _IdReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.identifiers: set[str] = set()

    def handle_starttag(self, tag, attrs):
        self.identifiers.update(value for key, value in attrs if key == "id" and value)


class MathPublicationNavigationTests(unittest.TestCase):
    def test_publication_map_exposes_current_hodge_carriers(self):
        # Regression: the 14 Nov map omitted Hodge entirely despite a live Hodge page.
        published = _read("research-publication.html")
        articles = re.findall(r'<article class="card">([\s\S]*?)</article>', published)
        hodge = next((article for article in articles if re.search(r"<h3>\s*Hodge", article)), None)
        self.assertIsNotNone(hodge, "publication map must include an actual Hodge research card")
        links = _hrefs(hodge)
        for expected in ("hodge.html", CURRENT_ZIP, CURRENT_FORMAL, CURRENT_RECIPE, CURRENT_CI):
            self.assertIn(expected, links, f"missing Hodge publication route: {expected}")
        for link in links:
            if link.startswith("https://"):
                continue
            self.assertTrue((ROOT / urlsplit(link).path).is_file(), f"broken map link: {link}")

    def test_review_crosswalk_contains_current_and_original_hodge_carriers(self):
        desk = _read("research/mathematics/REVIEW-CROSSWALK.md")
        lines = [line for line in desk.splitlines() if line.startswith("|")]
        current = [line for line in lines if "Hodge" in line and "2026-11-25" in line]
        self.assertEqual(len(current), 1, "a single current Hodge row should be reviewable")
        for file in (CURRENT_FORMAL, CURRENT_RECIPE, CURRENT_ZIP):
            self.assertIn(Path(file).name, current[0])
        self.assertIn("39/39", current[0])
        self.assertIn(CURRENT_CI, current[0])
        self.assertTrue(any("Hodge - exact bounded answer" in line and "2026-11-24" in line
                            for line in lines), "keep the previous bounded edition separately identifiable")

    def test_publication_status_points_to_the_latest_hodge_run(self):
        status = _read("research/mathematics/PUBLICATION-STATUS.md")
        current = [line for line in status.splitlines()
                   if line.startswith("|") and "Hodge" in line and "2026-11-25" in line]
        self.assertEqual(len(current), 1, "current published Hodge carrier missing from publication register")
        self.assertIn(Path(CURRENT_ZIP).name, current[0])
        self.assertIn("39/39", current[0])
        self.assertIn("hodge-public-evidence.yml", current[0])
        self.assertIn("Hodge - Exact Bounded Answer (2026-11-24)", status)

    def test_hodge_site_has_valid_local_navigation_anchors(self):
        site = _read("hodge.html")
        reader = _IdReader()
        reader.feed(site)
        self.assertIn("hodge-newk-lattice-closure-child-v1", reader.identifiers)
        self.assertIn("Author claim:", site)
        for target in _hrefs(site):
            if target.startswith("#"):
                self.assertIn(target[1:], reader.identifiers)
            elif target.startswith("research/hodge/"):
                self.assertTrue((ROOT / urlsplit(target).path).is_file(), f"broken Hodge file: {target}")

    def test_mirrored_lattice_archive_has_declared_original_hash(self):
        index = json.loads(_read("research/mathematics/INDEX.json"))
        child = next(row["newk_lattice_closure_child_v1"] for row in index["entries"]
                     if row.get("id") == "hodge-bounded-2026-11-24")
        archive = ROOT / CURRENT_ZIP
        observed = hashlib.sha256(archive.read_bytes()).hexdigest()
        self.assertEqual(observed, "ee0d52bbe2cb5498c2aafc1e578e266dec5f4d72d614f05f2fe753bf320cb1e4")
        self.assertEqual(observed, child["archive_sha256"])
        self.assertEqual(child["tests_passed"], 39)
        self.assertFalse(child["native_GEN_1056_authenticated"])


if __name__ == "__main__":
    unittest.main()
