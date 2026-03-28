"""Metadata retrieval and search tools."""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import Context, FastMCP  # noqa: TC002

from atlasopenmagic_mcp.tools._helpers import run_sync


def register(mcp: FastMCP) -> None:
    """Register metadata tools."""

    @mcp.tool()
    async def atlas_get_metadata(
        dataset: str,
        field: str | None = None,
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """Get metadata for a dataset (excludes file lists and skims).

        Returns physics parameters like cross-section, generator info,
        keywords, etc. Use atlas_get_all_info if you also need file URLs.

        Args:
            dataset: Dataset number (e.g. "301204") or physics_short name
                (e.g. "zprime_ee").
            field: Optional specific field to return (e.g. "cross_section_pb",
                "generator"). If omitted, returns all metadata fields.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            result = await run_sync(atom.get_metadata, dataset, field)
            return json.dumps(result, default=str)
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"

    @mcp.tool()
    async def atlas_get_all_info(
        dataset: str,
        field: str | None = None,
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """Get complete information for a dataset, including file lists and skims.

        Returns everything atlas_get_metadata returns, plus file_list (URLs)
        and skims (filtered event subsets with their own file lists).

        Args:
            dataset: Dataset number (e.g. "301204") or physics_short name.
            field: Optional specific field to return. If omitted, returns
                everything.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            result = await run_sync(atom.get_all_info, dataset, field)
            return json.dumps(result, default=str)
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"

    @mcp.tool()
    async def atlas_match_metadata(
        field: str,
        value: str,
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """Find datasets where a metadata field matches a given value.

        Supports substring matching for strings, approximate matching for
        floats, and membership testing for list fields (like keywords).

        For AND matching (all values must match), pass a comma-separated
        string, e.g. "top,Alternative" to find datasets with both keywords.

        Args:
            field: Metadata field to search (e.g. "keywords", "generator",
                "cross_section_pb"). Use atlas_get_metadata_fields to see
                available fields.
            value: Value to search for. Use comma-separated values for AND
                matching (e.g. "top,Alternative").
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            # Support AND matching via comma-separated values
            search_value: Any = value
            if "," in value:
                search_value = [v.strip() for v in value.split(",")]

            # Try numeric conversion for float fields
            if isinstance(search_value, str):
                try:
                    search_value = float(search_value)
                except ValueError:
                    pass

            matches = await run_sync(atom.match_metadata, field, search_value)
            if not matches:
                return "No matching datasets found."
            lines = ["| Dataset | physics_short |", "| --- | --- |"]
            lines.extend(f"| {dsid} | {name} |" for dsid, name in matches)
            return "\n".join(lines)
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"
