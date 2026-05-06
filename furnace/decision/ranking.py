from __future__ import annotations

from furnace.optimization.base import CandidateResult


def score_candidate(result: CandidateResult, weights: dict[str, float]) -> float:
    metrics = result.metrics
    positive = metrics.get("accuracy", 0.0) * weights.get("accuracy", 0.0)
    positive += metrics.get("f1", 0.0) * weights.get("f1", 0.0)
    negative = metrics.get("latency", 0.0) * weights.get("latency", 0.0)
    negative += metrics.get("memory", 0.0) * weights.get("memory", 0.0)
    negative += metrics.get("model_size", 0.0) * weights.get("model_size", 0.0)
    return positive - negative
