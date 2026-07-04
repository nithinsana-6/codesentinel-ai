import tempfile
import unittest
from pathlib import Path

from codesentinel.evaluator import Evaluator


class EvaluatorTest(unittest.TestCase):
    def test_runs_jsonl_eval_case(self):
        case = (
            '{"name":"secret","files":{"app.py":"API_KEY = \\"super-secret-token-123\\""},'
            '"expected_titles":["Possible hardcoded secret","No automated tests detected"]}\n'
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.jsonl"
            path.write_text(case, encoding="utf-8")
            results = Evaluator().run(path)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].recall, 1.0)


if __name__ == "__main__":
    unittest.main()
