from __future__ import annotations

from pathlib import Path

from .config import ScanConfig
from .models import SourceFile


class RepositoryScanner:
    def __init__(self, config: ScanConfig | None = None) -> None:
        self.config = config or ScanConfig()

    def scan(self, repo_path: str | Path) -> list[SourceFile]:
        root = Path(repo_path).resolve()
        if not root.exists():
            raise FileNotFoundError(f"Repository path does not exist: {root}")
        if not root.is_dir():
            raise NotADirectoryError(f"Repository path must be a directory: {root}")

        files: list[SourceFile] = []
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if self._is_excluded(path, root):
                continue
            language = self.config.language_for_suffix(path.suffix)
            if language is None:
                continue
            if path.stat().st_size > self.config.max_file_bytes:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            files.append(
                SourceFile(
                    path=path,
                    relative_path=path.relative_to(root).as_posix(),
                    language=language,
                    text=text,
                )
            )
        return files

    def _is_excluded(self, path: Path, root: Path) -> bool:
        relative_parts = path.relative_to(root).parts
        return any(part in self.config.exclude_dirs for part in relative_parts)
