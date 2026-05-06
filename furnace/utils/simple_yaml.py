from __future__ import annotations

from pathlib import Path
from typing import Any


def load(path: str | Path) -> dict[str, Any]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    data, _ = _parse_block(lines, 0, 0)
    if not isinstance(data, dict):
        raise ValueError("Top-level YAML structure must be a mapping.")
    return data


def dump(payload: dict[str, Any]) -> str:
    return _dump_value(payload, 0).rstrip() + "\n"


def _parse_block(lines: list[str], start_index: int, indent: int) -> tuple[Any, int]:
    mapping: dict[str, Any] = {}
    sequence: list[Any] | None = None
    index = start_index

    while index < len(lines):
        raw = lines[index]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            index += 1
            continue

        current_indent = len(raw) - len(raw.lstrip(" "))
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ValueError(f"Unexpected indentation at line {index + 1}: {raw}")

        content = raw[current_indent:]
        if content.startswith("- "):
            if mapping:
                raise ValueError("Cannot mix mapping and sequence at the same level.")
            if sequence is None:
                sequence = []

            item_content = content[2:].strip()
            if not item_content:
                nested, next_index = _parse_block(lines, index + 1, indent + 2)
                sequence.append(nested)
                index = next_index
                continue

            if ":" in item_content:
                key, value = _split_key_value(item_content)
                item: dict[str, Any] = {key: _parse_scalar(value)} if value else {}
                next_index = index + 1
                if next_index < len(lines):
                    nested_indent = _line_indent(lines[next_index])
                    if nested_indent > indent:
                        nested, next_index = _parse_block(lines, next_index, indent + 2)
                        if isinstance(nested, dict):
                            item.update(nested)
                sequence.append(item)
                index = next_index
                continue

            sequence.append(_parse_scalar(item_content))
            index += 1
            continue

        key, value = _split_key_value(content)
        if value:
            mapping[key] = _parse_scalar(value)
            index += 1
            continue

        nested, next_index = _parse_block(lines, index + 1, indent + 2)
        mapping[key] = nested
        index = next_index

    return (sequence if sequence is not None else mapping), index


def _split_key_value(content: str) -> tuple[str, str]:
    key, _, value = content.partition(":")
    return key.strip(), value.strip()


def _parse_scalar(value: str) -> Any:
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "none"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _dump_value(value: Any, indent: int) -> str:
    prefix = " " * indent
    if isinstance(value, dict):
        parts: list[str] = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                parts.append(f"{prefix}{key}:")
                parts.append(_dump_value(item, indent + 2))
            else:
                parts.append(f"{prefix}{key}: {_format_scalar(item)}")
        return "\n".join(parts)
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict):
                first = True
                for key, nested in item.items():
                    if first and not isinstance(nested, (dict, list)):
                        parts.append(f"{prefix}- {key}: {_format_scalar(nested)}")
                        first = False
                    else:
                        if first:
                            parts.append(f"{prefix}- {key}:")
                            first = False
                        elif isinstance(nested, (dict, list)):
                            parts.append(f"{prefix}  {key}:")
                        else:
                            parts.append(f"{prefix}  {key}: {_format_scalar(nested)}")
                        if isinstance(nested, (dict, list)):
                            parts.append(_dump_value(nested, indent + 4))
            else:
                parts.append(f"{prefix}- {_format_scalar(item)}")
        return "\n".join(parts)
    return f"{prefix}{_format_scalar(value)}"


def _format_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    return str(value)


def _line_indent(line: str) -> int:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return -1
    return len(line) - len(line.lstrip(" "))
