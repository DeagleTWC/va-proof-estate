#!/usr/bin/env python3
"""KCD public proof register fail-closed negative controls; temporary synthetic changes only."""
import copy
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import validate_kcd_register as validator


class KCDRegisterNegativeControls(unittest.TestCase):
    def setUp(self):
        self.original_root = validator.ROOT
        self.original_register = validator.REGISTER
        temp = tempfile.TemporaryDirectory(prefix="va-kcd-synthetic-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / "kcd").mkdir()
        self.register = self.root / "kcd" / "KCD-PROOF-REGISTER.json"
        self.original = json.loads(self.original_register.read_text(encoding="utf-8"))
        validator.ROOT = self.root
        validator.REGISTER = self.register
        self.addCleanup(self.restore)
        self.write(self.original)

    def restore(self):
        validator.ROOT = self.original_root
        validator.REGISTER = self.original_register

    def write(self, value):
        self.register.write_text(json.dumps(value), encoding="utf-8")

    def reject(self, mutate):
        candidate = copy.deepcopy(self.original)
        mutate(candidate)
        self.write(candidate)
        with self.assertRaises((ValueError, OSError, TypeError, KeyError)):
            with redirect_stdout(StringIO()):
                validator.main()

    def test_unmodified_public_record_passes_without_promotion(self):
        with redirect_stdout(StringIO()) as out:
            self.assertEqual(validator.main(), 0)
        result = json.loads(out.getvalue())
        self.assertEqual(result["formalized_claims"], 4)
        self.assertEqual(result["physical_packets"], 0)
        self.assertEqual(result["independent_packets"], 0)

    def test_program_b_cannot_inherit_standing(self):
        self.reject(lambda x: x.update(programBInheritedStanding=True))

    def test_protected_construction_release_cannot_be_silently_changed(self):
        self.reject(lambda x: x.update(protectedConstructionReleased=True))

    def test_corrected_source_identity_cannot_be_rewritten(self):
        self.reject(lambda x: x.update(source="Unverified alternate source"))

    def test_duplicate_ph_identity_refused(self):
        self.reject(lambda x: x["claims"][1].update(id="KCD-PH-01"))

    def test_synthetic_class_does_not_become_physical(self):
        self.reject(lambda x: x["claims"][0]["fieldClasses"].append("simulated"))

    def test_formal_only_class_cannot_claim_external_witness(self):
        self.reject(lambda x: x["claims"][0].update(independentWitnessAttached=True))

    def test_fake_observation_without_original_packet_is_refused(self):
        def mutate(x):
            x["claims"][0].update(evidenceStatus="OBSERVED_BOUNDED", physicalMeasurementAttached=True)
            x["observedPhysicalRunsAttached"] = 1
        self.reject(mutate)

    def test_fake_packet_name_cannot_supply_an_observation(self):
        def mutate(x):
            x["claims"][0].update(
                evidenceStatus="OBSERVED_BOUNDED",
                physicalMeasurementAttached=True,
                evidencePacket={"path":"kcd/evidence/never-published.json","sha256":"a" * 64},
            )
            x["observedPhysicalRunsAttached"] = 1
        self.reject(mutate)

    def test_forged_observation_count_is_refused(self):
        self.reject(lambda x: x.update(observedPhysicalRunsAttached=1))

    def test_unearned_independent_reproduction_count_is_refused(self):
        self.reject(lambda x: x.update(independentPhysicalRunsAttached=1))


if __name__ == "__main__":
    unittest.main()
