from __future__ import annotations

from dataclasses import dataclass

from furnace.core.config import ConstraintsConfig
from furnace.optimization.base import CandidateResult


@dataclass(frozen=True)
class Constraints:
    max_quality_loss: float
    max_latency_ms: float
    max_memory_mb: float
    max_model_size_mb: float

    @classmethod
    def from_config(cls, config: ConstraintsConfig) -> "Constraints":
        return cls(
            max_quality_loss=config.max_quality_loss,
            max_latency_ms=config.max_latency_ms,
            max_memory_mb=config.max_memory_mb,
            max_model_size_mb=config.max_model_size_mb,
        )

    def violations_for(self, result: CandidateResult) -> list[str]:
        violations: list[str] = []
        metrics = result.metrics
        if metrics.get("quality_loss", 0.0) > self.max_quality_loss:
            violations.append("quality_loss")
        if metrics.get("latency", 0.0) > self.max_latency_ms:
            violations.append("latency")
        if metrics.get("memory", 0.0) > self.max_memory_mb:
            violations.append("memory")
        if metrics.get("model_size", 0.0) > self.max_model_size_mb:
            violations.append("model_size")
        return violations
