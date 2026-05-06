from __future__ import annotations

from typing import Any

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from furnace.evaluation.base import Metric


def _predict(
    model: nn.Module, dataloader: DataLoader[tuple[torch.Tensor, torch.Tensor]]
) -> tuple[list[int], list[int]]:
    model.eval()
    predictions: list[int] = []
    targets: list[int] = []
    with torch.no_grad():
        for features, batch_targets in dataloader:
            logits = model(features)
            batch_predictions = torch.argmax(logits, dim=1)
            predictions.extend(batch_predictions.tolist())
            targets.extend(batch_targets.tolist())
    return predictions, targets


class AccuracyMetric(Metric):
    name = "accuracy"

    def compute(
        self,
        model: nn.Module,
        dataloader: DataLoader[tuple[torch.Tensor, torch.Tensor]],
        context: dict[str, Any],
    ) -> float:
        predictions, targets = _predict(model, dataloader)
        correct = sum(int(pred == target) for pred, target in zip(predictions, targets, strict=False))
        return float(correct / max(len(targets), 1))


class F1Metric(Metric):
    name = "f1"

    def compute(
        self,
        model: nn.Module,
        dataloader: DataLoader[tuple[torch.Tensor, torch.Tensor]],
        context: dict[str, Any],
    ) -> float:
        predictions, targets = _predict(model, dataloader)
        labels = sorted(set(targets) | set(predictions))
        total = len(targets)
        weighted_f1 = 0.0
        for label in labels:
            true_positive = sum(
                1
                for pred, target in zip(predictions, targets, strict=False)
                if pred == label and target == label
            )
            false_positive = sum(
                1
                for pred, target in zip(predictions, targets, strict=False)
                if pred == label and target != label
            )
            false_negative = sum(
                1
                for pred, target in zip(predictions, targets, strict=False)
                if pred != label and target == label
            )
            precision = true_positive / max(true_positive + false_positive, 1)
            recall = true_positive / max(true_positive + false_negative, 1)
            f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
            support = sum(1 for target in targets if target == label)
            weighted_f1 += f1 * (support / max(total, 1))
        return float(weighted_f1)
