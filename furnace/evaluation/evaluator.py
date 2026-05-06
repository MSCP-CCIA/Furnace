from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from furnace.evaluation.base import Metric
from furnace.evaluation.efficiency_metrics import MemoryMetric, ModelSizeMetric
from furnace.evaluation.latency_metrics import LatencyMetric
from furnace.evaluation.task_metrics import AccuracyMetric, F1Metric


class Evaluator:
    def __init__(self, metric_names: Iterable[str]) -> None:
        self.metrics = [_build_metric(metric_name) for metric_name in metric_names]

    def evaluate(
        self,
        model: nn.Module,
        dataloader: DataLoader[tuple[torch.Tensor, torch.Tensor]],
        labels: list[int],
        baseline_metrics: dict[str, float] | None = None,
    ) -> dict[str, float]:
        context: dict[str, Any] = {"labels": labels, "baseline_metrics": baseline_metrics}
        results = {metric.name: metric.compute(model, dataloader, context) for metric in self.metrics}
        if baseline_metrics is not None and "accuracy" in results:
            results["quality_loss"] = max(0.0, baseline_metrics["accuracy"] - results["accuracy"])
        else:
            results["quality_loss"] = 0.0
        return results


def _build_metric(metric_name: str) -> Metric:
    if metric_name == "accuracy":
        return AccuracyMetric()
    if metric_name == "f1":
        return F1Metric()
    if metric_name == "latency":
        return LatencyMetric()
    if metric_name == "memory":
        return MemoryMetric()
    if metric_name == "model_size":
        return ModelSizeMetric()
    raise ValueError(f"Unsupported metric: {metric_name}")
