from furnace.core.registry import Registry


def test_registry_creates_registered_object() -> None:
    registry: Registry[str] = Registry()
    registry.register("value", lambda: "ok")
    assert registry.create("value") == "ok"
