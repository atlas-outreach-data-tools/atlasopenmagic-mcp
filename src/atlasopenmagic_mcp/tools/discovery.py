"""Discovery tools: releases, datasets, skims, keywords, metadata fields."""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import Context, FastMCP  # noqa: TC002

from atlasopenmagic_mcp.tools._helpers import run_sync


def register(mcp: FastMCP) -> None:
    """Register discovery tools."""

    @mcp.tool()
    async def atlas_available_releases(
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """List all available ATLAS Open Data releases with descriptions.

        Returns a table of release names and their descriptions, covering
        both education and research releases at various energies.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        releases = atom.metadata.RELEASES_DESC
        lines = ["| Release | Description |", "| --- | --- |"]
        lines.extend(f"| {name} | {desc} |" for name, desc in releases.items())
        return "\n".join(lines)

    @mcp.tool()
    async def atlas_set_release(
        release: str,
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """Set the active ATLAS Open Data release for all subsequent queries.

        This must be called before querying datasets, metadata, or URLs.
        Changing the release clears any cached metadata.

        Args:
            release: Release name, e.g. "2024r-pp", "2020e-13tev",
                "2025e-13tev-beta". Use atlas_available_releases to see all options.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            await run_sync(atom.set_release, release)
            return f"Active release set to '{release}'."
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"

    @mcp.tool()
    async def atlas_get_current_release(
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """Return the name of the currently active ATLAS Open Data release."""
        atom = ctx.request_context.lifespan_context["atom"]
        return atom.get_current_release()

    @mcp.tool()
    async def atlas_available_datasets(
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """List all dataset numbers (DSIDs) in the current release.

        Returns a sorted list of numeric dataset identifiers. A release must
        be set first with atlas_set_release.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            datasets = await run_sync(atom.available_datasets)
            return json.dumps(datasets)
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"

    @mcp.tool()
    async def atlas_available_skims(
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """List available skims (pre-filtered event subsets) for the current release.

        Skims like 'exactly4lep' or '3lep' save processing time when your
        analysis selection is more restrictive than the skim selection.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            skims = await run_sync(atom.available_skims)
            return json.dumps(skims)
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"

    @mcp.tool()
    async def atlas_available_keywords(
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """List unique physics keywords used across datasets in the current release.

        Keywords like 'top', 'higgs', 'dilepton' can be used with
        atlas_match_metadata to find relevant datasets.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            keywords = await run_sync(atom.available_keywords)
            return json.dumps(keywords)
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"

    @mcp.tool()
    async def atlas_get_metadata_fields(
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """List available metadata fields for datasets in the current release.

        Returns the field names that can be used with atlas_get_metadata
        and atlas_match_metadata.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            fields = await run_sync(atom.get_metadata_fields)
            return json.dumps(fields)
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"
