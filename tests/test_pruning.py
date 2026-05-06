from furnace.core.config import ModelConfig
from furnace.models.loader import load_model
from furnace.optimization.pruning import PruningMethod


def test_pruning_placeholder_returns_input_model() -> None:
    bundle = load_model(ModelConfig())
    method = PruningMethod()
    assert method.apply(bundle.model) is bundle.model
