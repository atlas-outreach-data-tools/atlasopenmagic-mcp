"""Tests for metadata tools."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest


async def _passthrough(func, *args, **kwargs):
    return func(*args, **kwargs)


@pytest.fixture
def _patch_run_sync():
    with patch("atlasopenmagic_mcp.tools.metadata.run_sync", side_effect=_passthrough):
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
class TestMetadataTools:
    async def test_get_metadata(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.metadata import register
        tools = _capture_tools(register)

        result = await tools["atlas_get_metadata"](dataset="301204", ctx=mock_ctx)
        data = json.loads(result)
        assert data["dataset_number"] == "301204"
        assert data["physics_short"] == "zprime_ee"

    async def test_get_metadata_single_field(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.metadata import register

        mock_ctx.request_context.lifespan_context["atom"].get_metadata.return_value = 1.23
        tools = _capture_tools(register)

        result = await tools["atlas_get_metadata"](
            dataset="301204", field="cross_section_pb", ctx=mock_ctx
        )
        assert "1.23" in result

    async def test_get_all_info(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.metadata import register
        tools = _capture_tools(register)

        result = await tools["atlas_get_all_info"](dataset="301204", ctx=mock_ctx)
        data = json.loads(result)
        assert "file_list" in data

    async def test_match_metadata(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.metadata import register
        tools = _capture_tools(register)

        result = await tools["atlas_match_metadata"](
            field="keywords", value="higgs", ctx=mock_ctx
        )
        assert "301204" in result
        assert "zprime_ee" in result

    async def test_match_metadata_and(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.metadata import register
        tools = _capture_tools(register)

        result = await tools["atlas_match_metadata"](
            field="keywords", value="top,Alternative", ctx=mock_ctx
        )
        atom = mock_ctx.request_context.lifespan_context["atom"]
        atom.match_metadata.assert_called_with("keywords", ["top", "Alternative"])

    async def test_match_metadata_no_results(self, mock_ctx: MagicMock) -> None:
        from atlasopenmagic_mcp.tools.metadata import register

        mock_ctx.request_context.lifespan_context["atom"].match_metadata.return_value = []
        tools = _capture_tools(register)

        result = await tools["atlas_match_metadata"](
            field="keywords", value="nonexistent", ctx=mock_ctx
        )
        assert "No matching" in result
