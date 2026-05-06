from __future__ import annotations

from itertools import islice

from torch.utils.data import DataLoader


def calibration_batches(
    dataloader: DataLoader[tuple[object, object]], max_batches: int
) -> list[tuple[object, object]]:
    return list(islice(dataloader, max_batches))
