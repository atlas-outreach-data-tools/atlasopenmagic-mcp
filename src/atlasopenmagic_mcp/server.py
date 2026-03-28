"""FastMCP server setup for atlasopenmagic-mcp."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from mcp.server.fastmcp import FastMCP

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from atlasopenmagic_mcp.nomenclature import ATLAS_OPEN_DATA_GUIDE
from atlasopenmagic_mcp.resources import register as register_resources
from atlasopenmagic_mcp.tools import discovery, metadata, urls, weights

_INSTRUCTIONS = (
    "MCP server for the ATLAS Open Data portal. "
    "Provides tools to discover available data releases, datasets, and skims; "
    "retrieve dataset metadata (cross-sections, filter efficiencies, k-factors, "
    "generator info); obtain file URLs for streaming or download; search datasets "
    "by metadata fields and keywords; and query Monte Carlo weight metadata. "
    "No authentication is required — all data is publicly accessible.\n\n"
    + ATLAS_OPEN_DATA_GUIDE
)


def _make_mcp() -> FastMCP:
    """Build and return a configured FastMCP instance."""

    @asynccontextmanager
    async def _lifespan(_server: FastMCP) -> AsyncGenerator[dict[str, Any], None]:
        """Initialize atlasopenmagic for the lifetime of the MCP server.

        Imports atlasopenmagic and sets verbosity to error to suppress
        console output that would interfere with MCP stdio transport.
        """
        import atlasopenmagic as atom  # noqa: PLC0415

        atom.set_verbosity("error")
        yield {"atom": atom}

    mcp = FastMCP("atlasopenmagic-mcp", lifespan=_lifespan, instructions=_INSTRUCTIONS)

    for _module in [discovery, metadata, urls, weights]:
        _module.register(mcp)

    register_resources(mcp)

    return mcp


def serve() -> None:
    """Start the MCP server over stdio."""
    _make_mcp().run(transport="stdio")
