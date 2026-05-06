from furnace.core.config import DataConfig, ModelConfig
from furnace.evaluation.evaluator import Evaluator
from furnace.models.loader import load_model


def test_evaluator_returns_requested_metrics() -> None:
    bundle = load_model(ModelConfig(), DataConfig())
    evaluator = Evaluator(["accuracy", "f1", "latency", "memory", "model_size"])
    metrics = evaluator.evaluate(bundle.model, bundle.dataloader, bundle.labels)
    assert set(metrics) == {"accuracy", "f1", "latency", "memory", "model_size", "quality_loss"}
