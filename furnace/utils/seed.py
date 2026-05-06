from __future__ import annotations

import random

import torch


def set_seed(seed: int) -> None:
    random.seed(seed)
    try:
        import numpy as np  # type: ignore

        np.random.seed(seed)
    except ModuleNotFoundError:
        pass
    torch.manual_seed(seed)
