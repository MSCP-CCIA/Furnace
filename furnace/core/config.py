from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field

from furnace.utils import simple_yaml


class ProjectConfig(BaseModel):
    name: str = "default-study"
    output_dir: Path = Path("outputs/default-study")
    seed: int = 42


class ModelConfig(BaseModel):
    source: str = "toy"
    name: str = "toy_mlp"
    task: str = "classification"
    input_dim: int = 8
    hidden_dim: int = 16
    num_classes: int = 2


class DataConfig(BaseModel):
    dataset_name: str = "synthetic_classification"
    subset: str | None = None
    batch_size: int = 16
    num_samples: int = 256
    calibration_samples: int = 64


class OptimizationCandidateConfig(BaseModel):
    name: str
    method: str
    backend: str | None = None
    enabled: bool = True
    dtype: str | None = None
    mode: str | None = None
    amount: float | None = None


class EvaluationConfig(BaseModel):
    metrics: list[str] = Field(
        default_factory=lambda: ["accuracy", "f1", "latency", "memory", "model_size"]
    )


class ConstraintsConfig(BaseModel):
    max_quality_loss: float = 0.05
    max_latency_ms: float = 1000.0
    max_memory_mb: float = 4096.0
    max_model_size_mb: float = 1024.0


class DecisionConfig(BaseModel):
    weights: dict[str, float] = Field(
        default_factory=lambda: {
            "accuracy": 0.4,
            "f1": 0.2,
            "latency": 0.2,
            "memory": 0.1,
            "model_size": 0.1,
        }
    )


class ReportingConfig(BaseModel):
    formats: list[str] = Field(default_factory=lambda: ["markdown"])


class TrackingConfig(BaseModel):
    backend: str = "local"


class FurnaceConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    project: ProjectConfig = Field(default_factory=ProjectConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    optimization: dict[str, list[OptimizationCandidateConfig]] = Field(
        default_factory=lambda: {
            "candidates": [
                OptimizationCandidateConfig(name="baseline", method="baseline"),
                OptimizationCandidateConfig(name="dynamic_int8", method="dynamic_quantization"),
            ]
        }
    )
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)
    constraints: ConstraintsConfig = Field(default_factory=ConstraintsConfig)
    decision: DecisionConfig = Field(default_factory=DecisionConfig)
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)
    tracking: TrackingConfig = Field(default_factory=TrackingConfig)

    @property
    def candidates(self) -> list[OptimizationCandidateConfig]:
        return self.optimization["candidates"]


def load_config(path: str | Path) -> FurnaceConfig:
    try:
        import yaml  # type: ignore

        config_path = Path(path)
        payload = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    except ModuleNotFoundError:
        payload = simple_yaml.load(path)
    return FurnaceConfig.model_validate(payload)
