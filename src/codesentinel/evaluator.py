from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .agent import ReviewAgent


@dataclass(frozen=True)
class EvalCase:
    name: str
    files: dict[str, str]
    expected_titles: set[str]


@dataclass(frozen=True)
class EvalResult:
    name: str
    expected: set[str]
    observed: set[str]

    @property
    def true_positives(self) -> int:
        return len(self.expected & self.observed)

    @property
    def precision(self) -> float:
        return self.true_positives / len(self.observed) if self.observed else 1.0

    @property
    def recall(self) -> float:
        return self.true_positives / len(self.expected) if self.expected else 1.0


class Evaluator:
    def __init__(self, agent: ReviewAgent | None = None) -> None:
        self.agent = agent or ReviewAgent()

    def load_cases(self, path: str | Path) -> list[EvalCase]:
        cases: list[EvalCase] = []
        with Path(path).open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                raw = json.loads(line)
                cases.append(
                    EvalCase(
                        name=raw["name"],
                        files=dict(raw["files"]),
                        expected_titles=set(raw["expected_titles"]),
                    )
                )
        return cases

    def run(self, path: str | Path) -> list[EvalResult]:
        results = []
        for case in self.load_cases(path):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                for relative_path, text in case.files.items():
                    file_path = root / relative_path
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    file_path.write_text(text, encoding="utf-8")
                report = self.agent.review(root)
                observed = {finding.title for finding in report.findings}
                results.append(EvalResult(case.name, case.expected_titles, observed))
        return results


def render_eval_results(results: list[EvalResult]) -> str:
    lines = ["# CodeSentinel Evaluation", ""]
    if not results:
        return "# CodeSentinel Evaluation\n\nNo cases found."

    avg_precision = sum(result.precision for result in results) / len(results)
    avg_recall = sum(result.recall for result in results) / len(results)
    lines.extend(
        [
            f"Cases: **{len(results)}**",
            f"Average precision: **{avg_precision:.2f}**",
            f"Average recall: **{avg_recall:.2f}**",
            "",
            "| Case | Precision | Recall | Missing | Extra |",
            "|---|---:|---:|---|---|",
        ]
    )
    for result in results:
        missing = ", ".join(sorted(result.expected - result.observed)) or "-"
        extra = ", ".join(sorted(result.observed - result.expected)) or "-"
        lines.append(
            f"| {result.name} | {result.precision:.2f} | {result.recall:.2f} | {missing} | {extra} |"
        )
    return "\n".join(lines)
