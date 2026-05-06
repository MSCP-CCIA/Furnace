from __future__ import annotations

import copy
from dataclasses import dataclass

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from furnace.core.config import DataConfig, ModelConfig
from furnace.data.dataloaders import build_dataloader
from furnace.data.datasets import build_dataset


class ToyMLP(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, num_classes: int) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_classes),
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return self.network(inputs)


@dataclass
class ModelBundle:
    model: nn.Module
    dataloader: DataLoader[tuple[torch.Tensor, torch.Tensor]]
    labels: list[int]


def load_model(model_config: ModelConfig, data_config: DataConfig | None = None) -> ModelBundle:
    resolved_data_config = data_config or DataConfig(
        batch_size=16,
        num_samples=256,
        calibration_samples=64,
    )
    if model_config.source != "toy":
        raise ValueError("The MVP currently supports only source='toy'.")

    model = ToyMLP(
        input_dim=model_config.input_dim,
        hidden_dim=model_config.hidden_dim,
        num_classes=model_config.num_classes,
    )
    dataset = build_dataset(model_config, resolved_data_config)
    dataloader = build_dataloader(dataset, batch_size=resolved_data_config.batch_size)
    labels = copy.deepcopy(dataset.targets.tolist())
    return ModelBundle(model=model, dataloader=dataloader, labels=labels)
