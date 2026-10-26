#!/usr/bin/env python3
"""Synthetic negative controls for the M27 data-only readback checker.

No native execution, independent human witness, or external effect is generated.
"""
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path

from preflight_m27_target_readback import inspect


def digest(data):
    return hashlib.sha256(data).hexdigest()


def put(root, name, raw):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return {'path': name, 'sha256': digest(raw)}


def putjson(root, name, value):
    return put(root, name, json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def make_fixture(root):
    original = root.parent / 'frozen-source.bin'
    original.write_bytes(b'SYNTHETIC-NOT-A-NATIVE-VA-ORIGINAL')
    frozen = digest(original.read_bytes())
    cases = []
    for kind, code, pre, post, ci in [('ALLOW', 'permit001', b'0', b'1', 'open'),
                                     ('REFUSE', 'refuse001', b'1', b'1', 'revoked')]:
        base = 'cases/' + code + '/'
        condition = digest(ci.encode())
        item = {'kind': kind, 'caseId': code, 'candidateId': 'fixed_candidate',
                'route': 'protected_route', 'targetId': 'protected_target',
                'observerId': 'synthetic_observer', 'instrumentId': 'mock_reader',
                'readbackOutsideDecisionProcess': True,
                'governingConditionSHA256': condition}
        item['receipt'] = putjson(root, base + 'receipt.json', {
            'caseId': code, 'candidateId': item['candidateId'], 'route': item['route'],
            'targetId': item['targetId'], 'governingConditionSHA256': condition,
            'originalFrozenSHA256': frozen,
            'decision': 'EXECUTE' if kind == 'ALLOW' else 'REFUSE'})
        for stage, raw, sequence in [('before', pre, 1), ('after', post, 2)]:
            capture = put(root, base + stage + '.bin', raw)
            snap = {'schema': 'va-m27-target-snapshot/1.0', 'caseId': code,
                    'stage': stage, 'route': item['route'], 'targetId': item['targetId'],
                    'observerId': item['observerId'], 'instrumentId': item['instrumentId'],
                    'measurementSource': 'SEPARATE_TARGET_READBACK',
                    'decisionLabelIsMeasurement': False,
                    'calibrationOrAuditReference': 'SIMULATED-NOT-CALIBRATED',
                    'sequence': sequence, 'rawCapture': capture,
                    'readbackSHA256': capture['sha256']}
            item[stage] = putjson(root, base + stage + '.json', snap)
        cases.append(item)
    manifest = {'schema': 'va-m27-target-readback-candidate/1.0',
                'classification': 'PRIVATE_CUSTODIAL_REVIEW', 'releaseAuthorized': False,
                'independentEffectsQualified': False, 'originalFrozenSHA256': frozen,
                'declaredRoutes': ['protected_route', 'alternate_route'],
                'unexaminedRoutes': ['alternate_route'], 'cases': cases}
    (root / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    return original


class SyntheticM27Controls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'packet'
        self.root.mkdir()
        self.original = make_fixture(self.root)

    def run_check(self):
        return inspect(self.root, self.original)

    def manifest(self):
        return json.loads((self.root / 'manifest.json').read_text())

    def save(self, manifest):
        (self.root / 'manifest.json').write_text(json.dumps(manifest))

    def rewrite(self, ref, modifier):
        p = self.root / ref['path']
        data = json.loads(p.read_text())
        modifier(data)
        raw = json.dumps(data, sort_keys=True).encode()
        p.write_bytes(raw)
        ref['sha256'] = digest(raw)

    def expect_refused(self):
        with self.assertRaises((ValueError, KeyError, TypeError)):
            self.run_check()

    def test_valid_synthetic_record_is_not_effect_proof(self):
        report = self.run_check()
        self.assertTrue(report['permittedReadbackChanged'])
        self.assertTrue(report['refusedReadbackUnchanged'])
        self.assertTrue(report['frozenOriginalBytesRechecked'])
        self.assertFalse(report['M27CompletedByThisTool'])
        self.assertFalse(report['M28AuthorizedByThisTool'])
        self.assertFalse(report['realWorldEffectIndependentlyProvedByThisTool'])
        self.assertEqual(report['unexaminedEffectRoutes'], ['alternate_route'])

    def test_missing_original_is_not_silently_claimed(self):
        self.assertFalse(inspect(self.root)['frozenOriginalBytesRechecked'])

    def test_frozen_original_mutated(self):
        self.original.write_bytes(b'CHANGED')
        self.expect_refused()

    def test_raw_capture_mutated(self):
        (self.root / 'cases/permit001/after.bin').write_bytes(b'bad')
        self.expect_refused()

    def test_receipt_mutated(self):
        (self.root / 'cases/refuse001/receipt.json').write_bytes(b'{}')
        self.expect_refused()

    def test_refused_target_actually_changes(self):
        m = self.manifest()
        ref = m['cases'][1]['after']
        def change(snap):
            snap['rawCapture'] = put(self.root, 'cases/refuse001/new_after.bin', b'2')
            snap['readbackSHA256'] = snap['rawCapture']['sha256']
        self.rewrite(ref, change)
        self.save(m)
        self.expect_refused()

    def test_allowed_target_does_not_change(self):
        m = self.manifest()
        ref = m['cases'][0]['after']
        def change(snap):
            snap['rawCapture'] = put(self.root, 'cases/permit001/new_after.bin', b'0')
            snap['readbackSHA256'] = snap['rawCapture']['sha256']
        self.rewrite(ref, change)
        self.save(m)
        self.expect_refused()

    def test_spoofed_receipt_decision_even_with_rehash(self):
        m = self.manifest()
        self.rewrite(m['cases'][0]['receipt'], lambda x: x.update(decision='REFUSE'))
        self.save(m)
        self.expect_refused()

    def test_same_governing_condition_not_qualified(self):
        m = self.manifest()
        c = m['cases'][1]
        c['governingConditionSHA256'] = m['cases'][0]['governingConditionSHA256']
        self.rewrite(c['receipt'], lambda x: x.update(governingConditionSHA256=c['governingConditionSHA256']))
        self.save(m)
        self.expect_refused()

    def test_mismatched_candidate(self):
        m = self.manifest()
        c = m['cases'][1]
        c['candidateId'] = 'other_candidate'
        self.rewrite(c['receipt'], lambda x: x.update(candidateId='other_candidate'))
        for stage in ('before', 'after'):
            # Snapshot does not repeat candidate: same-route/target cross-case still checked.
            pass
        self.save(m)
        self.expect_refused()

    def test_missing_route_gap(self):
        m = self.manifest()
        m['unexaminedRoutes'] = []
        self.save(m)
        self.expect_refused()

    def test_false_public_promotion(self):
        m = self.manifest()
        m['releaseAuthorized'] = True
        self.save(m)
        self.expect_refused()

    def test_claiming_human_qualification(self):
        m = self.manifest()
        m['independentEffectsQualified'] = True
        self.save(m)
        self.expect_refused()

    def test_duplicate_source_capture_path(self):
        m = self.manifest()
        after = m['cases'][1]['after']
        def change(snap):
            snap['rawCapture'] = {'path': 'cases/refuse001/before.bin',
                                  'sha256': digest(b'1')}
            snap['readbackSHA256'] = digest(b'1')
        self.rewrite(after, change)
        self.save(m)
        self.expect_refused()

    def test_symlink_to_outside_is_rejected(self):
        m = self.manifest()
        path = self.root / 'cases/permit001/before.bin'
        path.unlink()
        path.symlink_to(self.original)
        self.expect_refused()

    def test_wrong_sequence_is_rejected(self):
        m = self.manifest()
        self.rewrite(m['cases'][0]['after'], lambda x: x.update(sequence=1))
        self.save(m)
        self.expect_refused()

    def test_decision_label_as_measurement_rejected(self):
        m = self.manifest()
        self.rewrite(m['cases'][0]['before'],
                     lambda x: x.update(decisionLabelIsMeasurement=True))
        self.save(m)
        self.expect_refused()

    def test_target_switched(self):
        m = self.manifest()
        m['cases'][1]['targetId'] = 'different_target'
        self.save(m)
        self.expect_refused()


if __name__ == '__main__':
    unittest.main(verbosity=2)
