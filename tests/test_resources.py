"""Tests for MCP resources."""

from __future__ import annotations

from unittest.mock import MagicMock

from atlasopenmagic_mcp.resources import register


def test_resources_registered() -> None:
    """Verify all resources are registered with the MCP server."""
    mcp = MagicMock()
    registered: list[str] = []

    def capture_resource(uri, **kwargs):
        def decorator(func):
            registered.append(uri)
            return func
        return decorator

    mcp.resource = capture_resource
    register(mcp)

    assert "atlas-open-data://guide" in registered
    assert "atlas-open-data://metadata-fields" in registered


def test_resource_content() -> None:
    """Verify resource functions return non-empty content."""
    from atlasopenmagic_mcp.nomenclature import (
        ATLAS_OPEN_DATA_GUIDE,
        METADATA_FIELDS_REFERENCE,
    )

    assert len(ATLAS_OPEN_DATA_GUIDE) > 100
    assert len(METADATA_FIELDS_REFERENCE) > 100
    assert "release" in ATLAS_OPEN_DATA_GUIDE.lower()
    assert "dataset_number" in METADATA_FIELDS_REFERENCE
