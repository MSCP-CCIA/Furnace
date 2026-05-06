# Furnace

Furnace is a production-aware framework for optimizing, benchmarking, and evaluating deep learning models across quality, latency, memory, and deployment trade-offs.

## Status

This repository now includes the initial MVP:

- Typed configuration models backed by YAML.
- A modular `OptimizationStudy` orchestration flow.
- Baseline evaluation plus dynamic quantization.
- Metrics for accuracy, F1, latency, memory, and model size.
- Constraint filtering, weighted ranking, and recommendation output.
- Markdown report generation.
- A `furnace` CLI implemented with Typer.
- Tests, docs skeleton, example configs, and CI skeletons.

## Project layout

The repository keeps the broad architecture requested in `README_FURNACE_CODEX.md`, but only the MVP path is implemented end to end:

```text
config -> study -> model/data loading -> optimization -> metrics -> decision -> report
```

The remaining modules are scaffolded so the project can grow without forcing a rewrite later.

## Quick start with uv

```bash
uv sync --extra dev
uv run furnace run --config configs/default.yaml
```

## CLI

```bash
uv run furnace run --config configs/default.yaml
uv run furnace profile --config configs/default.yaml
uv run furnace evaluate --config configs/default.yaml
uv run furnace optimize --config configs/default.yaml
uv run furnace report --run-dir outputs/default-study
```

## Python API

```python
from furnace import OptimizationStudy

study = OptimizationStudy.from_config("configs/default.yaml")
results = study.run()
recommendation = study.recommend()
study.generate_report()
```

## MVP scope

The current MVP is intentionally narrow:

- `toy_mlp` model loader for local iteration.
- Synthetic classification dataset for reproducible tests.
- Baseline and dynamic quantization candidates.
- Markdown report and structured JSON/CSV outputs.

This is enough to validate architecture, CLI, reproducibility, and decision logic before adding larger backends such as ONNX Runtime or TensorRT.
