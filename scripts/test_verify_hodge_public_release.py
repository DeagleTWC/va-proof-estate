"""Black-box checks for the public Hodge release verifier."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_hodge_public_release.py"
ARCHIVE = ROOT / "research" / "hodge" / "NEWK_HODGE_LATTICE_CLOSURE_CHILD_V1_2026-11-25.zip"


def run_verifier(archive: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--archive", str(archive)],
        capture_output=True,
        text=True,
        check=False,
    )


class PublicHodgeReleaseVerifierTests(unittest.TestCase):
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
