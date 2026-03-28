"""Tests for URL retrieval tools."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest


async def _passthrough(func, *args, **kwargs):
    return func(*args, **kwargs)


@pytest.fixture
def _patch_run_sync():
    with patch("atlasopenmagic_mcp.tools.urls.run_sync", side_effect=_passthrough):
        yield


def _capture_tools(register_func):
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
class TestUrlTools:
    async def test_get_urls_default(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.urls import register
        tools = _capture_tools(register)

        result = await tools["atlas_get_urls"](dataset="301204", ctx=mock_ctx)
        urls = json.loads(result)
        assert len(urls) == 2
        assert "opendata.cern.ch" in urls[0]

    async def test_get_urls_with_skim(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.urls import register
        tools = _capture_tools(register)

        await tools["atlas_get_urls"](
            dataset="301204", skim="exactly4lep", protocol="root", ctx=mock_ctx
        )
        atom = mock_ctx.request_context.lifespan_context["atom"]
        atom.get_urls.assert_called_with("301204", "exactly4lep", "root")

    async def test_get_urls_error(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.urls import register

        mock_ctx.request_context.lifespan_context["atom"].get_urls.side_effect = ValueError("not found")
        tools = _capture_tools(register)

        result = await tools["atlas_get_urls"](dataset="999999", ctx=mock_ctx)
        assert "Error" in result
