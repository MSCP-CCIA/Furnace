from pathlib import Path

from furnace import OptimizationStudy
from furnace.core.config import load_config


def test_study_runs_and_generates_outputs() -> None:
    config = load_config("configs/default.yaml")
    config.project.output_dir = Path("outputs/test-pipeline-run")
    study = OptimizationStudy(config)
    results = study.run()
    assert len(results) == 2
    assert (study.config.project.output_dir / "report.md").exists()
    assert (study.config.project.output_dir / "comparison.csv").exists()
