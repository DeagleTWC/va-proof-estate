#!/usr/bin/env python3
"""Inspect expressions in a manually dispatched workflow. Never triggers it."""
import re
import unittest
from pathlib import Path
SOURCE = Path(__file__).resolve().parents[1] / ".github/workflows/issue-fresh-challenge.yml"
EXPECTED = {"github.token":2, "github.repository":2, "github.actor":1,
            "inputs.freeze_comment_id":1, "github.run_id":2,
            "github.run_attempt":2, "github.sha":1,
            "inputs.family":1, "inputs.rounds":1}
def failures(src):
    out = []
    if "\\" + "$" + "{{" in src: out.append("escaped expression")
    exprs = re.findall(r"\$\{\{\s*([^}]+?)\s*\}\}", src)
    for expr, count in EXPECTED.items():
        if exprs.count(expr) != count: out.append("missing or changed " + expr)
    if len(exprs) != sum(EXPECTED.values()): out.append("unexpected expression")
    if "workflow_dispatch:" not in src or "issues: write" not in src: out.append("trigger or permissions changed")
    return out
class WorkflowExpressionTests(unittest.TestCase):
    def setUp(self): self.src = SOURCE.read_text(encoding="utf-8")
    def test_valid(self): self.assertEqual(failures(self.src), [])
    def test_escaping_rejected(self):
        s = self.src.replace("$" + "{{ github.token }}", "\\" + "$" + "{{ github.token }}", 1)
        self.assertTrue(any("escaped expression" in v for v in failures(s)))
    def test_missing_run_identifier_rejected(self):
        s = self.src.replace("$" + "{{ github.run_id }}", "unknown", 1)
        self.assertTrue(any("github.run_id" in v for v in failures(s)))
if __name__ == "__main__": unittest.main()
