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


def format_error(exc: Exception, *, recovery: list[str] | None = None) -> str:
    """Format an error with recovery guidance for the LLM.

    Follows the RECOVERY_GUIDE pattern: errors should teach, not just
    fail. Each message includes what went wrong and actionable steps the
    agent can take to recover.

    Args:
        exc: The caught exception.
        recovery: Suggested next actions the agent can take.

    Returns:
        A structured error string with actionable guidance.
    """
    parts = [f"Error: {exc}"]
    if recovery:
        parts.append("Recovery steps:")
        parts.extend(f"- {step}" for step in recovery)
    return "\n".join(parts)
