from __future__ import annotations

from furnace.optimization.base import OptimizationMethod


class TorchCompileMethod(OptimizationMethod):
    name = "torch_compile"

    def apply(self, model):  # type: ignore[override]
        return model
