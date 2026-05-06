from __future__ import annotations

from torch.utils.data import DataLoader, Dataset


def build_dataloader(
    dataset: Dataset[tuple[object, object]], batch_size: int
) -> DataLoader[tuple[object, object]]:
    return DataLoader(dataset, batch_size=batch_size, shuffle=False)
