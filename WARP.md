# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management, conversational memory via vector storage, TTS, and web search.

**Status**: Pre-implementation - specification documents exist in `Project/Spec/`

## Before Starting Development

Read the specification documents in order:
1. `Project/Spec/GENERAL_PRINCIPLES.md` - Core philosophy and constraints
2. `Project/Spec/functional/SPEC_OVERVIEW.md` - Application flow and UI
3. Relevant functional specs in `Project/Spec/functional/`
4. Technical specs in `Project/Spec/technical/`

## Key Architectural Decisions

### Configuration
- YAML-driven configuration with overlay system (user config overlays defaults)
- **No hard-coded defaults in code** - all defaults in default YAML file
- Pydantic for all validation
- Unrecognised config keys warn but don't crash

### Multi-Provider LLM
- Must support OpenAI, Anthropic, Google, Ollama
- Use pydantic-ai over LangChain for agent/API interactions

### Storage
- ChromaDB for vector store (embeddings, similarity search)
- SQLite for productivity data (tasks, lists, memories)
- **Never load entire vector store into memory**

### Command System
- Slash commands (`/help`, `/speak`, `/web`, etc.) for explicit actions
- Decorator-based registration - adding a command requires only one file
- **No natural language command interface** - commands use explicit syntax

### Error Handling
- Atomic exception handling (specific exceptions, not broad catches)
- Custom exception hierarchy (CatoError base class)
- Graceful degradation for non-critical failures
- Never silent failures

## Code Organisation Requirements

When implementation begins:
- Create `agent.txt` at root for AI navigation
- Each module directory must have a README explaining purpose and extension
- Numpy-format docstrings, type hints on all functions
- Relative imports within package

## Technology Stack

### Required
- Rich (formatting), prompt_toolkit (input)
- ChromaDB, OpenAI Embeddings API
- PyYAML, Pydantic
- pydantic-ai (productivity agent)

### Optional
- OpenAI TTS API
- DuckDuckGo/Google/Bing search
