from __future__ import annotations

import time
from contextlib import contextmanager
from collections.abc import Iterator


@contextmanager
def timer() -> Iterator[float]:
    started = time.perf_counter()
    yield started
