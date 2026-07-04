from __future__ import annotations

import argparse
import sys

from .agent import ReviewAgent
from .evaluator import Evaluator, render_eval_results
from .renderer import render_json, render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="codesentinel",
        description="Agentic code-review and evaluation workbench.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    review = subcommands.add_parser("review", help="Review a repository")
    review.add_argument("repo_path", help="Path to the repository to review")
    review.add_argument("--format", choices=["markdown", "json"], default="markdown")
    review.add_argument(
        "--fail-on-critical",
        action="store_true",
        help="Exit with status 1 when critical findings are present.",
    )

    evaluate = subcommands.add_parser("eval", help="Run labeled evaluation cases")
    evaluate.add_argument("cases_path", help="Path to a JSONL eval case file")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "review":
        report = ReviewAgent().review(args.repo_path)
        output = render_json(report) if args.format == "json" else render_markdown(report)
        print(output)
        if args.fail_on_critical and report.severity_counts()["critical"] > 0:
            return 1
        return 0

    if args.command == "eval":
        results = Evaluator().run(args.cases_path)
        print(render_eval_results(results))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
