from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Category(str, Enum):
    SECURITY = "security"
    RELIABILITY = "reliability"
    MAINTAINABILITY = "maintainability"
    TESTING = "testing"
    PERFORMANCE = "performance"


@dataclass(frozen=True)
class SourceFile:
    path: Path
    relative_path: str
    language: str
    text: str

    @property
    def lines(self) -> list[str]:
        return self.text.splitlines()


@dataclass(frozen=True)
class Finding:
    category: Category
    severity: Severity
    title: str
    description: str
    recommendation: str
    file_path: str
    line_number: int | None = None
    evidence: str | None = None

    def identity(self) -> str:
        return f"{self.category}:{self.severity}:{self.file_path}:{self.line_number}:{self.title}"


@dataclass(frozen=True)
class ReviewReport:
    repo_path: Path
    files_scanned: int
    findings: list[Finding] = field(default_factory=list)
    summary: str = ""

    def severity_counts(self) -> dict[str, int]:
        counts = {severity.value: 0 for severity in Severity}
        for finding in self.findings:
            counts[finding.severity.value] += 1
        return counts

    def category_counts(self) -> dict[str, int]:
        counts = {category.value: 0 for category in Category}
        for finding in self.findings:
            counts[finding.category.value] += 1
        return counts
