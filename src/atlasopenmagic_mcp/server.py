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


def _make_mcp(host: str = "127.0.0.1", port: int = 8000) -> FastMCP:
    """Build and return a configured FastMCP instance.

    Args:
        host: Bind address (passed to FastMCP constructor for HTTP transport).
        port: Port (passed to FastMCP constructor for HTTP transport).
    """

    @asynccontextmanager
    async def _lifespan(_server: FastMCP) -> AsyncGenerator[dict[str, Any], None]:
        """Initialize atlasopenmagic for the lifetime of the MCP server.

        Imports atlasopenmagic and sets verbosity to error to suppress
        console output that would interfere with MCP transport.
        """
        import atlasopenmagic as atom  # noqa: PLC0415

        atom.set_verbosity("error")
        yield {"atom": atom}

    mcp = FastMCP(
        "atlasopenmagic-mcp",
        lifespan=_lifespan,
        instructions=_INSTRUCTIONS,
        host=host,
        port=port,
    )

    for _module in [discovery, metadata, urls, weights]:
        _module.register(mcp)

    register_resources(mcp)

    return mcp


def serve(transport: str = "stdio", host: str = "0.0.0.0", port: int = 8000) -> None:
    """Start the MCP server.

    Args:
        transport: Transport protocol — "stdio" for CLI usage,
            "streamable-http" for HTTP (OpenWebUI, remote clients).
        host: Bind address for HTTP transport (default "0.0.0.0").
        port: Port for HTTP transport (default 8000).
    """
    mcp = _make_mcp(host=host, port=port)
    mcp.run(transport=transport)
