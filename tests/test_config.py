from pathlib import Path

from furnace.core.config import load_config


def test_load_config_reads_default_yaml() -> None:
    config = load_config(Path("configs/default.yaml"))
    assert config.project.name == "default-study"
    assert len(config.candidates) == 2
