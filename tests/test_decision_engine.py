from furnace.decision.constraints import Constraints
from furnace.decision.recommendation import DecisionEngine
from furnace.optimization.base import CandidateResult


def test_decision_engine_marks_recommendation() -> None:
    engine = DecisionEngine(
        constraints=Constraints(
            max_quality_loss=0.05,
            max_latency_ms=100.0,
            max_memory_mb=10.0,
            max_model_size_mb=10.0,
        ),
        weights={"accuracy": 1.0, "f1": 0.0, "latency": 0.01, "memory": 0.0, "model_size": 0.0},
    )
    baseline = CandidateResult(
        candidate_name="baseline",
        optimization_method="baseline",
        configuration={},
        metrics={"accuracy": 0.8, "f1": 0.8, "latency": 20.0, "memory": 1.0, "model_size": 1.0, "quality_loss": 0.0},
        artifacts={},
        runtime_metadata={},
    )
    optimized = CandidateResult(
        candidate_name="dynamic",
        optimization_method="dynamic_quantization",
        configuration={},
        metrics={"accuracy": 0.79, "f1": 0.79, "latency": 10.0, "memory": 0.5, "model_size": 0.5, "quality_loss": 0.01},
        artifacts={},
        runtime_metadata={},
    )
    recommendation = engine.recommend([baseline, optimized])
    assert recommendation.recommendation_status == "recommended"
