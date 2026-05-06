from __future__ import annotations

from pathlib import Path
from typing import Any

from furnace.core.artifacts import ArtifactStore
from furnace.core.config import FurnaceConfig, load_config
from furnace.core.pipeline import PipelineState
from furnace.decision.constraints import Constraints
from furnace.decision.recommendation import DecisionEngine
from furnace.evaluation.evaluator import Evaluator
from furnace.models.loader import load_model
from furnace.optimization.base import CandidateResult
from furnace.optimization.quantization import create_optimization_method
from furnace.reporting.markdown_report import MarkdownReportGenerator
from furnace.tracking.local_tracker import LocalTracker
from furnace.utils.device import resolve_device
from furnace.utils.logger import get_logger
from furnace.utils.seed import set_seed

LOGGER = get_logger(__name__)


class OptimizationStudy:
    """Coordinates the Furnace MVP workflow."""

    def __init__(self, config: FurnaceConfig) -> None:
        self.config = config
        self.state = PipelineState()
        self.tracker = LocalTracker()
        self.device = resolve_device()
        self.artifacts = ArtifactStore(self.config.project.output_dir)
        self.evaluator = Evaluator(metric_names=self.config.evaluation.metrics)
        self.decision_engine = DecisionEngine(
            constraints=Constraints.from_config(self.config.constraints),
            weights=self.config.decision.weights,
        )
        self._results: list[CandidateResult] = []
        self._comparison: list[dict[str, Any]] | None = None

    @classmethod
    def from_config(cls, path: str | Path) -> "OptimizationStudy":
        return cls(load_config(path))

    def run(self) -> list[CandidateResult]:
        set_seed(self.config.project.seed)
        self.artifacts.write_yaml("config.yaml", self.config.model_dump(mode="json"))

        bundle = load_model(self.config.model, self.config.data)
        self.tracker.log_metadata(
            {
                "study_name": self.config.project.name,
                "device": self.device,
                "model_name": self.config.model.name,
                "dataset_name": self.config.data.dataset_name,
            }
        )

        baseline_metrics: dict[str, float] | None = None
        self._results = []

        for candidate_config in self.config.candidates:
            if not candidate_config.enabled:
                continue

            LOGGER.info("Running candidate '%s' with method '%s'", candidate_config.name, candidate_config.method)
            method = create_optimization_method(candidate_config)
            model = method.apply(bundle.model)
            metrics = self.evaluator.evaluate(
                model=model,
                dataloader=bundle.dataloader,
                labels=bundle.labels,
                baseline_metrics=baseline_metrics,
            )
            result = CandidateResult(
                candidate_name=candidate_config.name,
                optimization_method=candidate_config.method,
                configuration=candidate_config.model_dump(mode="json"),
                metrics=metrics,
                artifacts={},
                runtime_metadata={"device": self.device},
            )
            self._results.append(result)
            self.artifacts.write_json(f"{candidate_config.name}/metrics.json", result.to_dict())

            if candidate_config.method == "baseline":
                baseline_metrics = metrics
                self.state.baseline_complete = True
            else:
                self.state.optimization_complete = True

        self.state.evaluation_complete = True
        self.recommend()
        self._comparison = self.compare()
        self.generate_report()
        return self._results

    def compare(self) -> list[dict[str, Any]]:
        rows = [
            {
                "candidate": result.candidate_name,
                "method": result.optimization_method,
                **result.metrics,
                "status": result.recommendation_status or "pending",
            }
            for result in self._results
        ]
        self._comparison = rows
        self.artifacts.write_frame("comparison.csv", rows)
        return rows

    def recommend(self) -> CandidateResult:
        if not self._results:
            raise ValueError("Study has not been run yet.")
        recommendation = self.decision_engine.recommend(self._results)
        self.artifacts.write_json("recommendation.json", recommendation.to_dict())
        return recommendation

    def generate_report(self, output_path: str | Path | None = None) -> Path:
        if not self._results:
            raise ValueError("Study has not been run yet.")
        generator = MarkdownReportGenerator()
        comparison = self._comparison if self._comparison is not None else self.compare()
        recommendation = self.recommend()
        report = generator.render(
            config=self.config,
            results=self._results,
            comparison=comparison,
            recommendation=recommendation,
        )
        target = Path(output_path) if output_path else self.artifacts.root / "report.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(report, encoding="utf-8")
        self.state.report_complete = True
        return target

    @property
    def results(self) -> list[CandidateResult]:
        return self._results

    @property
    def comparison(self) -> list[dict[str, Any]] | None:
        return self._comparison
