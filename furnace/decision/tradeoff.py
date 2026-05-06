from __future__ import annotations

from furnace.optimization.base import CandidateResult


def summarize_tradeoff(result: CandidateResult) -> str:
    metrics = result.metrics
    return (
        f"accuracy={metrics.get('accuracy', 0.0):.4f}, "
        f"latency={metrics.get('latency', 0.0):.3f} ms, "
        f"memory={metrics.get('memory', 0.0):.3f} MB"
    )
