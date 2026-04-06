"""Tests for discovery tools."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest


async def _passthrough(func, *args, **kwargs):
    """Call the function directly without threading."""
    return func(*args, **kwargs)


@pytest.fixture
def _patch_run_sync():
    """Patch run_sync to directly call the function (no threading)."""
    with patch("atlasopenmagic_mcp.tools.discovery.run_sync", side_effect=_passthrough):
        yield


def _capture_tools(register_func):
    """Helper to capture tools registered by a module."""
    mcp = MagicMock()
    tools: dict = {}

    def capture_tool():
        def decorator(func):
            tools[func.__name__] = func
            return func
        return decorator

    mcp.tool = capture_tool
    register_func(mcp)
    return tools


@pytest.mark.usefixtures("_patch_run_sync")
class TestDiscoveryTools:
    async def test_available_releases(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.discovery import register
        tools = _capture_tools(register)

        result = await tools["atlas_available_releases"](ctx=mock_ctx)
        assert "2024r-pp" in result
        assert "2020e-13tev" in result

    async def test_set_release(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.discovery import register
        tools = _capture_tools(register)

        result = await tools["atlas_set_release"](release="2024r-pp", ctx=mock_ctx)
        assert "2024r-pp" in result

    async def test_get_current_release(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.discovery import register
        tools = _capture_tools(register)

        result = await tools["atlas_get_current_release"](ctx=mock_ctx)
        assert result == "2024r-pp"

    async def test_available_datasets(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.discovery import register
        tools = _capture_tools(register)

        result = await tools["atlas_available_datasets"](ctx=mock_ctx)
        data = json.loads(result)
        assert data["count"] == 2
        assert "301204" in data["datasets"]

    async def test_available_skims(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.discovery import register
        tools = _capture_tools(register)

        result = await tools["atlas_available_skims"](ctx=mock_ctx)
        skims = json.loads(result)
        assert "exactly4lep" in skims

    async def test_available_keywords(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.discovery import register
        tools = _capture_tools(register)

        result = await tools["atlas_available_keywords"](ctx=mock_ctx)
        keywords = json.loads(result)
        assert "higgs" in keywords

    async def test_get_metadata_fields(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.discovery import register
        tools = _capture_tools(register)

        result = await tools["atlas_get_metadata_fields"](ctx=mock_ctx)
        fields = json.loads(result)
        assert "cross_section_pb" in fields
