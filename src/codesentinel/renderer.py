from __future__ import annotations

import json
from dataclasses import asdict

from .models import Finding, ReviewReport


def render_json(report: ReviewReport) -> str:
    payload = {
        "repo_path": str(report.repo_path),
        "files_scanned": report.files_scanned,
        "summary": report.summary,
        "severity_counts": report.severity_counts(),
        "category_counts": report.category_counts(),
        "findings": [_finding_to_dict(finding) for finding in report.findings],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def render_markdown(report: ReviewReport) -> str:
    lines = [
        "# CodeSentinel AI Review",
        "",
        f"Repository: `{report.repo_path}`",
        f"Files scanned: **{report.files_scanned}**",
        "",
        "## Summary",
        "",
        report.summary,
        "",
        "## Severity Counts",
        "",
    ]
    for severity, count in report.severity_counts().items():
        lines.append(f"- {severity}: {count}")

    lines.extend(["", "## Findings", ""])
    if not report.findings:
        lines.append("No findings.")
        return "\n".join(lines)

    for index, finding in enumerate(report.findings, start=1):
        location = finding.file_path
        if finding.line_number is not None:
            location = f"{location}:{finding.line_number}"
        lines.extend(
            [
                f"### {index}. {finding.title}",
                "",
                f"- Severity: `{finding.severity.value}`",
                f"- Category: `{finding.category.value}`",
                f"- Location: `{location}`",
                f"- Description: {finding.description}",
                f"- Recommendation: {finding.recommendation}",
            ]
        )
        if finding.evidence:
            lines.append(f"- Evidence: `{finding.evidence}`")
        lines.append("")
    return "\n".join(lines)


def _finding_to_dict(finding: Finding) -> dict[str, object]:
    payload = asdict(finding)
    payload["category"] = finding.category.value
    payload["severity"] = finding.severity.value
    return payload
