from __future__ import annotations

from furnace.optimization.base import OptimizationMethod


class PruningMethod(OptimizationMethod):
    name = "pruning"

    def apply(self, model):  # type: ignore[override]
        return model
