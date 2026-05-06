from __future__ import annotations

from typing import Any

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from furnace.evaluation.base import Metric


class FlopsMetric(Metric):
    name = "flops"
    higher_is_better = False

    def compute(
        self,
        model: nn.Module,
        dataloader: DataLoader[tuple[torch.Tensor, torch.Tensor]],
        context: dict[str, Any],
    ) -> float:
        del model, dataloader, context
        return 0.0
