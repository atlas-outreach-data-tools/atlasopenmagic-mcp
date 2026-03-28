"""Command-line interface for atlasopenmagic-mcp."""

from __future__ import annotations

import argparse

from atlasopenmagic_mcp.server import serve


def main() -> None:
    """Entry point for the atlasopenmagic-mcp command."""
    parser = argparse.ArgumentParser(
        prog="atlasopenmagic-mcp",
        description="MCP Server for ATLAS Open Data metadata and file retrieval",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    subparsers.add_parser(
        "serve",
        help="Start the MCP server (stdio transport)",
    )

    args = parser.parse_args()

    if args.command == "serve":
        serve()
    else:
        parser.print_help()
