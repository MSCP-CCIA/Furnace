from __future__ import annotations

from furnace.optimization.base import CandidateResult


def pareto_frontier(results: list[CandidateResult]) -> list[CandidateResult]:
    ordered = sorted(results, key=lambda item: (item.metrics.get("latency", 0.0), -item.metrics.get("accuracy", 0.0)))
    frontier: list[CandidateResult] = []
    best_accuracy = -1.0
    for result in ordered:
        accuracy = result.metrics.get("accuracy", 0.0)
        if accuracy >= best_accuracy:
            frontier.append(result)
            best_accuracy = accuracy
    return frontier
