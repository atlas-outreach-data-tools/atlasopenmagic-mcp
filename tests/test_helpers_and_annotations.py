"""Tests for response caps and read-only tool annotations."""

from __future__ import annotations

from atlasopenmagic_mcp.server import _make_mcp
from atlasopenmagic_mcp.tools._helpers import cap_response


def test_cap_response_keeps_short_text() -> None:
    assert cap_response("abc", limit=10) == "abc"


def test_cap_response_truncates_long_text() -> None:
    out = cap_response("x" * 100, limit=10)
    assert out.startswith("x" * 10)
    assert "Truncated" in out
    assert "x" * 11 not in out


async def test_only_set_release_is_not_read_only() -> None:
    tools = await _make_mcp().list_tools()
    assert len(tools) == 13
    writers = {t.name for t in tools if not (t.annotations and t.annotations.readOnlyHint)}
    assert writers == {"atlas_set_release"}
