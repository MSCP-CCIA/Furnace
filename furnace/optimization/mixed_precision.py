from __future__ import annotations

from furnace.optimization.base import OptimizationMethod


class MixedPrecisionMethod(OptimizationMethod):
    name = "mixed_precision"

    def apply(self, model):  # type: ignore[override]
        return model
