"""Tests for weight metadata tools."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest


async def _passthrough(func, *args, **kwargs):
    return func(*args, **kwargs)


@pytest.fixture
def _patch_run_sync():
    with patch("atlasopenmagic_mcp.tools.weights.run_sync", side_effect=_passthrough):
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
class TestWeightTools:
    async def test_get_weights(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.weights import register
        tools = _capture_tools(register)

        result = await tools["atlas_get_weights"](dataset="306600", ctx=mock_ctx)
        data = json.loads(result)
        assert data["weight_count"] == 3
        assert "nominal" in data["weights"]

    async def test_get_weights_with_etag(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.weights import register
        tools = _capture_tools(register)

        await tools["atlas_get_weights"](
            dataset="306600", e_tag="e8514", ctx=mock_ctx
        )
        atom = mock_ctx.request_context.lifespan_context["atom"]
        atom.get_weights.assert_called_with("306600", "e8514")

    async def test_get_all_weights_for_release(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.weights import register
        tools = _capture_tools(register)

        result = await tools["atlas_get_all_weights_for_release"](ctx=mock_ctx)
        data = json.loads(result)
        assert data["total_datasets_with_weights"] == 2
        assert "306600" in data["datasets"]

    async def test_get_all_weights_error(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.weights import register

        mock_ctx.request_context.lifespan_context["atom"].get_all_weights_for_release.side_effect = (
            ValueError("not available")
        )
        tools = _capture_tools(register)

        result = await tools["atlas_get_all_weights_for_release"](ctx=mock_ctx)
        assert "Error" in result
