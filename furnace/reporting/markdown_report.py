from __future__ import annotations

from furnace.core.config import FurnaceConfig
from furnace.optimization.base import CandidateResult
from furnace.reporting.tables import format_metrics_table


class MarkdownReportGenerator:
    def render(
        self,
        config: FurnaceConfig,
        results: list[CandidateResult],
        comparison,
        recommendation: CandidateResult,
    ) -> str:
        del results
        return "\n".join(
            [
                f"# Furnace Report: {config.project.name}",
                "",
                "## Summary",
                "",
                f"- Model: `{config.model.name}`",
                f"- Dataset: `{config.data.dataset_name}`",
                f"- Recommended candidate: `{recommendation.candidate_name}`",
                f"- Recommendation status: `{recommendation.recommendation_status}`",
                "",
                "## Candidate Comparison",
                "",
                format_metrics_table(comparison),
                "",
                "## Constraints",
                "",
                f"- Max quality loss: `{config.constraints.max_quality_loss}`",
                f"- Max latency ms: `{config.constraints.max_latency_ms}`",
                f"- Max memory mb: `{config.constraints.max_memory_mb}`",
                f"- Max model size mb: `{config.constraints.max_model_size_mb}`",
            ]
        )
