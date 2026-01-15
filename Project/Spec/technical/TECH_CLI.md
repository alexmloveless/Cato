# CLI Technical Specification

## Overview
This document defines the CLI implementation details, including argument parsing, configuration overrides, mode routing, and headless execution.

## Responsibilities
The CLI is part of the **Presentation** layer. It must:
- Parse arguments and validate combinations
- Load configuration and apply CLI overrides
- Route to interactive or headless execution
- Emit results to stdout and errors to stderr
- Avoid instantiating providers directly (use bootstrap/services)

## Entry Points
- `cato/main.py`: console script entry (`cato.main:main`)
- `cato/__main__.py`: module entry (`python -m cato`)

`__main__.py` must delegate to `cato.main:main` to ensure identical behavior.

## Parsing
- Use **click** for option parsing and help output.
- Define a single top-level command with flat options (no subcommands).
- Enforce mutual exclusivity for headless action flags in validation.
- `--help` / `--version` must exit before config load.

## Configuration Loading & Overrides

### Load Order
1. Determine config path from `--config` or `CATO_CONFIG_FILE`.
2. Load config using the standard loader (TECH_CONFIG_SYSTEM.md).
3. Apply CLI overrides (highest precedence).

### Override Mapping
| CLI Flag | Config Path |
|----------|-------------|
| `--log-level` | `logging.level` |
| `--debug` | `debug=true`, `logging.level=DEBUG` |
| `--provider` | `llm.provider` |
| `--model` | `llm.model` |
| `--temperature` | `llm.temperature` |
| `--max-tokens` | `llm.max_tokens` |
| `--timeout-seconds` | `llm.timeout_seconds` |
| `--no-markdown` | `display.markdown_enabled=false` |
| `--no-rich` | `display.no_rich=true` |
| `--no-color` | `display.no_color=true` |

Overrides must be applied **only** when the corresponding flag is provided; no implicit defaults beyond config.

## Mode Selection

### Headless Detection
Headless mode is active when:
- Any headless action flag is provided, or
- `--headless` is provided alongside a headless action.

If `--headless` is provided without an action, the CLI must fail with a usage error.

### Interactive Mode
If no headless action is provided, the CLI starts the interactive REPL via the application entry point.

## Headless Execution

### Implementation Requirements
- Do not initialize prompt_toolkit or interactive display components.
- Use the same service layer as interactive mode.
- Use a minimal display implementation (plain text, no spinners).
- Respect config-driven vector store enablement and chunking settings.

### Execution Flow (Headless)
1. Validate headless action and inputs.
2. Instantiate required services via bootstrap.
3. Execute the action.
4. Serialize result in `text` or `json` format.
5. Exit with the appropriate code.

### Output Formatting
- **Text**: print only the primary result (no decorative output).
- **JSON**: output a single JSON object as defined in SPEC_COMMAND_LINE.md.
- All non-result diagnostics must go to stderr.

## Error Handling
- CLI parsing errors → exit code `2`.
- Configuration validation errors → exit code `3`.
- Runtime errors → exit code `1`.
- All errors should be reported with a concise, user-readable message to stderr.

## Logging
- Logging uses the configured logger.
- In headless mode, logs must not pollute stdout.
- `--quiet` suppresses informational status output (stdout only); warnings/errors still surface on stderr.
