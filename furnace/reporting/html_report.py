from __future__ import annotations


def render_html_stub(markdown_body: str) -> str:
    return f"<html><body><pre>{markdown_body}</pre></body></html>"
