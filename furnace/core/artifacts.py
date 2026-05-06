from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from furnace.utils import simple_yaml


class ArtifactStore:
    """Manages structured study outputs under a run directory."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def write_json(self, relative_path: str, payload: dict[str, Any]) -> Path:
        target = self.root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return target

    def write_yaml(self, relative_path: str, payload: dict[str, Any]) -> Path:
        target = self.root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            import yaml  # type: ignore

            content = yaml.safe_dump(payload, sort_keys=False)
        except ModuleNotFoundError:
            content = simple_yaml.dump(payload)
        target.write_text(content, encoding="utf-8")
        return target

    def write_text(self, relative_path: str, content: str) -> Path:
        target = self.root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def write_frame(self, relative_path: str, rows: list[dict[str, Any]]) -> Path:
        target = self.root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if not rows:
            target.write_text("", encoding="utf-8")
            return target
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        return target
