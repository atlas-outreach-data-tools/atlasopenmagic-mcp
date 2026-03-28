# atlasopenmagic-mcp

MCP Server for [ATLAS Open Data](https://opendata.atlas.cern/) metadata and file retrieval.

This server wraps the [`atlasopenmagic`](https://github.com/atlas-outreach-data-tools/atlasopenmagic) Python library as an [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server, allowing LLMs to discover, query, and retrieve ATLAS Open Data datasets.

## Architecture

```
LLM <--MCP/stdio--> atlasopenmagic-mcp serve <--HTTPS--> ATLAS Open Data API
                                                          (atlasopenmagic-api.app.cern.ch)
```

No authentication is required — all ATLAS Open Data is publicly accessible.

## Installation

```bash
pip install atlasopenmagic-mcp
```

Or with pixi:

```bash
pixi install
```

## Usage

### As an MCP server

```bash
atlasopenmagic-mcp serve
```

### Claude Desktop configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "atlas-open-data": {
      "command": "atlasopenmagic-mcp",
      "args": ["serve"]
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `atlas_available_releases` | List all available data releases |
| `atlas_set_release` | Set the active release for subsequent queries |
| `atlas_get_current_release` | Get the currently active release |
| `atlas_available_datasets` | List dataset numbers (DSIDs) in the current release |
| `atlas_available_skims` | List available event skims |
| `atlas_available_keywords` | List physics keywords used in the release |
| `atlas_get_metadata_fields` | List available metadata fields |
| `atlas_get_metadata` | Get metadata for a dataset (no file lists) |
| `atlas_get_all_info` | Get complete dataset info including file URLs |
| `atlas_match_metadata` | Search datasets by metadata field values |
| `atlas_get_urls` | Get file URLs with skim and protocol options |
| `atlas_get_weights` | Get MC weight metadata for a dataset |
| `atlas_get_all_weights_for_release` | Get weights for all datasets in a release |

## Available Resources

| URI | Description |
|-----|-------------|
| `atlas-open-data://guide` | Quick reference for ATLAS Open Data concepts |
| `atlas-open-data://metadata-fields` | Complete metadata fields reference |

## Development

```bash
# Run tests
pixi run test

# Run linting
pixi run lint

# Run all checks
pixi run check-all
```

## Keeping in sync with atlasopenmagic

This server depends on `atlasopenmagic` as a pip dependency. When the upstream library is updated:

1. **Non-breaking changes** (new fields, new releases): work automatically — the MCP tools call through to `atlasopenmagic` functions, so new data surfaces without any changes here.
2. **New functions**: add a new tool module or extend an existing one, register it in `server.py`.
3. **Breaking changes** (renamed/removed functions, changed signatures): update the affected tool modules to match the new API, then bump the version pin in `pyproject.toml`.

To bump the dependency:
```bash
# In pyproject.toml, update:
#   "atlasopenmagic>=1.9"  →  "atlasopenmagic>=1.10"
```

## License

Apache-2.0
