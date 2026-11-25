"""Black-box checks for the public Hodge release verifier."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import json
import hashlib


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_hodge_public_release.py"
ARCHIVE = ROOT / "research" / "hodge" / "NEWK_HODGE_LATTICE_CLOSURE_CHILD_V1_2026-11-25.zip"


def run_verifier(archive: Path, receipt_dir: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPT), "--archive", str(archive)]
    if receipt_dir is not None:
        command.extend(["--receipt-dir", str(receipt_dir)])
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )


class PublicHodgeReleaseVerifierTests(unittest.TestCase):
    def test_successful_audit_emits_downloadable_exact_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "evidence"
            result = run_verifier(ARCHIVE, evidence_dir)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(len(list(evidence_dir.iterdir())), 7)
            summary = json.loads((evidence_dir / "audit_summary.json").read_text())
            self.assertEqual(summary["schema"], "VA_HODGE_PUBLIC_CI_EVIDENCE_V1")
            self.assertEqual(summary["tests_passed"], 39)
            self.assertFalse(summary["unrestricted_hodge_proved_by_child"])
            self.assertFalse(summary["protected_gen1056_authenticated"])
            for case, gate, exit_code in (
                ("carry", "CARRY", 0),
                ("reexamine", "REEXAMINE", 2),
                ("refuse", "REFUSE", 3),
            ):
                item = summary["cases"][case]
                self.assertEqual(item["gate"], gate)
                self.assertEqual(item["run_exit_code"], exit_code)
                receipt = evidence_dir / item["receipt_file"]
                exact = evidence_dir / item["exact_evidence_file"]
                self.assertEqual(hashlib.sha256(receipt.read_bytes()).hexdigest(), item["receipt_file_sha256"])
                self.assertEqual(hashlib.sha256(exact.read_bytes()).hexdigest(), item["exact_evidence_file_sha256"])
                self.assertEqual(json.loads(receipt.read_text())["gate"], gate)

    def test_failed_archive_never_emits_success_bundle(self):
        with tempfile.TemporaryDirectory() as temporary:
            changed = Path(temporary) / "tampered.zip"
            changed.write_bytes(ARCHIVE.read_bytes() + b"bad")
            evidence_dir = Path(temporary) / "evidence"
            result = run_verifier(changed, evidence_dir)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(evidence_dir.exists())

    def test_verified_archive_runs_full_suite_and_three_gates(self):
        result = run_verifier(ARCHIVE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("HODGE_PUBLIC_AUDIT PASS", result.stdout)
        self.assertIn("39/39", result.stdout)
        self.assertIn("CARRY=0", result.stdout)
        self.assertIn("REEXAMINE=2", result.stdout)
        self.assertIn("REFUSE=3", result.stdout)
        self.assertIn("REPLAYS=3/3", result.stdout)

    def test_modified_archive_refuses_before_execution(self):
        with tempfile.TemporaryDirectory() as temporary:
            changed = Path(temporary) / "changed.zip"
            changed.write_bytes(ARCHIVE.read_bytes() + b"X")
            result = run_verifier(changed)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("archive SHA-256 mismatch", result.stderr)

    def test_missing_archive_refuses(self):
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing.zip"
            result = run_verifier(missing)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("archive not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
