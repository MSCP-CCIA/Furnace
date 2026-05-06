from __future__ import annotations

import copy

import torch
import torch.nn as nn

from furnace.core.config import OptimizationCandidateConfig
from furnace.optimization.base import OptimizationMethod


class BaselineMethod(OptimizationMethod):
    name = "baseline"

    def apply(self, model: nn.Module) -> nn.Module:
        return copy.deepcopy(model).eval()


class DynamicQuantizationMethod(OptimizationMethod):
    name = "dynamic_quantization"

    def apply(self, model: nn.Module) -> nn.Module:
        candidate = copy.deepcopy(model).eval()
        return torch.quantization.quantize_dynamic(candidate, {nn.Linear}, dtype=torch.qint8)


def create_optimization_method(candidate: OptimizationCandidateConfig) -> OptimizationMethod:
    if candidate.method == "baseline":
        return BaselineMethod()
    if candidate.method == "dynamic_quantization":
        return DynamicQuantizationMethod()
    raise ValueError(f"Unsupported optimization method: {candidate.method}")
