"""Monte Carlo weight metadata tools."""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import Context, FastMCP  # noqa: TC002

from atlasopenmagic_mcp.tools._helpers import run_sync


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
            return f"Error: {exc}"

    @mcp.tool()
    async def atlas_get_all_weights_for_release(
        release_name: str | None = None,
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """Get weight metadata for all datasets in a release.

        Returns weight names for every dataset in the specified (or current)
        release. This can be a large response. The release must be set as
        active first with atlas_set_release.

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
            return f"Error: {exc}"
