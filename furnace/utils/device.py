from __future__ import annotations

import torch


def resolve_device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"
