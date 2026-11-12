# Changelog

All notable changes follow [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- `readOnlyHint` annotations on all tools (`atlas_set_release` is marked as state-changing).
- 2 MiB cap on every tool response.
- CI (ruff, tests on Python 3.10–3.13, `pip-audit`), Dependabot, release workflow with CycloneDX SBOM and PyPI trusted publishing.
- `SECURITY.md`, `CODEOWNERS`, tool card.

### Changed
- Dependencies now have an upper bound: `atlasopenmagic<2`, `mcp<2`.

## [0.1.0]

- First release: 13 tools and 2 resources over the ATLAS Open Data API.
