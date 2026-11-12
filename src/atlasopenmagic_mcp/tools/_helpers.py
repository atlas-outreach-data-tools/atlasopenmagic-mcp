"""Shared helpers for atlasopenmagic-mcp tool implementations."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp.types import ToolAnnotations

# Every tool except atlas_set_release only reads public data.
READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True)
# atlas_set_release changes the session's active release but writes nothing remote.
SET_STATE = ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True, openWorldHint=False)

# Upper bound for one tool response, as in fts-mcp (2 MiB).
MAX_RESPONSE_CHARS = 2 * 1024 * 1024


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


def cap_response(text: str, limit: int = MAX_RESPONSE_CHARS) -> str:
    """Truncate an oversized tool response and tell the agent how to narrow it."""
    if len(text) <= limit:
        return text
    return (
        text[:limit]
        + f"\n\n[Truncated: response exceeded {limit} characters. "
        "Narrow the request (specific dataset, skim, or field) and retry.]"
    )


def dumps_capped(obj: Any, **kwargs: Any) -> str:
    """Serialize to JSON and cap the size."""
    return cap_response(json.dumps(obj, **kwargs))
