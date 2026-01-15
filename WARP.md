# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Current Status (Actual)
- **Implementation has not started**. This repo currently contains specifications only.
- The authoritative source of truth is `Project/Spec/`.
- `AGENTS.md` is a symlink to this file.

## Where to Look
- `Project/Spec/` — canonical functional + technical specifications
- `Project/Notes/` — dated human notes
- `Project/Reports/` — critical agent reports on project state
- `Project/Sessions/` — prior LLM sessions (only use if explicitly required)

## Before Starting Development
Read the specification documents in order:
1. `Project/Spec/GENERAL_PRINCIPLES.md`
2. `Project/Spec/functional/SPEC_OVERVIEW.md`
3. Relevant functional specs in `Project/Spec/functional/`
   - Includes `SPEC_COMMAND_SYSTEM.md` and `SPEC_HELP_SYSTEM.md`
4. Technical specs in `Project/Spec/technical/`
   - Start with `TECH_ARCHITECTURE.md`
   - Key: `TECH_COMMAND_FRAMEWORK.md`, `TECH_HELP_SYSTEM.md`

## Planned Architecture (From Specs)

### Layered Architecture
```
Presentation → Commands → Services → Providers → Storage → Core
```
- Each layer may only import from layers below it
- No circular dependencies
- Cross-cutting concerns (logging, errors) live in Core

### Command System
- Slash commands for explicit actions
- Decorator-based registration
- No natural language command interface

### Configuration
- YAML overlay system
- No hard-coded defaults in code
- Pydantic validation

### Storage
- ChromaDB for vector store
- SQLite for productivity data
- Never load entire vector store into memory

### LLM Providers
- Must support OpenAI, Anthropic, Google, Ollama
- Use pydantic-ai for agent/API interactions

## Planned Directory Structure (Not Yet Implemented)
```
cato/
├── cato/
│   ├── app.py
│   ├── commands/
│   ├── core/
│   ├── providers/
│   ├── services/
│   ├── storage/
│   ├── display/
│   └── resources/
└── tests/
```

## Code Organisation Requirements
- Each module directory must have a README
- Numpy-format docstrings, type hints on all functions
- Relative imports within package
- Single responsibility per file

## Development Workflow
- `main` is the stable branch; all work on feature branches
- Branch naming: `feature/<description>` or `fix/<description>`
- CI should be fast (< 5 minutes)
- Use uv project workflow: `uv sync`, `uv add`, `uv run`, `uv lock`

## Required Actions for Any Change
For every change you make, complete the applicable steps below:

1. **Identify scope**
   - Locate the relevant functional and technical specs in `Project/Spec/`.
   - If no spec exists, add or update the appropriate spec first.

2. **Update documentation**
   - If you add or modify a command, update help docs per `SPEC_HELP_SYSTEM.md` and `TECH_HELP_SYSTEM.md`.
   - Ensure any user-facing behavior change is reflected in the functional spec.

3. **Code quality**
   - Add type hints and NumPy-format docstrings for all new/changed Python functions.
   - Add inline comments where logic is non-obvious or implicit.

4. **Configuration exposure**
   - If a default affects user-visible behavior, expose it via config or top-level API.

5. **Validation**
   - Run the most relevant tests (unit/integration) for the change.
   - Run lint/typecheck if the repo provides commands for them.

6. **Summary**
   - Provide a concise summary of what changed and which specs/docs were updated.
