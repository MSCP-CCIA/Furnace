from __future__ import annotations


def format_metrics_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No results available_"
    headers = list(rows[0].keys())
    header_row = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join("---" for _ in headers) + " |"
    body = [
        "| " + " | ".join(str(row.get(header, "")) for header in headers) + " |"
        for row in rows
    ]
    return "\n".join([header_row, separator, *body])
