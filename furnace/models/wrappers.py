from __future__ import annotations

from dataclasses import dataclass

import torch.nn as nn


@dataclass
class ModelWrapper:
    """Simple container for future model metadata extensions."""

    model: nn.Module
    task: str
