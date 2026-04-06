# PATs Review: atlasopenmagic-mcp

Applied [Patterns for Agentic Tools (PATs)](https://arcade.dev/patterns/llm.txt) to
improve how LLMs discover, invoke, and recover from errors when using this MCP server.

## Changes by pattern

### RECOVERY_GUIDE (PAT 41) — actionable error messages

**Before:** every tool returned bare `f"Error: {exc}"` strings.
An LLM receiving these has no way to self-correct.

**After:** a shared `format_error()` helper structures errors with
tool-specific recovery steps:

```
Error: no release is currently set
Recovery steps:
- Ensure a release is set with atlas_set_release.
- Use atlas_available_releases to see valid release names.
```

**Files:** `_helpers.py`, `discovery.py`, `metadata.py`, `urls.py`, `weights.py`

---

### DEPENDENCY_HINT (PAT 14) — prerequisite guidance in descriptions

**Before:** only `atlas_available_datasets` mentioned the release prerequisite.
Nine other tools silently required a release to be active.

**After:** all tools that need a release include:
> Requires an active release — call atlas_set_release first.

**Files:** `discovery.py`, `metadata.py`, `urls.py`, `weights.py`

---

### CONSTRAINED_INPUT (PAT 6) — enum types for fixed-choice parameters

**Before:** `protocol: str = "https"` — an LLM could send `"http"`, `"xrootd"`,
or any other invalid string.

**After:** `protocol: Literal["https", "root", "eos"] = "https"` — valid values
are now visible in the tool's JSON schema, preventing invalid calls.

**Files:** `urls.py`

---

### NEXT_ACTION_HINT (PAT 33) — workflow guidance in outputs

**Before:** tools returned raw data with no workflow context.

**After:** key tools append a suggested next step:

| Tool | Hint |
|---|---|
| `atlas_available_releases` | "Next: call atlas_set_release(release_name) to activate a release." |
| `atlas_set_release` | "Next: use atlas_available_datasets to list DSIDs, or atlas_match_metadata to search." |
| `atlas_match_metadata` | "Tip: use atlas_get_metadata(dataset_number) for full details on any match." |

**Files:** `discovery.py`, `metadata.py`

---

### TOOL_DESCRIPTION (PAT 5) — LLM-optimized descriptions

**Before:** descriptions were accurate but human-oriented, missing examples and
cross-references.

**After:**

- `atlas_available_releases`: marked as "typically the first tool to call"
- `atlas_get_metadata`: added "Prefer this over atlas_get_all_info unless you
  specifically need file URLs"
- `atlas_get_all_info`: added large-response warning and preference note
- `atlas_match_metadata`: added inline examples
  (`field="keywords", value="higgs"`)
- `atlas_get_all_weights_for_release`: fixed misleading description (said
  "can be a large response" but it already returns a summary)
- `atlas_get_metadata_fields`: added example field names in description

**Files:** `discovery.py`, `metadata.py`, `urls.py`, `weights.py`

---

### TOKEN_EFFICIENT_RESPONSE (PAT 30) — structured list responses

**Before:** `atlas_available_datasets` and `atlas_get_urls` returned bare JSON
arrays, giving the LLM no count without parsing the full list.

**After:** both wrap results with a count:

```json
{"count": 245, "datasets": ["301204", "301205", ...]}
{"count": 12, "urls": ["https://opendata.cern.ch/..."]}
```

**Files:** `discovery.py`, `urls.py`

---

## Test updates

Tests in `test_tools_discovery.py` and `test_tools_urls.py` were updated to
unwrap the new `{"count": N, ...}` response envelopes. All 22 tests pass.

---

## Commit message

```
refactor: apply PATs (Patterns for Agentic Tools) to MCP tools

- RECOVERY_GUIDE (PAT 41): replace bare "Error: ..." strings with
  structured error messages containing tool-specific recovery steps
- DEPENDENCY_HINT (PAT 14): add "requires active release" prerequisite
  to all tool descriptions that need it
- CONSTRAINED_INPUT (PAT 6): use Literal type for protocol parameter
  so valid values appear in the tool JSON schema
- NEXT_ACTION_HINT (PAT 33): append suggested next tools to key outputs
  (set_release, match_metadata, available_releases)
- TOOL_DESCRIPTION (PAT 5): add examples, cross-references, and
  when-to-use guidance to all tool docstrings
- TOKEN_EFFICIENT (PAT 30): wrap list responses with count envelope

Reference: https://arcade.dev/patterns/llm.txt
```
