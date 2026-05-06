from __future__ import annotations

import time
from typing import Any

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from furnace.evaluation.base import Metric


class LatencyMetric(Metric):
    name = "latency"
    higher_is_better = False

    def compute(
        self,
        model: nn.Module,
        dataloader: DataLoader[tuple[torch.Tensor, torch.Tensor]],
        context: dict[str, Any],
    ) -> float:
        model.eval()
        elapsed = 0.0
        batches = 0
        with torch.no_grad():
            for features, _ in dataloader:
                started = time.perf_counter()
                _ = model(features)
                elapsed += (time.perf_counter() - started) * 1000
                batches += 1
        return elapsed / max(batches, 1)
