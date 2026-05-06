from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import torch.nn as nn


class OptimizationMethod(ABC):
    name: str

    @abstractmethod
    def apply(self, model: nn.Module) -> nn.Module:
        raise NotImplementedError


@dataclass
class CandidateResult:
    candidate_name: str
    optimization_method: str
    configuration: dict[str, Any]
    metrics: dict[str, float]
    artifacts: dict[str, str]
    runtime_metadata: dict[str, Any]
    recommendation_status: str | None = None
    score: float | None = None
    violations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_name": self.candidate_name,
            "optimization_method": self.optimization_method,
            "configuration": self.configuration,
            "metrics": self.metrics,
            "artifacts": self.artifacts,
            "runtime_metadata": self.runtime_metadata,
            "recommendation_status": self.recommendation_status,
            "score": self.score,
            "violations": self.violations,
        }
