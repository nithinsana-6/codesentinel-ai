from __future__ import annotations

from typing import Protocol

from .models import Finding, SourceFile


class ReviewProvider(Protocol):
    def summarize(self, files: list[SourceFile], findings: list[Finding]) -> str:
        """Return a human-readable review summary."""


class DeterministicReviewProvider:
    """Offline provider that keeps demos and tests reproducible."""

    def summarize(self, files: list[SourceFile], findings: list[Finding]) -> str:
        if not findings:
            return f"Scanned {len(files)} files. No high-confidence risks were detected."

        critical_or_high = [
            finding for finding in findings if finding.severity.value in {"critical", "high"}
        ]
        if critical_or_high:
            return (
                f"Scanned {len(files)} files and found {len(findings)} risks. "
                f"Prioritize {len(critical_or_high)} critical/high-severity findings before release."
            )
        return (
            f"Scanned {len(files)} files and found {len(findings)} maintainability or reliability issues. "
            "Address the highest-impact findings and add regression tests where appropriate."
        )
