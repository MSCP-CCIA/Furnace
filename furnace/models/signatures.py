from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelSignature:
    name: str
    task: str
    input_dim: int
    num_classes: int
