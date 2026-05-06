from __future__ import annotations

import io
from typing import Any

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from furnace.evaluation.base import Metric


class MemoryMetric(Metric):
    name = "memory"
    higher_is_better = False

    def compute(
        self,
        model: nn.Module,
        dataloader: DataLoader[tuple[torch.Tensor, torch.Tensor]],
        context: dict[str, Any],
    ) -> float:
        del dataloader, context
        parameter_bytes = sum(parameter.numel() * parameter.element_size() for parameter in model.parameters())
        buffer_bytes = sum(buffer.numel() * buffer.element_size() for buffer in model.buffers())
        return float((parameter_bytes + buffer_bytes) / (1024 * 1024))


class ModelSizeMetric(Metric):
    name = "model_size"
    higher_is_better = False

    def compute(
        self,
        model: nn.Module,
        dataloader: DataLoader[tuple[torch.Tensor, torch.Tensor]],
        context: dict[str, Any],
    ) -> float:
        del dataloader, context
        buffer = io.BytesIO()
        torch.save(model.state_dict(), buffer)
        return float(buffer.tell() / (1024 * 1024))
