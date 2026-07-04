from __future__ import annotations

from pathlib import Path

from .analyzer import StaticAnalyzer
from .config import ScanConfig
from .models import ReviewReport
from .providers import DeterministicReviewProvider, ReviewProvider
from .scanner import RepositoryScanner


class ReviewAgent:
    def __init__(
        self,
        config: ScanConfig | None = None,
        provider: ReviewProvider | None = None,
    ) -> None:
        self.config = config or ScanConfig()
        self.scanner = RepositoryScanner(self.config)
        self.analyzer = StaticAnalyzer(self.config)
        self.provider = provider or DeterministicReviewProvider()

    def review(self, repo_path: str | Path) -> ReviewReport:
        root = Path(repo_path).resolve()
        files = self.scanner.scan(root)
        findings = self.analyzer.analyze(files)
        summary = self.provider.summarize(files, findings)
        return ReviewReport(
            repo_path=root,
            files_scanned=len(files),
            findings=findings,
            summary=summary,
        )
