from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar

from furnace.core.exceptions import RegistryError

T = TypeVar("T")


class Registry(Generic[T]):
    """Minimal string-to-factory registry for extensible components."""

    def __init__(self) -> None:
        self._items: dict[str, Callable[..., T]] = {}

    def register(self, name: str, factory: Callable[..., T]) -> None:
        self._items[name] = factory

    def create(self, name: str, **kwargs: object) -> T:
        try:
            factory = self._items[name]
        except KeyError as exc:
            available = ", ".join(sorted(self._items))
            raise RegistryError(f"Unknown registry entry '{name}'. Available: {available}") from exc
        return factory(**kwargs)

    def names(self) -> list[str]:
        return sorted(self._items)
