from __future__ import annotations

from pathlib import Path

from furnace import OptimizationStudy


def run_study(config_path: Path) -> Path:
    study = OptimizationStudy.from_config(config_path)
    study.run()
    return study.config.project.output_dir
