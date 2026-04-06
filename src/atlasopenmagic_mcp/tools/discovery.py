"""Discovery tools: releases, datasets, skims, keywords, metadata fields."""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import Context, FastMCP  # noqa: TC002

from atlasopenmagic_mcp.tools._helpers import format_error, run_sync


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

        This is typically the first tool to call. After reviewing releases,
        use atlas_set_release to activate one before querying datasets.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        releases = atom.metadata.RELEASES_DESC
        lines = ["| Release | Description |", "| --- | --- |"]
        lines.extend(f"| {name} | {desc} |" for name, desc in releases.items())
        lines.append(
            "\nNext: call atlas_set_release(release_name) to activate a release."
        )
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
            return (
                f"Active release set to '{release}'. "
                "Next: use atlas_available_datasets to list DSIDs, "
                "or atlas_match_metadata to search by keyword or field."
            )
        except Exception as exc:  # noqa: BLE001
            return format_error(exc, recovery=[
                "Use atlas_available_releases to see valid release names.",
            ])

    @mcp.tool()
    async def atlas_get_current_release(
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """Return the name of the currently active ATLAS Open Data release.

        If no release has been set, call atlas_set_release first.
        Use atlas_available_releases to see all options.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        return atom.get_current_release()

    @mcp.tool()
    async def atlas_available_datasets(
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """List all dataset numbers (DSIDs) in the current release.

        Returns a JSON object with count and sorted list of numeric dataset
        identifiers. Requires an active release — call atlas_set_release first.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            datasets = await run_sync(atom.available_datasets)
            return json.dumps({"count": len(datasets), "datasets": datasets})
        except Exception as exc:  # noqa: BLE001
            return format_error(exc, recovery=[
                "Ensure a release is set with atlas_set_release.",
                "Use atlas_available_releases to see valid release names.",
            ])

    @mcp.tool()
    async def atlas_available_skims(
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """List available skims (pre-filtered event subsets) for the current release.

        Skims like 'exactly4lep' or '3lep' save processing time when your
        analysis selection is more restrictive than the skim selection.

        Requires an active release — call atlas_set_release first.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            skims = await run_sync(atom.available_skims)
            return json.dumps(skims)
        except Exception as exc:  # noqa: BLE001
            return format_error(exc, recovery=[
                "Ensure a release is set with atlas_set_release.",
                "Use atlas_available_releases to see valid release names.",
            ])

    @mcp.tool()
    async def atlas_available_keywords(
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """List unique physics keywords used across datasets in the current release.

        Keywords like 'top', 'higgs', 'dilepton' can be used with
        atlas_match_metadata to find relevant datasets.

        Requires an active release — call atlas_set_release first.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            keywords = await run_sync(atom.available_keywords)
            return json.dumps(keywords)
        except Exception as exc:  # noqa: BLE001
            return format_error(exc, recovery=[
                "Ensure a release is set with atlas_set_release.",
                "Use atlas_available_releases to see valid release names.",
            ])

    @mcp.tool()
    async def atlas_get_metadata_fields(
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """List available metadata fields for datasets in the current release.

        Returns field names that can be used with atlas_get_metadata
        and atlas_match_metadata, e.g. "cross_section_pb", "keywords",
        "generator".

        Requires an active release — call atlas_set_release first.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            fields = await run_sync(atom.get_metadata_fields)
            return json.dumps(fields)
        except Exception as exc:  # noqa: BLE001
            return format_error(exc, recovery=[
                "Ensure a release is set with atlas_set_release.",
                "Use atlas_available_releases to see valid release names.",
            ])
