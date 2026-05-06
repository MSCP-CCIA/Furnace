from __future__ import annotations

from dataclasses import dataclass

import torch
from torch.utils.data import Dataset

from furnace.core.config import DataConfig, ModelConfig


@dataclass
class SyntheticClassificationDataset(Dataset[tuple[torch.Tensor, torch.Tensor]]):
    features: torch.Tensor
    targets: torch.Tensor

    def __len__(self) -> int:
        return int(self.targets.shape[0])

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.features[index], self.targets[index]


def build_dataset(model_config: ModelConfig, data_config: DataConfig) -> SyntheticClassificationDataset:
    generator = torch.Generator().manual_seed(42)
    features = torch.randn(data_config.num_samples, model_config.input_dim, generator=generator)
    weights = torch.randn(model_config.input_dim, model_config.num_classes, generator=generator)
    logits = features @ weights
    targets = torch.argmax(logits, dim=1)
    return SyntheticClassificationDataset(features=features, targets=targets)
