import unittest
from pathlib import Path

from codesentinel.models import ReviewReport
from codesentinel.renderer import render_json, render_markdown


class RendererTest(unittest.TestCase):
    def test_renders_empty_report(self):
        report = ReviewReport(repo_path=Path("."), files_scanned=0, findings=[], summary="Clean")

        self.assertIn("Clean", render_markdown(report))
        self.assertIn('"files_scanned": 0', render_json(report))


if __name__ == "__main__":
    unittest.main()
