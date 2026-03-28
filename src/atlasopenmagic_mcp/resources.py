"""MCP resources exposing ATLAS Open Data documentation to the LLM."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP  # noqa: TC002

from atlasopenmagic_mcp.nomenclature import (
    ATLAS_OPEN_DATA_GUIDE,
    METADATA_FIELDS_REFERENCE,
)


def register(mcp: FastMCP) -> None:
    """Register documentation resources with the MCP server."""

    @mcp.resource(
        "atlas-open-data://guide",
        name="ATLAS Open Data Guide",
        description=(
            "Quick reference for ATLAS Open Data: available releases, dataset "
            "identification (DSID, physics_short), skims, metadata fields, "
            "file URL protocols, keywords, and weight metadata."
        ),
        mime_type="text/plain",
    )
    def get_atlas_open_data_guide() -> str:
        return ATLAS_OPEN_DATA_GUIDE

    @mcp.resource(
        "atlas-open-data://metadata-fields",
        name="ATLAS Open Data Metadata Fields Reference",
        description=(
            "Complete reference for dataset metadata fields: core identification "
            "(DSID, physics_short, e_tag), physics parameters (cross-section, "
            "genFiltEff, kFactor), generation details, and file access fields."
        ),
        mime_type="text/plain",
    )
    def get_metadata_fields_reference() -> str:
        return METADATA_FIELDS_REFERENCE
