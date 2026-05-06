from __future__ import annotations

from pathlib import Path

from furnace.cli.run import run_study


def optimize_study(config_path: Path) -> Path:
    return run_study(config_path)
