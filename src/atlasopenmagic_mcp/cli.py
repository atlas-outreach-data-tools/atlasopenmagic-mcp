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

    serve_parser = subparsers.add_parser(
        "serve",
        help="Start the MCP server",
    )
    serve_parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol (default: stdio). Use 'streamable-http' for OpenWebUI / remote clients.",
    )
    serve_parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Bind address for HTTP transport (default: 0.0.0.0)",
    )
    serve_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP transport (default: 8000)",
    )

    args = parser.parse_args()

    if args.command == "serve":
        serve(transport=args.transport, host=args.host, port=args.port)
    else:
        parser.print_help()
