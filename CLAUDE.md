# atlasopenmagic-mcp — Contributor Guide

## Architecture

```
LLM <--MCP/stdio--> atlasopenmagic-mcp serve <--HTTPS--> ATLAS Open Data API
                          |                                (atlasopenmagic-api.app.cern.ch)
                          |
                          +-- atlasopenmagic (Python library, pip dependency)
```

The MCP server is a thin async wrapper around `atlasopenmagic`. Tools call
library functions via `_run_sync()` (which uses `asyncio.to_thread()`) to
keep the MCP event loop responsive.

## Project Layout

```
src/atlasopenmagic_mcp/
├── __init__.py           # Package version
├── cli.py                # argparse CLI: `atlasopenmagic-mcp serve`
├── server.py             # FastMCP setup, lifespan, _run_sync helper
├── nomenclature.py       # Reference docs (embedded in instructions + resources)
├── resources.py          # MCP resource registration
└── tools/
    ├── __init__.py
    ├── _helpers.py       # run_sync (asyncio.to_thread wrapper)
    ├── discovery.py      # Releases, datasets, skims, keywords, fields
    ├── metadata.py       # get_metadata, get_all_info, match_metadata
    ├── urls.py           # get_urls (file URL retrieval)
    └── weights.py        # MC weight metadata
```

## Key Conventions

### Tool Registration Pattern

Every tool module exports `register(mcp: FastMCP) -> None`. Inside it,
define tools with `@mcp.tool()`:

```python
def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def my_tool(arg: str, *, ctx: Context[Any, Any]) -> str:
        atom = ctx.request_context.lifespan_context["atom"]
        result = await run_sync(atom.some_function, arg)
        return json.dumps(result, default=str)
```

### Error Handling

Tools return error strings, never raise:
```python
try:
    ...
except Exception as exc:  # noqa: BLE001
    return f"Error: {exc}"
```

### Async / Threading

`atlasopenmagic` uses blocking `requests` calls. Always wrap with:
```python
from atlasopenmagic_mcp.tools._helpers import run_sync
result = await run_sync(atom.some_function, arg1, arg2)
```

### Lifespan Context

The `atlasopenmagic` module is imported and configured in the server lifespan.
Tools access it via `ctx.request_context.lifespan_context["atom"]`.

Verbosity is set to "error" at startup to suppress console output that
would interfere with MCP's stdio transport.

## Adding a New Tool

1. Create `src/atlasopenmagic_mcp/tools/my_module.py` with a `register(mcp)` function.
2. Import and register in `server.py`:
   ```python
   from atlasopenmagic_mcp.tools import my_module
   # in _make_mcp():
   for _module in [discovery, metadata, urls, weights, my_module]:
   ```
3. Add tests in `tests/test_tools_my_module.py`.
4. Run `pixi run check`.

## Build & Test

```bash
pixi run test          # Quick tests (mocked)
pixi run test-cov      # With coverage
pixi run lint          # Pre-commit + pylint
pixi run check         # Lint + test
pixi run check-all     # Lint + all tests with coverage
```

## Relationship to atlasopenmagic

This server depends on `atlasopenmagic>=1.9` as a pip dependency.
The library handles all HTTP communication, caching, and data parsing.
The MCP layer only:
- Wraps sync calls with `asyncio.to_thread`
- Serializes results to JSON/markdown strings
- Provides MCP-specific docstrings (tool descriptions)
- Exposes reference documentation as MCP resources

When `atlasopenmagic` adds new public functions, add corresponding tool
wrappers here. Non-breaking additions (new releases, fields, etc.)
propagate automatically.
