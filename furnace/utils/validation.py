from __future__ import annotations

from pathlib import Path


def ensure_exists(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(path)
    return path
