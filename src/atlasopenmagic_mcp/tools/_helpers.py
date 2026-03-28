"""Shared helpers for atlasopenmagic-mcp tool implementations."""

from __future__ import annotations

import asyncio
from typing import Any


async def run_sync(func: Any, *args: Any, **kwargs: Any) -> Any:
    """Run a synchronous atlasopenmagic call in a thread.

    atlasopenmagic uses blocking HTTP requests internally. This wrapper
    offloads calls to asyncio's thread pool so the MCP event loop stays
    responsive.

    Args:
        func: A callable (e.g. atom.get_metadata).
        *args: Positional arguments forwarded to func.
        **kwargs: Keyword arguments forwarded to func.

    Returns:
        Whatever func returns.
    """
    return await asyncio.to_thread(func, *args, **kwargs)
