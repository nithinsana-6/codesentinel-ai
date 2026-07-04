from __future__ import annotations

from dataclasses import dataclass, field


DEFAULT_EXCLUDES = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".pytest_cache",
}

DEFAULT_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".jsx": "javascript",
    ".go": "go",
    ".java": "java",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".toml": "toml",
    ".md": "markdown",
}


@dataclass(frozen=True)
class ScanConfig:
    max_file_bytes: int = 200_000
    exclude_dirs: set[str] = field(default_factory=lambda: set(DEFAULT_EXCLUDES))
    extensions: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_EXTENSIONS))
    require_tests: bool = True

    def language_for_suffix(self, suffix: str) -> str | None:
        return self.extensions.get(suffix.lower())
