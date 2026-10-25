#!/usr/bin/env python3
"""Synthetic positive/negative packet admission regression; not independent witness evidence."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from external_witness_admission import admit, FILES, STATUS
from independent_challenge import freeze, issue, examine, save, sign

ROOT = Path(__file__).resolve().parent


def keypair(root, name):
    priv, pub = root / (name + "-secret.pem"), root / (name + "-public.pem")
    subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:2048",
                    "-out", str(priv)], capture_output=True, check=True)
    subprocess.run(["openssl", "pkey", "-in", str(priv), "-pubout", "-out", str(pub)],
                   capture_output=True, check=True)
    return priv, pub


def packet(dir_path):
    artifact = ROOT / "example_layer.py"
    original = freeze(artifact, "Bounded external adapter", "candidate-001")
    issued = issue(original, "matrix", 1)
    save(dir_path / "freeze.json", original)
    save(dir_path / "challenge.json", issued)
    private = []
    for side, name in [("left", "Examiner Alpha"), ("right", "Examiner Beta")]:
        r, w = examine(original, issued, artifact, name, [sys.executable, str(artifact)])
        save(dir_path / (side + "-report.json"), r)
        save(dir_path / (side + "-record.json"), w)
        secret, public = keypair(dir_path, side)
        private.append(secret)
        shutil.copyfile(public, dir_path / (side + "-public.pem"))
        save(dir_path / (side + "-signature.json"), sign(w, secret, public))
    return private


class TestPacket(unittest.TestCase):
    def test_positive_and_negative_controls(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            secret_paths = packet(root)
            result = admit(root)
            self.assertEqual(result["status"], STATUS)
            self.assertEqual(result["cases"], 9)
            self.assertEqual(result["matching_observations"], 9)
            self.assertFalse(result["examiner_identity_authenticated"])
            self.assertEqual(result["independent_witness_standing"], "NOT ESTABLISHED")
            self.assertFalse(result["public_release_cleared"])
            self.assertEqual(set(result["original_file_manifest"]), set(FILES))

            source = root / "left-report.json"
            orig = source.read_bytes()
            source.write_bytes(orig + b"\n")
            self.assertEqual(admit(root)["independent_witness_standing"], "NOT ESTABLISHED")
            source.write_bytes(orig)

            record_file = root / "left-record.json"
            original = record_file.read_bytes()
            record = json.loads(original)
            record["pass_count"] = -1
            record_file.write_text(json.dumps(record), encoding="utf8")
            with self.assertRaises(ValueError):
                admit(root)
            record_file.write_bytes(original)

            challenge_file = root / "challenge.json"
            original = challenge_file.read_bytes()
            issue_data = json.loads(original)
            issue_data["seed"] += 1
            challenge_file.write_text(json.dumps(issue_data), encoding="utf8")
            with self.assertRaises(ValueError):
                admit(root)
            challenge_file.write_bytes(original)

            right_key = root / "right-public.pem"
            orig_key = right_key.read_bytes()
            right_key.write_bytes((root / "left-public.pem").read_bytes())
            with self.assertRaises(ValueError):
                admit(root)
            right_key.write_bytes(orig_key)

            right_key.write_bytes(secret_paths[1].read_bytes())
            with self.assertRaises(ValueError):
                admit(root)
            right_key.write_bytes(orig_key)

            missing = root / "right-record.json"
            original = missing.read_bytes()
            missing.unlink()
            with self.assertRaises(ValueError):
                admit(root)
            missing.write_bytes(original)

    def test_symlink_carrier_must_fail(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            packet(root)
            ref = root / "left-public.pem"
            content = ref.read_bytes()
            ref.unlink()
            ext = root / "extra.pem"
            ext.write_bytes(content)
            ref.symlink_to(ext)
            with self.assertRaises(ValueError):
                admit(root)


if __name__ == "__main__":
    unittest.main()
