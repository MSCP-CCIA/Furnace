from furnace.core.config import OptimizationCandidateConfig
from furnace.core.config import ModelConfig
from furnace.models.loader import load_model
from furnace.optimization.quantization import create_optimization_method


def test_dynamic_quantization_returns_model() -> None:
    bundle = load_model(ModelConfig())
    method = create_optimization_method(
        OptimizationCandidateConfig(name="dynamic_int8", method="dynamic_quantization")
    )
    quantized = method.apply(bundle.model)
    assert quantized is not None
