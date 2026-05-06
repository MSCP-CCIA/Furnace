from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PipelineState:
    """Captures high-level study execution state."""

    baseline_complete: bool = False
    optimization_complete: bool = False
    evaluation_complete: bool = False
    report_complete: bool = False
    notes: list[str] = field(default_factory=list)
