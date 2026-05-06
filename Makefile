PYTHON ?= python
UV ?= uv

.PHONY: install install-dev format lint test run-example

install:
	$(UV) sync

install-dev:
	$(UV) sync --extra dev

format:
	$(UV) run black furnace tests examples
	$(UV) run ruff check --fix furnace tests examples

lint:
	$(UV) run ruff check furnace tests examples
	$(UV) run mypy furnace

test:
	$(UV) run pytest

run-example:
	$(UV) run furnace run --config configs/default.yaml
