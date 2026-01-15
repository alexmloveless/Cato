# Command-Line Interface (CLI) Specification

## Overview
Cato is launched from the command line. The CLI controls configuration selection, run mode, and a small set of one-shot (headless) operations.

## Goals
- Provide a consistent entry point (`cato` or `python -m cato`)
- Allow temporary, session-scoped overrides without editing config files
- Support headless usage for automation and scripting
- Keep the option surface small and stable (MVP)

## Entry Points
- `cato` (console script)
- `python -m cato` (equivalent to `cato`)

## Modes

### Interactive (default)
- Starts the REPL loop.
- Uses Rich + prompt_toolkit for display and input.
- Shows the welcome panel and prompt per SPEC_OVERVIEW.md.
- Requires a TTY for input.

### Headless (non-interactive)
- Triggered by any headless action flag or by `--headless`.
- Does not start the REPL.
- Accepts input via CLI arguments or stdin.
- Outputs results to stdout; errors and logs to stderr.
- Limited scope: one-shot LLM query and vector store operations only.

## CLI Syntax
- GNU-style options with short and long forms.
- `--` ends option parsing; remaining tokens are treated as literal arguments.
- Shell quoting rules apply; the CLI does not perform additional escaping.

## Option Reference

### Common options (all modes)
| Option | Argument | Default | Behavior |
|--------|----------|---------|----------|
| `-h, --help` | - | - | Show help and exit. |
| `-V, --version` | - | - | Show version and exit. |
| `--config` | PATH | none | Path to configuration file (highest precedence). |
| `--log-level` | LEVEL | none | Override `logging.level` (DEBUG, INFO, WARNING, ERROR). |
| `--debug` | - | false | Set `debug=true` and `logging.level=DEBUG` unless `--log-level` is provided. |
| `--dummy-mode` | - | false | Use mock LLM responses; no external API calls. |

### LLM override options
| Option | Argument | Default | Behavior |
|--------|----------|---------|----------|
| `--provider` | PROVIDER | none | Override `llm.provider`. |
| `--model` | MODEL | none | Override `llm.model`. |
| `--temperature` | FLOAT | none | Override `llm.temperature`. |
| `--max-tokens` | INT | none | Override `llm.max_tokens`. |
| `--timeout-seconds` | INT | none | Override `llm.timeout_seconds`. |

### Display override options
| Option | Argument | Default | Behavior |
|--------|----------|---------|----------|
| `--no-markdown` | - | false | Set `display.markdown_enabled=false`. |
| `--no-rich` | - | false | Disable Rich rendering (plain text only). |
| `--no-color` | - | false | Disable ANSI color output. |

### Headless actions (mutually exclusive)
Only one headless action may be specified at a time.

| Option | Argument | Default | Behavior |
|--------|----------|---------|----------|
| `--headless` | - | false | Force headless mode. Requires a headless action. |
| `--ask` | TEXT | none | Send a single prompt to the LLM and exit. |
| `--stdin` | - | false | Read prompt text from stdin (used with `--ask`). |
| `--add-to-vector-store` | PATH | none | Add a document to the vector store and exit. |
| `--query-vector-store` | QUERY | none | Query vector store and exit. |
| `--vector-store-stats` | - | false | Show vector store stats and exit. |

### Headless output controls
| Option | Argument | Default | Behavior |
|--------|----------|---------|----------|
| `--output` | FORMAT | text | Output format for headless mode: `text` or `json`. |
| `--quiet` | - | false | Suppress non-essential status messages (stdout only). |

## Behavior Details

### Precedence
Configuration precedence is (highest to lowest): CLI arguments → environment variables → user config → defaults.

### Debug vs Log Level
- `--debug` sets `debug=true` and `logging.level=DEBUG`.
- If `--log-level` is supplied, it overrides the level implied by `--debug`.

### Dummy Mode
- Replaces the LLM provider with a deterministic mock provider.
- No external API calls are made.
- Compatible with interactive and headless modes.

### Headless Action Semantics

#### `--ask`
- Runs a single LLM completion and exits.
- Uses system prompts and config-driven settings.
- Uses vector store context retrieval if enabled.
- If `--stdin` is set, the prompt is read from stdin; otherwise uses the `--ask` value.
- Empty prompt is an error.

#### `--add-to-vector-store`
- Loads the file at PATH and ingests it into the vector store.
- Uses the configured chunking strategy and embedding provider.
- Errors if vector store is disabled or file cannot be read.

#### `--query-vector-store`
- Executes a similarity search using the provided QUERY.
- Number of results is controlled by `vector_store.context_results`.
- Errors if vector store is disabled.

#### `--vector-store-stats`
- Prints summary statistics for the configured vector store.

### Output (Headless)
- **stdout**: results only.
- **stderr**: errors and logs.
- `--output text` prints the primary result without banners, spinners, or decorative formatting.
- `--output json` prints a single JSON object.

#### JSON Output Schema (Headless)
```json
{
  "ok": true,
  "mode": "headless",
  "action": "ask | add_to_vector_store | query_vector_store | vector_store_stats",
  "result": {},
  "error": null,
  "meta": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "duration_ms": 1234,
    "config_path": "/path/to/config.yaml"
  }
}
```

Action-specific `result` payloads:
- **ask**: `{ "text": "...", "usage": { "input_tokens": 0, "output_tokens": 0 } }`
- **add_to_vector_store**: `{ "source_path": "...", "added_chunks": 0 }`
- **query_vector_store**: `{ "results": [ { "id": "...", "score": 0.0, "excerpt": "...", "metadata": {} } ] }`
- **vector_store_stats**: `{ "collection": "...", "document_count": 0, "path": "..." }`

### Exit Codes
- `0`: Success
- `1`: Runtime failure (provider errors, file I/O, vector store errors)
- `2`: CLI usage error (invalid options, conflicting actions)
- `3`: Configuration error (invalid or missing config)
