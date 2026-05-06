from __future__ import annotations

from furnace.optimization.base import OptimizationMethod


class DistillationMethod(OptimizationMethod):
    name = "distillation"

    def apply(self, model):  # type: ignore[override]
        return model
