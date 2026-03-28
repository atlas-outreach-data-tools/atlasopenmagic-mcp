"""File URL retrieval tools."""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import Context, FastMCP  # noqa: TC002

from atlasopenmagic_mcp.tools._helpers import run_sync


def register(mcp: FastMCP) -> None:
    """Register URL retrieval tools."""

    @mcp.tool()
    async def atlas_get_urls(
        dataset: str,
        skim: str = "noskim",
        protocol: str = "https",
        *,
        ctx: Context[Any, Any],
    ) -> str:
        """Get file URLs for a dataset, with optional skim and protocol selection.

        Returns a list of ROOT file URLs that can be used for streaming or
        downloading ATLAS Open Data files.

        Args:
            dataset: Dataset number (e.g. "301204") or physics_short name.
            skim: Skim type to retrieve. Use "noskim" (default) for the full
                dataset, or a specific skim like "exactly4lep", "3lep".
                Use atlas_available_skims to see available options.
            protocol: URL protocol — "https" (default, web download),
                "root" (XRootD streaming), or "eos" (EOS POSIX path).
        """
        atom = ctx.request_context.lifespan_context["atom"]
        try:
            urls = await run_sync(atom.get_urls, dataset, skim, protocol)
            return json.dumps(urls)
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"
