#!/usr/bin/env python3
"""Synthetic negative controls for anchored website-publication source history."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from verify_public_release_history import validate


class ReleaseGitHistoryTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="va-public-git-history-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Local Test")
        self.git("config", "user.email", "test@example.invalid")
        original = []
        for ver in ["2.0", "2.1", "2.2"]:
            body = f"Public website release {ver}\n".encode("utf-8")
            (self.root / "index.html").write_bytes(body)
            self.git("add", "index.html")
            self.git("commit", "-qm", f"synthetic version {ver}")
            commit = self.git("rev-parse", "HEAD").strip()
            original.append({"release": ver, "edition": {"2.0": "02", "2.1": "03", "2.2": "04"}[ver],
                             "indexSourceCommit": commit, "mainFileSHA256": hashlib.sha256(body).hexdigest()})
        self.manifest = {
            "releaseHistory": original[:2],
            "previousWebsiteRelease": {**original[1], "preservedInGitHistory": True},
            "release": "2.2",
            "mainFileSHA256": original[2]["mainFileSHA256"],
            "currentIndexSourceCommit": original[2]["indexSourceCommit"],
        }
        self.save()

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True)

    def save(self):
        (self.root / "proof-estate-manifest.json").write_text(
            json.dumps(self.manifest) + "\n", encoding="utf-8"
        )

    def test_pinned_originals_verify(self):
        self.assertEqual(validate(self.root), [])

    def test_forged_historical_hash_fails(self):
        self.manifest["releaseHistory"][0]["mainFileSHA256"] = "0" * 64
        self.save()
        self.assertTrue(any("Historic source digest mismatch" in x for x in validate(self.root)))

    def test_unavailable_original_git_commit_fails(self):
        self.manifest["releaseHistory"][1]["indexSourceCommit"] = "0" * 40
        self.save()
        self.assertTrue(any("Unable to read Git source" in x for x in validate(self.root)))

    def test_current_unpinned_changes_fail(self):
        (self.root / "index.html").write_text("mutation", encoding="utf-8")
        self.assertTrue(any("Current website source differs" in x for x in validate(self.root)))

    def test_previous_release_cannot_change_while_history_stays_fixed(self):
        self.manifest["previousWebsiteRelease"]["indexSourceCommit"] = "a" * 40
        self.save()
        self.assertTrue(any("Previous release does not match" in x for x in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
