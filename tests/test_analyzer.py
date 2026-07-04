import unittest

from codesentinel.analyzer import StaticAnalyzer
from codesentinel.models import SourceFile


class StaticAnalyzerTest(unittest.TestCase):
    def test_detects_secret_and_unsafe_shell(self):
        source = SourceFile(
            path="app.py",
            relative_path="app.py",
            language="python",
            text='API_KEY = "super-secret-token-123"\nsubprocess.run(cmd, shell=True)\n',
        )

        findings = StaticAnalyzer().analyze([source])
        titles = {finding.title for finding in findings}

        self.assertIn("Possible hardcoded secret", titles)
        self.assertIn("Unsafe shell execution", titles)

    def test_detects_missing_tests_for_python_repo(self):
        source = SourceFile(
            path="app.py",
            relative_path="app.py",
            language="python",
            text="print('hello')\n",
        )

        findings = StaticAnalyzer().analyze([source])

        self.assertIn("No automated tests detected", {finding.title for finding in findings})


if __name__ == "__main__":
    unittest.main()
