from __future__ import annotations

from typing import Any

from furnace.utils.logger import get_logger

LOGGER = get_logger(__name__)


class LocalTracker:
    def log_metadata(self, metadata: dict[str, Any]) -> None:
        LOGGER.info("Tracking metadata: %s", metadata)
