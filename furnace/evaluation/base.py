from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import torch
import torch.nn as nn
from torch.utils.data import DataLoader


class Metric(ABC):
    name: str
    higher_is_better: bool = True

    @abstractmethod
    def compute(
        self,
        model: nn.Module,
        dataloader: DataLoader[tuple[torch.Tensor, torch.Tensor]],
        context: dict[str, Any],
    ) -> float:
        raise NotImplementedError
