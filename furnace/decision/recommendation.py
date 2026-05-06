from __future__ import annotations

from furnace.decision.constraints import Constraints
from furnace.decision.ranking import score_candidate
from furnace.optimization.base import CandidateResult


class DecisionEngine:
    def __init__(self, constraints: Constraints, weights: dict[str, float]) -> None:
        self.constraints = constraints
        self.weights = weights

    def recommend(self, results: list[CandidateResult]) -> CandidateResult:
        viable: list[CandidateResult] = []
        for result in results:
            result.violations = self.constraints.violations_for(result)
            result.recommendation_status = "rejected" if result.violations else "valid"
            result.score = score_candidate(result, self.weights)
            if not result.violations:
                viable.append(result)

        pool = viable if viable else results
        winner = max(pool, key=lambda item: item.score if item.score is not None else float("-inf"))
        winner.recommendation_status = "recommended"
        return winner
