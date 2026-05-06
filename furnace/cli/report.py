from __future__ import annotations

from pathlib import Path


def report_path(run_dir: Path) -> Path:
    return run_dir / "report.md"
