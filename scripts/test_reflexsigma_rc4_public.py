#!/usr/bin/env python3
"""Public exhibit consistency and no-false-promotion controls."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PublicReflexSigmaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.meta = json.loads((ROOT / 'reflexsigma-rc4/PUBLIC_EVIDENCE.json').read_text())
        cls.page = (ROOT / 'reflexsigma-rc4/index.html').read_text()
        cls.home = (ROOT / 'index.html').read_text()
        cls.manifest = json.loads((ROOT / 'proof-estate-manifest.json').read_text())
        cls.readme = (ROOT / 'reflexsigma-rc4/README.md').read_text()

    def test_four_source_recorded_distinct_receipts(self):
        runs = self.meta['recordedSoftwareRuns']
        self.assertEqual(len(runs), 4)
        self.assertEqual([r['outcome'] for r in runs], ['HOLD', 'HOLD', 'ESCALATE_NO_BIND', 'REFUSE'])
        self.assertTrue(all(r['noBind'] is True for r in runs))
        self.assertEqual(len({r['receiptSHA256'] for r in runs}), 4)
        self.assertEqual(runs[0]['decisionSHA256'], runs[1]['decisionSHA256'])
        for run in runs:
            for field in ['receiptSHA256', 'decisionSHA256']:
                self.assertRegex(run[field], r'^[a-f0-9]{64}$')
                self.assertIn(run[field], self.page)

    def test_qualified_software_only(self):
        self.assertEqual(self.meta['rc6SoftwareTests'], {'passed': 274, 'total': 274})
        self.assertEqual(self.meta['rc4SoftwareTests'], {'passed': 39, 'total': 39})
        self.assertEqual(self.meta['rc6SourceCustody'], {'passed': 389, 'total': 389})
        self.assertEqual(self.meta['originalFusionV8Acceptance'], {'passed': 4, 'total': 9})
        self.assertEqual(self.meta['originalFusionV8StrictSourceAcceptance'], {'passed': 3, 'total': 9})
        for key in ['nativeCorrectedNewKQualification', 'physicalEquipmentQualification', 'independentExaminerAttestation']:
            self.assertEqual(self.meta['qualificationCeilings'][key], 'NOT_ESTABLISHED')
        for phrase in ['recorded playback', 'NOT ESTABLISHED', '4/9']:
            self.assertIn(phrase.lower(), self.page.lower())

    def test_exact_mark_integrity_and_public_route(self):
        self.assertIn('c18391f95a487ea8b11141bc4ebe7781aaa33e767ed8003f854e52a49e68eace', self.page)
        self.assertIn('../zero-x/assets/logo-parts/', self.page)
        self.assertIn('reflexsigma-rc4/', self.home)
        self.assertIn('PUBLIC_EVIDENCE.json', self.page)
        self.assertIn('reflexsigma-rc4/README.md', self.home)

    def test_no_private_distribution_or_false_qualifications(self):
        for document in [self.page, self.readme, json.dumps(self.meta)]:
            self.assertNotIn('PRIVATE_REVIEW.zip', document)
            self.assertNotIn('private review archive download', document.lower())
        self.assertEqual(self.meta['evidenceClass'], 'OBSERVED_INTERNAL_SOFTWARE')
        self.assertEqual(self.meta['publicDisplayType'], 'RECORDED_PLAYBACK_ONLY')

    def test_site_identity_preserved_and_current_digest(self):
        self.assertEqual(self.manifest['release'], '2.7')
        self.assertEqual(self.manifest['edition'], '09')
        self.assertEqual(self.manifest['systemVersionReference']['designation'], 'V12')
        self.assertEqual(self.manifest['currentSiteIndexSHA256'], hashlib.sha256(self.home.encode()).hexdigest())

    def test_ci_tracks_exhibit_and_runs_public_checks(self):
        workflow = (ROOT / '.github/workflows/public-proof-integrity.yml').read_text()
        self.assertGreaterEqual(workflow.count('"reflexsigma-rc4/**"'), 2)
        self.assertIn('python scripts/test_reflexsigma_rc4_public.py', workflow)

    def test_gold_corridor_is_recorded_and_reduced_motion_safe(self):
        self.assertIn('class="corridor-rail"', self.page)
        self.assertIn('VISUAL GUIDE · RECORDED, NOT LIVE', self.page)
        for node in ['SOURCE', 'STANDING', 'BOUNDARY', 'RECEIPT']:
            self.assertIn(f'data-stage="{node.lower()}"', self.page)
        self.assertIn('data-state="HOLD"', self.page)
        self.assertIn("document.querySelector('.demo').dataset.state=run.outcome", self.page)
        self.assertIn('prefers-reduced-motion: reduce', self.page)


if __name__ == '__main__':
    unittest.main()
