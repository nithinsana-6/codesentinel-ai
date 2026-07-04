from __future__ import annotations

import re

from .config import ScanConfig
from .models import Category, Finding, Severity, SourceFile


SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]

UNSAFE_SHELL_PATTERNS = [
    re.compile(r"subprocess\.(run|call|Popen)\(.*shell\s*=\s*True"),
    re.compile(r"os\.system\("),
]


class StaticAnalyzer:
    def __init__(self, config: ScanConfig | None = None) -> None:
        self.config = config or ScanConfig()

    def analyze(self, files: list[SourceFile]) -> list[Finding]:
        findings: list[Finding] = []
        for source in files:
            findings.extend(self._analyze_file(source))
        findings.extend(self._analyze_repo_shape(files))
        return sorted(findings, key=lambda item: (item.file_path, item.line_number or 0, item.severity.value))

    def _analyze_file(self, source: SourceFile) -> list[Finding]:
        findings: list[Finding] = []
        for index, line in enumerate(source.lines, start=1):
            stripped = line.strip()
            findings.extend(self._check_secrets(source, index, stripped))
            findings.extend(self._check_unsafe_shell(source, index, stripped))
            findings.extend(self._check_broad_exception(source, index, stripped))
            findings.extend(self._check_todo(source, index, stripped))
            findings.extend(self._check_debug_flags(source, index, stripped))
        return findings

    def _check_secrets(self, source: SourceFile, line_number: int, line: str) -> list[Finding]:
        if any(pattern.search(line) for pattern in SECRET_PATTERNS):
            return [
                Finding(
                    category=Category.SECURITY,
                    severity=Severity.CRITICAL,
                    title="Possible hardcoded secret",
                    description="The code appears to contain a credential-like value committed in plaintext.",
                    recommendation="Move secrets to a managed secret store or environment variable and rotate the exposed value.",
                    file_path=source.relative_path,
                    line_number=line_number,
                    evidence=line[:160],
                )
            ]
        return []

    def _check_unsafe_shell(self, source: SourceFile, line_number: int, line: str) -> list[Finding]:
        if source.language != "python":
            return []
        if any(pattern.search(line) for pattern in UNSAFE_SHELL_PATTERNS):
            return [
                Finding(
                    category=Category.SECURITY,
                    severity=Severity.HIGH,
                    title="Unsafe shell execution",
                    description="Shell execution can allow command injection when arguments include user-controlled input.",
                    recommendation="Use argument arrays with shell=False and validate all external input before execution.",
                    file_path=source.relative_path,
                    line_number=line_number,
                    evidence=line[:160],
                )
            ]
        return []

    def _check_broad_exception(self, source: SourceFile, line_number: int, line: str) -> list[Finding]:
        if source.language == "python" and re.match(r"except\s+Exception\s*:|except\s*:", line):
            return [
                Finding(
                    category=Category.RELIABILITY,
                    severity=Severity.MEDIUM,
                    title="Broad exception handler",
                    description="Catching every exception can hide operational failures and make debugging harder.",
                    recommendation="Catch specific exception types, log useful context, and re-raise unexpected failures.",
                    file_path=source.relative_path,
                    line_number=line_number,
                    evidence=line[:160],
                )
            ]
        return []

    def _check_todo(self, source: SourceFile, line_number: int, line: str) -> list[Finding]:
        if "TODO" in line or "FIXME" in line:
            return [
                Finding(
                    category=Category.MAINTAINABILITY,
                    severity=Severity.LOW,
                    title="Unresolved engineering note",
                    description="TODO/FIXME comments can indicate known incomplete behavior or deferred risk.",
                    recommendation="Convert the note into a tracked issue or resolve it before release.",
                    file_path=source.relative_path,
                    line_number=line_number,
                    evidence=line[:160],
                )
            ]
        return []

    def _check_debug_flags(self, source: SourceFile, line_number: int, line: str) -> list[Finding]:
        if source.language == "python" and re.search(r"debug\s*=\s*True", line):
            return [
                Finding(
                    category=Category.SECURITY,
                    severity=Severity.HIGH,
                    title="Debug mode enabled",
                    description="Debug mode can expose stack traces, environment details, and unsafe development behavior.",
                    recommendation="Disable debug mode by default and control it through environment-specific configuration.",
                    file_path=source.relative_path,
                    line_number=line_number,
                    evidence=line[:160],
                )
            ]
        return []

    def _analyze_repo_shape(self, files: list[SourceFile]) -> list[Finding]:
        if not self.config.require_tests:
            return []
        has_python = any(source.language == "python" for source in files)
        has_tests = any(
            source.relative_path.startswith("tests/")
            or source.relative_path.endswith("_test.py")
            or source.relative_path.startswith("test_")
            for source in files
        )
        if has_python and not has_tests:
            return [
                Finding(
                    category=Category.TESTING,
                    severity=Severity.MEDIUM,
                    title="No automated tests detected",
                    description="The repository contains Python code but no obvious automated test suite.",
                    recommendation="Add unit tests for critical behavior and run them in CI before merging changes.",
                    file_path=".",
                )
            ]
        return []
