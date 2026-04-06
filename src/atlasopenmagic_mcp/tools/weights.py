"""Monte Carlo weight metadata tools."""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import Context, FastMCP  # noqa: TC002

from atlasopenmagic_mcp.tools._helpers import format_error, run_sync


def register(mcp: FastMCP) -> None:
    """Register weight metadata tools."""

    @mcp.tool()
    async def atlas_get_weights(
        dataset: str,
        e_tag: str | None = None,
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """Get weight metadata for a Monte Carlo dataset.

        Returns the list of available weight names (systematic variations,
        PDF sets) along with release and energy information.

        Requires an active release — call atlas_set_release first.

        Args:
            dataset: Dataset number (e.g. "306600").
            e_tag: Optional specific event-generation tag (e.g. "e8514").
                If omitted, resolved automatically from dataset metadata.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            result = await run_sync(atom.get_weights, dataset, e_tag)
            return json.dumps(result, default=str)
        except Exception as exc:  # noqa: BLE001
            return format_error(exc, recovery=[
                "Ensure a release is set with atlas_set_release.",
                "Use atlas_available_datasets to check valid DSIDs.",
                "Weight metadata is only available for event-generation releases "
                "(e.g. 2025r-evgen-13tev, 2025r-evgen-13p6tev).",
            ])

    @mcp.tool()
    async def atlas_get_all_weights_for_release(
        release_name: str | None = None,
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """Get a summary of weight metadata for all datasets in a release.

        Returns dataset count and per-dataset weight counts for the
        specified (or current) release. Use atlas_get_weights(dataset)
        to get full weight names for a specific dataset.

        Requires an active release — call atlas_set_release first.

        Args:
            release_name: Release to query. If omitted, uses the currently
                active release.
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            result = await run_sync(atom.get_all_weights_for_release, release_name)
            # Summarize to avoid enormous responses
            datasets = result.get("datasets", {})
            summary = {
                "release_name": result.get("release_name"),
                "energy_level": result.get("energy_level"),
                "total_datasets_with_weights": len(datasets),
                "datasets": {
                    dsid: len(wts) for dsid, wts in datasets.items()
                },
            }
            return json.dumps(summary, default=str)
        except Exception as exc:  # noqa: BLE001
            return format_error(exc, recovery=[
                "Ensure a release is set with atlas_set_release.",
                "Weight metadata is only available for event-generation releases "
                "(e.g. 2025r-evgen-13tev, 2025r-evgen-13p6tev).",
            ])
