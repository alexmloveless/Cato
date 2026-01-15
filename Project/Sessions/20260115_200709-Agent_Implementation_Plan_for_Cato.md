USER:
create a detailed agent implementation plan for Cato

AGENT:


**Files Read:**

**/home/alex/Documents/repos/Cato/AGENTS.md**
```
# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management, conversational context via vector storage, TTS, and web search.

**Status**: Pre-implementation - specification documents exist in `Project/Spec/`

### Purpose
Cato exists to provide maximum control over LLM interactions, tailored to specific user needs and idiosyncrasies. It is a chat client first, productivity client second.

### Intent
Cato provides a unified terminal interface for:
- Conversational AI interactions with multiple LLM providers
- Personal productivity management (tasks, lists, time tracking)
- File operations and code management
- Persistent conversational context with retrieval
- Text-to-speech synthesis and web search integration

### Target User
- Single user on a single machine
- Users who are highly changeable, like to tinker and experiment
- Users who want flexible, modular architecture they can customise
- Multiple instances may run with different configurations simultaneously

## Before Starting Development

Read the specification documents in order:
1. `Project/Spec/GENERAL_PRINCIPLES.md` - Core philosophy and constraints
2. `Project/Spec/functional/SPEC_OVERVIEW.md` - Application flow and UI
3. Relevant functional specs in `Project/Spec/functional/`
4. Technical specs in `Project/Spec/technical/` (start with TECH_ARCHITECTURE.md)

## Architecture Overview

### Layered Architecture
```
Presentation → Commands → Services → Providers → Storage → Core
```
- Each layer may only import from layers below it
- No circular dependencies between layers
- Cross-cutting concerns (logging, errors) live in Core

### Protocol-Based Abstractions
- Key interfaces defined as Python `Protocol` classes
- Enables duck typing without inheritance
- Easy to create test mocks and swap implementations via config

### Dependency Injection
- Components receive dependencies at construction time
- `bootstrap.py` handles all component wiring
- No hard-coded provider instantiation in services

## Key Architectural Decisions

### Configuration
- YAML-driven configuration with overlay system (user config overlays defaults)
- **No hard-coded defaults in code** - all defaults in `cato/resources/defaults.yaml`
- Pydantic for all validation
- Unrecognised config keys warn but don't crash

### Multi-Provider LLM
- Must support OpenAI, Anthropic, Google, Ollama
- Use pydantic-ai over LangChain for agent/API interactions
- Each provider implements `LLMProvider` protocol

### Storage
- ChromaDB for vector store (embeddings, similarity search)
- SQLite for productivity data (tasks, lists)
- **Never load entire vector store into memory**
- Storage layer contains no business logic—pure data access

### Command System
- Slash commands (`/help`, `/speak`, `/web`, etc.) for explicit actions
- Decorator-based registration - adding a command requires only one file
- **No natural language command interface** - commands use explicit syntax

### Error Handling
- Atomic exception handling (specific exceptions, not broad catches)
- Custom exception hierarchy (`CatoError` base class in `cato/core/exceptions.py`)
- Graceful degradation for non-critical failures
- Never silent failures
- Errors flow upward: Storage → Service → Command → Presentation

## Directory Structure

```
cato/                        # Repository root
├── pyproject.toml           # Package metadata (uv/PEP 621)
├── AGENTS.md                # AI navigation (repo-level)
├── WARP.md                  # AI rules for Warp
├── cato/                    # Python package
│   ├── __main__.py          # Entry point: python -m cato
│   ├── bootstrap.py         # Component wiring
│   ├── app.py               # Main run loop
│   ├── core/                # Config, exceptions, logging, types
│   ├── providers/           # LLM, search, TTS backends
│   │   ├── llm/             # OpenAI, Anthropic, Google, Ollama
│   │   ├── search/          # DuckDuckGo, Google
│   │   └── tts/             # OpenAI TTS
│   ├── storage/             # ChromaDB, SQLite
│   ├── services/            # Business logic orchestration
│   ├── commands/            # Slash command implementations
│   ├── display/             # Rich console, prompt_toolkit
│   └── resources/           # defaults.yaml, help files
└── tests/                   # Unit, integration, e2e
```

## Code Organisation Requirements

- Root-level AI guidance lives in `AGENTS.md` and `WARP.md`
- Subdirectory `agent.md` files follow the standard in `Project/Spec/technical/TECH_CODE_ORGANISATION.md`
- Each module directory must have a README explaining purpose and extension
- Numpy-format docstrings, type hints on all functions
- Relative imports within package
- Single responsibility per file

## Testing Strategy

- **Unit tests**: Individual functions/classes in isolation with mocked dependencies
- **Integration tests**: Service + storage, command + service combinations
- **E2E tests**: Critical user journeys only (minimal—they're slow and brittle)
- Use pytest with fixtures for test database setup/teardown
- Mock external APIs at HTTP level
- Focus on core functionality, not exhaustive coverage

## Technology Stack

### Required
- Rich (formatting), prompt_toolkit (input)
- ChromaDB, OpenAI Embeddings API
- PyYAML, Pydantic
- pydantic-ai (productivity agent)
- LLM provider SDKs (OpenAI, Anthropic, Google)

### Optional
- OpenAI TTS API
- DuckDuckGo/Google/Bing search
- Ollama (local LLM)

## Development Workflow

- `main` is the stable branch; all work on feature branches
- Branch naming: `feature/<description>` or `fix/<description>`
- CI should be fast (< 5 minutes)
- Releases when meaningful changes accumulate

```

**/home/alex/Documents/repos/Cato/WARP.md**
```
# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management, conversational context via vector storage, TTS, and web search.

**Status**: Pre-implementation - specification documents exist in `Project/Spec/`

### Purpose
Cato exists to provide maximum control over LLM interactions, tailored to specific user needs and idiosyncrasies. It is a chat client first, productivity client second.

### Intent
Cato provides a unified terminal interface for:
- Conversational AI interactions with multiple LLM providers
- Personal productivity management (tasks, lists, time tracking)
- File operations and code management
- Persistent conversational context with retrieval
- Text-to-speech synthesis and web search integration

### Target User
- Single user on a single machine
- Users who are highly changeable, like to tinker and experiment
- Users who want flexible, modular architecture they can customise
- Multiple instances may run with different configurations simultaneously

## Before Starting Development

Read the specification documents in order:
1. `Project/Spec/GENERAL_PRINCIPLES.md` - Core philosophy and constraints
2. `Project/Spec/functional/SPEC_OVERVIEW.md` - Application flow and UI
3. Relevant functional specs in `Project/Spec/functional/`
4. Technical specs in `Project/Spec/technical/` (start with TECH_ARCHITECTURE.md)

## Architecture Overview

### Layered Architecture
```
Presentation → Commands → Services → Providers → Storage → Core
```
- Each layer may only import from layers below it
- No circular dependencies between layers
- Cross-cutting concerns (logging, errors) live in Core

### Protocol-Based Abstractions
- Key interfaces defined as Python `Protocol` classes
- Enables duck typing without inheritance
- Easy to create test mocks and swap implementations via config

### Dependency Injection
- Components receive dependencies at construction time
- `bootstrap.py` handles all component wiring
- No hard-coded provider instantiation in services

## Key Architectural Decisions

### Configuration
- YAML-driven configuration with overlay system (user config overlays defaults)
- **No hard-coded defaults in code** - all defaults in `cato/resources/defaults.yaml`
- Pydantic for all validation
- Unrecognised config keys warn but don't crash

### Multi-Provider LLM
- Must support OpenAI, Anthropic, Google, Ollama
- Use pydantic-ai over LangChain for agent/API interactions
- Each provider implements `LLMProvider` protocol

### Storage
- ChromaDB for vector store (embeddings, similarity search)
- SQLite for productivity data (tasks, lists)
- **Never load entire vector store into memory**
- Storage layer contains no business logic—pure data access

### Command System
- Slash commands (`/help`, `/speak`, `/web`, etc.) for explicit actions
- Decorator-based registration - adding a command requires only one file
- **No natural language command interface** - commands use explicit syntax

### Error Handling
- Atomic exception handling (specific exceptions, not broad catches)
- Custom exception hierarchy (`CatoError` base class in `cato/core/exceptions.py`)
- Graceful degradation for non-critical failures
- Never silent failures
- Errors flow upward: Storage → Service → Command → Presentation

## Directory Structure

```
cato/                        # Repository root
├── pyproject.toml           # Package metadata (uv/PEP 621)
├── AGENTS.md                # AI navigation (repo-level)
├── WARP.md                  # AI rules for Warp
├── cato/                    # Python package
│   ├── __main__.py          # Entry point: python -m cato
│   ├── bootstrap.py         # Component wiring
│   ├── app.py               # Main run loop
│   ├── core/                # Config, exceptions, logging, types
│   ├── providers/           # LLM, search, TTS backends
│   │   ├── llm/             # OpenAI, Anthropic, Google, Ollama
│   │   ├── search/          # DuckDuckGo, Google
│   │   └── tts/             # OpenAI TTS
│   ├── storage/             # ChromaDB, SQLite
│   ├── services/            # Business logic orchestration
│   ├── commands/            # Slash command implementations
│   ├── display/             # Rich console, prompt_toolkit
│   └── resources/           # defaults.yaml, help files
└── tests/                   # Unit, integration, e2e
```

## Code Organisation Requirements

- Root-level AI guidance lives in `AGENTS.md` and `WARP.md`
- Subdirectory `agent.md` files follow the standard in `Project/Spec/technical/TECH_CODE_ORGANISATION.md`
- Each module directory must have a README explaining purpose and extension
- Numpy-format docstrings, type hints on all functions
- Relative imports within package
- Single responsibility per file

## Testing Strategy

- **Unit tests**: Individual functions/classes in isolation with mocked dependencies
- **Integration tests**: Service + storage, command + service combinations
- **E2E tests**: Critical user journeys only (minimal—they're slow and brittle)
- Use pytest with fixtures for test database setup/teardown
- Mock external APIs at HTTP level
- Focus on core functionality, not exhaustive coverage

## Technology Stack

### Required
- Rich (formatting), prompt_toolkit (input)
- ChromaDB, OpenAI Embeddings API
- PyYAML, Pydantic
- pydantic-ai (productivity agent)
- LLM provider SDKs (OpenAI, Anthropic, Google)

### Optional
- OpenAI TTS API
- DuckDuckGo/Google/Bing search
- Ollama (local LLM)

## Development Workflow

- `main` is the stable branch; all work on feature branches
- Branch naming: `feature/<description>` or `fix/<description>`
- CI should be fast (< 5 minutes)
- Releases when meaningful changes accumulate

```

**/home/alex/Documents/repos/Cato/Project/Spec/GENERAL_PRINCIPLES.md**
```
# Cato General Principles

## Purpose
Cato (Chat at the Terminal Orchestrator) exists to provide maximum control over LLM interactions, tailored to specific user needs and idiosyncrasies. It is a chat client first, productivity client second.

## Core Philosophy

### Terminal-First
- Cato is a terminal application. Alternative frontends should use terminal paradigms.
- Separation of logic and display enables pluggable terminal frontends.
- Style configuration should be kept separate unless very specific to a frontend paradigm.

### Single User Focus
- Built for a single user on a single machine.
- Designed for users who are highly changeable, like to tinker and experiment.
- Configuration and architecture should be as flexible as possible.
- Multiple instances may run with different configurations simultaneously - users should manage collisions manually.

### Quality Over Convenience
- No tolerance for poor design decisions, bad architecture, or lazy coding.
- Core architecture must remain flexible and modular.
- Any component should be easily unplugged or switched out.
- Highest engineering standards required.

## Specification-Driven Development
- The functional specification is the bible for all development.
- The specification is not static - it must be kept updated at all times.
- Any decision that adds to or alters the specification must be documented with what changed and when.
- All development, design, and architecture decisions must be logged.

## Configuration Philosophy
- Configuration file driven as much as possible.
- YAML format with extensive inline documentation.
- **No hard-coded inline values** - all defaults stored in YAML, not as function/method defaults.
- User configuration overlays default configuration - only override what differs.
- A single key-value pair in user config is sufficient; all other values fall back to defaults.
- Use Pydantic extensively for validation.
- Unrecognised config items should warn but not crash - continue with defaults.

## Dependency Management
- Favour the Pydantic stack for API interactions (pydantic-ai over LangChain).
- Minimise external library dependencies where existing approved dependencies suffice.
- Do not code natively what can be done with approved dependencies.
- Do not add new dependencies outside the approved stack without explicit approval.

## Agent Architecture
- Cato is NOT an agent - it is a chat and productivity client.
- Agent-like features for specific tasks may be added later but are not in initial scope.
- Natural language interface to productivity/commands is explicitly NOT wanted - commands use slash syntax.

## Documentation Philosophy

### Codebase Self-Documentation
- Separated modules (especially in directories) should contain a README explaining:
  - What is in the directory
  - What it is used for
  - Pointers to common functions/classes/methods
  - How to add legitimate elements
- Root-level AI guidance lives in `AGENTS.md` and `WARP.md`.
- Subdirectory `agent.md` files follow the standard in `Project/Spec/technical/TECH_CODE_ORGANISATION.md`.
- Goal: minimise code scanning by models/agents to understand the system.

### User Documentation
- In-app help must be extensive, robust, and always kept up to date.
- Help system should be easy to navigate without relying on the model.
- The model does not need to know how Cato works unless explicitly asked via `/help model`.

### System Prompt
- Base/master system prompt contains minimum needed for model to do its job.
- Master prompt is sacrosanct - changes treated as code changes.
- User system prompt is appended to master prompt.
- Model does not need awareness of UI mechanics.

## Error Handling Philosophy
- Atomic exception handling - as specific as possible.
- No broad exception catching.
- Favour catching exceptions over returning error messages from Python.
- Clear, human-readable error messages.
- Errors should be expensive and visible - don't hide problems.
- Application should almost diagnose itself.

### Logging Modes
- **Debug mode**: Extremely chatty, comprehensive logging throughout stack.
- **Warn mode**: Chatty but only relevant to user experience.
- Never do anything silently - report failures to user clearly.

## Performance Requirements
- Boot as quickly as possible - effectively instantaneous.
- All database interactions in real-time - no data caching outside context.
- **Never load entire vector store into memory**.
- No gradual streamed output required, but show waiting indicator for long responses.

## Multi-Provider Support
- Assume multiple models from multiple providers will be used.
- Assume multiple agents from multiple providers will be used.
- Architecture must support any combination.

## Future Considerations
- Architecture should allow for multimodal elements (not in initial spec).
- Headless mode for one-shot queries (limited functionality).
- Real-time context retrieval from vector store as conversation topics change.

```

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md**
```
# Cato Functional Specification - Overview

## Application Summary

**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management capabilities, and conversational context through vector storage.

## Purpose

Cato provides a unified terminal interface for:
- Conversational AI interactions with multiple LLM providers
- Personal productivity management (tasks, lists)
- File operations and code management
- Persistent conversational context with retrieval
- Text-to-speech synthesis
- Web search integration

## Core Design Principles

1. **Terminal-First**: All functionality accessible via keyboard in a command-line interface
2. **Rich Output**: Markdown rendering, syntax highlighting, and formatted tables
3. **Unified Experience**: Single interface for chat, productivity, and file operations
4. **Persistent Storage**: Conversation and productivity data persisted across sessions
5. **Extensible Commands**: Slash command system for explicit actions
6. **Graceful Degradation**: Continue operation when individual components fail

## Application Flow

### Startup
1. Load configuration (YAML file → environment variables → CLI overrides)
2. Initialize Rich console for formatted output
3. Display welcome panel with model and profile information
4. Initialize chat session:
   - Set up LLM backend based on configured provider
   - Initialize vector store for conversation memory
   - Initialize productivity system (SQLite storage)
   - Initialize file tools integration
5. Enter interactive REPL loop

### Input Processing Order
User input is processed in the following priority order:

1. **Slash commands**: Input starting with `/` routes to command parser
2. **Regular chat**: All other input sent to LLM with context retrieval

### Session State
- **Session ID**: Unique UUID generated per application launch
- **Thread ID**: Unique UUID for conversation continuity
- **Message history**: List of messages (system, user, assistant)
- **Current directory**: For file operations
- **Context mode**: Debug display mode for showing retrieved context (off/on/summary)

## Specification Documents

This specification is divided into the following functional areas:

| Document | Description |
|----------|-------------|
| SPEC_CORE_CHAT.md | LLM integration, message processing, display |
| SPEC_COMMAND_SYSTEM.md | Slash command framework and all commands |
| SPEC_PRODUCTIVITY.md | Tasks, lists |
| SPEC_FILE_OPERATIONS.md | File commands, attach, export, aliases |
| SPEC_VECTOR_STORE.md | Conversation storage, similarity search |
| SPEC_TTS.md | Text-to-speech functionality |
| SPEC_WEB_SEARCH.md | Web search and URL content fetching |
| SPEC_CONFIGURATION.md | All configuration options |
| SPEC_COMMAND_LINE.md | CLI options, modes, and headless behavior |

Canonical references:
- CONFIG_REFERENCE.md (config keys, paths, context semantics)
- DATA_MODELS.md (canonical data models)
- GLOSSARY.md (terminology)

## User Interface

### Welcome Message
The welcome message displays key configuration that affects behaviour (excluding style):

```
─ 🐱 Cato ─────────────────────────────────────────────────
Welcome to Cato - Chat at the Terminal Orchestrator

Type your messages to chat with the LLM.
Type /help to see available commands.
Type /exit to quit the application.

Config: Margaret (~/.config/cato/margaret.yaml)
Model: gpt-4o-mini
Vector Store: enabled (~/.local/share/cato/vectordb)
TTS: enabled
───────────────────────────────────────────────────────────
```

**Required information:**
- Configuration name (`profile_name`) and file path
- Current model
- Behavioural settings that differ from defaults (not style)

**Purpose:** User can scroll to top of session to see exactly what configuration is active without checking files

### Prompt
Default: `🐱 > ` (configurable via `display.prompt_symbol`)

### Response Display
- Assistant responses rendered with clear visual separation (NOT bordered panels)
- Response text must be directly copy-pasteable without formatting artifacts
- Markdown formatting with syntax highlighting for code
- Configurable line width and styling
- Visual delimiter between exchanges

### Status Indicators
- 🔵 Active
- 🟡 In Progress  
- ✅ Completed
- 🗑️ Deleted
- 💭 Context indicator
- 🔊 TTS indicator

## Technology Stack

### Required Dependencies
- **LLM Clients**: OpenAI, Anthropic, Google Generative AI (via provider SDKs)
- **Local LLM**: Ollama (optional)
- **Vector Database**: ChromaDB
- **Embeddings**: OpenAI or Ollama (via embedding provider)
- **Productivity Storage**: SQLite
- **CLI Framework**: Rich (formatting), prompt_toolkit (input)
- **Configuration**: PyYAML, Pydantic (validation)
- **AI Agent**: pydantic-ai (for productivity agent)

### Optional Dependencies
- **TTS**: OpenAI TTS API
- **Audio Playback**: mpg123, ffplay, or system audio player
- **Web Search**: DuckDuckGo, Google, Bing (via HTTP requests)

## Error Handling Philosophy

1. **Non-critical failures**: Log warning, continue with reduced functionality
   - Vector store unavailable → chat continues without context retrieval
   - TTS playback fails → show error, continue chat
   - Web search fails → show error, allow retry

2. **Critical failures**: Log error, show user message, exit gracefully
   - Configuration invalid
   - LLM backend cannot initialize
   - No API key when required

3. **User cancellation**: Ctrl+C interrupts current operation, returns to prompt

```

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**
```
# Architecture Technical Specification

## Overview
This document defines Cato's core architectural patterns, component organisation, and the principles that enable modularity and flexibility.

## Design Goals
1. **Swappable components**: Any major component (LLM provider, storage backend, display) replaceable via configuration
2. **Easy extension**: Adding commands, providers, or features requires minimal changes to existing code
3. **Testability**: All components testable in isolation through dependency injection
4. **Configuration-driven**: Behaviour controlled by YAML, not code changes
5. **Clear boundaries**: Each module has a single responsibility with explicit interfaces

## Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Presentation                           │
│              (Rich console, prompt_toolkit)                 │
├─────────────────────────────────────────────────────────────┤
│                        Commands                             │
│           (Slash commands, input routing, REPL)             │
├─────────────────────────────────────────────────────────────┤
│                        Services                             │
│          (Chat, Productivity, TTS, Web Search)              │
├─────────────────────────────────────────────────────────────┤
│                        Providers                            │
│       (LLM backends, Search engines, TTS engines)           │
├─────────────────────────────────────────────────────────────┤
│                        Storage                              │
│              (ChromaDB, SQLite, File I/O)                   │
├─────────────────────────────────────────────────────────────┤
│                          Core                               │
│              (Config, Errors, Logging, Types)               │
└─────────────────────────────────────────────────────────────┘
```

### Layer Rules
- Each layer may only import from layers below it
- No circular dependencies between layers
- Cross-cutting concerns (logging, errors) live in Core and are available to all layers

### Layer Responsibilities

#### Core
- Configuration loading, validation, and access
- Custom exception hierarchy
- Logging setup and configuration
- Shared type definitions and data classes

#### Storage
- Vector store operations (ChromaDB)
- Productivity data persistence (SQLite)
- File operations for attachments and exports
- No business logic—pure data access

#### Providers
- LLM API integration (OpenAI, Anthropic, Google, Ollama)
- Search engine integration (DuckDuckGo, Google, Bing)
- TTS engine integration (OpenAI TTS)
- Each provider implements a common protocol

#### Services
- Business logic orchestration
- Chat service: message handling, context retrieval, response generation
- Productivity service: task/list operations
- TTS service: text processing, audio generation
- Web service: search execution, URL fetching

#### Commands
- Slash command parsing and dispatch
- Command registration and discovery
- Input routing (commands vs chat vs productivity)
- REPL loop management

#### Presentation
- Console output formatting (Rich)
- User input handling (prompt_toolkit)
- Theming and styling
- Spinners and progress indicators

## Protocol-Based Abstractions

Key interfaces are defined as Python `Protocol` classes, enabling duck typing without inheritance.

### LLM Provider Protocol
```python
from typing import Protocol, AsyncIterator

class LLMProvider(Protocol):
    """Protocol for LLM backend implementations."""
    
    @property
    def model_name(self) -> str:
        """Return the current model identifier."""
        ...
    
    async def complete(
        self, 
        messages: list[Message], 
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> CompletionResponse:
        """Generate a completion for the given messages."""
        ...
    
    async def stream(
        self, 
        messages: list[Message],
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> AsyncIterator[str]:
        """Stream a completion token by token."""
        ...
```

### Vector Store Protocol
```python
class VectorStore(Protocol):
    """Protocol for vector storage backends."""

    async def add(self, documents: list[VectorDocument]) -> list[str]:
        """Add documents to the store."""
        ...

    async def search(
        self,
        query: str,
        n_results: int = 5,
        filter: dict[str, Any] | None = None
    ) -> list[SearchResult]:
        """Search for similar documents."""
        ...

    async def get(self, ids: list[str]) -> list[VectorDocument]:
        """Retrieve documents by ID."""
        ...

    async def delete(self, ids: list[str]) -> None:
        """Delete documents by ID."""
        ...

    async def count(self) -> int:
        """Return total document count."""
        ...
```

### Benefits of Protocols
- No base class inheritance required
- Any class with matching methods satisfies the protocol
- Easy to create test mocks
- Swap implementations by changing config, not code

## Dependency Injection

Components receive their dependencies at construction time rather than creating them internally.

### Pattern
```python
# Services receive providers via constructor
class ChatService:
    def __init__(
        self,
        llm: LLMProvider,
        vector_store: VectorStore,
        config: ChatConfig
    ):
        self._llm = llm
        self._vector_store = vector_store
        self._config = config

# NOT this - creates tight coupling
class ChatService:
    def __init__(self):
        self._llm = OpenAIProvider()  # Locked to OpenAI
```

### Bootstrap Module
A dedicated `bootstrap.py` module handles component wiring:
1. Load configuration
2. Instantiate providers based on config
3. Instantiate services with their dependencies
4. Instantiate commands with service references
5. Return fully-wired application instance

```python
def create_application(config_path: Path | None = None) -> Application:
    """Wire up all components and return runnable application."""
    config = load_config(config_path)
    
    # Create providers based on config
    llm = create_llm_provider(config.llm)
    vector_store = create_vector_store(config.vector_store)
    productivity_db = create_productivity_db(config.storage)
    
    # Create services with dependencies
    chat_service = ChatService(llm, vector_store, config.chat)
    productivity_service = ProductivityService(productivity_db, config.productivity)
    
    # Create command registry with services
    commands = create_command_registry(
        chat=chat_service,
        productivity=productivity_service,
        config=config
    )
    
    # Create display layer
    display = create_display(config.display)
    
    return Application(
        commands=commands,
        display=display,
        config=config
    )
```

## Directory Structure

```
cato/                        # Repository root
├── pyproject.toml           # Package metadata, dependencies (uv/PEP 621)
├── README.md
├── CHANGELOG.md
├── LICENSE
├── AGENTS.md                # AI navigation (repo-level)
├── WARP.md                  # AI rules for Warp
├── .gitignore
│
├── cato/                    # Python package
│   ├── __init__.py
│   ├── __main__.py          # Entry point: python -m cato
│   ├── main.py              # CLI entry point for `cato` command
│   ├── bootstrap.py         # Component wiring and initialisation
│   ├── app.py               # Application class, main run loop
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── README.md        # Module documentation
│   │   ├── config.py        # Config loading, Pydantic models
│   │   ├── exceptions.py    # CatoError hierarchy
│   │   ├── logging.py       # Logging setup
│   │   └── types.py         # Shared data classes (Message, etc.)
│   │
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # LLMProvider protocol
│   │   │   ├── openai.py
│   │   │   ├── anthropic.py
│   │   │   ├── google.py
│   │   │   └── ollama.py
│   │   ├── search/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # SearchProvider protocol
│   │   │   ├── duckduckgo.py
│   │   │   └── google.py
│   │   └── tts/
│   │       ├── __init__.py
│   │       ├── base.py      # TTSProvider protocol
│   │       └── openai.py
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── vector/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # VectorStore protocol
│   │   │   └── chromadb.py
│   │   └── productivity/
│   │       ├── __init__.py
│   │       ├── base.py      # ProductivityStore protocol
│   │       └── sqlite.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── chat.py          # Chat orchestration
│   │   ├── productivity.py  # Task/list logic
│   │   ├── tts.py           # TTS orchestration
│   │   └── web.py           # Web search orchestration
│   │
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── base.py          # @command decorator, registry
│   │   ├── core.py          # /help, /exit, /clear, /config
│   │   ├── history.py       # /history, /delete, /model, /showsys
│   │   ├── context.py       # /showcontext, /continue, /casual
│   │   ├── files.py         # /attach, /cd, /ls, /cat, /pwd
│   │   ├── export.py        # /writemd, /writecode, /writejson, etc.
│   │   ├── vector.py        # /vadd, /vdoc, /vquery, /vstats, /vdelete
│   │   ├── productivity.py  # /st, /list
│   │   ├── tts.py           # /speak, /speaklike
│   │   └── web.py           # /web, /url
│   │
│   ├── display/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── console.py       # Rich console, output formatting
│   │   ├── input.py         # prompt_toolkit setup
│   │   ├── markdown.py      # Markdown rendering
│   │   └── themes.py        # Style definitions
│   │
│   └── resources/
│       ├── defaults.yaml    # Default configuration
│       └── help/            # Help text files
│           ├── overview.md
│           ├── commands.md
│           └── ...
│
└── tests/                   # Test suite
    ├── conftest.py          # Shared fixtures
    ├── unit/
    │   ├── test_config.py
    │   ├── test_commands.py
    │   └── ...
    ├── integration/
    │   ├── test_chat_service.py
    │   ├── test_vector_store.py
    │   └── ...
    └── e2e/
        ├── test_startup.py
        └── test_commands.py
```

## Extension Points

### Adding a New LLM Provider
1. Create `cato/providers/llm/newprovider.py`
2. Implement the `LLMProvider` protocol
3. Register in provider factory (one line)
4. Add config schema for provider-specific options
5. User selects via `llm.provider: newprovider` in config

### Adding a New Command
1. Create or edit file in `cato/commands/`
2. Use `@command` decorator:
```python
@command(name="mycommand", aliases=["mc"])
async def my_command(ctx: CommandContext, args: list[str]) -> CommandResult:
    """Help text for the command."""
    # Implementation
    return CommandResult(success=True, message="Done")
```
3. No other registration needed—decorator handles it

### Adding a New Storage Backend
1. Create implementation in `cato/storage/`
2. Implement relevant protocol (VectorStore or ProductivityStore)
3. Register in storage factory
4. User selects via config

## Configuration Integration

All components receive configuration through typed Pydantic models:

```python
# Components don't read config files directly
# They receive pre-validated config objects

class ChatService:
    def __init__(self, config: ChatConfig):
        self._temperature = config.temperature  # Already validated
        self._max_tokens = config.max_tokens
```

This ensures:
- No hard-coded defaults in implementation code
- Type safety throughout
- Single source of truth (YAML files)
- Easy testing with custom config objects

## Error Propagation

Errors flow upward through layers:
1. **Storage/Provider layer**: Raise specific exceptions (e.g., `VectorStoreError`, `ProviderAPIError`)
2. **Service layer**: Catch, log, optionally wrap in service-specific exception or re-raise
3. **Command layer**: Catch service exceptions, convert to user-friendly `CommandResult`
4. **Presentation layer**: Display error to user appropriately

```python
# Storage layer
async def search(self, query: str) -> list[Result]:
    try:
        return await self._client.search(query)
    except chromadb.errors.InvalidCollectionException as e:
        raise VectorStoreError(f"Collection not found: {e}") from e

# Service layer
async def get_context(self, query: str) -> list[str]:
    try:
        results = await self._vector_store.search(query)
        return [r.document.content for r in results]
    except VectorStoreError:
        logger.warning("Vector store unavailable, continuing without context")
        return []  # Graceful degradation

# Command layer
async def execute(self, args: list[str]) -> CommandResult:
    try:
        context = await self._chat.get_context(args[0])
        return CommandResult(success=True, data=context)
    except CatoError as e:
        return CommandResult(success=False, message=str(e))
```

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Use protocol-based mocks for dependencies
- Test config validation separately

### Integration Tests
- Test service + storage combinations
- Test command + service combinations
- Use test fixtures for database state

### End-to-End Tests
- Test full REPL interactions
- Use subprocess or pytest fixtures
- Verify user-visible behaviour

## Flexibility Summary

| Requirement | How Achieved |
|-------------|--------------|
| Swap LLM providers | Protocol abstraction + config selection |
| Add commands easily | Decorator-based registration |
| Customise appearance | Config-driven theming, separate display layer |
| Run multiple configs | CLI `--config` flag, isolated instances |
| Test components | Dependency injection, protocol mocks |
| Extend storage | Protocol abstraction + factory pattern |
| Modify without breaking | Layered architecture, explicit interfaces |

```




_Read files error: These files do not exist: /home/alex/Documents/repos/Cato/Project/Spec/technical/CONFIG_REFERENCE.md, /home/alex/Documents/repos/Cato/Project/Spec/technical/DATA_MODELS.md, /home/alex/Documents/repos/Cato/Project/Spec/technical/GLOSSARY.md _


**Command Executed:**
```bash
ls -la /home/alex/Documents/repos/Cato/Project/Spec
```

**Output:**
```
total 40
drwxr-xr-x 4 alex alex 4096 Jan 15 19:37 .
drwxr-xr-x 6 alex alex 4096 Jan 15 17:16 ..
-rw-r--r-- 1 alex alex   42 Jan 15 17:16 agents.md
-rw-r--r-- 1 alex alex 2784 Jan 15 19:41 CONFIG_REFERENCE.md
-rw-r--r-- 1 alex alex 1349 Jan 15 17:16 DATA_MODELS.md
drwxr-xr-x 2 alex alex 4096 Jan 15 19:37 functional
-rw-r--r-- 1 alex alex 4974 Jan 15 17:16 GENERAL_PRINCIPLES.md
-rw-r--r-- 1 alex alex 1613 Jan 15 17:16 GLOSSARY.md
drwxr-xr-x 2 alex alex 4096 Jan 15 19:37 technical
```


**Command Executed:**
```bash
ls -la /home/alex/Documents/repos/Cato/Project/Spec/functional
```

**Output:**
```
total 100
drwxr-xr-x 2 alex alex 4096 Jan 15 19:37 .
drwxr-xr-x 4 alex alex 4096 Jan 15 19:37 ..
-rw-r--r-- 1 alex alex 5967 Jan 15 17:16 SPEC_COMMAND_LINE.md
-rw-r--r-- 1 alex alex 9344 Jan 15 17:16 SPEC_COMMAND_SYSTEM.md
-rw-r--r-- 1 alex alex 9540 Jan 15 19:40 SPEC_CONFIGURATION.md
-rw-r--r-- 1 alex alex 7231 Jan 15 19:37 SPEC_CORE_CHAT.md
-rw-r--r-- 1 alex alex 7541 Jan 14 18:18 SPEC_FILE_OPERATIONS.md
-rw-r--r-- 1 alex alex 5765 Jan 15 17:16 SPEC_OVERVIEW.md
-rw-r--r-- 1 alex alex 6065 Jan 15 17:16 SPEC_PRODUCTIVITY.md
-rw-r--r-- 1 alex alex 5101 Jan 14 18:18 SPEC_TTS.md
-rw-r--r-- 1 alex alex 9921 Jan 15 17:16 SPEC_VECTOR_STORE.md
-rw-r--r-- 1 alex alex 6562 Jan 14 18:18 SPEC_WEB_SEARCH.md
```


**Command Executed:**
```bash
ls -la /home/alex/Documents/repos/Cato/Project/Spec/technical
```

**Output:**
```
total 176
drwxr-xr-x 2 alex alex  4096 Jan 15 19:37 .
drwxr-xr-x 4 alex alex  4096 Jan 15 19:37 ..
-rw-r--r-- 1 alex alex 16152 Jan 15 17:16 TECH_ARCHITECTURE.md
-rw-r--r-- 1 alex alex  3509 Jan 15 19:37 TECH_CLI.md
-rw-r--r-- 1 alex alex  2884 Jan 15 17:16 TECH_CODE_ORGANISATION.md
-rw-r--r-- 1 alex alex 17025 Jan 15 17:16 TECH_COMMAND_FRAMEWORK.md
-rw-r--r-- 1 alex alex 15883 Jan 15 19:41 TECH_CONFIG_SYSTEM.md
-rw-r--r-- 1 alex alex 12011 Jan 15 17:16 TECH_DEVELOPMENT.md
-rw-r--r-- 1 alex alex 19869 Jan 15 19:42 TECH_DISPLAY.md
-rw-r--r-- 1 alex alex  9726 Jan 15 19:37 TECH_ERROR_HANDLING.md
-rw-r--r-- 1 alex alex 15489 Jan 15 19:37 TECH_LLM_INTEGRATION.md
-rw-r--r-- 1 alex alex  2491 Jan 15 19:37 TECH_PERFORMANCE.md
-rw-r--r-- 1 alex alex 16765 Jan 15 17:16 TECH_STORAGE.md
-rw-r--r-- 1 alex alex 20972 Jan 15 19:37 TECH_VECTOR_STORE.md
```



**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/agents.md**
```
This directory contains the project specs

```

**/home/alex/Documents/repos/Cato/Project/Spec/CONFIG_REFERENCE.md**
```
# Configuration Reference (Canonical)

This document is the single source of truth for configuration keys, file locations, and context handling semantics. Other specs should reference this document rather than restating config details.

## Canonical Paths (XDG)

```
~/.config/cato/         # Config directory
~/.local/share/cato/    # Data directory
~/.cache/cato/          # Cache directory
```

## Config File Resolution Order

1. `--config <path>` CLI argument  
2. `CATO_CONFIG_FILE` environment variable  
3. `~/.config/cato/config.yaml`

## Core Configuration Keys

### Root
- `profile_name` (string, optional)
- `debug` (bool)

### LLM (`llm`)
- `provider` (required): `openai | anthropic | google | ollama`
- `model` (required): exact provider model identifier (no auto-detection)
- `temperature`
- `max_tokens`
- `timeout_seconds`
- `system_prompt_files`
- `base_prompt_file`
- `override_base_prompt`
- Provider-specific sections: `llm.openai`, `llm.anthropic`, `llm.google`, `llm.ollama`

### Vector Store (`vector_store`)
- `enabled`
- `backend` (currently `chromadb`)
- `path`
- `collection_name`
- `context_results`
- `search_context_window`
- `similarity_threshold`
- `dynamic_threshold`
- `retrieval_strategy`
- `chat_window`
- Embedding:
  - `embedding_provider` (`openai | ollama`)
  - `embedding_model`
  - `embedding_dimensions`
- Chunking:
  - `chunking_strategy`
  - `chunk_size`
  - `chunk_overlap`
  - `max_chunk_size`
  - `preserve_sentence_boundaries`

### Storage (`storage`)
- `database_path`
- `backup_enabled`
- `backup_frequency_hours`

### Display (`display`)
- `theme`
- `markdown_enabled`
- `code_theme`
- `max_width`
- `timestamps`
- `spinner_style`
- `prompt_symbol`
- `line_width`
- `exchange_delimiter`
- `exchange_delimiter_length`
- `style_overrides`
- `prompt_style`
- `input_style`

### Logging (`logging`)
- `level` (`DEBUG | INFO | WARNING | ERROR`)
- `file_path`
- `format`
- `max_file_size_mb`
- `backup_count`
### Commands (`commands`)
- `prefix`
- `history_file`

### Paths (`paths`)
- `data_dir`
- `config_dir`
- `cache_dir`

### TTS (`tts`)
- `enabled`
- `voice`
- `model`
- `audio_dir`

### Web Search (`web_search`)
- `enabled`
- `default_engine`
- `content_threshold`
- `max_results`
- `timeout`
- `engines`

### Locations (`locations`)
Alias map of name → path.

## Context Handling Semantics

- Context retrieval occurs on every chat turn when the vector store is enabled.
- Retrieved context **is always injected** into the LLM request if it passes the similarity threshold.
- `context_mode` (toggled via `/showcontext`) is **display-only**:
  - `off`: show nothing
  - `on`: show excerpts
  - `summary`: show count only

## Defaults

All defaults live in `cato/resources/defaults.yaml`. No defaults are hard-coded in Python.

```

**/home/alex/Documents/repos/Cato/Project/Spec/DATA_MODELS.md**
```
# Data Models (Canonical)

This document defines canonical data models. Functional and technical specs should align to these fields.

## Conversation Exchange

Stored in the vector store as a single document per exchange.

- `id` (UUID)
- `session_id` (UUID)
- `thread_id` (UUID | null)
- `user_message` (string)
- `assistant_message` (string)
- `timestamp` (ISO 8601)
- `prior_exchange_ids` (list[UUID])
- `thread_session_id` (string)
- `thread_continuation_seq` (int)
- `metadata` (dict)

## Vector Document

- `id` (string)
- `content` (string)
- `metadata` (dict)
- `embedding` (list[float] | null)

## Search Result

- `document` (VectorDocument)
- `score` (float)

## Task

- `id` (string)
- `title` (string)
- `description` (string | null)
- `status` (`active | in_progress | completed | deleted`)
- `priority` (`low | medium | high | urgent`)
- `category` (string | null)
- `due_date` (ISO 8601 | null)
- `created_at` (ISO 8601)
- `updated_at` (ISO 8601)
- `completed_at` (ISO 8601 | null)
- `metadata` (dict)

## List

- `id` (string)
- `name` (string)
- `description` (string | null)
- `created_at` (ISO 8601)
- `updated_at` (ISO 8601)
- `metadata` (dict)

## List Item

- `id` (string)
- `list_id` (string)
- `content` (string)
- `checked` (bool)
- `position` (int)
- `created_at` (ISO 8601)
- `updated_at` (ISO 8601)
- `metadata` (dict)

```

**/home/alex/Documents/repos/Cato/Project/Spec/GLOSSARY.md**
```
# Glossary (Canonical)

## Exchange
A single user message and its assistant response, stored together for retrieval.

## Session
A single application run. Identified by a unique UUID and used for grouping exchanges.

## Thread
A logical conversation chain. Multiple sessions may continue the same thread.

## Context (Retrieved Context)
Relevant past exchanges or documents retrieved from the vector store for a new turn.

## Context Injection
Including retrieved context in the LLM request so it can influence the response.

## Context Mode
Display-only debug setting controlling how retrieved context is shown to the user (`off | on | summary`). It does not affect whether context is injected.

## Vector Store
Persistent storage of embeddings for similarity search across exchanges and documents.

## Vector Document
A stored item in the vector store containing `id`, `content`, `metadata`, and optional `embedding`.

## Embedding
A numeric representation of text used for semantic similarity comparisons.

## Embedding Provider
The component that generates embeddings (e.g., OpenAI or Ollama).

## Retrieval Strategy
The algorithm used to select and rank context results (e.g., default, dynamic).

## Similarity Threshold
Minimum similarity score required for a context result to be considered.

## Chunking
Splitting long documents into smaller parts for embedding and retrieval.

## Provider
An LLM vendor/backend (OpenAI, Anthropic, Google, Ollama).

## Model Identifier
The exact model name required by a provider API (no auto-detection).

## Slash Command
An explicit command triggered by a leading `/`.

```

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md**
```
# Core Chat Specification

## Overview

The core chat system provides the primary LLM interaction loop, managing conversation history, context retrieval, and response display.

## LLM Provider Support

### Supported Providers

| Provider | Model Examples | API Key Environment Variable |
|----------|---------------|------------------------------|
| OpenAI | gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo | OPENAI_API_KEY |
| Anthropic | claude-3-opus, claude-3-sonnet, claude-3-haiku | ANTHROPIC_API_KEY |
| Google | gemini-pro, gemini-1.5-pro | GOOGLE_API_KEY |
| Ollama | llama2, mistral, codellama (local) | N/A (local) |

### Provider Selection
Provider selection is explicit:
- `llm.provider` selects the provider
- `llm.model` must match the provider's exact API model identifier

See CONFIG_REFERENCE.md for canonical config keys.

### LLM Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| model | gpt-4o-mini | Provider-specific | LLM model identifier |
| temperature | 1.0 | 0.0-2.0 | Response randomness |
| max_tokens | 4000 | >0 | Maximum response tokens |

## Conversation Management

### Message Types

| Role | Purpose |
|------|---------|
| system | System prompts defining assistant behavior |
| user | User input messages |
| assistant | LLM responses |

### Message Processing Flow

```
User Input
    ↓
Check for slash command (/) → Route to CommandParser
    ↓
Regular message processing:
    1. Add user message to history
    2. Retrieve relevant context from vector store
    3. Prepare messages for LLM API
    4. Generate response with progress indicator
    5. Add assistant response to history
    6. Store exchange in vector store
    7. Display formatted response
```

### System Prompts

#### Master/Base Prompt
A master base prompt is loaded from the package's `prompts/base_prompt.md` file. This establishes core assistant behavior.

**The master prompt is sacrosanct:**
- Contains only the minimum necessary for the model to do its job
- Does not include UI mechanics or Cato-specific knowledge
- Changes to the master prompt should be treated as code changes
- Should only be updated when absolutely necessary

The base prompt is automatically enhanced with:
- Current session timestamp (local and UTC)

#### User System Prompts
Additional system prompts can be loaded from files specified in configuration:
```yaml
llm:
  system_prompt_files:
    - ~/prompts/my_custom_prompt.md
    - ~/prompts/domain_knowledge.md
```

User prompts are **appended** to the master prompt (unless `override_base_prompt: true`).

#### Final System Prompt Structure
The generated system prompt has clear sections:
1. Master prompt (core behaviour)
2. User system prompts (appended)
3. Session metadata (timestamp, etc.)

### Context Retrieval

Before generating a response, the system:

1. **Builds search query** from recent non-command exchanges
   - Excludes messages starting with `/`
   - Uses configurable `search_context_window`

2. **Retrieves similar exchanges** from vector store
   - Uses similarity threshold from config
   - Returns up to `context_results` exchanges

3. **Injects context** into the API request when vector store is enabled and results pass the similarity threshold
4. **Displays context** based on `context_mode` (display-only)

### Context Display Modes

Controlled via `/showcontext` command:

| Mode | Behavior |
|------|----------|
| off | No context shown |
| on | Context excerpts displayed |
| summary | Only a count displayed |

When context is used, indicators appear before the response:
```
💭 Using context from 3 previous exchange(s):
   1. User: How do I configure... 
      Assistant: You can modify the...
```

## Response Generation

### Progress Indicator
While waiting for LLM response:
```
⠋ Generating response... (Press Ctrl+C to cancel)
```

### Timeout Handling
- Timeout: `llm.timeout_seconds` (default 60 seconds)
- On timeout: Show error message, return to prompt
- On Ctrl+C: Cancel request, return to prompt

### Dummy Mode
When `--dummy-mode` flag is set:
- Uses MockLLMBackend instead of real API
- Returns placeholder responses for testing
- Skips vector store writes

### Debug Mode
When `--debug` flag is set:
- Detailed logging of message processing
- Token estimation and timing
- API request/response details
- Context retrieval details

## Response Display

### Display Philosophy
**Response text must be directly copy-pasteable.**

- Do NOT use boxed/bordered panels that interfere with text selection
- Clear visual separation between exchanges without disrupting copy/paste
- Use delimiter lines and labels for clarity, not enclosing boxes

### Response Formatting

```
─ 🤖 Assistant ──────────────────────────────────────────────

Response content with **markdown** rendering

```python
def example():
    return "syntax highlighted"
```

──────────────────────────────────────────────────────────────
```

**Key points:**
- Header line with label and delimiter
- Response text is NOT enclosed in a box
- Markdown rendering applied to text
- Code blocks with syntax highlighting
- Footer delimiter to separate from next exchange

### Display Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| line_width | 80 | Terminal width for formatting |
| exchange_delimiter | "─" | Character for visual separation |
| exchange_delimiter_length | 60 | Length of delimiter line |

### Code Highlighting
- Automatic language detection from markdown fence
- Monokai theme when high_contrast enabled
- Default theme otherwise

## Conversation History

### In-Session History
- All messages stored in memory during session
- System messages preserved on `/clear`
- Arrow key navigation through input history

### Clear Command
`/clear` performs:
1. Remove all user/assistant messages
2. Keep system messages
3. Clear console screen
4. Show welcome message

### History Command
`/history [n]` displays:
- Last n messages (default: all)
- Excludes system messages
- Truncates long messages for readability

### Delete Command
`/delete [n]` removes:
- Last n user/assistant exchange pairs (default: 1)
- Preserves system messages

## Thread Continuation

### Continue Command
`/continue <thread_id>` allows resuming a previous conversation:

1. Validates thread_id exists in vector store
2. Clears current conversation (like `/clear`)
3. Loads all exchanges from the thread
4. Displays thread history to user
5. Sets thread continuation sequence number
6. New exchanges stored with incremented sequence

### Thread Identification
- Thread ID: UUID assigned at session start
- Session ID: UUID assigned at session start
- Thread Session ID: `{thread_id}_{session_id}` composite
- Continuation Sequence: Increments each time thread is continued

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Submit input |
| Up/Down | Navigate input history |
| Ctrl+C | Cancel current operation |
| Ctrl+D | Exit application |

```

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md**
```
# Command System Specification

## Overview

Cato uses a slash command system for explicit actions. Commands start with `/` and are parsed before any other input processing.

## Command Framework

### Command Detection
Input is treated as a command if it starts with `/` (after whitespace trimming).

### Command Parsing
Commands are parsed using shell-like tokenization:
- Command name extracted after `/`
- Arguments split by whitespace
- Quoted arguments preserved as single tokens

Example:
```
/web "search query with spaces" google
```
Parses to: command=`web`, args=`["search query with spaces", "google"]`

### Command Result
Each command returns a result with:
- `success`: Boolean indicating success/failure
- `message`: User-facing message
- `data`: Optional structured data for further processing

## Command Reference

### Core Commands

#### /help
Display help information.
```
/help                    # Show overview
/help commands           # Show all commands
/help productivity       # Show productivity help
/help files              # Show file operations help
/help websearch          # Show web search help
/help speak              # Show TTS help
/help config             # Show configuration help
/help model "question"   # Ask the model about Cato (see below)
```

##### /help model
Ask the model for help with Cato functionality.
```
/help model "how do I add a new command?"
/help model "what configuration options affect the vector store?"
```

**Behavior:**
1. Loads all user help files into context
2. Creates a one-off message to the model with:
   - Help file contents
   - Instruction to derive response from help documentation
   - The user's question
3. Model responds based solely on help documentation
4. This exchange is NOT added to the conversation history
5. Does not affect the main conversation context

#### /exit, /quit, /q
Exit the application.
```
/exit
/quit
/q
```

#### /clear
Clear conversation history and screen.
```
/clear
```
Behavior:
- Removes all user/assistant messages
- Preserves system messages
- Clears terminal screen
- Displays welcome message

#### /config
Show current configuration settings.
```
/config
```
Displays table with:
- Model, temperature, max tokens
- Vector store settings
- Display settings
- Logging level

### History Commands

#### /history
Show conversation history.
```
/history        # Show all messages
/history 10     # Show last 10 messages
```

#### /delete
Remove recent exchanges from history.
```
/delete         # Remove last exchange
/delete 3       # Remove last 3 exchanges
```

#### /model
Change or display the current LLM model. This overrides the setting in the user config file.
```
/model                  # Show current model
/model gpt-4o           # Change to gpt-4o
/model claude-3-sonnet  # Change to Claude
```

#### /showsys
Display the current system prompt.
```
/showsys
```

#### /loglevel
Change logging verbosity.
```
/loglevel           # Show current level
/loglevel DEBUG     # Set to DEBUG
/loglevel INFO      # Set to INFO
/loglevel WARNING   # Set to WARNING
/loglevel ERROR     # Set to ERROR
```

### Context Commands

#### /showcontext
Toggle context display mode for all future exchanges.
```
/showcontext        # Toggle on/off (shows new state)
/showcontext on     # Enable context display with excerpts
/showcontext off    # Disable context display
/showcontext summary # Show only a count of retrieved context
```

**Behavior:**
- Acts as a **toggle** - calling `/showcontext` without arguments flips the current state
- When **on**: Context excerpts displayed before each response
- When **summary**: Only a count is displayed
- When **off**: No context information displayed (default)
- Context injection is always on when vector store is enabled and results pass the similarity threshold
- State persists for the duration of the session

#### /continue, /cont
Continue an existing conversation thread.
```
/continue <thread_id>
/cont <thread_id>
```

#### /casual
Toggle casual conversation mode.
```
/casual on      # Enable casual mode
/casual off     # Disable casual mode
```

### File Commands

#### /attach
Attach files as conversation context.
```
/attach file1.txt                    # Attach single file
/attach file1.txt file2.py file3.md  # Attach multiple (max 5)
```

#### /pwd
Show current working directory.
```
/pwd
```

#### /cd
Change current directory.
```
/cd /path/to/directory
/cd ..
/cd ~
```

#### /ls
List directory contents (alias for `/file list`).
```
/ls              # List current directory
/ls /path/to     # List specific directory
```

#### /cat
Display file contents (alias for `/file read`).
```
/cat filename.txt
/cat alias:filename.txt
```

#### /locations
Show configured location aliases.
```
/locations
```

### Export Commands

#### /writecode
Extract code blocks from last response.
```
/writecode output.py
```
Extracts all code blocks (from markdown fences) and saves to file.

#### /writejson
Export conversation to JSON.
```
/writejson conversation.json
```
Exports:
- All messages with roles and content
- Configuration metadata (model, temperature)

#### /writemd, /w
Export conversation thread to Markdown.
```
/writemd output.md
/w output.md
```
Exports user/assistant exchanges (excludes system prompts).

#### /writemdall
Export full conversation to Markdown (includes system prompts).
```
/writemdall output.md
```

#### /writeresp
Export last exchange to file.
```
/writeresp output.txt           # Plain text
/writeresp output.json json     # JSON format
/writeresp output.md md         # Markdown format
```

#### /append
Append to an existing file.
```
/append notes.txt "Additional content"
/append notes.txt                       # Append last exchange
```

### Clipboard Commands

#### /copy
Copy last assistant response to clipboard.
```
/copy
```

### Vector Store Commands

See SPEC_VECTOR_STORE.md for detailed vector store documentation.

#### /vadd
Add text directly to vector store.
```
/vadd This is important information to remember
```

#### /vdoc
Add a document file to vector store with chunking.
```
/vdoc /path/to/document.txt
/vdoc alias:document.md
```

#### /vdelete
Delete an exchange from vector store.
```
/vdelete <exchange_id>
```

#### /vget
Retrieve exchanges by ID, session, or thread.
```
/vget <exchange_id>      # Get specific exchange
/vget session            # Get current session exchanges
/vget thread             # Get current thread exchanges
```

#### /vquery
Query vector store for similar content.
```
/vquery "search query"       # Default results
/vquery "search query" 10    # Return 10 results
```

#### /vstats
Display vector store statistics.
```
/vstats
```

### Productivity Commands

See SPEC_PRODUCTIVITY.md for detailed productivity documentation.

#### /st, /show-tasks, /tasks
Show open tasks.
```
/st                         # Show all open tasks
/st work                    # Filter by category
/st -p high                 # Filter by priority
/st -s priority -o desc     # Sort by priority descending
/st --status=completed      # Show completed tasks
```

**Options:**
- `-s, --sort=<field>`: Sort by created, priority, category, due, id, status
- `-o, --order=<asc|desc>`: Sort order
- `-p, --priority=<level>`: Filter by priority
- `-c, --category=<name>`: Filter by category
- `-S, --status=<status>`: Filter by status (active, in_progress, completed)

#### /list, /lists, /show-lists
Show lists and list items.
```
/list                   # Show all lists with counts
/list shopping          # Show items in shopping list
```

### Web Commands

See SPEC_WEB_SEARCH.md for detailed web search documentation.

#### /web
Search the web and add results to context.
```
/web "search query"                  # Use default engine
/web "search query" google           # Use specific engine
/web "search query" duckduckgo       # Use DuckDuckGo
```

#### /url
Fetch and attach content from a URL.
```
/url https://example.com/page.html
```

### TTS Commands

See SPEC_TTS.md for detailed TTS documentation.

#### /speak, /s
Speak the last assistant response.
```
/speak              # Default voice and model
/speak nova         # Specific voice
/speak nova tts-1   # Specific voice and model
/s                  # Alias
```

**Available Voices:** alloy, echo, fable, nova, onyx, shimmer

**Available Models:** tts-1, tts-1-hd

#### /speaklike, /sl
Speak with custom instructions.
```
/speaklike "Speak slowly and clearly"
/speaklike "Read as a news anchor" nova tts-1-hd
```

## Command Aliases

| Command | Aliases |
|---------|---------|
| /exit | /quit, /q |
| /continue | /cont |
| /speak | /s |
| /speaklike | /sl |
| /st | /show-tasks, /tasks |
| /list | /lists, /show-lists |
| /writemd | /w |

## Error Handling

Commands return appropriate error messages for:
- Missing required arguments
- Invalid argument values
- File not found / permission denied
- Feature disabled in configuration
- External service failures (API, network)

Example error display:
```
❌ Command error: No file path specified. Usage: /file read <path>
```

## Command Extension

The command system is designed for extensibility:
- Commands registered via `@command` decorator
- BaseCommand abstract class for implementation
- CommandRegistry for lookup and alias resolution
- Async execute method for each command

```

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_PRODUCTIVITY.md**
```
# Productivity System Specification

## Overview

The productivity system provides task management and list organization through explicit slash commands. It uses a dedicated agent/service to manage productivity data stored in SQLite.


## Entity Types

### Tasks

Tasks represent actionable items with optional due dates, categories, and priorities.

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Task title |
| description | string | No | Task details |
| status | enum | No | active, in_progress, completed, deleted |
| due_date | datetime | No | When task is due |
| category | string | No | Project or category name |
| priority | enum | No | urgent, high, medium, low |
| pseudo_id | string | Auto | Human-readable ID (task001, task002) |
| created_at | datetime | Auto | Creation timestamp |
| updated_at | datetime | Auto | Last update timestamp |


**Status Transitions:**
- `active` → `in_progress` → `completed`
- `active` → `deleted`
- Any status → `deleted`

### Lists and List Items

Lists provide a way to organize items into named collections (shopping, projects, ideas, etc.).

**List Item Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| content | string | Yes | Item description |
| list_id | string | Yes | ID of the parent list |
| checked | bool | No | Item completed flag |
| position | int | No | Sort/order position |
| pseudo_id | string | Auto | Human-readable ID (001) |
| created_at | datetime | Auto | Creation timestamp |


## Commands

### /st (Show Tasks)

Display open tasks with filtering and sorting options.

**Usage:**
```
/st                              # All open tasks
/st work                         # Filter by category
/st -p high                      # Filter by priority
/st -s priority -o asc           # Sort by priority ascending
/st --status=completed           # Show completed tasks
```

**Options:**
| Option | Values | Default |
|--------|--------|---------|
| -s, --sort | created, priority, category, due, id, status | created |
| -o, --order | asc, desc | desc (for created), asc (others) |
| -p, --priority | urgent, high, medium, low | none |
| -c, --category | any string | none |
| -S, --status | active, in_progress, completed | active + in_progress |

**Display:**
```
┌──────────────────────────────────────────────────────────┐
│ Open Tasks sorted by created ↓ (5)                       │
├─────┬──────────┬──────────┬───────┬─────────────┬────────┤
│ S   │ Priority │ Category │ ID    │ Task        │ Due    │
├─────┼──────────┼──────────┼───────┼─────────────┼────────┤
│ 🔵  │ 🔥 URGENT│ work     │ 005   │ Fix bug     │ Today  │
│ 🟡  │ ⚡ HIGH  │ personal │ 004   │ Call dentist│ 01/15  │
│ 🔵  │ ● MED    │ work     │ 003   │ Review doc  │        │
└─────┴──────────┴──────────┴───────┴─────────────┴────────┘
```

### /list (Show Lists)

Display lists and list items.

**Usage:**
```
/list                    # Show all lists with item counts
/list shopping           # Show items in shopping list
```

**List Overview Display:**
```
┌─────────────────────────────────────┐
│ Available Lists (3 lists)           │
├─────────────────┬───────────────────┤
│ List Name       │ Items             │
├─────────────────┼───────────────────┤
│ shopping        │ 12                │
│ ideas           │ 5                 │
│ books           │ 8                 │
└─────────────────┴───────────────────┘
```

**List Items Display:**
```
┌───────────────────────────────────────────────┐
│ List: shopping (12 items)                     │
├───────┬─────┬────────────────────┬───────────┤
│ ID    │ S   │ Item               │ Added     │
├───────┼─────┼────────────────────┼───────────┤
│ 001   │ 🔵  │ Milk               │ 01/10     │
│ 002   │ 🔵  │ Apples             │ 01/10     │
│ 003   │ ✅  │ Bread              │ 01/09     │
└───────┴─────┴────────────────────┴───────────┘
```


## Storage

### SQLite Database
Productivity data is stored in SQLite for:
- Persistence across sessions
- Efficient querying and filtering
- Structured data with relationships

### Pseudo IDs
All entities receive human-readable IDs:
- Tasks: `001`, `002`, ...
- List items: `001`, `002`, ...

IDs are assigned sequentially and used for:
- Display in tables
- Reference in commands
- Updates and deletions

## Integration with Chat

### Productivity Agent
A dedicated AI agent processes productivity requests:
- Determines appropriate action
- Executes database operations
- Returns formatted response

### Response Format
Productivity responses are displayed in the assistant panel but not added to conversation history, keeping the main LLM context clean.

```

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CONFIGURATION.md**
```
# Configuration Specification

## Overview

Cato uses a layered configuration system with the following precedence (highest to lowest):
1. Command-line arguments
2. Environment variables
3. User configuration file (YAML)
4. Default configuration file (YAML with extensive inline documentation)

## Configuration Philosophy

### Overlay Behaviour
The user configuration file **overlays** the default configuration:
- User config only needs to specify values that differ from defaults
- A single key-value pair in user config is sufficient
- All unspecified values fall back to defaults
- No hard-coded defaults in code - all defaults stored in default YAML file

### Default Configuration File
The package includes a default configuration file with:
- All configuration options
- Sensible default values
- Extensive inline comments documenting each option
- This serves as both default values and user documentation

See CONFIG_REFERENCE.md for canonical keys, defaults, and paths.

## Configuration File

### File Locations (checked in order)
1. Path specified via `--config` CLI argument
2. `CATO_CONFIG_FILE` environment variable
3. `~/.config/cato/config.yaml`

### File Format
YAML configuration with nested sections:

```yaml
profile_name: "My Profile"
debug: false

section_1:
  value_1: whatever
  value_2: 1.0

section_2:
  value_3: whatever
  value_4: 1.0
```

## Configuration Sections

### Root Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| profile_name | string | null | Human-readable name for this configuration (e.g. "Work", "Personal") |
| debug | bool | false | Enable comprehensive debug mode |

### LLM Configuration (`llm`)

| Setting | Type | Default | Range | Description |
|---------|------|---------|-------|-------------|
| provider | string | openai | openai, anthropic, google, ollama | LLM provider selection |
| model | string | gpt-4o-mini | - | LLM model identifier |
| temperature | float | 1.0 | 0.0-2.0 | Response randomness |
| max_tokens | int | 4000 | >0 | Maximum response tokens |
| timeout_seconds | int | 60 | 1-300 | Request timeout (seconds) |
| system_prompt_files | list | [] | - | Additional prompt files |
| base_prompt_file | string | null | - | Alternative prompt file path (null uses package default) |
| override_base_prompt | bool | false | - | Only has an effect if base_prompt_file is populated. If true will override the base in its entirety. If false, it will append. |

### Vector Store Configuration (`vector_store`)
See CONFIG_REFERENCE.md for canonical structure.

| Setting | Type | Default | Range | Description |
|---------|------|---------|-------|-------------|
| enabled | bool | true | - | Enable vector store |
| backend | string | chromadb | - | Vector store backend |
| path | string | ~/.local/share/cato/vectordb | - | Storage directory |
| collection_name | string | cato_memory | - | Collection name |
| chat_window | int | -1 | >0 | Max recent exchanges to retain in memory (-1 = all) |
| context_results | int | 5 | >0 | Max context exchanges returned |
| similarity_threshold | float | 0.65 | 0.0-1.0 | Minimum similarity score |
| dynamic_threshold | bool | true | - | Enable dynamic similarity thresholding |
| retrieval_strategy | string | default | - | Similarity retrieval strategy (see SPEC_VECTOR_STORE.md) |
| search_context_window | int | 3 | >0 | Recent exchanges used to build the search query |

**Embedding settings** (within `vector_store`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| embedding_provider | string | openai | openai, ollama |
| embedding_model | string | text-embedding-3-small | Embedding model |
| embedding_dimensions | int | 1536 | Vector dimensions |

**Chunking settings** (within `vector_store`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| chunking_strategy | string | semantic | truncate, fixed_size, semantic, hybrid |
| chunk_size | int | 1000 | Target chunk size (chars) |
| chunk_overlap | int | 100 | Overlap between chunks (chars) |
| max_chunk_size | int | 1500 | Maximum chunk size |
| preserve_sentence_boundaries | bool | true | Avoid mid-sentence splits |

### Display Configuration (`display`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| theme | string | default | Display theme name |
| markdown_enabled | bool | true | Enable markdown rendering |
| code_theme | string | monokai | Syntax highlighting theme |
| max_width | int | null | Max render width (null = terminal width) |
| timestamps | bool | false | Show timestamps on messages |
| spinner_style | string | dots | Spinner style name |
| prompt_symbol | string | 🐱 >  | Input prompt (supports Unicode/emoji) |
| line_width | int | 80 | Terminal width for response formatting (chars) |
| exchange_delimiter | string | ─ | Character for separation |
| exchange_delimiter_length | int | 60 | Delimiter line length |
| style_overrides | dict | {} | Rich style overrides keyed by role (user, assistant, system, error, warning, info, code) |
| prompt_style | string | null | prompt_toolkit style for the prompt (null uses theme/default) |
| input_style | string | null | prompt_toolkit style for input text (null uses theme/default) |


### Logging Configuration (`logging`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| level | string | WARNING | DEBUG, INFO, WARNING, ERROR |
| file_path | string | ~/.local/share/cato/cato.log | Log file path (null disables file logging) |
| format | string | %(asctime)s - %(name)s - %(levelname)s - %(message)s | Log message format |
| max_file_size_mb | int | 10 | Max size per log file |
| backup_count | int | 3 | Number of rotated log files to keep |

### Command Configuration (`commands`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| prefix | string | / | Slash command prefix |
| history_file | string | ~/.local/share/cato/command_history | Prompt history file |

### Path Configuration (`paths`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| data_dir | string | ~/.local/share/cato | Data directory |
| config_dir | string | ~/.config/cato | Config directory |
| cache_dir | string | ~/.cache/cato | Cache directory |

### TTS Configuration (`tts`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| enabled | bool | true | Enable TTS functionality |
| voice | string | nova | Default voice |
| model | string | tts-1 | Default TTS model |
| audio_dir | string | /tmp | Audio file directory |

### Web Search Configuration (`web_search`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| enabled | bool | true | Enable web search |
| default_engine | string | duckduckgo | Default search engine |
| content_threshold | int | 500 | Max words per page |
| max_results | int | 3 | Max results to process (≤10) |
| timeout | int | 10 | Request timeout (seconds) |
| engines | dict | (built-in) | Search engine URLs |

### Location Aliases (`locations`)

Key-value pairs mapping alias names to paths:
```yaml
locations:
  docs: ~/Documents
  projects: ~/Code/projects
  config: ~/.config
```

## Command-Line Interface

CLI options, modes (including headless), and outputs are specified in `SPEC_COMMAND_LINE.md`. This document focuses on configuration data and precedence; CLI overrides remain the highest-precedence layer in the configuration stack.

## Environment Variables

### API Keys
| Variable | Description |
|----------|-------------|
| OPENAI_API_KEY | OpenAI API key (LLM, embeddings, TTS) |
| ANTHROPIC_API_KEY | Anthropic API key |
| GOOGLE_API_KEY | Google API key |

### Configuration Overrides

| Variable | Description |
|----------|-------------|
| CATO_CONFIG_FILE |  The path to the config file to use if one wasn't passed in the cmd args|

## Validation

### On Startup
1. Load defaults and user config (if found)
2. Parse YAML structure
3. Deep-merge user config over defaults
4. Apply environment variable overrides
5. Validate using Pydantic models:
   - Type checking
   - Range validation
   - Enum validation
6. Validate location aliases (paths exist)
7. Apply CLI argument overrides (highest precedence) and validate CLI values
8. Report validation errors

If there is an appropriate existing parser or validator in pydantic (e.g. for file location validation) the you should use that in preference to creating a native one.

### Error Handling
- Invalid YAML: Show parse error, exit
- Missing required key: Show error, exit
- Invalid value: Show error, exit
- Invalid location alias: Log warning, continue


## Example Configurations

### Minimal Configuration
```yaml
llm:
  provider: openai
  model: gpt-4o-mini
```

### Development Configuration
```yaml
profile_name: Development
debug: true

llm:
  provider: openai
  model: gpt-4o-mini
  temperature: 0.7

logging:
  level: DEBUG

vector_store:
  path: ~/.local/share/cato/vectordb-dev
```

### Production Configuration
```yaml
profile_name: Production

llm:
  provider: openai
  model: gpt-4o
  temperature: 1.0
  max_tokens: 8000

vector_store:
  enabled: true
  similarity_threshold: 0.7

logging:
  level: WARNING
```

### Local Development (Ollama)
```yaml
profile_name: Local Ollama

llm:
  provider: ollama
  model: llama2
  temperature: 0.8

vector_store:
  enabled: false  # Optional for local

tts:
  enabled: false
```

```

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_VECTOR_STORE.md**
```
# Vector Store Specification

## Overview

The vector store provides persistent conversation context using vector embeddings for semantic similarity search. It enables context retrieval from previous conversations and document storage for future reference.

## Critical Performance Requirements

**NEVER load the entire vector store into memory.**

- All queries must be performed on-demand against the database
- No caching of vector store contents outside current conversation context
- Startup must not be delayed by vector store loading
- See TECH_PERFORMANCE.md for detailed performance requirements

## Storage Backend

### ChromaDB
- Persistent storage using DuckDB backend
- Cosine similarity for vector comparison
- Automatic persistence on write

### Embeddings
- Provider: OpenAI or Ollama (configurable)
- Model and dimensions are configurable
- Provider API key required when applicable

See CONFIG_REFERENCE.md for canonical keys.

## Exchange Storage

### Exchange Data Model

Each conversation exchange stores:

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| thread_id | UUID | Conversation thread grouping |
| session_id | UUID | Application session identifier |
| user_message | string | User's input message |
| assistant_message | string | Assistant's response |
| timestamp | string | ISO 8601 timestamp |
| prior_exchange_ids | list | Context exchanges used |
| thread_session_id | string | Composite ID (thread_id_session_id) |
| thread_continuation_seq | int | Continuation sequence (0 for original) |

### Storage Flow

1. User sends message, assistant responds
2. Combined text created: `"User: {user_message}\nAssistant: {assistant_message}"`
3. Text embedded using the configured embedding provider
4. Exchange stored in ChromaDB with metadata

### Automatic Storage
All conversation exchanges are automatically stored (except in dummy mode) for:
- Future context retrieval
- Thread continuation
- Conversation history
- Productivity exchanges and outputs are **not** stored

## Similarity Search

### Query Process
1. Query text embedded using the configured embedding provider
2. ChromaDB performs cosine similarity search
3. Results filtered by similarity threshold (static or dynamic)
4. Top-k results returned

### Retrieval Strategy Architecture

The retrieval system is designed to be **pluggable** to allow experimentation with different strategies and algorithms.

#### Strategy Interface
All retrieval strategies must implement a common interface:
- Accept query embedding and parameters
- Return ranked results with similarity scores
- Support configuration options

#### Built-in Strategies

| Strategy | Description |
|----------|-------------|
| default | Standard cosine similarity with static threshold |
| dynamic | Adjusts threshold based on context length |
| (extensible) | Additional strategies can be added |

#### Dynamic Thresholding
When `dynamic_threshold: true` in config:
- Threshold adjusts based on current conversation context length
- Shorter context → lower threshold (more permissive retrieval)
- Longer context → higher threshold (more selective)
- Algorithm: Simple linear adjustment based on context message count
- Can be disabled to use static `similarity_threshold`

### Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| similarity_threshold | 0.65 | Minimum similarity score (static, used when dynamic disabled) |
| dynamic_threshold | true | Enable dynamic threshold adjustment |
| retrieval_strategy | default | Which retrieval strategy to use |
| context_results | 5 | Maximum context exchanges returned |
| search_context_window | 3 | Recent exchanges used to build the search query |

### Context Retrieval

During response generation:

1. **Build query** from recent exchanges (excluding commands)
2. **Select strategy** based on configuration
3. **Search regular context** using configured retrieval strategy
4. **Filter and rank** by similarity score
5. **Inject into prompt** when enabled and above similarity threshold
6. **Display context** based on `context_mode` (display-only)

## Document Indexing

### Document Chunking

Long documents are split into chunks for better retrieval.

**Chunking Strategies:**

| Strategy | Description |
|----------|-------------|
| truncate | Simple truncation to chunk_size |
| fixed_size | Split into equal-sized chunks with overlap |
| semantic | Split at paragraph/sentence boundaries |
| hybrid | Combine semantic splitting with size limits |

**Configuration:**

| Setting | Default | Description |
|---------|---------|-------------|
| chunking_strategy | semantic | Chunking strategy |
| chunk_size | 1000 | Target chunk size (characters) |
| chunk_overlap | 100 | Overlap between chunks |
| max_chunk_size | 1500 | Maximum chunk size (hard limit) |
| preserve_sentence_boundaries | true | Avoid mid-sentence splits |

### /vadd Command
Add text directly to vector store.

```
/vadd This is important information to remember
```

**Behavior:**
- Short text: Stored as single exchange
- Long text: Automatically chunked using configured strategy
- Metadata: `source: vadd_command, manual_entry: true`

### /vdoc Command
Add a document file with chunking.

```
/vdoc /path/to/document.txt
/vdoc docs:readme.md
```

**Behavior:**
1. Read file content
2. Apply chunking strategy
3. Store each chunk as exchange
4. Link chunks via metadata

**Metadata:**
- `source: vdoc_command`
- `source_file: {filepath}`
- `chunk_index: n`
- `total_chunks: N`


## Vector Store Commands

### /vquery
Query for similar exchanges.

```
/vquery "search query"       # Default k results
/vquery "search query" 10    # Return 10 results
```

**Display:**
```
┌─ Vector Store Query Results ─────────────────────────────────┐
│ Result 1 (similarity: 0.89)                                  │
│ Thread: abc123... | Session: def456...                       │
│ User: How do I configure...                                  │
│ Assistant: You can modify the config file...                 │
├──────────────────────────────────────────────────────────────┤
│ Result 2 (similarity: 0.82)                                  │
│ ...                                                          │
└──────────────────────────────────────────────────────────────┘
```

### /vget
Retrieve specific exchanges.

```
/vget <exchange_id>      # Get by ID
/vget session            # Get current session's exchanges
/vget thread             # Get current thread's exchanges
```

### /vdelete
Delete an exchange by ID.

```
/vdelete <exchange_id>
```

**Behavior:**
- Removes from ChromaDB
- Cannot be undone
- Does not affect conversation history

### /vstats
Display vector store statistics.

```
/vstats
```

**Display:**
```
┌─ Vector Store Statistics ────────────────────────────────────┐
│ Metric           │ Value                                     │
├──────────────────┼───────────────────────────────────────────┤
│ Total Exchanges  │ 1,234                                     │
│ Store Path       │ ~/.local/share/cato/vectordb              │
│ Vector Dimension │ 1536                                      │
│ Embedding Model  │ text-embedding-3-small                    │
└──────────────────┴───────────────────────────────────────────┘
```

## Thread Management

### Thread Continuation
`/continue <thread_id>` loads a previous thread:

1. Fetch all exchanges with matching thread_id
2. Sort by timestamp
3. Calculate next continuation sequence
4. Clear current conversation
5. Load thread history as messages
6. Display history to user
7. Resume conversation with new session

### Thread Session Tracking
- Each exchange has `thread_id` and `session_id`
- Composite `thread_session_id` for unique identification
- `thread_continuation_seq` tracks which continuation (0 = original)

## Headless Operations

### CLI Arguments
For automation without interactive session:

```bash
# Add document to vector store
cato --add-to-vector-store /path/to/document.txt

# Query vector store
cato --query-vector-store "search query"

# Show statistics
cato --vector-store-stats
```

## Configuration

### Vector Store Config
```yaml
vector_store:
  enabled: true
  backend: chromadb
  path: ~/.local/share/cato/vectordb
  collection_name: cato_memory
  context_results: 5
  search_context_window: 3
  similarity_threshold: 0.65
  dynamic_threshold: true
  retrieval_strategy: default
  embedding_provider: openai
  embedding_model: text-embedding-3-small
  embedding_dimensions: 1536
  chunking_strategy: semantic
  chunk_size: 1000
  chunk_overlap: 100
  max_chunk_size: 1500
  preserve_sentence_boundaries: true
```

## Error Handling

### Graceful Degradation
If vector store fails to initialize:
- Log warning
- Continue without context retrieval
- Conversation still works

### Operation Failures
- Failed storage: Log warning, continue chat
- Failed retrieval: Use empty context
- Invalid queries: Show error message

## Disabling Vector Store

```yaml
vector_store:
  enabled: false
```

Or via CLI:
```bash
cato --no-vector-store
```

When disabled:
- No context retrieval
- No `/v*` commands available
- `/continue` unavailable

```

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_LINE.md**
```
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

```





**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_COMMAND_FRAMEWORK.md**
```
# Command Framework Technical Specification

## Overview
Cato uses a decorator-based command registration system. Commands are self-contained modules that register themselves on import, enabling easy addition of new commands without modifying core code.

## Command Protocol

### Base Interface
```python
from typing import Protocol
from dataclasses import dataclass

@dataclass
class CommandResult:
    """
    Result from command execution.
    
    Note: Uses dataclass rather than Pydantic as it's internal return data,
    not data crossing system boundaries.
    """
    success: bool
    message: str
    data: dict | None = None


class Command(Protocol):
    """
    Protocol for command implementations.
    
    Commands are stateless—all state accessed via injected dependencies.
    """
    
    @property
    def name(self) -> str:
        """Primary command name (without slash)."""
        ...
    
    @property
    def aliases(self) -> list[str]:
        """Alternative names for the command."""
        ...
    
    @property
    def description(self) -> str:
        """Brief description for help text."""
        ...
    
    @property
    def usage(self) -> str:
        """Usage pattern string."""
        ...
    
    async def execute(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        """
        Execute the command.
        
        Parameters
        ----------
        args
            Parsed arguments (command name excluded).
        context
            Execution context with dependencies.
        
        Returns
        -------
        CommandResult
            Result with success status and message.
        """
        ...
```

### Command Context
```python
@dataclass
class CommandContext:
    """
    Execution context providing access to application services.
    
    Injected at runtime—commands should not instantiate dependencies.
    Uses dataclass as it's a dependency container, not external data.
    """
    
    config: CatoConfig
    conversation: Conversation
    llm: LLMProvider
    vector_store: VectorStore | None
    storage: Storage
    display: Display
    
    # Current state
    cwd: Path  # Current working directory
    session_id: str
    thread_id: str | None
```

## Command Registration

### Decorator Pattern
```python
from typing import Callable, Type

# Global command registry
_COMMANDS: dict[str, Type[Command]] = {}
_ALIASES: dict[str, str] = {}  # alias -> primary name


def command(
    name: str,
    aliases: list[str] | None = None,
    description: str = "",
    usage: str = "",
) -> Callable[[Type], Type]:
    """
    Decorator to register a command class.
    
    Parameters
    ----------
    name
        Primary command name (without slash).
    aliases
        Alternative names.
    description
        Brief description for help.
    usage
        Usage pattern string.
    
    Returns
    -------
    Callable
        Decorator that registers the class.
    
    Example
    -------
    @command("help", aliases=["h", "?"], description="Show help")
    class HelpCommand:
        async def execute(self, args, context):
            ...
    """
    def decorator(cls: Type) -> Type:
        # Attach metadata to class
        cls._cmd_name = name
        cls._cmd_aliases = aliases or []
        cls._cmd_description = description
        cls._cmd_usage = usage
        
        # Register
        _COMMANDS[name] = cls
        for alias in (aliases or []):
            _ALIASES[alias] = name
        
        return cls
    return decorator
```

### Registry Access
```python
class CommandRegistry:
    """
    Central registry for command lookup and execution.
    
    Commands are discovered automatically when their modules are imported.
    """
    
    def __init__(self) -> None:
        self._commands = _COMMANDS
        self._aliases = _ALIASES
    
    def get(self, name: str) -> Type[Command] | None:
        """
        Look up a command by name or alias.
        
        Parameters
        ----------
        name
            Command name (with or without slash).
        
        Returns
        -------
        Type[Command] | None
            Command class if found.
        """
        # Strip leading slash if present
        name = name.lstrip("/")
        
        # Check aliases first
        if name in self._aliases:
            name = self._aliases[name]
        
        return self._commands.get(name)
    
    def list_commands(self) -> list[tuple[str, str, list[str]]]:
        """
        List all registered commands.
        
        Returns
        -------
        list[tuple[str, str, list[str]]]
            List of (name, description, aliases) tuples.
        """
        return [
            (name, cls._cmd_description, cls._cmd_aliases)
            for name, cls in sorted(self._commands.items())
        ]
    
    def resolve_alias(self, name: str) -> str:
        """Resolve an alias to its primary command name."""
        return self._aliases.get(name.lstrip("/"), name.lstrip("/"))
```

## Command Parsing

### Input Tokenization
```python
import shlex

def parse_command_input(input_text: str) -> tuple[str, list[str]] | None:
    """
    Parse user input into command name and arguments.
    
    Parameters
    ----------
    input_text
        Raw user input.
    
    Returns
    -------
    tuple[str, list[str]] | None
        (command_name, args) if input is a command, None otherwise.
    
    Examples
    --------
    >>> parse_command_input("/help")
    ("help", [])
    >>> parse_command_input('/web "search query" google')
    ("web", ["search query", "google"])
    >>> parse_command_input("hello")
    None
    """
    text = input_text.strip()
    
    # Must start with /
    if not text.startswith("/"):
        return None
    
    # Remove leading slash
    text = text[1:]
    
    # Handle empty command
    if not text:
        return None
    
    try:
        # Use shlex for shell-like tokenization
        tokens = shlex.split(text)
    except ValueError:
        # Unbalanced quotes - treat rest as single argument
        parts = text.split(maxsplit=1)
        tokens = [parts[0], parts[1]] if len(parts) > 1 else [parts[0]]
    
    command_name = tokens[0].lower()
    args = tokens[1:] if len(tokens) > 1 else []
    
    return (command_name, args)
```

### Argument Parsing
Commands can use argument parsers for complex arguments:

```python
from argparse import ArgumentParser, Namespace

class TaskCommand:
    """Show tasks with filtering and sorting."""
    
    def __init__(self) -> None:
        self._parser = ArgumentParser(prog="/st", add_help=False)
        self._parser.add_argument("category", nargs="?", default=None)
        self._parser.add_argument("-p", "--priority", choices=["low", "medium", "high"])
        self._parser.add_argument("-s", "--sort", default="created")
        self._parser.add_argument("-o", "--order", choices=["asc", "desc"], default="asc")
        self._parser.add_argument("-S", "--status", default="active")
    
    async def execute(self, args: list[str], context: CommandContext) -> CommandResult:
        try:
            parsed = self._parser.parse_args(args)
        except SystemExit:
            return CommandResult(
                success=False,
                message=f"Invalid arguments. Usage: {self._cmd_usage}",
            )
        
        # Use parsed.category, parsed.priority, etc.
        ...
```

## Command Execution

### Execution Flow
```python
class CommandExecutor:
    """
    Executes commands with proper context and error handling.
    """
    
    def __init__(
        self,
        registry: CommandRegistry,
        context_factory: Callable[[], CommandContext],
    ) -> None:
        self._registry = registry
        self._context_factory = context_factory
    
    async def execute(self, input_text: str) -> CommandResult | None:
        """
        Parse and execute a command from user input.
        
        Parameters
        ----------
        input_text
            Raw user input.
        
        Returns
        -------
        CommandResult | None
            Result if input was a command, None if not a command.
        
        Raises
        ------
        CommandNotFoundError
            Unknown command name.
        CommandExecutionError
            Command failed during execution.
        """
        parsed = parse_command_input(input_text)
        if parsed is None:
            return None  # Not a command
        
        command_name, args = parsed
        
        # Look up command
        command_cls = self._registry.get(command_name)
        if command_cls is None:
            raise CommandNotFoundError(
                f"Unknown command: /{command_name}",
                context={"available": [c[0] for c in self._registry.list_commands()]},
            )
        
        # Create instance and execute
        command = command_cls()
        context = self._context_factory()
        
        try:
            return await command.execute(args, context)
        except CatoError:
            raise  # Let Cato errors propagate
        except Exception as e:
            raise CommandExecutionError(
                f"Command /{command_name} failed: {e}",
                context={"command": command_name, "args": args},
            ) from e
```

## Command Implementation Examples

### Simple Command
```python
@command("clear", description="Clear conversation and screen")
class ClearCommand:
    """Clear conversation history and terminal screen."""
    
    @property
    def name(self) -> str:
        return "clear"
    
    @property
    def aliases(self) -> list[str]:
        return []
    
    @property
    def description(self) -> str:
        return "Clear conversation and screen"
    
    @property
    def usage(self) -> str:
        return "/clear"
    
    async def execute(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        # Clear conversation (keep system prompt)
        context.conversation.messages.clear()
        
        # Clear screen
        context.display.clear()
        context.display.show_welcome()
        
        return CommandResult(success=True, message="Conversation cleared")
```

### Command with Arguments
```python
@command(
    "history",
    aliases=["h"],
    description="Show conversation history",
    usage="/history [count]",
)
class HistoryCommand:
    """Display conversation history."""
    
    @property
    def name(self) -> str:
        return "history"
    
    @property
    def aliases(self) -> list[str]:
        return ["h"]
    
    @property
    def description(self) -> str:
        return "Show conversation history"
    
    @property
    def usage(self) -> str:
        return "/history [count]"
    
    async def execute(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        # Parse optional count argument
        count = None
        if args:
            try:
                count = int(args[0])
                if count < 1:
                    raise ValueError()
            except ValueError:
                return CommandResult(
                    success=False,
                    message=f"Invalid count: {args[0]}. Must be a positive integer.",
                )
        
        # Get messages
        messages = context.conversation.messages
        if count:
            messages = messages[-count:]
        
        # Format and display
        for msg in messages:
            context.display.show_message(msg.role, msg.content)
        
        return CommandResult(
            success=True,
            message=f"Showing {len(messages)} messages",
        )
```

### Command with Subcommands
```python
@command(
    "help",
    aliases=["h", "?"],
    description="Show help information",
    usage="/help [topic]",
)
class HelpCommand:
    """Display help information."""
    
    # Subcommand handlers
    _TOPICS = {
        "commands": "_show_commands",
        "productivity": "_show_productivity",
        "files": "_show_files",
        "model": "_ask_model",
    }
    
    async def execute(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        if not args:
            return await self._show_overview(context)
        
        topic = args[0].lower()
        handler_name = self._TOPICS.get(topic)
        
        if handler_name:
            handler = getattr(self, handler_name)
            return await handler(args[1:], context)
        
        return CommandResult(
            success=False,
            message=f"Unknown help topic: {topic}",
            data={"available": list(self._TOPICS.keys())},
        )
    
    async def _show_overview(self, context: CommandContext) -> CommandResult:
        # Show general help
        ...
    
    async def _ask_model(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        # Special handling for /help model "question"
        if not args:
            return CommandResult(
                success=False,
                message='Usage: /help model "your question"',
            )
        
        question = " ".join(args)
        # Load help docs, query model, return response
        ...
```

## Command Discovery

### Auto-Import Pattern
Commands are discovered by importing all modules in `cato/commands/`:

```python
# cato/commands/__init__.py
import importlib
import pkgutil
from pathlib import Path

def discover_commands() -> None:
    """
    Import all command modules to trigger registration.
    
    Called once at startup after core is initialised.
    """
    package_dir = Path(__file__).parent
    
    for module_info in pkgutil.iter_modules([str(package_dir)]):
        if not module_info.name.startswith("_"):
            importlib.import_module(f"cato.commands.{module_info.name}")
```

### File Structure
```
cato/commands/
├── __init__.py          # discover_commands()
├── base.py              # Command protocol, decorator, registry
├── core.py              # /help, /exit, /clear, /config
├── history.py           # /history, /delete, /showsys
├── files.py             # /attach, /pwd, /cd, /ls, /cat
├── export.py            # /writecode, /writemd, /writejson
├── vector.py            # /vadd, /vdoc, /vquery, /vstats
├── productivity.py      # /st, /list
├── web.py               # /web, /url
└── tts.py               # /speak, /speaklike
```

## Adding New Commands

To add a new command:

1. Create file in `cato/commands/` (or add to existing related file)
2. Import decorator: `from cato.commands.base import command`
3. Implement class with `@command` decorator
4. Command is auto-discovered on next startup

```python
# cato/commands/mycommand.py
from cato.commands.base import command, CommandContext, CommandResult

@command(
    "mycommand",
    aliases=["mc"],
    description="Do something useful",
    usage="/mycommand <arg>",
)
class MyCommand:
    """Implementation of mycommand."""
    
    @property
    def name(self) -> str:
        return "mycommand"
    
    @property
    def aliases(self) -> list[str]:
        return ["mc"]
    
    @property
    def description(self) -> str:
        return "Do something useful"
    
    @property
    def usage(self) -> str:
        return "/mycommand <arg>"
    
    async def execute(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        if not args:
            return CommandResult(
                success=False,
                message="Missing required argument",
            )
        
        # Do the thing
        result = await self._do_something(args[0], context)
        
        return CommandResult(
            success=True,
            message=f"Done: {result}",
            data={"result": result},
        )
```

## Error Handling

Commands should:
- Validate arguments before execution
- Return `CommandResult(success=False, ...)` for user errors
- Raise `CommandArgumentError` for invalid argument types
- Let other exceptions propagate (caught by executor)

```python
async def execute(self, args: list[str], context: CommandContext) -> CommandResult:
    # Validate required args
    if len(args) < 1:
        return CommandResult(
            success=False,
            message=f"Missing required argument. Usage: {self.usage}",
        )
    
    # Validate argument types
    try:
        count = int(args[0])
    except ValueError:
        raise CommandArgumentError(
            f"Expected integer, got: {args[0]}",
            context={"argument": "count", "value": args[0]},
        )
    
    # Execute - let other errors propagate
    result = await context.storage.get_items(count)
    return CommandResult(success=True, message="OK", data={"items": result})
```

```

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md**
```
# Configuration System Technical Specification

## Overview
Cato uses a layered YAML configuration system where user settings overlay defaults. All configurable values live in YAML files—no hard-coded defaults in code.

## Configuration Hierarchy
```
defaults.yaml          # Shipped with Cato, never modified by user
    ↓
user_config.yaml       # User overrides, sparse (only differences)
    ↓
environment vars       # CATO_* overrides + provider API keys (OPENAI_API_KEY, etc.)
    ↓
CLI arguments          # Highest precedence, session-specific
```

## File Locations
```
~/.config/cato/
├── config.yaml        # User configuration
├── prompts/           # Custom system prompts
└── themes/            # Custom display themes

$PACKAGE/
└── defaults/
    ├── defaults.yaml  # Default configuration
    ├── prompts/       # Default prompts
    └── themes/        # Default themes
```

## Configuration Loading

### Load Sequence
```python
def load_config(user_path: Path | None = None) -> CatoConfig:
    """
    Load configuration with overlay system.
    
    Parameters
    ----------
    user_path
        Optional custom path to user config. If None, uses default location.
    
    Returns
    -------
    CatoConfig
        Validated configuration object.
    """
    # 1. Load defaults (always present, shipped with package)
    defaults = load_yaml(get_default_config_path())
    
    # 2. Load user config if exists
    user_config = {}
    if user_path and user_path.exists():
        user_config = load_yaml(user_path)
    elif default_user_path().exists():
        user_config = load_yaml(default_user_path())
    
    # 3. Deep merge: user overlays defaults
    merged = deep_merge(defaults, user_config)
    
    # 4. Apply environment variable overrides
    merged = apply_env_overrides(merged)
    
    # 5. Validate with Pydantic
    return CatoConfig.model_validate(merged)
```

### Deep Merge Behaviour
```python
# defaults.yaml
llm:
  provider: "openai"
  model: "gpt-4o-mini"
  temperature: 1.0
  max_tokens: 4000

# user_config.yaml
llm:
  model: "gpt-4-turbo"

# Result after merge
llm:
  provider: "openai"        # from defaults
  model: "gpt-4-turbo"      # from user (override)
  temperature: 1.0          # from defaults
  max_tokens: 4000          # from defaults
```

## Pydantic Schema

### Root Configuration
```python
class CatoConfig(BaseModel):
    """Root configuration model."""
    
    model_config = ConfigDict(extra="ignore")  # Warn on unknown keys separately
    
    profile_name: str | None = None
    debug: bool = False
    llm: LLMConfig
    vector_store: VectorStoreConfig
    storage: StorageConfig
    display: DisplayConfig
    commands: CommandConfig
    logging: LoggingConfig
    paths: PathConfig
    tts: TTSConfig
    web_search: WebSearchConfig
    locations: dict[str, str] = Field(default_factory=dict)
```

### LLM Configuration
```python
class LLMConfig(BaseModel):
    """LLM provider configuration."""
    
    provider: Literal["openai", "anthropic", "google", "ollama"]
    model: str
    temperature: float = Field(ge=0.0, le=2.0)
    max_tokens: int = Field(ge=1, le=200000)
    timeout_seconds: int = Field(ge=1, le=300)
    system_prompt_files: list[Path] | None = None
    base_prompt_file: Path | None = None
    override_base_prompt: bool = False
    
    # Provider-specific settings
    openai: OpenAIConfig | None = None
    anthropic: AnthropicConfig | None = None
    google: GoogleConfig | None = None
    ollama: OllamaConfig | None = None
```

### Vector Store Configuration
```python
class VectorStoreConfig(BaseModel):
    """Vector store configuration."""
    
    enabled: bool
    backend: Literal["chromadb"]
    path: Path
    collection_name: str
    context_results: int = Field(ge=1)
    search_context_window: int = Field(ge=1)
    similarity_threshold: float = Field(ge=0.0, le=1.0)
    dynamic_threshold: bool
    retrieval_strategy: str
    chat_window: int
    embedding_provider: Literal["openai", "ollama"]
    embedding_model: str
    embedding_dimensions: int = Field(ge=1)
    chunking_strategy: Literal["truncate", "fixed_size", "semantic", "hybrid"]
    chunk_size: int = Field(ge=100, le=10000)
    chunk_overlap: int = Field(ge=0)
    max_chunk_size: int = Field(ge=100, le=10000)
    preserve_sentence_boundaries: bool
    
    @field_validator("chunk_overlap")
    @classmethod
    def overlap_less_than_size(cls, v: int, info: ValidationInfo) -> int:
        if "chunk_size" in info.data and v >= info.data["chunk_size"]:
            raise ValueError("chunk_overlap must be less than chunk_size")
        return v
```

### Storage Configuration
```python
class StorageConfig(BaseModel):
    """SQLite storage configuration."""
    
    database_path: Path
    backup_enabled: bool
    backup_frequency_hours: int = Field(ge=1)
```

### Display Configuration
```python
class DisplayConfig(BaseModel):
    """Display and UI configuration."""
    
    theme: str
    markdown_enabled: bool
    code_theme: str
    max_width: int | None = Field(ge=40, default=None)
    timestamps: bool
    spinner_style: str
    prompt_symbol: str
    line_width: int
    exchange_delimiter: str
    exchange_delimiter_length: int
    style_overrides: dict[str, str]
    prompt_style: str | None
    input_style: str | None
```

### Logging Configuration
```python
class LoggingConfig(BaseModel):
    """Logging configuration."""
    
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]
    file_path: Path | None
    format: str
    max_file_size_mb: int = Field(ge=1)
    backup_count: int = Field(ge=0)
```

### Command Configuration
```python
class CommandConfig(BaseModel):
    """Command system configuration."""
    
    prefix: str
    history_file: Path
```

### Path Configuration
```python
class PathConfig(BaseModel):
    """Base application paths."""
    
    data_dir: Path
    config_dir: Path
    cache_dir: Path
```

### TTS Configuration
```python
class TTSConfig(BaseModel):
    """Text-to-speech configuration."""
    
    enabled: bool
    voice: str
    model: str
    audio_dir: Path
```

### Web Search Configuration
```python
class WebSearchConfig(BaseModel):
    """Web search configuration."""
    
    enabled: bool
    default_engine: str
    content_threshold: int = Field(ge=1)
    max_results: int = Field(ge=1, le=10)
    timeout: int = Field(ge=1)
    engines: dict[str, str]
```

## Environment Variable Overrides

### Naming Convention
```
CATO_<SECTION>_<KEY>=value
CATO_<SECTION>_<SUBSECTION>_<KEY>=value
```

### Examples
```bash
# Override LLM model
CATO_LLM_MODEL="claude-3-opus"

# Override logging level
CATO_LOGGING_LEVEL="DEBUG"

# Provider API keys (used via ${OPENAI_API_KEY} etc. in config)
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."
GOOGLE_API_KEY="..."
```

### Implementation
```python
def apply_env_overrides(config: dict) -> dict:
    """
    Apply CATO_* environment variables as config overrides.
    
    Parameters
    ----------
    config
        Configuration dict to modify.
    
    Returns
    -------
    dict
        Configuration with env overrides applied.
    """
    prefix = "CATO_"
    for key, value in os.environ.items():
        if not key.startswith(prefix):
            continue
        
        # Parse key path: CATO_LLM_MODEL -> ["llm", "model"]
        parts = key[len(prefix):].lower().split("_")
        
        # Navigate to nested location and set value
        set_nested(config, parts, parse_env_value(value))
    
    return config
```

## CLI Argument Overrides
```python
@click.command()
@click.option("--config", type=Path, help="Path to config file")
@click.option("--model", help="Override LLM model")
@click.option("--debug", is_flag=True, help="Enable debug logging")
def main(config: Path | None, model: str | None, debug: bool) -> None:
    """Cato entry point."""
    cfg = load_config(config)
    
    # CLI overrides (highest precedence)
    if model:
        cfg.llm.model = model
    if debug:
        cfg.logging.level = "DEBUG"
```

## Validation Behaviour

All validation is handled by Pydantic. The config system uses Pydantic's features to enforce constraints and provide defaults.

### Pydantic Model Configuration
```python
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo

class CatoConfig(BaseModel):
    """Root configuration with validation."""
    
    model_config = ConfigDict(
        extra="ignore",          # Ignore unknown keys (warn separately)
        validate_default=True,   # Validate default values too
        str_strip_whitespace=True,
    )
    
    profile_name: str | None = None
    debug: bool = False
    llm: LLMConfig
    vector_store: VectorStoreConfig
    storage: StorageConfig
    display: DisplayConfig
    commands: CommandConfig
    logging: LoggingConfig
    paths: PathConfig
    tts: TTSConfig
    web_search: WebSearchConfig
    locations: dict[str, str] = Field(default_factory=dict)
```

### Field-Level Validation
Pydantic handles all value constraints:
```python
class LLMConfig(BaseModel):
    """LLM configuration with Pydantic validation."""
    
    provider: Literal["openai", "anthropic", "google", "ollama"]
    model: str = Field(min_length=1)  # Non-empty string
    temperature: float = Field(ge=0.0, le=2.0)
    max_tokens: int = Field(ge=1, le=200000)
    timeout_seconds: int = Field(ge=1, le=300)
```

### Cross-Field Validation
```python
class VectorStoreConfig(BaseModel):
    """Vector store config with cross-field validation."""
    
    enabled: bool
    chunk_size: int = Field(ge=100, le=10000)
    chunk_overlap: int = Field(ge=0)
    
    @field_validator("chunk_overlap")
    @classmethod
    def overlap_less_than_size(cls, v: int, info: ValidationInfo) -> int:
        """Ensure overlap is smaller than chunk size."""
        if "chunk_size" in info.data and v >= info.data["chunk_size"]:
            raise ValueError("chunk_overlap must be less than chunk_size")
        return v
```

### Unknown Keys Warning
```python
def load_config_with_warnings(data: dict) -> CatoConfig:
    """
    Load config, warning about unknown keys.
    
    Parameters
    ----------
    data
        Raw config dict.
    
    Returns
    -------
    CatoConfig
        Validated config (unknown keys ignored).
    """
    # Check for unknown keys before Pydantic ignores them
    warn_unknown_keys(data, CatoConfig)
    
    # Pydantic validates and ignores unknown keys
    return CatoConfig.model_validate(data)


def warn_unknown_keys(data: dict, model: type[BaseModel], path: str = "") -> None:
    """Recursively warn about unknown keys in config."""
    if not isinstance(data, dict):
        return
    
    model_fields = set(model.model_fields.keys())
    for key in data:
        full_path = f"{path}.{key}" if path else key
        if key not in model_fields:
            logger.warning(f"Unknown config key '{full_path}', ignoring")
        elif key in model_fields:
            field_type = model.model_fields[key].annotation
            # Recurse into nested models
            if hasattr(field_type, "model_fields"):
                warn_unknown_keys(data[key], field_type, full_path)
```

### Validation Error Handling
```python
def load_config(user_path: Path | None = None) -> CatoConfig:
    """
    Load and validate configuration.
    
    On validation error: log the error and exit (fail fast).
    Invalid config should not silently use defaults—user must fix it.
    """
    defaults = load_yaml(get_default_config_path())
    user_config = load_yaml(user_path) if user_path else {}
    merged = deep_merge(defaults, user_config)
    merged = apply_env_overrides(merged)
    
    try:
        return load_config_with_warnings(merged)
    except ValidationError as e:
        for error in e.errors():
            path = ".".join(str(loc) for loc in error["loc"])
            logger.error(f"Config error at '{path}': {error['msg']}")
        raise ConfigurationError("Invalid configuration. See errors above.")
```

### Default Values in Pydantic
Defaults come from the YAML file, not from Pydantic `Field(default=...)`. This keeps all defaults in one place:
```python
# GOOD: Defaults in YAML, Pydantic validates
class LLMConfig(BaseModel):
    temperature: float = Field(ge=0.0, le=2.0)  # No default here

# defaults.yaml provides the actual default:
# llm:
#   temperature: 1.0

# BAD: Defaults scattered in code
class LLMConfig(BaseModel):
    temperature: float = Field(default=1.0, ge=0.0, le=2.0)  # Don't do this
```

## Default Configuration File
```yaml
# defaults.yaml - Shipped with Cato, do not modify

profile_name: null
debug: false

llm:
  provider: "openai"
  model: "gpt-4o-mini"
  temperature: 1.0
  max_tokens: 4000
  timeout_seconds: 60
  system_prompt_files: []
  base_prompt_file: null
  override_base_prompt: false

  # Provider-specific settings
  openai:
    api_key: "${OPENAI_API_KEY}"
    organization: null
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
  google:
    api_key: "${GOOGLE_API_KEY}"
  ollama:
    base_url: "http://localhost:11434"

vector_store:
  enabled: true
  backend: "chromadb"
  path: "~/.local/share/cato/vectordb"
  collection_name: "cato_memory"
  context_results: 5
  search_context_window: 3
  similarity_threshold: 0.65
  dynamic_threshold: true
  retrieval_strategy: "default"
  chat_window: -1
  embedding_provider: "openai"
  embedding_model: "text-embedding-3-small"
  embedding_dimensions: 1536
  chunking_strategy: "semantic"
  chunk_size: 1000
  chunk_overlap: 100
  max_chunk_size: 1500
  preserve_sentence_boundaries: true

storage:
  database_path: "~/.local/share/cato/cato.db"
  backup_enabled: true
  backup_frequency_hours: 24

display:
  theme: "default"
  markdown_enabled: true
  code_theme: "monokai"
  max_width: null
  timestamps: false
  spinner_style: "dots"
  prompt_symbol: "🐱 > "
  line_width: 80
  exchange_delimiter: "─"
  exchange_delimiter_length: 60
  style_overrides: {}
  prompt_style: null
  input_style: null

commands:
  prefix: "/"
  history_file: "~/.local/share/cato/command_history"

logging:
  level: "WARNING"
  file_path: "~/.local/share/cato/cato.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  max_file_size_mb: 10
  backup_count: 3

paths:
  data_dir: "~/.local/share/cato"
  config_dir: "~/.config/cato"
  cache_dir: "~/.cache/cato"

tts:
  enabled: true
  voice: "nova"
  model: "tts-1"
  audio_dir: "/tmp"

web_search:
  enabled: true
  default_engine: "duckduckgo"
  content_threshold: 500
  max_results: 3
  timeout: 10
  engines:
    duckduckgo: "https://duckduckgo.com/html/?q={query}"
    google: "https://www.google.com/search?q={query}"
    bing: "https://www.bing.com/search?q={query}"

locations: {}
```

## User Configuration Example
```yaml
# ~/.config/cato/config.yaml
# Only specify values that differ from defaults

llm:
  model: "gpt-4-turbo"
  temperature: 0.7

display:
  theme: "gruvbox-dark"
  timestamps: true

logging:
  level: "DEBUG"
```

## Runtime Configuration Access
```python
# Configuration is loaded once at startup and passed via dependency injection
class ChatService:
    def __init__(self, config: CatoConfig, llm: LLMProvider) -> None:
        self._config = config
        self._llm = llm
    
    async def send_message(self, message: str) -> str:
        return await self._llm.complete(
            message,
            temperature=self._config.llm.temperature,
            max_tokens=self._config.llm.max_tokens,
        )
```

## Path Expansion
All paths in configuration support:
- `~` for home directory
- Environment variables via `${VAR}`

```python
def expand_path(path: str | Path) -> Path:
    """Expand ~ and environment variables in path."""
    return Path(os.path.expandvars(os.path.expanduser(str(path))))
```

```

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_LLM_INTEGRATION.md**
```
# LLM Integration Technical Specification

## Overview
Cato supports multiple LLM providers through a unified protocol-based abstraction. Providers are interchangeable at runtime via configuration.

## Provider Protocol

### Interface Definition
```python
from typing import Protocol, AsyncIterator
from pydantic import BaseModel

class Message(BaseModel):
    """Normalised message format."""
    role: Literal["system", "user", "assistant"]
    content: str

class TokenUsage(BaseModel):
    """Token usage statistics."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class CompletionResult(BaseModel):
    """Result from LLM completion."""
    content: str
    model: str
    usage: TokenUsage | None = None
    finish_reason: str | None = None


class LLMProvider(Protocol):
    """
    Protocol for LLM provider implementations.
    
    Any class implementing these methods can be used as a provider.
    """
    
    @property
    def name(self) -> str:
        """Provider identifier (e.g., 'openai', 'anthropic')."""
        ...
    
    @property
    def model(self) -> str:
        """Currently configured model."""
        ...
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        """
        Generate a completion for the given messages.
        
        Parameters
        ----------
        messages
            Conversation history in normalised format.
        temperature
            Override configured temperature.
        max_tokens
            Override configured max tokens.
        
        Returns
        -------
        CompletionResult
            The model's response with metadata.
        
        Raises
        ------
        LLMConnectionError
            Cannot reach the provider.
        LLMAuthenticationError
            Invalid API key.
        LLMRateLimitError
            Rate limit exceeded.
        LLMContextLengthError
            Input exceeds context window.
        """
        ...
    
    async def complete_stream(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream completion tokens as they arrive.
        
        Yields
        ------
        str
            Individual tokens or token chunks.
        """
        ...
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text for this provider's tokenizer.
        
        Parameters
        ----------
        text
            Text to tokenize.
        
        Returns
        -------
        int
            Token count.
        """
        ...
```

## Provider Implementations

### OpenAI Provider
```python
class OpenAIProvider:
    """OpenAI API provider implementation."""
    
    def __init__(self, config: OpenAIConfig) -> None:
        self._config = config
        self._client = AsyncOpenAI(api_key=config.api_key)
        self._model = config.model
    
    @property
    def name(self) -> str:
        return "openai"
    
    @property
    def model(self) -> str:
        return self._model
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[self._to_openai_message(m) for m in messages],
                temperature=temperature or self._config.temperature,
                max_tokens=max_tokens or self._config.max_tokens,
            )
            return self._to_result(response)
        except openai.AuthenticationError as e:
            raise LLMAuthenticationError(str(e))
        except openai.RateLimitError as e:
            raise LLMRateLimitError(str(e), retry_after=self._parse_retry(e))
        except openai.APIConnectionError as e:
            raise LLMConnectionError(str(e))
    
    def _to_openai_message(self, msg: Message) -> dict:
        return {"role": msg.role, "content": msg.content}
    
    def _to_result(self, response) -> CompletionResult:
        choice = response.choices[0]
        return CompletionResult(
            content=choice.message.content,
            model=response.model,
            usage=TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            finish_reason=choice.finish_reason,
        )
```

### Anthropic Provider
```python
class AnthropicProvider:
    """Anthropic Claude API provider implementation."""
    
    def __init__(self, config: AnthropicConfig) -> None:
        self._config = config
        self._client = AsyncAnthropic(api_key=config.api_key)
        self._model = config.model
    
    @property
    def name(self) -> str:
        return "anthropic"
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        # Extract system message (Anthropic handles it separately)
        system_msg = None
        chat_messages = []
        for msg in messages:
            if msg.role == "system":
                system_msg = msg.content
            else:
                chat_messages.append({"role": msg.role, "content": msg.content})
        
        try:
            response = await self._client.messages.create(
                model=self._model,
                system=system_msg,
                messages=chat_messages,
                temperature=temperature or self._config.temperature,
                max_tokens=max_tokens or self._config.max_tokens,
            )
            return self._to_result(response)
        except anthropic.AuthenticationError as e:
            raise LLMAuthenticationError(str(e))
        except anthropic.RateLimitError as e:
            raise LLMRateLimitError(str(e))
```

### Google Provider
```python
class GoogleProvider:
    """Google Gemini API provider implementation."""
    
    def __init__(self, config: GoogleConfig) -> None:
        self._config = config
        genai.configure(api_key=config.api_key)
        self._model = genai.GenerativeModel(config.model)
    
    @property
    def name(self) -> str:
        return "google"
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        # Convert to Gemini format
        history = self._build_history(messages[:-1])
        chat = self._model.start_chat(history=history)
        
        response = await chat.send_message_async(
            messages[-1].content,
            generation_config=genai.GenerationConfig(
                temperature=temperature or self._config.temperature,
                max_output_tokens=max_tokens or self._config.max_tokens,
            ),
        )
        return CompletionResult(
            content=response.text,
            model=self._config.model,
        )
```

### Ollama Provider
```python
class OllamaProvider:
    """Ollama local model provider implementation."""
    
    def __init__(self, config: OllamaConfig) -> None:
        self._config = config
        self._base_url = config.base_url or "http://localhost:11434"
        self._model = config.model
    
    @property
    def name(self) -> str:
        return "ollama"
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/api/chat",
                json={
                    "model": self._model,
                    "messages": [{"role": m.role, "content": m.content} for m in messages],
                    "options": {
                        "temperature": temperature or self._config.temperature,
                        "num_predict": max_tokens or self._config.max_tokens,
                    },
                    "stream": False,
                },
                timeout=self._config.timeout_seconds,
            )
            response.raise_for_status()
            data = response.json()
            return CompletionResult(
                content=data["message"]["content"],
                model=self._model,
            )
```

## Provider Factory

### Registration and Creation
```python
from typing import Callable

# Provider registry: maps name to factory function
_PROVIDERS: dict[str, Callable[[CatoConfig], LLMProvider]] = {}


def register_provider(name: str) -> Callable:
    """
    Decorator to register a provider factory.
    
    Parameters
    ----------
    name
        Provider identifier (must match config value).
    """
    def decorator(factory: Callable[[CatoConfig], LLMProvider]) -> Callable:
        _PROVIDERS[name] = factory
        return factory
    return decorator


@register_provider("openai")
def create_openai(config: CatoConfig) -> LLMProvider:
    return OpenAIProvider(config.llm.openai)


@register_provider("anthropic")
def create_anthropic(config: CatoConfig) -> LLMProvider:
    return AnthropicProvider(config.llm.anthropic)


@register_provider("google")
def create_google(config: CatoConfig) -> LLMProvider:
    return GoogleProvider(config.llm.google)


@register_provider("ollama")
def create_ollama(config: CatoConfig) -> LLMProvider:
    return OllamaProvider(config.llm.ollama)


def create_provider(config: CatoConfig) -> LLMProvider:
    """
    Create the configured LLM provider.
    
    Parameters
    ----------
    config
        Application configuration.
    
    Returns
    -------
    LLMProvider
        Configured provider instance.
    
    Raises
    ------
    ConfigurationError
        Unknown provider name.
    """
    provider_name = config.llm.provider
    if provider_name not in _PROVIDERS:
        raise ConfigurationError(
            f"Unknown LLM provider: {provider_name}",
            context={"available": list(_PROVIDERS.keys())},
        )
    return _PROVIDERS[provider_name](config)
```

## Message Normalisation

### Conversation History
```python
from dataclasses import dataclass, field

@dataclass
class Conversation:
    """
    Manages conversation state and history.
    
    Note: Uses dataclass rather than Pydantic as it's mutable internal state,
    not data crossing system boundaries.
    """
    
    system_prompt: str
    messages: list[Message] = field(default_factory=list)
    
    def add_user_message(self, content: str) -> None:
        """Add a user message to history."""
        self.messages.append(Message(role="user", content=content))
    
    def add_assistant_message(self, content: str) -> None:
        """Add an assistant response to history."""
        self.messages.append(Message(role="assistant", content=content))
    
    def to_messages(self) -> list[Message]:
        """
        Get full message list for LLM request.
        
        Returns
        -------
        list[Message]
            System prompt followed by conversation history.
        """
        return [Message(role="system", content=self.system_prompt)] + self.messages
    
    def truncate_to_tokens(self, max_tokens: int, counter: Callable[[str], int]) -> None:
        """
        Truncate history to fit within token limit.
        
        Removes oldest messages (after system prompt) until within limit.
        Always keeps system prompt and most recent exchange.
        
        Parameters
        ----------
        max_tokens
            Maximum allowed tokens.
        counter
            Function to count tokens in text.
        """
        while self._count_tokens(counter) > max_tokens and len(self.messages) > 2:
            self.messages.pop(0)  # Remove oldest message
    
    def _count_tokens(self, counter: Callable[[str], int]) -> int:
        total = counter(self.system_prompt)
        for msg in self.messages:
            total += counter(msg.content)
        return total
```

## Error Handling

### Provider-Specific to Generic Mapping
Each provider implementation maps its specific exceptions to the generic hierarchy:

```python
# Exception mapping pattern
OPENAI_EXCEPTION_MAP = {
    openai.AuthenticationError: LLMAuthenticationError,
    openai.RateLimitError: LLMRateLimitError,
    openai.APIConnectionError: LLMConnectionError,
    openai.BadRequestError: LLMContextLengthError,  # Often context length
}

def map_exception(e: Exception, mapping: dict) -> CatoError:
    """Map provider exception to Cato exception."""
    for provider_exc, cato_exc in mapping.items():
        if isinstance(e, provider_exc):
            return cato_exc(str(e))
    return LLMError(str(e))
```

### Retry Logic
```python
async def complete_with_retry(
    provider: LLMProvider,
    messages: list[Message],
    max_retries: int = 3,
) -> CompletionResult:
    """
    Complete with automatic retry on transient failures.
    
    Parameters
    ----------
    provider
        LLM provider to use.
    messages
        Messages to send.
    max_retries
        Maximum retry attempts.
    
    Returns
    -------
    CompletionResult
        Successful completion result.
    
    Raises
    ------
    LLMError
        After all retries exhausted.
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            return await provider.complete(messages)
        except LLMRateLimitError as e:
            last_error = e
            if e.retry_after:
                await asyncio.sleep(e.retry_after)
            else:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        except LLMConnectionError as e:
            last_error = e
            await asyncio.sleep(2 ** attempt)
    
    raise last_error or LLMError("Max retries exceeded")
```

## Configuration

### Provider-Specific Config
```yaml
llm:
  provider: "openai"  # Which provider to use
  model: "gpt-4o-mini"
  temperature: 1.0
  max_tokens: 4000
  timeout_seconds: 60
  
  # Provider-specific settings (only relevant one is used)
  openai:
    api_key: "${OPENAI_API_KEY}"
    organization: null
    
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    
  google:
    api_key: "${GOOGLE_API_KEY}"
    
  ollama:
    base_url: "http://localhost:11434"
```

## Adding New Providers

To add a new provider:

1. Create `cato/providers/<name>.py`
2. Implement the `LLMProvider` protocol
3. Register with `@register_provider("<name>")`
4. Add config model to `cato/core/config.py`
5. Add to config schema validation

```python
# cato/providers/newprovider.py
from cato.providers.base import LLMProvider, register_provider

@register_provider("newprovider")
def create_newprovider(config: CatoConfig) -> LLMProvider:
    return NewProvider(config.llm.newprovider)

class NewProvider:
    """New provider implementation."""
    
    def __init__(self, config: NewProviderConfig) -> None:
        # Setup
        pass
    
    # Implement protocol methods...
```

```

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_STORAGE.md**
```
# Storage Technical Specification

## Overview
Cato uses SQLite for structured data storage (tasks, lists). The database provides persistent storage for productivity features with a simple data access layer.

## Database Location
```
~/.local/share/cato/cato.db
```

Configurable via `storage.database_path` in config.

## Schema

### Tasks Table
```sql
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'active',  -- active, in_progress, completed, deleted
    priority TEXT DEFAULT 'medium',          -- low, medium, high, urgent
    category TEXT,
    due_date TEXT,                           -- ISO 8601 format
    created_at TEXT NOT NULL,                -- ISO 8601 format
    updated_at TEXT NOT NULL,                -- ISO 8601 format
    completed_at TEXT,                       -- ISO 8601 format
    metadata TEXT                            -- JSON for extensibility
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
```

### Lists Table
```sql
CREATE TABLE IF NOT EXISTS lists (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS list_items (
    id TEXT PRIMARY KEY,
    list_id TEXT NOT NULL,
    content TEXT NOT NULL,
    checked INTEGER NOT NULL DEFAULT 0,
    position INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metadata TEXT,
    FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_list_items_list_id ON list_items(list_id);
```


### Sessions Table
```sql
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    message_count INTEGER DEFAULT 0,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS threads (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    name TEXT,
    created_at TEXT NOT NULL,
    metadata TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);
```

## Data Access Layer

### Repository Protocol
```python
from typing import Protocol, TypeVar, Generic

T = TypeVar("T")

class Repository(Protocol[T]):
    """Generic repository protocol for CRUD operations."""
    
    async def get(self, id: str) -> T | None:
        """Get entity by ID."""
        ...
    
    async def get_all(self, **filters) -> list[T]:
        """Get all entities, optionally filtered."""
        ...
    
    async def create(self, entity: T) -> str:
        """Create entity, return ID."""
        ...
    
    async def update(self, entity: T) -> None:
        """Update existing entity."""
        ...
    
    async def delete(self, id: str) -> None:
        """Delete entity by ID."""
        ...
```

### Task Repository
```python
from pydantic import BaseModel

class Task(BaseModel):
    """
    Task entity.
    
    Uses Pydantic for validation as data crosses SQLite boundary.
    """
    id: str
    title: str
    description: str | None
    status: Literal["active", "in_progress", "completed", "deleted"]
    priority: Literal["low", "medium", "high", "urgent"]
    category: str | None
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
    metadata: dict


class TaskRepository:
    """SQLite-backed task repository."""
    
    def __init__(self, db: Database) -> None:
        self._db = db
    
    async def get(self, id: str) -> Task | None:
        """
        Get task by ID.
        
        Parameters
        ----------
        id
            Task ID.
        
        Returns
        -------
        Task | None
            Task if found.
        """
        row = await self._db.fetchone(
            "SELECT * FROM tasks WHERE id = ?",
            (id,),
        )
        return self._row_to_task(row) if row else None
    
    async def get_all(
        self,
        status: str | None = None,
        category: str | None = None,
        priority: str | None = None,
        sort_by: str = "created_at",
        order: str = "asc",
    ) -> list[Task]:
        """
        Get tasks with optional filters.
        
        Parameters
        ----------
        status
            Filter by status.
        category
            Filter by category.
        priority
            Filter by priority.
        sort_by
            Sort field.
        order
            Sort order (asc/desc).
        
        Returns
        -------
        list[Task]
            Matching tasks.
        """
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        if category:
            query += " AND category = ?"
            params.append(category)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        
        # Validate sort field to prevent SQL injection
        valid_sorts = {"created_at", "updated_at", "priority", "due_date", "title"}
        if sort_by not in valid_sorts:
            sort_by = "created_at"
        
        order = "DESC" if order.lower() == "desc" else "ASC"
        query += f" ORDER BY {sort_by} {order}"
        
        rows = await self._db.fetchall(query, tuple(params))
        return [self._row_to_task(row) for row in rows]
    
    async def create(self, task: Task) -> str:
        """Create new task."""
        await self._db.execute(
            """
            INSERT INTO tasks (
                id, title, description, status, priority, category,
                due_date, created_at, updated_at, completed_at, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task.id,
                task.title,
                task.description,
                task.status,
                task.priority,
                task.category,
                task.due_date.isoformat() if task.due_date else None,
                task.created_at.isoformat(),
                task.updated_at.isoformat(),
                task.completed_at.isoformat() if task.completed_at else None,
                json.dumps(task.metadata) if task.metadata else None,
            ),
        )
        return task.id
    
    async def update(self, task: Task) -> None:
        """Update existing task."""
        task.updated_at = datetime.now()
        await self._db.execute(
            """
            UPDATE tasks SET
                title = ?, description = ?, status = ?, priority = ?,
                category = ?, due_date = ?, updated_at = ?,
                completed_at = ?, metadata = ?
            WHERE id = ?
            """,
            (
                task.title,
                task.description,
                task.status,
                task.priority,
                task.category,
                task.due_date.isoformat() if task.due_date else None,
                task.updated_at.isoformat(),
                task.completed_at.isoformat() if task.completed_at else None,
                json.dumps(task.metadata) if task.metadata else None,
                task.id,
            ),
        )
    
    async def delete(self, id: str) -> None:
        """Delete task by ID."""
        await self._db.execute("DELETE FROM tasks WHERE id = ?", (id,))
    
    def _row_to_task(self, row: dict) -> Task:
        """Convert database row to Task entity."""
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=row["status"],
            priority=row["priority"],
            category=row["category"],
            due_date=datetime.fromisoformat(row["due_date"]) if row["due_date"] else None,
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
        )
```

### Database Connection
```python
import aiosqlite
from pathlib import Path

class Database:
    """Async SQLite database wrapper."""
    
    def __init__(self, path: Path) -> None:
        self._path = path
        self._conn: aiosqlite.Connection | None = None
    
    async def connect(self) -> None:
        """Open database connection and initialise schema."""
        # Ensure directory exists
        self._path.parent.mkdir(parents=True, exist_ok=True)
        
        self._conn = await aiosqlite.connect(self._path)
        self._conn.row_factory = aiosqlite.Row
        
        # Enable foreign keys
        await self._conn.execute("PRAGMA foreign_keys = ON")
        
        # Run migrations
        await self._run_migrations()
    
    async def close(self) -> None:
        """Close database connection."""
        if self._conn:
            await self._conn.close()
            self._conn = None
    
    async def execute(self, query: str, params: tuple = ()) -> None:
        """Execute a write query."""
        async with self._conn.execute(query, params):
            await self._conn.commit()
    
    async def fetchone(self, query: str, params: tuple = ()) -> dict | None:
        """Fetch single row."""
        async with self._conn.execute(query, params) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def fetchall(self, query: str, params: tuple = ()) -> list[dict]:
        """Fetch all rows."""
        async with self._conn.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def _run_migrations(self) -> None:
        """Apply database migrations."""
        # Create migrations table if not exists
        await self._conn.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                applied_at TEXT NOT NULL
            )
        """)
        await self._conn.commit()
        
        # Get applied migrations
        cursor = await self._conn.execute("SELECT name FROM migrations")
        applied = {row[0] for row in await cursor.fetchall()}
        
        # Apply pending migrations
        for migration in MIGRATIONS:
            if migration.name not in applied:
                await migration.apply(self._conn)
                await self._conn.execute(
                    "INSERT INTO migrations (name, applied_at) VALUES (?, ?)",
                    (migration.name, datetime.now().isoformat()),
                )
                await self._conn.commit()
                logger.info(f"Applied migration: {migration.name}")
```

## Migrations

### Migration Definition
```python
from dataclasses import dataclass

@dataclass
class Migration:
    """
    Database migration.
    
    Note: Uses dataclass as it's internal configuration, not external data.
    """
    name: str
    sql: str
    
    async def apply(self, conn: aiosqlite.Connection) -> None:
        """Apply migration."""
        await conn.executescript(self.sql)


# Ordered list of migrations
MIGRATIONS = [
    Migration(
        name="001_initial_schema",
        sql="""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            priority TEXT DEFAULT 'medium',
            category TEXT,
            due_date TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            completed_at TEXT,
            metadata TEXT
        );
        
        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
        
        CREATE TABLE IF NOT EXISTS lists (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            metadata TEXT
        );
        
        CREATE TABLE IF NOT EXISTS list_items (
            id TEXT PRIMARY KEY,
            list_id TEXT NOT NULL,
            content TEXT NOT NULL,
            checked INTEGER NOT NULL DEFAULT 0,
            position INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            metadata TEXT,
            FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE
        );
        
        CREATE INDEX IF NOT EXISTS idx_list_items_list_id ON list_items(list_id);
        """,
    ),
    Migration(
        name="002_sessions",
        sql="""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            message_count INTEGER DEFAULT 0,
            metadata TEXT
        );
        
        CREATE TABLE IF NOT EXISTS threads (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            name TEXT,
            created_at TEXT NOT NULL,
            metadata TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
        );
        """,
    ),
]
```

## Storage Service

### Unified Access
```python
class Storage:
    """
    Unified storage service.
    
    Provides access to all repositories through a single interface.
    """
    
    def __init__(self, db: Database) -> None:
        self._db = db
        self.tasks = TaskRepository(db)
        self.lists = ListRepository(db)
        self.sessions = SessionRepository(db)
    
    async def connect(self) -> None:
        """Connect to database."""
        await self._db.connect()
    
    async def close(self) -> None:
        """Close database connection."""
        await self._db.close()


# Usage in bootstrap
async def create_storage(config: CatoConfig) -> Storage:
    """
    Create and connect storage service.
    
    Parameters
    ----------
    config
        Application configuration.
    
    Returns
    -------
    Storage
        Connected storage service.
    """
    db = Database(expand_path(config.storage.database_path))
    storage = Storage(db)
    await storage.connect()
    return storage
```

## Backup

### Automatic Backup
```python
import shutil
from datetime import datetime

class BackupManager:
    """Manage database backups."""
    
    def __init__(self, config: StorageConfig) -> None:
        self._config = config
        self._db_path = expand_path(config.database_path)
        self._backup_dir = self._db_path.parent / "backups"
    
    async def create_backup(self) -> Path:
        """
        Create database backup.
        
        Returns
        -------
        Path
            Path to backup file.
        """
        self._backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self._backup_dir / f"cato_{timestamp}.db"
        
        # Copy database file
        shutil.copy2(self._db_path, backup_path)
        
        # Clean old backups (keep last 7)
        self._cleanup_old_backups(keep=7)
        
        logger.info(f"Database backed up to: {backup_path}")
        return backup_path
    
    def _cleanup_old_backups(self, keep: int) -> None:
        """Remove old backups, keeping the most recent."""
        backups = sorted(
            self._backup_dir.glob("cato_*.db"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        
        for backup in backups[keep:]:
            backup.unlink()
            logger.debug(f"Removed old backup: {backup}")
```

## Configuration

### Storage Config
```yaml
storage:
  database_path: "~/.local/share/cato/cato.db"
  backup_enabled: true
  backup_frequency_hours: 24
```

## ID Generation
```python
import uuid
from datetime import datetime

def generate_id(prefix: str = "") -> str:
    """
    Generate unique ID.
    
    Parameters
    ----------
    prefix
        Optional prefix for ID.
    
    Returns
    -------
    str
        Unique ID string.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique = uuid.uuid4().hex[:8]
    
    if prefix:
        return f"{prefix}_{timestamp}_{unique}"
    return f"{timestamp}_{unique}"
```

```

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_VECTOR_STORE.md**
```
# Vector Store Technical Specification

## Overview
Cato uses ChromaDB for persistent vector storage, enabling semantic search over conversation history and documents. The vector store is query-only at runtime—never load the full store into memory.

## Vector Store Protocol

### Interface Definition
```python
from typing import Protocol
from pydantic import BaseModel, ConfigDict

class VectorDocument(BaseModel):
    """
    Document stored in vector store.
    
    Uses Pydantic for validation as data crosses ChromaDB boundary.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: str
    content: str
    metadata: dict
    embedding: list[float] | None = None  # May not always be returned


class SearchResult(BaseModel):
    """Result from similarity search."""
    document: VectorDocument
    score: float  # Distance/similarity score


class VectorStore(Protocol):
    """
    Protocol for vector store implementations.
    
    All operations are async to support potential remote backends.
    """
    
    async def add(
        self,
        documents: list[VectorDocument],
    ) -> list[str]:
        """
        Add documents to the store.
        
        Parameters
        ----------
        documents
            Documents to add (embeddings generated if not provided).
        
        Returns
        -------
        list[str]
            IDs of added documents.
        """
        ...
    
    async def search(
        self,
        query: str,
        n_results: int = 5,
        filter: dict | None = None,
    ) -> list[SearchResult]:
        """
        Search for similar documents.
        
        Parameters
        ----------
        query
            Search query (will be embedded).
        n_results
            Maximum results to return.
        filter
            Metadata filter (ChromaDB where clause).
        
        Returns
        -------
        list[SearchResult]
            Matching documents with scores.
        """
        ...
    
    async def get(
        self,
        ids: list[str],
    ) -> list[VectorDocument]:
        """
        Retrieve documents by ID.
        
        Parameters
        ----------
        ids
            Document IDs to retrieve.
        
        Returns
        -------
        list[VectorDocument]
            Retrieved documents.
        """
        ...
    
    async def delete(
        self,
        ids: list[str],
    ) -> None:
        """
        Delete documents by ID.
        
        Parameters
        ----------
        ids
            Document IDs to delete.
        """
        ...
    
    async def count(self) -> int:
        """Return total document count."""
        ...
```

## ChromaDB Implementation

### Setup and Initialisation
```python
import chromadb
from chromadb.config import Settings

class ChromaVectorStore:
    """ChromaDB-backed vector store implementation."""
    
    def __init__(
        self,
        config: VectorStoreConfig,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        self._config = config
        self._embedder = embedding_provider
        
        # Persistent client (disk-backed)
        self._client = chromadb.PersistentClient(
            path=str(config.path),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=False,
            ),
        )
        
        # Get or create collection
        self._collection = self._client.get_or_create_collection(
            name=config.collection_name,
            metadata={"hnsw:space": "cosine"},  # Cosine similarity
        )
    
    async def add(self, documents: list[VectorDocument]) -> list[str]:
        """Add documents with embeddings."""
        # Generate embeddings for documents without them
        texts_to_embed = [
            (i, doc.content)
            for i, doc in enumerate(documents)
            if doc.embedding is None
        ]
        
        if texts_to_embed:
            embeddings = await self._embedder.embed_batch(
                [t[1] for t in texts_to_embed]
            )
            for (i, _), embedding in zip(texts_to_embed, embeddings):
                documents[i].embedding = embedding
        
        # Add to ChromaDB
        self._collection.add(
            ids=[doc.id for doc in documents],
            embeddings=[doc.embedding for doc in documents],
            documents=[doc.content for doc in documents],
            metadatas=[doc.metadata for doc in documents],
        )
        
        return [doc.id for doc in documents]
    
    async def search(
        self,
        query: str,
        n_results: int = 5,
        filter: dict | None = None,
    ) -> list[SearchResult]:
        """Search by semantic similarity."""
        # Embed query
        query_embedding = await self._embedder.embed(query)
        
        # Query ChromaDB
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter,
            include=["documents", "metadatas", "distances"],
        )
        
        # Convert to SearchResult
        search_results = []
        for i in range(len(results["ids"][0])):
            doc = VectorDocument(
                id=results["ids"][0][i],
                content=results["documents"][0][i],
                metadata=results["metadatas"][0][i],
            )
            search_results.append(SearchResult(
                document=doc,
                score=results["distances"][0][i],
            ))
        
        return search_results
```

## Embedding Provider

### Protocol
```python
from typing import Protocol

class EmbeddingProvider(Protocol):
    """Protocol for embedding providers."""

    async def embed(self, text: str) -> list[float]:
        """Generate embedding for single text."""
        ...

    async def embed_batch(
        self,
        texts: list[str],
        batch_size: int = 100,
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        ...
```

### OpenAI Embeddings
```python
class OpenAIEmbeddingProvider:
    """OpenAI API embeddings."""
    
    def __init__(self, config: EmbeddingConfig) -> None:
        self._client = AsyncOpenAI(api_key=config.api_key)
        self._model = config.model  # e.g., "text-embedding-3-small"
    
    async def embed(self, text: str) -> list[float]:
        """
        Generate embedding for single text.
        
        Parameters
        ----------
        text
            Text to embed.
        
        Returns
        -------
        list[float]
            Embedding vector.
        """
        response = await self._client.embeddings.create(
            model=self._model,
            input=text,
        )
        return response.data[0].embedding
    
    async def embed_batch(
        self,
        texts: list[str],
        batch_size: int = 100,
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        
        Parameters
        ----------
        texts
            Texts to embed.
        batch_size
            Max texts per API call.
        
        Returns
        -------
        list[list[float]]
            Embedding vectors in same order.
        """
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = await self._client.embeddings.create(
                model=self._model,
                input=batch,
            )
            embeddings.extend([d.embedding for d in response.data])
        
        return embeddings
```

### Ollama Embeddings
```python
class OllamaEmbeddingProvider:
    """Ollama local embeddings."""

    def __init__(self, config: EmbeddingConfig) -> None:
        self._base_url = config.base_url or "http://localhost:11434"
        self._model = config.model

    async def embed(self, text: str) -> list[float]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/api/embeddings",
                json={"model": self._model, "prompt": text},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()["embedding"]
```

## Document Chunking

### Text Splitter
```python
class TextChunker:
    """
    Split documents into chunks for embedding.
    
    Uses recursive character splitting with overlap.
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        separators: list[str] | None = None,
    ) -> None:
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._separators = separators or ["\n\n", "\n", ". ", " ", ""]
    
    def split(self, text: str) -> list[str]:
        """
        Split text into chunks.
        
        Parameters
        ----------
        text
            Text to split.
        
        Returns
        -------
        list[str]
            Text chunks with overlap.
        """
        return self._split_recursive(text, self._separators)
    
    def _split_recursive(
        self,
        text: str,
        separators: list[str],
    ) -> list[str]:
        """Recursively split using separators in order."""
        if not text:
            return []
        
        # If text fits in chunk, return it
        if len(text) <= self._chunk_size:
            return [text]
        
        # Find separator to use
        separator = separators[-1]  # Default to last (empty string)
        for sep in separators:
            if sep in text:
                separator = sep
                break
        
        # Split and merge
        splits = text.split(separator) if separator else list(text)
        return self._merge_splits(splits, separator, separators)
    
    def _merge_splits(
        self,
        splits: list[str],
        separator: str,
        separators: list[str],
    ) -> list[str]:
        """Merge splits into chunks with overlap."""
        chunks = []
        current_chunk = []
        current_length = 0
        
        for split in splits:
            split_length = len(split) + len(separator)
            
            if current_length + split_length > self._chunk_size and current_chunk:
                # Save current chunk
                chunk_text = separator.join(current_chunk)
                chunks.append(chunk_text)
                
                # Start new chunk with overlap
                overlap_length = 0
                while current_chunk and overlap_length < self._chunk_overlap:
                    overlap_length += len(current_chunk[-1]) + len(separator)
                    if overlap_length > self._chunk_overlap:
                        current_chunk.pop(0)
                        break
                    current_chunk.pop(0)
                
                current_length = sum(len(s) for s in current_chunk) + len(separator) * len(current_chunk)
            
            current_chunk.append(split)
            current_length += split_length
        
        # Don't forget last chunk
        if current_chunk:
            chunks.append(separator.join(current_chunk))
        
        return chunks
```

### Document Processor
```python
class DocumentProcessor:
    """Process documents for vector storage."""
    
    def __init__(
        self,
        chunker: TextChunker,
        vector_store: VectorStore,
    ) -> None:
        self._chunker = chunker
        self._store = vector_store
    
    async def add_document(
        self,
        content: str,
        source: str,
        metadata: dict | None = None,
    ) -> list[str]:
        """
        Process and add a document to the vector store.
        
        Parameters
        ----------
        content
            Document content.
        source
            Source identifier (filename, URL, etc.).
        metadata
            Additional metadata.
        
        Returns
        -------
        list[str]
            IDs of created chunks.
        """
        # Split into chunks
        chunks = self._chunker.split(content)
        
        # Create documents
        base_metadata = metadata or {}
        base_metadata["source"] = source
        base_metadata["total_chunks"] = len(chunks)
        
        documents = [
            VectorDocument(
                id=f"{source}:{i}",
                content=chunk,
                metadata={
                    **base_metadata,
                    "chunk_index": i,
                },
            )
            for i, chunk in enumerate(chunks)
        ]
        
        # Add to store
        return await self._store.add(documents)
```

## Exchange Storage

### Conversation Exchange Format
```python
from pydantic import BaseModel

class Exchange(BaseModel):
    """
    A user/assistant exchange for storage.
    
    Uses Pydantic for validation as data crosses vector store boundary.
    """
    id: str
    session_id: str
    thread_id: str | None
    user_message: str
    assistant_message: str
    timestamp: datetime
    prior_exchange_ids: list[str]
    thread_session_id: str
    thread_continuation_seq: int
    metadata: dict


class ExchangeStore:
    """Store conversation exchanges in vector store."""
    
    def __init__(self, vector_store: VectorStore) -> None:
        self._store = vector_store
    
    async def add_exchange(self, exchange: Exchange) -> str:
        """
        Add a conversation exchange.
        
        Parameters
        ----------
        exchange
            Exchange to store.
        
        Returns
        -------
        str
            Exchange ID.
        """
        # Combine user and assistant messages for embedding
        combined_content = (
            f"User: {exchange.user_message}\n\n"
            f"Assistant: {exchange.assistant_message}"
        )
        
        doc = VectorDocument(
            id=exchange.id,
            content=combined_content,
            metadata={
                "type": "exchange",
                "session_id": exchange.session_id,
                "thread_id": exchange.thread_id or "",
                "timestamp": exchange.timestamp.isoformat(),
                "user_message": exchange.user_message[:500],  # Truncated for metadata
                **exchange.metadata,
            },
        )
        
        await self._store.add([doc])
        return exchange.id
    
    async def search_exchanges(
        self,
        query: str,
        n_results: int = 5,
        session_id: str | None = None,
        thread_id: str | None = None,
    ) -> list[SearchResult]:
        """
        Search exchanges by semantic similarity.
        
        Parameters
        ----------
        query
            Search query.
        n_results
            Max results.
        session_id
            Filter to specific session.
        thread_id
            Filter to specific thread.
        
        Returns
        -------
        list[SearchResult]
            Matching exchanges.
        """
        filter_clause = {"type": "exchange"}
        if session_id:
            filter_clause["session_id"] = session_id
        if thread_id:
            filter_clause["thread_id"] = thread_id
        
        return await self._store.search(
            query=query,
            n_results=n_results,
            filter=filter_clause,
        )
```

## Context Retrieval

### Automatic Context
```python
class ContextRetriever:
    """Retrieve relevant context for conversations."""
    
    def __init__(
        self,
        exchange_store: ExchangeStore,
        config: VectorStoreConfig,
    ) -> None:
        self._store = exchange_store
        self._config = config
    
    async def get_relevant_context(
        self,
        query: str,
        max_results: int = 3,
        max_tokens: int = 2000,
        token_counter: Callable[[str], int] | None = None,
    ) -> list[str]:
        """
        Retrieve context relevant to the query.
        
        Parameters
        ----------
        query
            User's message/query.
        max_results
            Maximum context items.
        max_tokens
            Maximum total tokens in context.
        token_counter
            Function to count tokens.
        
        Returns
        -------
        list[str]
            Relevant context excerpts.
        """
        results = await self._store.search_exchanges(
            query=query,
            n_results=max_results * 2,  # Get extra for filtering
        )
        
        context = []
        total_tokens = 0
        counter = token_counter or (lambda x: len(x) // 4)  # Rough estimate
        
        for result in results:
            content = result.document.content
            tokens = counter(content)
            
            if total_tokens + tokens > max_tokens:
                continue
            
            context.append(content)
            total_tokens += tokens
            
            if len(context) >= max_results:
                break
        
        return context
```

## Configuration

### Vector Store Config
```yaml
vector_store:
  enabled: true
  backend: "chromadb"
  path: "~/.local/share/cato/vectordb"
  collection_name: "cato_memory"

  # Retrieval settings
  context_results: 5
  search_context_window: 3
  similarity_threshold: 0.65
  dynamic_threshold: true
  retrieval_strategy: "default"

  # Embedding settings
  embedding_provider: "openai"
  embedding_model: "text-embedding-3-small"
  embedding_dimensions: 1536

  # Chunking settings
  chunking_strategy: "semantic"
  chunk_size: 1000
  chunk_overlap: 100
  max_chunk_size: 1500
  preserve_sentence_boundaries: true
```

## Initialisation

### Bootstrap Integration
```python
def create_embedding_provider(config: VectorStoreConfig) -> EmbeddingProvider:
    """Create embedding provider based on config."""
    if config.embedding_provider == "openai":
        return OpenAIEmbeddingProvider(
            EmbeddingConfig(
                api_key=os.environ.get("OPENAI_API_KEY"),
                model=config.embedding_model,
            )
        )
    if config.embedding_provider == "ollama":
        return OllamaEmbeddingProvider(
            EmbeddingConfig(
                model=config.embedding_model,
            )
        )
    raise ConfigurationError(f"Unknown embedding provider: {config.embedding_provider}")
def create_vector_store(config: CatoConfig) -> VectorStore | None:
    """
    Create vector store if enabled.
    
    Parameters
    ----------
    config
        Application configuration.
    
    Returns
    -------
    VectorStore | None
        Configured vector store or None if disabled.
    """
    if not config.vector_store.enabled:
        logger.info("Vector store disabled in configuration")
        return None
    
    try:
        embedding_provider = create_embedding_provider(config.vector_store)
        
        store = ChromaVectorStore(
            config=config.vector_store,
            embedding_provider=embedding_provider,
        )
        
        logger.info(
            f"Vector store initialised: {config.vector_store.path}, "
            f"collection={config.vector_store.collection_name}"
        )
        return store
        
    except Exception as e:
        logger.warning(f"Failed to initialise vector store: {e}")
        return None  # Continue without vector store
```

## Performance Considerations

### Memory Management
- **Never load full store**: Always use queries with limits
- **Batch embeddings**: Use batch API for multiple documents
- **Lazy loading**: Don't initialise until first use if startup time critical

### Query Optimisation
```python
# Use metadata filters to reduce search space
results = await store.search(
    query="python error handling",
    n_results=5,
    filter={
        "type": "exchange",
        "session_id": current_session,  # Limit to current session first
    },
)
```

### Caching
```python
from functools import lru_cache

class CachedEmbeddingProvider:
    """Embedding provider with caching for repeated queries."""
    
    def __init__(self, provider: EmbeddingProvider, max_cache: int = 1000) -> None:
        self._provider = provider
        self._cache: dict[str, list[float]] = {}
        self._max_cache = max_cache
    
    async def embed(self, text: str) -> list[float]:
        # Check cache
        cache_key = text[:500]  # Truncate for key
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Generate and cache
        embedding = await self._provider.embed(text)
        
        if len(self._cache) >= self._max_cache:
            # Simple eviction: remove oldest
            self._cache.pop(next(iter(self._cache)))
        
        self._cache[cache_key] = embedding
        return embedding
```

```

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md**
```
# Error Handling Technical Specification

## Philosophy
Errors should be visible, clear, and actionable. The application should almost diagnose itself.

## Exception Handling Patterns

### Atomic Exceptions
- Catch specific exceptions, not broad `Exception` or `BaseException`
- Each try/except block should handle one logical error scenario

```python
# GOOD - specific exception handling
try:
    config = load_yaml(path)
except FileNotFoundError:
    logger.warning(f"Config file not found at {path}, using defaults")
    config = default_config
except yaml.YAMLError as e:
    logger.error(f"Invalid YAML in config file: {e}")
    raise ConfigurationError(f"Cannot parse {path}: {e}")

# BAD - broad exception handling
try:
    config = load_yaml(path)
except Exception as e:
    logger.error(f"Config error: {e}")
```

### Exception vs Return Value
- Prefer raising exceptions for errors over returning error tuples/dicts
- Use custom exception classes for domain-specific errors
- Exceptions should carry enough context for debugging

## Custom Exception Hierarchy

### Base Exception
```python
class CatoError(Exception):
    """
    Base exception for all Cato errors.
    
    All custom exceptions inherit from this to enable catching
    any Cato-specific error with a single except clause when needed.
    
    Parameters
    ----------
    message
        Human-readable error description.
    context
        Optional dict of contextual data for debugging.
    """
    
    def __init__(self, message: str, context: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.context = context or {}
    
    def __str__(self) -> str:
        if self.context:
            ctx = ", ".join(f"{k}={v!r}" for k, v in self.context.items())
            return f"{self.message} ({ctx})"
        return self.message
```

### Complete Hierarchy
```python
# Configuration
class ConfigurationError(CatoError):
    """Configuration loading or validation error."""
    pass

class ConfigFileNotFoundError(ConfigurationError):
    """Required configuration file missing."""
    pass

class ConfigValidationError(ConfigurationError):
    """Configuration value failed validation."""
    pass

# LLM Provider
class LLMError(CatoError):
    """LLM provider or API error."""
    pass

class LLMConnectionError(LLMError):
    """Cannot connect to LLM provider."""
    pass

class LLMAuthenticationError(LLMError):
    """API key invalid or missing."""
    pass

class LLMRateLimitError(LLMError):
    """Rate limit exceeded."""
    
    def __init__(self, message: str, retry_after: int | None = None, **kwargs) -> None:
        super().__init__(message, **kwargs)
        self.retry_after = retry_after

class LLMContextLengthError(LLMError):
    """Input exceeds model context window."""
    pass

class LLMResponseError(LLMError):
    """Invalid or unexpected response from LLM."""
    pass

# Vector Store
class VectorStoreError(CatoError):
    """Vector store operation error."""
    pass

class VectorStoreConnectionError(VectorStoreError):
    """Cannot connect to vector store."""
    pass

class EmbeddingError(VectorStoreError):
    """Error generating embeddings."""
    pass

# Storage (SQLite)
class StorageError(CatoError):
    """Database storage error."""
    pass

class StorageConnectionError(StorageError):
    """Cannot connect to database."""
    pass

class StorageQueryError(StorageError):
    """Database query failed."""
    pass

# Commands
class CommandError(CatoError):
    """Command execution error."""
    pass

class CommandNotFoundError(CommandError):
    """Unknown command."""
    pass

class CommandArgumentError(CommandError):
    """Invalid command arguments."""
    pass

class CommandExecutionError(CommandError):
    """Command failed during execution."""
    pass

# Input/Output
class IOError(CatoError):
    """File or network I/O error."""
    pass

class FileAccessError(IOError):
    """Cannot read or write file."""
    pass

class NetworkError(IOError):
    """Network operation failed."""
    pass

# Display
class DisplayError(CatoError):
    """Display/rendering error."""
    pass
```

### Exception Location
All exceptions defined in `cato/core/exceptions.py` and imported where needed:
```python
from cato.core.exceptions import (
    CatoError,
    ConfigurationError,
    LLMError,
    LLMRateLimitError,
    # ... etc
)
```

## User-Facing Error Messages

### Format
- Clear, human-readable language
- Include what went wrong
- Include actionable guidance where possible
- Use emoji indicators for visual clarity

```python
# Error display format
"❌ Command error: File not found: /path/to/file.txt"
"⚠️ Warning: Unrecognised config key 'foo', ignoring"
"❌ API error: OpenAI rate limit exceeded. Try again in 60 seconds."
```

### Information Levels
- **User message**: What happened and what to do
- **Log message**: Technical details for debugging
- Don't expose stack traces to user unless in debug mode

## Configuration Error Handling

### Validation Behaviour
- Invalid YAML syntax: Log error, exit
- Missing config file: Use defaults, log info
- Unrecognised config key: Warn user, ignore key, continue
- Invalid value type: Log error, exit
- Value out of range: Log error, exit

### Example
```python
# On startup with invalid config value
"❌ Config error: 'temperature' must be 0.0-2.0, got 5.0. Fix the config and retry."
```

## Graceful Degradation

### Component Failures
When a non-critical component fails:
1. Log the error appropriately
2. Inform the user clearly
3. Continue with reduced functionality

```python
# Vector store unavailable
"⚠️ Vector store could not initialise: {error}. Continuing without memory features."

# TTS unavailable
"⚠️ TTS failed: {error}. Speech features disabled for this session."
```

### Network/API Failures
- Implement reasonable timeouts
- Provide clear feedback on timeout
- Allow retry where appropriate

## Logging System

### Logger Setup
```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(config: LoggingConfig) -> None:
    """
    Configure application-wide logging.
    
    Parameters
    ----------
    config
        Logging configuration from main config.
    """
    root_logger = logging.getLogger("cato")
    root_logger.setLevel(config.level)
    
    # Console handler (always present)
    console = logging.StreamHandler()
    console.setLevel(config.level)
    console.setFormatter(logging.Formatter(
        "%(levelname)s: %(message)s"
    ))
    root_logger.addHandler(console)
    
    # File handler (if configured)
    if config.file_path:
        file_handler = RotatingFileHandler(
            config.file_path,
            maxBytes=config.max_file_size_mb * 1024 * 1024,
            backupCount=config.backup_count,
        )
        file_handler.setLevel(logging.DEBUG)  # File gets everything
        file_handler.setFormatter(logging.Formatter(config.format))
        root_logger.addHandler(file_handler)
```

### Module Loggers
Each module creates its own logger:
```python
# In cato/providers/openai.py
import logging

logger = logging.getLogger(__name__)  # "cato.providers.openai"

class OpenAIProvider:
    async def complete(self, prompt: str) -> str:
        logger.debug(f"Sending completion request, prompt length: {len(prompt)}")
        try:
            response = await self._client.complete(prompt)
            logger.debug(f"Received response, length: {len(response)}")
            return response
        except RateLimitError as e:
            logger.warning(f"Rate limited, retry after: {e.retry_after}s")
            raise LLMRateLimitError(str(e), retry_after=e.retry_after)
```

### Log Levels

| Level | Use Case | Example |
|-------|----------|--------|
| DEBUG | Detailed diagnostic info | "Sending request to OpenAI, model=gpt-4" |
| INFO | Notable events | "Vector store initialised with 1,234 documents" |
| WARNING | Recoverable issues | "Config key 'foo' unrecognised, ignoring" |
| ERROR | Failures requiring attention | "Failed to connect to database" |

### Debug Mode
When `logging.level: DEBUG`:
- All layers emit detailed logs
- Request/response payloads logged (truncated)
- Timing information for operations
- Stack traces for all exceptions

```python
logger.debug(
    f"LLM request: provider={provider}, model={model}, "
    f"temperature={temp}, tokens={len(messages)}"
)
```

### Warn Mode
When `logging.level: WARNING`:
- Only issues affecting user experience
- Degraded functionality notifications
- Performance warnings

### Sensitive Data
Never log:
- API keys (even partial)
- User credentials
- Full conversation content (log lengths instead)

```python
# GOOD
logger.debug(f"API request with key ending in ...{api_key[-4:]}")
logger.debug(f"Processing message, length: {len(content)} chars")

# BAD
logger.debug(f"API key: {api_key}")
logger.debug(f"User message: {content}")
```

## Error Logging
- All errors must be logged
- Log level appropriate to severity
- Include context for debugging

```python
try:
    result = await provider.complete(prompt)
except LLMRateLimitError as e:
    logger.warning(
        f"Rate limit hit",
        extra={"provider": provider.name, "retry_after": e.retry_after}
    )
    raise
except LLMError as e:
    logger.error(
        f"LLM request failed: {e}",
        extra={"provider": provider.name, "model": model},
        exc_info=True  # Include stack trace
    )
    raise
```

## Never Silent Failures
- Never swallow exceptions without logging
- Never retry infinitely without user feedback
- Always inform user when something doesn't work as expected

```

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_PERFORMANCE.md**
```
# Performance Technical Specification

## Startup Performance

### Target
Cato should start effectively instantaneously. User should see the prompt within 1-2 seconds maximum.

### Requirements
- **No eager data loading**: Do not load vector store contents into memory at startup
- **Lazy initialisation**: Initialise components only when first needed where possible
- **Minimal imports**: Use lazy imports for heavy dependencies if necessary

### Prohibited Patterns
```python
# NEVER do this - loads entire vector store
class VectorStore:
    def __init__(self):
        self.all_embeddings = self.db.get_all()  # BAD

# Instead - query on demand
class VectorStore:
    def query(self, text: str, k: int):
        return self.db.query(text, k)  # GOOD
```

## Runtime Performance

### Database Interactions
- All database queries should be real-time
- No caching of database contents outside current conversation context
- Use appropriate indices for common query patterns

### Vector Store Queries
- Query performance should scale reasonably with store size
- Use efficient similarity search algorithms (cosine similarity via ChromaDB)
- Limit result sets appropriately (`context_results` config)

### Context Management
- Maintain only current conversation in memory
- Retrieved context from vector store is transient
- Clear context appropriately on `/clear`

## Response Generation

### Waiting Indicator
- Display spinner while waiting for LLM response
- Spinner style configurable via `display.spinner_style`
- Show cancellation hint (Ctrl+C)

### Timeout Handling
- API timeout configured via `llm.timeout_seconds` (default 60 seconds)
- Graceful cancellation on Ctrl+C
- Clear feedback on timeout

## Memory Management

### What to Keep in Memory
- Current conversation messages
- Active configuration
- Session metadata (IDs, state flags)

### What NOT to Keep in Memory
- Historical conversations
- Vector store contents
- Productivity database contents

## Async Operations
- Use async/await for I/O bound operations
- LLM API calls should be async
- File operations can be sync (typically fast enough)
- Vector store operations should not block UI

## Startup Sequence (Optimised)
1. Parse CLI arguments
2. Load and validate configuration
3. Initialise display (Rich console)
4. Display welcome message
5. **Lazy init**: Vector store connection (don't load data)
6. **Lazy init**: LLM backend
7. Enter REPL loop
8. First vector store query triggers any necessary index loading

```





**Documents Created:**

**Document 402d467f-1917-4ea2-9c88-5d4401a65665**
```
# Problem statement
Create a detailed implementation plan for adding an agent subsystem to Cato that aligns with the specs: Cato remains a chat/productivity client (not a general agent), while enabling a dedicated productivity agent using pydantic-ai, explicit commands, and the existing layered architecture.
# Current state summary
Cato is pre-implementation with specs defining a layered architecture, dependency injection, and explicit slash commands. Productivity features are specified to use a dedicated agent/service backed by SQLite. Configuration is YAML-driven with no hard-coded defaults and Pydantic validation. Multi-provider LLM support is required, and natural language command interfaces are explicitly disallowed. Key references: `Project/Spec/GENERAL_PRINCIPLES.md`, `Project/Spec/functional/SPEC_PRODUCTIVITY.md`, `Project/Spec/functional/SPEC_COMMAND_SYSTEM.md`, `Project/Spec/functional/SPEC_CONFIGURATION.md`, `Project/Spec/technical/TECH_ARCHITECTURE.md`, `Project/Spec/technical/TECH_LLM_INTEGRATION.md`, `Project/Spec/technical/TECH_COMMAND_FRAMEWORK.md`, `Project/Spec/technical/TECH_STORAGE.md`.
# Proposed changes
## Scope and guiding constraints
* Treat “agent” strictly as an internal productivity agent, not a natural-language command interface, and only invoked from explicit slash commands.
* Use pydantic-ai for agent logic, but keep all defaults in YAML and expose relevant parameters at the top-level config surface.
* Preserve layering: Commands depend on Services; Services depend on Providers/Storage/Core; no upward imports.
* Ensure productivity outputs are displayed but not added to main chat history per spec.
## Agent subsystem (core abstractions)
* Add a small agent runtime module (suggested location: `cato/services/agents/`), defining:
    * `AgentRequest` and `AgentResult` data models (Pydantic) for validation across boundaries.
    * `AgentError` types that map to existing `CatoError` hierarchy (from `cato/core/exceptions.py`).
    * A thin `AgentRunner` that accepts a request, invokes the pydantic-ai agent, and returns a structured result.
* Provide a provider-agnostic adapter that can construct a pydantic-ai model using the configured LLM provider credentials (OpenAI/Anthropic/Google/Ollama), aligned with `TECH_LLM_INTEGRATION.md`.
## Productivity agent (MVP)
* Implement a `ProductivityAgent` as a pydantic-ai agent with explicit tool functions for:
    * Listing tasks with filters/sorting and formatting for `/st`.
    * Listing lists and list items for `/list`.
* Keep the agent’s tool surface deterministic and grounded in the existing SQLite repositories defined in `TECH_STORAGE.md`.
* Use a strict output schema that returns structured data for display (e.g., rows + column metadata) rather than free-form text.
* Ensure the agent does not write to the vector store and does not append to conversation history.
## Command integration
* Update `cato/commands/productivity.py` to:
    * Parse arguments as specified in `SPEC_PRODUCTIVITY.md` and `SPEC_COMMAND_SYSTEM.md`.
    * Construct a `ProductivityRequest` and call the productivity agent via a service layer.
    * Render responses through the display layer using the specified tables and status indicators.
* Keep `/st` and `/list` behavior exactly as specified; do not introduce natural-language shortcuts.
## Configuration integration
* Decide on configuration source for the agent:
    * MVP: reuse `llm.*` configuration for the productivity agent to avoid new config keys.
    * If separate tuning is required, add `productivity_agent` config section and update:
        * `cato/resources/defaults.yaml` (defaults)
        * `cato/core/config.py` (Pydantic schema)
        * `Project/Spec/CONFIG_REFERENCE.md` and `Project/Spec/functional/SPEC_CONFIGURATION.md`
* Ensure any adjustable parameters (model, temperature, max_tokens, timeout) are configurable at the top level.
## Error handling and logging
* Map pydantic-ai and provider errors to the `CatoError` hierarchy with clear user messages.
* Follow atomic exception handling and graceful degradation rules in `TECH_ERROR_HANDLING.md`.
* Log productivity agent execution in debug mode without exposing internal stack traces to the user.
## Testing strategy
* Unit tests for:
    * Agent request/response validation
    * Tool functions that access storage repositories (mocked)
    * Command parsing and invocation
* Integration tests for productivity flows using a temp SQLite database.
* Mock external LLM calls; no network in tests.
## Documentation and spec updates
* Update help docs for productivity commands if behavior or outputs change.
* If any behavior deviates from current specs, update the relevant spec files and log the changes as required by `GENERAL_PRINCIPLES.md`.
# Open questions
* Should the productivity agent have its own config section, or should it strictly reuse `llm.*` settings?
* Is there a planned set of additional productivity commands beyond `/st` and `/list` that should be covered in the initial agent tools?

```



Plan created. Review it and let me know what to change or confirm, especially the open questions about agent configuration and scope beyond `/st` and `/list`.

USER:
what are my options for isolated environments?

AGENT:
Here are the main options for isolated environments:

**Python-only (lightweight)**
- **`venv`**: built‑in, simple, per‑project isolation.
- **`virtualenv`**: like `venv` but faster/more flexible.
- **`uv venv`**: fast venv creation + installs with `uv` (fits your preference to use uv).

**Python+dependencies with locking**
- **Poetry**: manages venv + lockfile + publishing.
- **Pipenv**: venv + Pipfile/Pipfile.lock (less popular now).
- **uv + `pyproject.toml`**: modern, fast alternative to Poetry; good for reproducible envs.

**Per‑tool isolation**
- **`pipx`**: isolated env per CLI tool (great for global tools without polluting project envs).

**Full system isolation**
- **Containers (Docker/Podman)**: OS‑level isolation, reproducible builds.
- **Nix shells**: reproducible dev environments across machines.

If you want, tell me your goal (e.g., “per‑project Python dev,” “reproducible CI,” “isolated tools”) and I’ll recommend a specific setup with minimal commands.

USER:
my preference is uv, but I don't know a lot about it. I want an isolated env to avoid dependency clashes with other apps.

AGENT:
If you want an isolated env with **uv**, you have two clean options. Both avoid dependency clashes.

## Option A — quick per‑project venv (minimal setup)
Use this when you just want an isolated env and will install packages manually.

```bash
uv venv
uv pip install <package>
```
- `uv venv` creates a virtual environment (default name) and uv will auto‑use it on later commands. ([docs.astral.sh](https://docs.astral.sh/uv/pip/environments/?utm_source=openai))  
- You can activate it if you want:  
```bash
  source .venv/bin/activate
```
- You can request a specific Python and uv can download it if needed:  
```bash
  uv venv --python 3.11
```
  ([docs.astral.sh](https://docs.astral.sh/uv/pip/environments/?utm_source=openai))  

## Option B — uv project workflow (recommended for reproducible deps)
Use this if you want lockfiles + managed deps.

```bash
uv init
uv add <package>
```
- `uv init` scaffolds a project with `pyproject.toml`. ([docs.astral.sh](https://docs.astral.sh/uv/guides/projects/?utm_source=openai))  
- First project command (`uv add`, `uv run`, `uv sync`, `uv lock`) creates a virtual environment and `uv.lock`. ([docs.astral.sh](https://docs.astral.sh/uv/guides/projects/?utm_source=openai))  
- Add deps from a requirements file:
```bash
  uv add -r requirements.txt
```
  ([docs.astral.sh](https://docs.astral.sh/uv/guides/projects/?utm_source=openai))  

---

### Which should you pick?
- **Just want isolation quickly:** Option A.  
- **Want reproducible builds / clean dependency tracking:** Option B.

Tell me which workflow you want and whether this is a new or existing project, and I’ll give you the exact minimal commands.

USER:
i need option b since Cato is an installable package. Please document in specs and agents files accordingly

AGENT:


**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md**
```
# Development, Testing and Release Technical Specification

## Overview
This document defines the development workflow, testing strategy, continuous integration, and release process for Cato.

## Development Philosophy

### Single User, Local First
- Cato is developed for a single user on a single machine
- No multi-user deployment considerations
- Local development and testing is the primary workflow
- CI exists to catch regressions, not for complex deployment pipelines

### Minimal Ceremony
- Lightweight processes that don't impede rapid iteration
- Testing focused on core functionality, not exhaustive coverage
- Releases when meaningful changes accumulate, not on fixed schedules

## Branch Strategy

### Main Branch
- `main` is the stable branch
- All development work happens on feature branches
- Direct commits to `main` are prohibited

### Feature Branches
- Create a new branch for each feature or bug fix
- Branch naming: `feature/<short-description>` or `fix/<short-description>`
- Keep branches short-lived where possible
- Merge to `main` via pull request (or direct merge for solo development)

```bash
# Starting new work
git checkout main
git pull
git checkout -b feature/add-anthropic-provider

# After completion
git checkout main
git merge feature/add-anthropic-provider
git branch -d feature/add-anthropic-provider
```

## Testing Strategy

### Test Pyramid
```
        /\
       /  \     E2E Tests (few)
      /----\    - Full REPL interactions
     /      \   - Critical user journeys
    /--------\  Integration Tests (moderate)
   /          \ - Service + storage
  /------------\- Command + service
 /              \
/----------------\  Unit Tests (many)
                    - Individual functions
                    - Config validation
                    - Protocol implementations
```

### Unit Tests
**Scope**: Individual functions, classes, and methods in isolation

**What to test**:
- Configuration loading and validation
- Command argument parsing
- Message formatting
- Utility functions
- Protocol implementations with mocked dependencies

**Tools**: pytest

```python
# Example: testing config validation
def test_temperature_must_be_in_range():
    with pytest.raises(ValidationError):
        LLMConfig(temperature=5.0)  # Invalid: must be 0-2

def test_valid_config_loads():
    config = LLMConfig(provider="openai", model="gpt-4o")
    assert config.provider == "openai"
```

### Integration Tests
**Scope**: Multiple components working together

**What to test**:
- Service layer with real storage (test database)
- Command execution with mocked services
- Provider implementations with mocked API responses

**Approach**:
- Use pytest fixtures for test database setup/teardown
- Mock external APIs (OpenAI, Anthropic, etc.) at HTTP level
- Test realistic workflows

```python
# Example: testing chat service with vector store
@pytest.fixture
def test_vector_store(tmp_path):
    """Create a temporary ChromaDB instance."""
    return ChromaDBStore(path=tmp_path / "test_vectors")

def test_context_retrieval(test_vector_store):
    # Store some content
    test_vector_store.store("Python is a programming language", {})
    
    # Query should find it
    results = test_vector_store.query("What is Python?", k=1)
    assert len(results) == 1
    assert "Python" in results[0].content
```

### End-to-End Tests
**Scope**: Full application behaviour from user perspective

**What to test**:
- Application startup and shutdown
- Critical command flows (/help, /exit, /clear)
- Basic chat interaction (with mocked LLM)
- Error handling and graceful degradation

**Approach**:
- Use subprocess or pexpect to drive the REPL
- Mock LLM responses at API level
- Keep E2E tests minimal—they're slow and brittle

```python
# Example: testing /help command
def test_help_command(cato_process):
    cato_process.sendline("/help")
    output = cato_process.expect_output(timeout=5)
    assert "Available commands" in output
```

### What NOT to Test
- Third-party library internals (Rich, ChromaDB, etc.)
- Exact output formatting (too brittle)
- Every error path (focus on critical ones)
- Performance benchmarks (not initially)

### Test Organisation
```
tests/
├── conftest.py           # Shared fixtures
├── unit/
│   ├── test_config.py
│   ├── test_commands.py
│   ├── test_message_parsing.py
│   └── ...
├── integration/
│   ├── test_chat_service.py
│   ├── test_vector_store.py
│   ├── test_productivity.py
│   └── ...
└── e2e/
    ├── test_startup.py
    ├── test_basic_chat.py
    └── test_commands.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run with coverage
pytest --cov=cato --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_config.py

# Run tests matching pattern
pytest -k "test_config"
```

## Continuous Integration

### CI Philosophy
- CI should be fast (< 5 minutes)
- Fail fast on obvious issues
- Don't block on non-critical checks

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e ".[dev]"
      
      - name: Run linting
        run: ruff check cato/
      
      - name: Run type checking
        run: mypy cato/
      
      - name: Run tests
        run: pytest tests/unit tests/integration --tb=short

  # E2E tests run separately, only on main
  e2e:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    needs: test
    
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e ".[dev]"
      - name: Run E2E tests
        run: pytest tests/e2e --tb=short
```

### CI Checks
1. **Linting** (ruff): Code style and common errors
2. **Type checking** (mypy): Static type verification
3. **Unit tests**: Fast, isolated tests
4. **Integration tests**: Component interaction tests
5. **E2E tests**: Full application tests (main branch only)

### Pre-commit Hooks (Optional)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Code Quality Tools

### Linting: Ruff
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
]
```

### Type Checking: Mypy
```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
```

### Test Coverage
- Aim for ~70-80% coverage on core modules
- Don't chase 100%—diminishing returns
- Focus coverage on business logic, not boilerplate

## Release Process

### Versioning
Semantic versioning: `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes to config or commands
- **MINOR**: New features, new commands
- **PATCH**: Bug fixes, minor improvements

Pre-1.0: `0.x.y` where breaking changes are expected

### Release Checklist
1. Ensure all tests pass on `main`
2. Update version in `pyproject.toml`
3. Update CHANGELOG.md with notable changes
4. Create git tag: `git tag -a v0.1.0 -m "Release 0.1.0"`
5. Push tag: `git push origin v0.1.0`

### Changelog Format
```markdown
# Changelog

## [0.2.0] - 2026-01-20
### Added
- Anthropic provider support
- /speaklike command for custom TTS instructions

### Changed
- Improved context retrieval performance

### Fixed
- Vector store connection error on startup

## [0.1.0] - 2026-01-14
- Initial release
```

### No PyPI Publishing (Initially)
- Cato is for personal use
- Install from git: `pip install git+https://github.com/user/cato.git`
- Or local editable install: `pip install -e .`

## Package Management: uv

Cato uses **uv** for package management. uv is a fast, modern Python package manager from Astral (the Ruff team).

### Why uv
- **Speed**: 10-100x faster than pip/Poetry for dependency resolution
- **Standard format**: Uses PEP 621 compliant `pyproject.toml` (no custom sections)
- **Deterministic**: Cross-platform lockfile support
- **Simple**: Single tool for venv, install, and lock

### pyproject.toml
```toml
[project]
name = "cato"
version = "0.1.0"
description = "Chat at the Terminal Orchestrator"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "Alex Loveless", email = "alex@alexloveless.uk"}
]

dependencies = [
    "rich>=13.0",
    "prompt-toolkit>=3.0",
    "pyyaml>=6.0",
    "pydantic>=2.0",
    "pydantic-ai>=0.1",
    "chromadb>=0.4",
    "openai>=1.0",
    "anthropic>=0.18",
    "google-generativeai>=0.4",
    "httpx>=0.27",
    "aiosqlite>=0.19",
    "click>=8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.23",
    "mypy>=1.8",
    "ruff>=0.3",
    "pre-commit>=3.0",
]

[project.scripts]
cato = "cato.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## Development Environment

### Initial Setup
```bash
# Clone repository
git clone https://github.com/user/cato.git
cd cato

# Create conda environment
conda create -n cato python=3.12
conda activate cato

# Install uv (if not already installed)
pip install uv

# Install Cato in editable mode with dev dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

### Daily Workflow
```bash
# Activate environment
conda activate cato

# Sync dependencies (if pyproject.toml changed)
uv pip install -e ".[dev]"

# Run tests
pytest

# Run linting and type checking
ruff check cato/
mypy cato/
```

### Adding Dependencies
```bash
# Add to pyproject.toml manually, then:
uv pip install -e ".[dev]"

# Or install directly (for experimentation)
uv pip install some-package
```

### Lockfile (Optional)
For reproducible builds, generate a lockfile:
```bash
# Generate lockfile from pyproject.toml
uv pip compile pyproject.toml -o requirements.lock

# Install from lockfile
uv pip sync requirements.lock
```

### Running Locally
```bash
# Run from source (after install)
cato

# Or run as module
python -m cato

# Run with specific config
cato --config ~/.config/cato/dev.yaml

# Run with debug logging
cato --debug
```

## Documentation

### Code Documentation
- Numpy-format docstrings on all public functions
- Type hints on all function signatures
- README.md in each module directory
- `AGENTS.md` and `WARP.md` at repo root for AI navigation and rules
- Subdirectory `agent.md` files follow `Project/Spec/technical/TECH_CODE_ORGANISATION.md`

### User Documentation
- In-app help system (`/help`)
- Help files in `cato/resources/help/`
- Keep help in sync with implementation

### Specification Maintenance
- Update specs when implementation diverges
- Log significant decisions in specs
- Specs are living documents, not write-once

```

**/home/alex/Documents/repos/Cato/AGENTS.md**
```
# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management, conversational context via vector storage, TTS, and web search.

**Status**: Pre-implementation - specification documents exist in `Project/Spec/`

### Purpose
Cato exists to provide maximum control over LLM interactions, tailored to specific user needs and idiosyncrasies. It is a chat client first, productivity client second.

### Intent
Cato provides a unified terminal interface for:
- Conversational AI interactions with multiple LLM providers
- Personal productivity management (tasks, lists, time tracking)
- File operations and code management
- Persistent conversational context with retrieval
- Text-to-speech synthesis and web search integration

### Target User
- Single user on a single machine
- Users who are highly changeable, like to tinker and experiment
- Users who want flexible, modular architecture they can customise
- Multiple instances may run with different configurations simultaneously

## Before Starting Development

Read the specification documents in order:
1. `Project/Spec/GENERAL_PRINCIPLES.md` - Core philosophy and constraints
2. `Project/Spec/functional/SPEC_OVERVIEW.md` - Application flow and UI
3. Relevant functional specs in `Project/Spec/functional/`
4. Technical specs in `Project/Spec/technical/` (start with TECH_ARCHITECTURE.md)

## Architecture Overview

### Layered Architecture
```
Presentation → Commands → Services → Providers → Storage → Core
```
- Each layer may only import from layers below it
- No circular dependencies between layers
- Cross-cutting concerns (logging, errors) live in Core

### Protocol-Based Abstractions
- Key interfaces defined as Python `Protocol` classes
- Enables duck typing without inheritance
- Easy to create test mocks and swap implementations via config

### Dependency Injection
- Components receive dependencies at construction time
- `bootstrap.py` handles all component wiring
- No hard-coded provider instantiation in services

## Key Architectural Decisions

### Configuration
- YAML-driven configuration with overlay system (user config overlays defaults)
- **No hard-coded defaults in code** - all defaults in `cato/resources/defaults.yaml`
- Pydantic for all validation
- Unrecognised config keys warn but don't crash

### Multi-Provider LLM
- Must support OpenAI, Anthropic, Google, Ollama
- Use pydantic-ai over LangChain for agent/API interactions
- Each provider implements `LLMProvider` protocol

### Storage
- ChromaDB for vector store (embeddings, similarity search)
- SQLite for productivity data (tasks, lists)
- **Never load entire vector store into memory**
- Storage layer contains no business logic—pure data access

### Command System
- Slash commands (`/help`, `/speak`, `/web`, etc.) for explicit actions
- Decorator-based registration - adding a command requires only one file
- **No natural language command interface** - commands use explicit syntax

### Error Handling
- Atomic exception handling (specific exceptions, not broad catches)
- Custom exception hierarchy (`CatoError` base class in `cato/core/exceptions.py`)
- Graceful degradation for non-critical failures
- Never silent failures
- Errors flow upward: Storage → Service → Command → Presentation

## Directory Structure

```
cato/                        # Repository root
├── pyproject.toml           # Package metadata (uv/PEP 621)
├── AGENTS.md                # AI navigation (repo-level)
├── WARP.md                  # AI rules for Warp
├── cato/                    # Python package
│   ├── __main__.py          # Entry point: python -m cato
│   ├── bootstrap.py         # Component wiring
│   ├── app.py               # Main run loop
│   ├── core/                # Config, exceptions, logging, types
│   ├── providers/           # LLM, search, TTS backends
│   │   ├── llm/             # OpenAI, Anthropic, Google, Ollama
│   │   ├── search/          # DuckDuckGo, Google
│   │   └── tts/             # OpenAI TTS
│   ├── storage/             # ChromaDB, SQLite
│   ├── services/            # Business logic orchestration
│   ├── commands/            # Slash command implementations
│   ├── display/             # Rich console, prompt_toolkit
│   └── resources/           # defaults.yaml, help files
└── tests/                   # Unit, integration, e2e
```

## Code Organisation Requirements

- Root-level AI guidance lives in `AGENTS.md` and `WARP.md`
- Subdirectory `agent.md` files follow the standard in `Project/Spec/technical/TECH_CODE_ORGANISATION.md`
- Each module directory must have a README explaining purpose and extension
- Numpy-format docstrings, type hints on all functions
- Relative imports within package
- Single responsibility per file

## Testing Strategy

- **Unit tests**: Individual functions/classes in isolation with mocked dependencies
- **Integration tests**: Service + storage, command + service combinations
- **E2E tests**: Critical user journeys only (minimal—they're slow and brittle)
- Use pytest with fixtures for test database setup/teardown
- Mock external APIs at HTTP level
- Focus on core functionality, not exhaustive coverage

## Technology Stack

### Required
- Rich (formatting), prompt_toolkit (input)
- ChromaDB, OpenAI Embeddings API
- PyYAML, Pydantic
- pydantic-ai (productivity agent)
- LLM provider SDKs (OpenAI, Anthropic, Google)

### Optional
- OpenAI TTS API
- DuckDuckGo/Google/Bing search
- Ollama (local LLM)

## Development Workflow

- `main` is the stable branch; all work on feature branches
- Branch naming: `feature/<description>` or `fix/<description>`
- CI should be fast (< 5 minutes)
- Releases when meaningful changes accumulate

```




_File edits failed: Could not apply all diffs to /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md. The changes to /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md were already made. _



**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md**
```
# Development, Testing and Release Technical Specification

## Overview
This document defines the development workflow, testing strategy, continuous integration, and release process for Cato.

## Development Philosophy

### Single User, Local First
- Cato is developed for a single user on a single machine
- No multi-user deployment considerations
- Local development and testing is the primary workflow
- CI exists to catch regressions, not for complex deployment pipelines

### Minimal Ceremony
- Lightweight processes that don't impede rapid iteration
- Testing focused on core functionality, not exhaustive coverage
- Releases when meaningful changes accumulate, not on fixed schedules

## Branch Strategy

### Main Branch
- `main` is the stable branch
- All development work happens on feature branches
- Direct commits to `main` are prohibited

### Feature Branches
- Create a new branch for each feature or bug fix
- Branch naming: `feature/<short-description>` or `fix/<short-description>`
- Keep branches short-lived where possible
- Merge to `main` via pull request (or direct merge for solo development)

```bash
# Starting new work
git checkout main
git pull
git checkout -b feature/add-anthropic-provider

# After completion
git checkout main
git merge feature/add-anthropic-provider
git branch -d feature/add-anthropic-provider
```

## Testing Strategy

### Test Pyramid
```
        /\
       /  \     E2E Tests (few)
      /----\    - Full REPL interactions
     /      \   - Critical user journeys
    /--------\  Integration Tests (moderate)
   /          \ - Service + storage
  /------------\- Command + service
 /              \
/----------------\  Unit Tests (many)
                    - Individual functions
                    - Config validation
                    - Protocol implementations
```

### Unit Tests
**Scope**: Individual functions, classes, and methods in isolation

**What to test**:
- Configuration loading and validation
- Command argument parsing
- Message formatting
- Utility functions
- Protocol implementations with mocked dependencies

**Tools**: pytest

```python
# Example: testing config validation
def test_temperature_must_be_in_range():
    with pytest.raises(ValidationError):
        LLMConfig(temperature=5.0)  # Invalid: must be 0-2

def test_valid_config_loads():
    config = LLMConfig(provider="openai", model="gpt-4o")
    assert config.provider == "openai"
```

### Integration Tests
**Scope**: Multiple components working together

**What to test**:
- Service layer with real storage (test database)
- Command execution with mocked services
- Provider implementations with mocked API responses

**Approach**:
- Use pytest fixtures for test database setup/teardown
- Mock external APIs (OpenAI, Anthropic, etc.) at HTTP level
- Test realistic workflows

```python
# Example: testing chat service with vector store
@pytest.fixture
def test_vector_store(tmp_path):
    """Create a temporary ChromaDB instance."""
    return ChromaDBStore(path=tmp_path / "test_vectors")

def test_context_retrieval(test_vector_store):
    # Store some content
    test_vector_store.store("Python is a programming language", {})
    
    # Query should find it
    results = test_vector_store.query("What is Python?", k=1)
    assert len(results) == 1
    assert "Python" in results[0].content
```

### End-to-End Tests
**Scope**: Full application behaviour from user perspective

**What to test**:
- Application startup and shutdown
- Critical command flows (/help, /exit, /clear)
- Basic chat interaction (with mocked LLM)
- Error handling and graceful degradation

**Approach**:
- Use subprocess or pexpect to drive the REPL
- Mock LLM responses at API level
- Keep E2E tests minimal—they're slow and brittle

```python
# Example: testing /help command
def test_help_command(cato_process):
    cato_process.sendline("/help")
    output = cato_process.expect_output(timeout=5)
    assert "Available commands" in output
```

### What NOT to Test
- Third-party library internals (Rich, ChromaDB, etc.)
- Exact output formatting (too brittle)
- Every error path (focus on critical ones)
- Performance benchmarks (not initially)

### Test Organisation
```
tests/
├── conftest.py           # Shared fixtures
├── unit/
│   ├── test_config.py
│   ├── test_commands.py
│   ├── test_message_parsing.py
│   └── ...
├── integration/
│   ├── test_chat_service.py
│   ├── test_vector_store.py
│   ├── test_productivity.py
│   └── ...
└── e2e/
    ├── test_startup.py
    ├── test_basic_chat.py
    └── test_commands.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run with coverage
pytest --cov=cato --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_config.py

# Run tests matching pattern
pytest -k "test_config"
```

## Continuous Integration

### CI Philosophy
- CI should be fast (< 5 minutes)
- Fail fast on obvious issues
- Don't block on non-critical checks

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e ".[dev]"
      
      - name: Run linting
        run: ruff check cato/
      
      - name: Run type checking
        run: mypy cato/
      
      - name: Run tests
        run: pytest tests/unit tests/integration --tb=short

  # E2E tests run separately, only on main
  e2e:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    needs: test
    
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e ".[dev]"
      - name: Run E2E tests
        run: pytest tests/e2e --tb=short
```

### CI Checks
1. **Linting** (ruff): Code style and common errors
2. **Type checking** (mypy): Static type verification
3. **Unit tests**: Fast, isolated tests
4. **Integration tests**: Component interaction tests
5. **E2E tests**: Full application tests (main branch only)

### Pre-commit Hooks (Optional)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Code Quality Tools

### Linting: Ruff
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
]
```

### Type Checking: Mypy
```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
```

### Test Coverage
- Aim for ~70-80% coverage on core modules
- Don't chase 100%—diminishing returns
- Focus coverage on business logic, not boilerplate

## Release Process

### Versioning
Semantic versioning: `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes to config or commands
- **MINOR**: New features, new commands
- **PATCH**: Bug fixes, minor improvements

Pre-1.0: `0.x.y` where breaking changes are expected

### Release Checklist
1. Ensure all tests pass on `main`
2. Update version in `pyproject.toml`
3. Update CHANGELOG.md with notable changes
4. Create git tag: `git tag -a v0.1.0 -m "Release 0.1.0"`
5. Push tag: `git push origin v0.1.0`

### Changelog Format
```markdown
# Changelog

## [0.2.0] - 2026-01-20
### Added
- Anthropic provider support
- /speaklike command for custom TTS instructions

### Changed
- Improved context retrieval performance

### Fixed
- Vector store connection error on startup

## [0.1.0] - 2026-01-14
- Initial release
```

### No PyPI Publishing (Initially)
- Cato is for personal use
- Install from git: `pip install git+https://github.com/user/cato.git`
- Or local editable install: `pip install -e .`

## Package Management: uv

Cato uses **uv** for package management. uv is a fast, modern Python package manager from Astral (the Ruff team).

### Why uv
- **Speed**: 10-100x faster than pip/Poetry for dependency resolution
- **Standard format**: Uses PEP 621 compliant `pyproject.toml` (no custom sections)
- **Deterministic**: Cross-platform lockfile support
- **Simple**: Single tool for venv, install, and lock

### pyproject.toml
```toml
[project]
name = "cato"
version = "0.1.0"
description = "Chat at the Terminal Orchestrator"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "Alex Loveless", email = "alex@alexloveless.uk"}
]

dependencies = [
    "rich>=13.0",
    "prompt-toolkit>=3.0",
    "pyyaml>=6.0",
    "pydantic>=2.0",
    "pydantic-ai>=0.1",
    "chromadb>=0.4",
    "openai>=1.0",
    "anthropic>=0.18",
    "google-generativeai>=0.4",
    "httpx>=0.27",
    "aiosqlite>=0.19",
    "click>=8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.23",
    "mypy>=1.8",
    "ruff>=0.3",
    "pre-commit>=3.0",
]

[project.scripts]
cato = "cato.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## Development Environment

### Initial Setup
```bash
# Clone repository
git clone https://github.com/user/cato.git
cd cato

# Create conda environment
conda create -n cato python=3.12
conda activate cato

# Install uv (if not already installed)
pip install uv

# Install Cato in editable mode with dev dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

### Daily Workflow
```bash
# Activate environment
conda activate cato

# Sync dependencies (if pyproject.toml changed)
uv pip install -e ".[dev]"

# Run tests
pytest

# Run linting and type checking
ruff check cato/
mypy cato/
```

### Adding Dependencies
```bash
# Add to pyproject.toml manually, then:
uv pip install -e ".[dev]"

# Or install directly (for experimentation)
uv pip install some-package
```

### Lockfile (Optional)
For reproducible builds, generate a lockfile:
```bash
# Generate lockfile from pyproject.toml
uv pip compile pyproject.toml -o requirements.lock

# Install from lockfile
uv pip sync requirements.lock
```

### Running Locally
```bash
# Run from source (after install)
cato

# Or run as module
python -m cato

# Run with specific config
cato --config ~/.config/cato/dev.yaml

# Run with debug logging
cato --debug
```

## Documentation

### Code Documentation
- Numpy-format docstrings on all public functions
- Type hints on all function signatures
- README.md in each module directory
- `AGENTS.md` and `WARP.md` at repo root for AI navigation and rules
- Subdirectory `agent.md` files follow `Project/Spec/technical/TECH_CODE_ORGANISATION.md`

### User Documentation
- In-app help system (`/help`)
- Help files in `cato/resources/help/`
- Keep help in sync with implementation

### Specification Maintenance
- Update specs when implementation diverges
- Log significant decisions in specs
- Specs are living documents, not write-once

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
@@ -214,7 +214,8 @@
       - name: Install dependencies
         run: |
           pip install uv
-          uv pip install -e ".[dev]"
+          uv sync --frozen --group dev
+v
       
       - name: Run linting
         run: ruff check cato/

```





**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md**
```
# Development, Testing and Release Technical Specification

## Overview
This document defines the development workflow, testing strategy, continuous integration, and release process for Cato.

## Development Philosophy

### Single User, Local First
- Cato is developed for a single user on a single machine
- No multi-user deployment considerations
- Local development and testing is the primary workflow
- CI exists to catch regressions, not for complex deployment pipelines

### Minimal Ceremony
- Lightweight processes that don't impede rapid iteration
- Testing focused on core functionality, not exhaustive coverage
- Releases when meaningful changes accumulate, not on fixed schedules

## Branch Strategy

### Main Branch
- `main` is the stable branch
- All development work happens on feature branches
- Direct commits to `main` are prohibited

### Feature Branches
- Create a new branch for each feature or bug fix
- Branch naming: `feature/<short-description>` or `fix/<short-description>`
- Keep branches short-lived where possible
- Merge to `main` via pull request (or direct merge for solo development)

```bash
# Starting new work
git checkout main
git pull
git checkout -b feature/add-anthropic-provider

# After completion
git checkout main
git merge feature/add-anthropic-provider
git branch -d feature/add-anthropic-provider
```

## Testing Strategy

### Test Pyramid
```
        /\
       /  \     E2E Tests (few)
      /----\    - Full REPL interactions
     /      \   - Critical user journeys
    /--------\  Integration Tests (moderate)
   /          \ - Service + storage
  /------------\- Command + service
 /              \
/----------------\  Unit Tests (many)
                    - Individual functions
                    - Config validation
                    - Protocol implementations
```

### Unit Tests
**Scope**: Individual functions, classes, and methods in isolation

**What to test**:
- Configuration loading and validation
- Command argument parsing
- Message formatting
- Utility functions
- Protocol implementations with mocked dependencies

**Tools**: pytest

```python
# Example: testing config validation
def test_temperature_must_be_in_range():
    with pytest.raises(ValidationError):
        LLMConfig(temperature=5.0)  # Invalid: must be 0-2

def test_valid_config_loads():
    config = LLMConfig(provider="openai", model="gpt-4o")
    assert config.provider == "openai"
```

### Integration Tests
**Scope**: Multiple components working together

**What to test**:
- Service layer with real storage (test database)
- Command execution with mocked services
- Provider implementations with mocked API responses

**Approach**:
- Use pytest fixtures for test database setup/teardown
- Mock external APIs (OpenAI, Anthropic, etc.) at HTTP level
- Test realistic workflows

```python
# Example: testing chat service with vector store
@pytest.fixture
def test_vector_store(tmp_path):
    """Create a temporary ChromaDB instance."""
    return ChromaDBStore(path=tmp_path / "test_vectors")

def test_context_retrieval(test_vector_store):
    # Store some content
    test_vector_store.store("Python is a programming language", {})
    
    # Query should find it
    results = test_vector_store.query("What is Python?", k=1)
    assert len(results) == 1
    assert "Python" in results[0].content
```

### End-to-End Tests
**Scope**: Full application behaviour from user perspective

**What to test**:
- Application startup and shutdown
- Critical command flows (/help, /exit, /clear)
- Basic chat interaction (with mocked LLM)
- Error handling and graceful degradation

**Approach**:
- Use subprocess or pexpect to drive the REPL
- Mock LLM responses at API level
- Keep E2E tests minimal—they're slow and brittle

```python
# Example: testing /help command
def test_help_command(cato_process):
    cato_process.sendline("/help")
    output = cato_process.expect_output(timeout=5)
    assert "Available commands" in output
```

### What NOT to Test
- Third-party library internals (Rich, ChromaDB, etc.)
- Exact output formatting (too brittle)
- Every error path (focus on critical ones)
- Performance benchmarks (not initially)

### Test Organisation
```
tests/
├── conftest.py           # Shared fixtures
├── unit/
│   ├── test_config.py
│   ├── test_commands.py
│   ├── test_message_parsing.py
│   └── ...
├── integration/
│   ├── test_chat_service.py
│   ├── test_vector_store.py
│   ├── test_productivity.py
│   └── ...
└── e2e/
    ├── test_startup.py
    ├── test_basic_chat.py
    └── test_commands.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run with coverage
pytest --cov=cato --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_config.py

# Run tests matching pattern
pytest -k "test_config"
```

## Continuous Integration

### CI Philosophy
- CI should be fast (< 5 minutes)
- Fail fast on obvious issues
- Don't block on non-critical checks

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install uv
          uv sync --frozen --group dev
v
      
      - name: Run linting
        run: ruff check cato/
      
      - name: Run type checking
        run: mypy cato/
      
      - name: Run tests
        run: pytest tests/unit tests/integration --tb=short

  # E2E tests run separately, only on main
  e2e:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    needs: test
    
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e ".[dev]"
      - name: Run E2E tests
        run: pytest tests/e2e --tb=short
```

### CI Checks
1. **Linting** (ruff): Code style and common errors
2. **Type checking** (mypy): Static type verification
3. **Unit tests**: Fast, isolated tests
4. **Integration tests**: Component interaction tests
5. **E2E tests**: Full application tests (main branch only)

### Pre-commit Hooks (Optional)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Code Quality Tools

### Linting: Ruff
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
]
```

### Type Checking: Mypy
```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
```

### Test Coverage
- Aim for ~70-80% coverage on core modules
- Don't chase 100%—diminishing returns
- Focus coverage on business logic, not boilerplate

## Release Process

### Versioning
Semantic versioning: `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes to config or commands
- **MINOR**: New features, new commands
- **PATCH**: Bug fixes, minor improvements

Pre-1.0: `0.x.y` where breaking changes are expected

### Release Checklist
1. Ensure all tests pass on `main`
2. Update version in `pyproject.toml`
3. Update CHANGELOG.md with notable changes
4. Create git tag: `git tag -a v0.1.0 -m "Release 0.1.0"`
5. Push tag: `git push origin v0.1.0`

### Changelog Format
```markdown
# Changelog

## [0.2.0] - 2026-01-20
### Added
- Anthropic provider support
- /speaklike command for custom TTS instructions

### Changed
- Improved context retrieval performance

### Fixed
- Vector store connection error on startup

## [0.1.0] - 2026-01-14
- Initial release
```

### No PyPI Publishing (Initially)
- Cato is for personal use
- Install from git: `pip install git+https://github.com/user/cato.git`
- Or local editable install: `pip install -e .`

## Package Management: uv

Cato uses **uv** for package management. uv is a fast, modern Python package manager from Astral (the Ruff team).

### Why uv
- **Speed**: 10-100x faster than pip/Poetry for dependency resolution
- **Standard format**: Uses PEP 621 compliant `pyproject.toml` (no custom sections)
- **Deterministic**: Cross-platform lockfile support
- **Simple**: Single tool for venv, install, and lock

### pyproject.toml
```toml
[project]
name = "cato"
version = "0.1.0"
description = "Chat at the Terminal Orchestrator"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "Alex Loveless", email = "alex@alexloveless.uk"}
]

dependencies = [
    "rich>=13.0",
    "prompt-toolkit>=3.0",
    "pyyaml>=6.0",
    "pydantic>=2.0",
    "pydantic-ai>=0.1",
    "chromadb>=0.4",
    "openai>=1.0",
    "anthropic>=0.18",
    "google-generativeai>=0.4",
    "httpx>=0.27",
    "aiosqlite>=0.19",
    "click>=8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.23",
    "mypy>=1.8",
    "ruff>=0.3",
    "pre-commit>=3.0",
]

[project.scripts]
cato = "cato.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## Development Environment

### Initial Setup
```bash
# Clone repository
git clone https://github.com/user/cato.git
cd cato

# Create conda environment
conda create -n cato python=3.12
conda activate cato

# Install uv (if not already installed)
pip install uv

# Install Cato in editable mode with dev dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

### Daily Workflow
```bash
# Activate environment
conda activate cato

# Sync dependencies (if pyproject.toml changed)
uv pip install -e ".[dev]"

# Run tests
pytest

# Run linting and type checking
ruff check cato/
mypy cato/
```

### Adding Dependencies
```bash
# Add to pyproject.toml manually, then:
uv pip install -e ".[dev]"

# Or install directly (for experimentation)
uv pip install some-package
```

### Lockfile (Optional)
For reproducible builds, generate a lockfile:
```bash
# Generate lockfile from pyproject.toml
uv pip compile pyproject.toml -o requirements.lock

# Install from lockfile
uv pip sync requirements.lock
```

### Running Locally
```bash
# Run from source (after install)
cato

# Or run as module
python -m cato

# Run with specific config
cato --config ~/.config/cato/dev.yaml

# Run with debug logging
cato --debug
```

## Documentation

### Code Documentation
- Numpy-format docstrings on all public functions
- Type hints on all function signatures
- README.md in each module directory
- `AGENTS.md` and `WARP.md` at repo root for AI navigation and rules
- Subdirectory `agent.md` files follow `Project/Spec/technical/TECH_CODE_ORGANISATION.md`

### User Documentation
- In-app help system (`/help`)
- Help files in `cato/resources/help/`
- Keep help in sync with implementation

### Specification Maintenance
- Update specs when implementation diverges
- Log significant decisions in specs
- Specs are living documents, not write-once

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
@@ -215,7 +215,6 @@
         run: |
           pip install uv
           uv sync --frozen --group dev
-v
       
       - name: Run linting
         run: ruff check cato/
@@ -241,7 +240,7 @@
       - name: Install dependencies
         run: |
           pip install uv
-          uv pip install -e ".[dev]"
+          uv sync --frozen --group dev
       - name: Run E2E tests
         run: pytest tests/e2e --tb=short
 ```

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
@@ -377,7 +377,7 @@
     "click>=8.0",
 ]
 
-[project.optional-dependencies]
+[dependency-groups]
 dev = [
     "pytest>=8.0",
     "pytest-cov>=4.0",

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
@@ -426,19 +426,19 @@
 # Clone repository
 git clone https://github.com/user/cato.git
 cd cato
-
-# Create conda environment
-conda create -n cato python=3.12
 conda activate cato
 
 # Install uv (if not already installed)
 pip install uv
+# Sync project environment (creates .venv and uv.lock on first sync)
+uv sync
 
-# Install Cato in editable mode with dev dependencies
+# Include dev dependency group (if defined)
+uv sync --group dev
 uv pip install -e ".[dev]"
 
 # Install pre-commit hooks (optional)
-pre-commit install
+uv run pre-commit install
 ```
 
 ### Daily Workflow

```





**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md**
```
# Development, Testing and Release Technical Specification

## Overview
This document defines the development workflow, testing strategy, continuous integration, and release process for Cato.

## Development Philosophy

### Single User, Local First
- Cato is developed for a single user on a single machine
- No multi-user deployment considerations
- Local development and testing is the primary workflow
- CI exists to catch regressions, not for complex deployment pipelines

### Minimal Ceremony
- Lightweight processes that don't impede rapid iteration
- Testing focused on core functionality, not exhaustive coverage
- Releases when meaningful changes accumulate, not on fixed schedules

## Branch Strategy

### Main Branch
- `main` is the stable branch
- All development work happens on feature branches
- Direct commits to `main` are prohibited

### Feature Branches
- Create a new branch for each feature or bug fix
- Branch naming: `feature/<short-description>` or `fix/<short-description>`
- Keep branches short-lived where possible
- Merge to `main` via pull request (or direct merge for solo development)

```bash
# Starting new work
git checkout main
git pull
git checkout -b feature/add-anthropic-provider

# After completion
git checkout main
git merge feature/add-anthropic-provider
git branch -d feature/add-anthropic-provider
```

## Testing Strategy

### Test Pyramid
```
        /\
       /  \     E2E Tests (few)
      /----\    - Full REPL interactions
     /      \   - Critical user journeys
    /--------\  Integration Tests (moderate)
   /          \ - Service + storage
  /------------\- Command + service
 /              \
/----------------\  Unit Tests (many)
                    - Individual functions
                    - Config validation
                    - Protocol implementations
```

### Unit Tests
**Scope**: Individual functions, classes, and methods in isolation

**What to test**:
- Configuration loading and validation
- Command argument parsing
- Message formatting
- Utility functions
- Protocol implementations with mocked dependencies

**Tools**: pytest

```python
# Example: testing config validation
def test_temperature_must_be_in_range():
    with pytest.raises(ValidationError):
        LLMConfig(temperature=5.0)  # Invalid: must be 0-2

def test_valid_config_loads():
    config = LLMConfig(provider="openai", model="gpt-4o")
    assert config.provider == "openai"
```

### Integration Tests
**Scope**: Multiple components working together

**What to test**:
- Service layer with real storage (test database)
- Command execution with mocked services
- Provider implementations with mocked API responses

**Approach**:
- Use pytest fixtures for test database setup/teardown
- Mock external APIs (OpenAI, Anthropic, etc.) at HTTP level
- Test realistic workflows

```python
# Example: testing chat service with vector store
@pytest.fixture
def test_vector_store(tmp_path):
    """Create a temporary ChromaDB instance."""
    return ChromaDBStore(path=tmp_path / "test_vectors")

def test_context_retrieval(test_vector_store):
    # Store some content
    test_vector_store.store("Python is a programming language", {})
    
    # Query should find it
    results = test_vector_store.query("What is Python?", k=1)
    assert len(results) == 1
    assert "Python" in results[0].content
```

### End-to-End Tests
**Scope**: Full application behaviour from user perspective

**What to test**:
- Application startup and shutdown
- Critical command flows (/help, /exit, /clear)
- Basic chat interaction (with mocked LLM)
- Error handling and graceful degradation

**Approach**:
- Use subprocess or pexpect to drive the REPL
- Mock LLM responses at API level
- Keep E2E tests minimal—they're slow and brittle

```python
# Example: testing /help command
def test_help_command(cato_process):
    cato_process.sendline("/help")
    output = cato_process.expect_output(timeout=5)
    assert "Available commands" in output
```

### What NOT to Test
- Third-party library internals (Rich, ChromaDB, etc.)
- Exact output formatting (too brittle)
- Every error path (focus on critical ones)
- Performance benchmarks (not initially)

### Test Organisation
```
tests/
├── conftest.py           # Shared fixtures
├── unit/
│   ├── test_config.py
│   ├── test_commands.py
│   ├── test_message_parsing.py
│   └── ...
├── integration/
│   ├── test_chat_service.py
│   ├── test_vector_store.py
│   ├── test_productivity.py
│   └── ...
└── e2e/
    ├── test_startup.py
    ├── test_basic_chat.py
    └── test_commands.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run with coverage
pytest --cov=cato --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_config.py

# Run tests matching pattern
pytest -k "test_config"
```

## Continuous Integration

### CI Philosophy
- CI should be fast (< 5 minutes)
- Fail fast on obvious issues
- Don't block on non-critical checks

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install uv
          uv sync --frozen --group dev
      
      - name: Run linting
        run: ruff check cato/
      
      - name: Run type checking
        run: mypy cato/
      
      - name: Run tests
        run: pytest tests/unit tests/integration --tb=short

  # E2E tests run separately, only on main
  e2e:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    needs: test
    
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          pip install uv
          uv sync --frozen --group dev
      - name: Run E2E tests
        run: pytest tests/e2e --tb=short
```

### CI Checks
1. **Linting** (ruff): Code style and common errors
2. **Type checking** (mypy): Static type verification
3. **Unit tests**: Fast, isolated tests
4. **Integration tests**: Component interaction tests
5. **E2E tests**: Full application tests (main branch only)

### Pre-commit Hooks (Optional)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Code Quality Tools

### Linting: Ruff
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
]
```

### Type Checking: Mypy
```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
```

### Test Coverage
- Aim for ~70-80% coverage on core modules
- Don't chase 100%—diminishing returns
- Focus coverage on business logic, not boilerplate

## Release Process

### Versioning
Semantic versioning: `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes to config or commands
- **MINOR**: New features, new commands
- **PATCH**: Bug fixes, minor improvements

Pre-1.0: `0.x.y` where breaking changes are expected

### Release Checklist
1. Ensure all tests pass on `main`
2. Update version in `pyproject.toml`
3. Update CHANGELOG.md with notable changes
4. Create git tag: `git tag -a v0.1.0 -m "Release 0.1.0"`
5. Push tag: `git push origin v0.1.0`

### Changelog Format
```markdown
# Changelog

## [0.2.0] - 2026-01-20
### Added
- Anthropic provider support
- /speaklike command for custom TTS instructions

### Changed
- Improved context retrieval performance

### Fixed
- Vector store connection error on startup

## [0.1.0] - 2026-01-14
- Initial release
```

### No PyPI Publishing (Initially)
- Cato is for personal use
- Install from git: `pip install git+https://github.com/user/cato.git`
- Or local editable install: `pip install -e .`

## Package Management: uv

Cato uses **uv** for package management. uv is a fast, modern Python package manager from Astral (the Ruff team).

### Why uv
- **Speed**: 10-100x faster than pip/Poetry for dependency resolution
- **Standard format**: Uses PEP 621 compliant `pyproject.toml` (no custom sections)
- **Deterministic**: Cross-platform lockfile support
- **Simple**: Single tool for venv, install, and lock

### pyproject.toml
```toml
[project]
name = "cato"
version = "0.1.0"
description = "Chat at the Terminal Orchestrator"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "Alex Loveless", email = "alex@alexloveless.uk"}
]

dependencies = [
    "rich>=13.0",
    "prompt-toolkit>=3.0",
    "pyyaml>=6.0",
    "pydantic>=2.0",
    "pydantic-ai>=0.1",
    "chromadb>=0.4",
    "openai>=1.0",
    "anthropic>=0.18",
    "google-generativeai>=0.4",
    "httpx>=0.27",
    "aiosqlite>=0.19",
    "click>=8.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.23",
    "mypy>=1.8",
    "ruff>=0.3",
    "pre-commit>=3.0",
]

[project.scripts]
cato = "cato.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## Development Environment

### Initial Setup
```bash
# Clone repository
git clone https://github.com/user/cato.git
cd cato
conda activate cato

# Install uv (if not already installed)
pip install uv
# Sync project environment (creates .venv and uv.lock on first sync)
uv sync

# Include dev dependency group (if defined)
uv sync --group dev
uv pip install -e ".[dev]"

# Install pre-commit hooks (optional)
uv run pre-commit install
```

### Daily Workflow
```bash
# Activate environment
conda activate cato

# Sync dependencies (if pyproject.toml changed)
uv pip install -e ".[dev]"

# Run tests
pytest

# Run linting and type checking
ruff check cato/
mypy cato/
```

### Adding Dependencies
```bash
# Add to pyproject.toml manually, then:
uv pip install -e ".[dev]"

# Or install directly (for experimentation)
uv pip install some-package
```

### Lockfile (Optional)
For reproducible builds, generate a lockfile:
```bash
# Generate lockfile from pyproject.toml
uv pip compile pyproject.toml -o requirements.lock

# Install from lockfile
uv pip sync requirements.lock
```

### Running Locally
```bash
# Run from source (after install)
cato

# Or run as module
python -m cato

# Run with specific config
cato --config ~/.config/cato/dev.yaml

# Run with debug logging
cato --debug
```

## Documentation

### Code Documentation
- Numpy-format docstrings on all public functions
- Type hints on all function signatures
- README.md in each module directory
- `AGENTS.md` and `WARP.md` at repo root for AI navigation and rules
- Subdirectory `agent.md` files follow `Project/Spec/technical/TECH_CODE_ORGANISATION.md`

### User Documentation
- In-app help system (`/help`)
- Help files in `cato/resources/help/`
- Keep help in sync with implementation

### Specification Maintenance
- Update specs when implementation diverges
- Log significant decisions in specs
- Specs are living documents, not write-once

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
@@ -426,7 +426,6 @@
 # Clone repository
 git clone https://github.com/user/cato.git
 cd cato
-conda activate cato
 
 # Install uv (if not already installed)
 pip install uv
@@ -435,7 +434,6 @@
 
 # Include dev dependency group (if defined)
 uv sync --group dev
-uv pip install -e ".[dev]"
 
 # Install pre-commit hooks (optional)
 uv run pre-commit install

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
@@ -441,18 +441,17 @@
 
 ### Daily Workflow
 ```bash
-# Activate environment
-conda activate cato
-
-# Sync dependencies (if pyproject.toml changed)
-uv pip install -e ".[dev]"
+# Sync environment (if pyproject.toml or uv.lock changed)
+uv sync
+# If you use the dev dependency group:
+uv sync --group dev
 
 # Run tests
-pytest
+uv run pytest
 
 # Run linting and type checking
-ruff check cato/
-mypy cato/
+uv run ruff check cato/
+uv run mypy cato/
 ```
 
 ### Adding Dependencies

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
@@ -456,11 +456,17 @@
 
 ### Adding Dependencies
 ```bash
-# Add to pyproject.toml manually, then:
-uv pip install -e ".[dev]"
+# Add a runtime dependency
+uv add some-package
+
+# Add a dev-only dependency (if using dependency groups)
+uv add --group dev some-dev-tool
+
+# Remove a dependency
+uv remove some-package
 
-# Or install directly (for experimentation)
-uv pip install some-package
+# Upgrade a specific package in the lockfile
+uv lock --upgrade-package some-package
 ```
 
 ### Lockfile (Optional)

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
@@ -469,14 +469,14 @@
 uv lock --upgrade-package some-package
 ```
 
-### Lockfile (Optional)
-For reproducible builds, generate a lockfile:
+### Lockfile (uv.lock)
+For reproducible builds, generate/update the lockfile and sync from it:
 ```bash
-# Generate lockfile from pyproject.toml
-uv pip compile pyproject.toml -o requirements.lock
+# Generate or update lockfile
+uv lock
 
-# Install from lockfile
-uv pip sync requirements.lock
+# Install exactly from lockfile (no updates)
+uv sync --frozen
 ```
 
 ### Running Locally

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/WARP.md
+++ /home/alex/Documents/repos/Cato/WARP.md
@@ -146,3 +146,4 @@
 - Branch naming: `feature/<description>` or `fix/<description>`
 - CI should be fast (< 5 minutes)
 - Releases when meaningful changes accumulate
+- Use uv project workflow for isolated environments: `uv sync` creates `.venv` and installs deps, `uv add` manages deps, `uv run` executes commands, and `uv lock` maintains `uv.lock`.

```





**Files Read:**

**/home/alex/Documents/repos/Cato/AGENTS.md**
```
# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management, conversational context via vector storage, TTS, and web search.

**Status**: Pre-implementation - specification documents exist in `Project/Spec/`

### Purpose
Cato exists to provide maximum control over LLM interactions, tailored to specific user needs and idiosyncrasies. It is a chat client first, productivity client second.

### Intent
Cato provides a unified terminal interface for:
- Conversational AI interactions with multiple LLM providers
- Personal productivity management (tasks, lists, time tracking)
- File operations and code management
- Persistent conversational context with retrieval
- Text-to-speech synthesis and web search integration

### Target User
- Single user on a single machine
- Users who are highly changeable, like to tinker and experiment
- Users who want flexible, modular architecture they can customise
- Multiple instances may run with different configurations simultaneously

## Before Starting Development

Read the specification documents in order:
1. `Project/Spec/GENERAL_PRINCIPLES.md` - Core philosophy and constraints
2. `Project/Spec/functional/SPEC_OVERVIEW.md` - Application flow and UI
3. Relevant functional specs in `Project/Spec/functional/`
4. Technical specs in `Project/Spec/technical/` (start with TECH_ARCHITECTURE.md)

## Architecture Overview

### Layered Architecture
```
Presentation → Commands → Services → Providers → Storage → Core
```
- Each layer may only import from layers below it
- No circular dependencies between layers
- Cross-cutting concerns (logging, errors) live in Core

### Protocol-Based Abstractions
- Key interfaces defined as Python `Protocol` classes
- Enables duck typing without inheritance
- Easy to create test mocks and swap implementations via config

### Dependency Injection
- Components receive dependencies at construction time
- `bootstrap.py` handles all component wiring
- No hard-coded provider instantiation in services

## Key Architectural Decisions

### Configuration
- YAML-driven configuration with overlay system (user config overlays defaults)
- **No hard-coded defaults in code** - all defaults in `cato/resources/defaults.yaml`
- Pydantic for all validation
- Unrecognised config keys warn but don't crash

### Multi-Provider LLM
- Must support OpenAI, Anthropic, Google, Ollama
- Use pydantic-ai over LangChain for agent/API interactions
- Each provider implements `LLMProvider` protocol

### Storage
- ChromaDB for vector store (embeddings, similarity search)
- SQLite for productivity data (tasks, lists)
- **Never load entire vector store into memory**
- Storage layer contains no business logic—pure data access

### Command System
- Slash commands (`/help`, `/speak`, `/web`, etc.) for explicit actions
- Decorator-based registration - adding a command requires only one file
- **No natural language command interface** - commands use explicit syntax

### Error Handling
- Atomic exception handling (specific exceptions, not broad catches)
- Custom exception hierarchy (`CatoError` base class in `cato/core/exceptions.py`)
- Graceful degradation for non-critical failures
- Never silent failures
- Errors flow upward: Storage → Service → Command → Presentation

## Directory Structure

```
cato/                        # Repository root
├── pyproject.toml           # Package metadata (uv/PEP 621)
├── AGENTS.md                # AI navigation (repo-level)
├── WARP.md                  # AI rules for Warp
├── cato/                    # Python package
│   ├── __main__.py          # Entry point: python -m cato
│   ├── bootstrap.py         # Component wiring
│   ├── app.py               # Main run loop
│   ├── core/                # Config, exceptions, logging, types
│   ├── providers/           # LLM, search, TTS backends
│   │   ├── llm/             # OpenAI, Anthropic, Google, Ollama
│   │   ├── search/          # DuckDuckGo, Google
│   │   └── tts/             # OpenAI TTS
│   ├── storage/             # ChromaDB, SQLite
│   ├── services/            # Business logic orchestration
│   ├── commands/            # Slash command implementations
│   ├── display/             # Rich console, prompt_toolkit
│   └── resources/           # defaults.yaml, help files
└── tests/                   # Unit, integration, e2e
```

## Code Organisation Requirements

- Root-level AI guidance lives in `AGENTS.md` and `WARP.md`
- Subdirectory `agent.md` files follow the standard in `Project/Spec/technical/TECH_CODE_ORGANISATION.md`
- Each module directory must have a README explaining purpose and extension
- Numpy-format docstrings, type hints on all functions
- Relative imports within package
- Single responsibility per file

## Testing Strategy

- **Unit tests**: Individual functions/classes in isolation with mocked dependencies
- **Integration tests**: Service + storage, command + service combinations
- **E2E tests**: Critical user journeys only (minimal—they're slow and brittle)
- Use pytest with fixtures for test database setup/teardown
- Mock external APIs at HTTP level
- Focus on core functionality, not exhaustive coverage

## Technology Stack

### Required
- Rich (formatting), prompt_toolkit (input)
- ChromaDB, OpenAI Embeddings API
- PyYAML, Pydantic
- pydantic-ai (productivity agent)
- LLM provider SDKs (OpenAI, Anthropic, Google)

### Optional
- OpenAI TTS API
- DuckDuckGo/Google/Bing search
- Ollama (local LLM)

## Development Workflow

- `main` is the stable branch; all work on feature branches
- Branch naming: `feature/<description>` or `fix/<description>`
- CI should be fast (< 5 minutes)
- Releases when meaningful changes accumulate
- Use uv project workflow for isolated environments: `uv sync` creates `.venv` and installs deps, `uv add` manages deps, `uv run` executes commands, and `uv lock` maintains `uv.lock`.

```

**/home/alex/Documents/repos/Cato/WARP.md**
```
# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management, conversational context via vector storage, TTS, and web search.

**Status**: Pre-implementation - specification documents exist in `Project/Spec/`

### Purpose
Cato exists to provide maximum control over LLM interactions, tailored to specific user needs and idiosyncrasies. It is a chat client first, productivity client second.

### Intent
Cato provides a unified terminal interface for:
- Conversational AI interactions with multiple LLM providers
- Personal productivity management (tasks, lists, time tracking)
- File operations and code management
- Persistent conversational context with retrieval
- Text-to-speech synthesis and web search integration

### Target User
- Single user on a single machine
- Users who are highly changeable, like to tinker and experiment
- Users who want flexible, modular architecture they can customise
- Multiple instances may run with different configurations simultaneously

## Before Starting Development

Read the specification documents in order:
1. `Project/Spec/GENERAL_PRINCIPLES.md` - Core philosophy and constraints
2. `Project/Spec/functional/SPEC_OVERVIEW.md` - Application flow and UI
3. Relevant functional specs in `Project/Spec/functional/`
4. Technical specs in `Project/Spec/technical/` (start with TECH_ARCHITECTURE.md)

## Architecture Overview

### Layered Architecture
```
Presentation → Commands → Services → Providers → Storage → Core
```
- Each layer may only import from layers below it
- No circular dependencies between layers
- Cross-cutting concerns (logging, errors) live in Core

### Protocol-Based Abstractions
- Key interfaces defined as Python `Protocol` classes
- Enables duck typing without inheritance
- Easy to create test mocks and swap implementations via config

### Dependency Injection
- Components receive dependencies at construction time
- `bootstrap.py` handles all component wiring
- No hard-coded provider instantiation in services

## Key Architectural Decisions

### Configuration
- YAML-driven configuration with overlay system (user config overlays defaults)
- **No hard-coded defaults in code** - all defaults in `cato/resources/defaults.yaml`
- Pydantic for all validation
- Unrecognised config keys warn but don't crash

### Multi-Provider LLM
- Must support OpenAI, Anthropic, Google, Ollama
- Use pydantic-ai over LangChain for agent/API interactions
- Each provider implements `LLMProvider` protocol

### Storage
- ChromaDB for vector store (embeddings, similarity search)
- SQLite for productivity data (tasks, lists)
- **Never load entire vector store into memory**
- Storage layer contains no business logic—pure data access

### Command System
- Slash commands (`/help`, `/speak`, `/web`, etc.) for explicit actions
- Decorator-based registration - adding a command requires only one file
- **No natural language command interface** - commands use explicit syntax

### Error Handling
- Atomic exception handling (specific exceptions, not broad catches)
- Custom exception hierarchy (`CatoError` base class in `cato/core/exceptions.py`)
- Graceful degradation for non-critical failures
- Never silent failures
- Errors flow upward: Storage → Service → Command → Presentation

## Directory Structure

```
cato/                        # Repository root
├── pyproject.toml           # Package metadata (uv/PEP 621)
├── AGENTS.md                # AI navigation (repo-level)
├── WARP.md                  # AI rules for Warp
├── cato/                    # Python package
│   ├── __main__.py          # Entry point: python -m cato
│   ├── bootstrap.py         # Component wiring
│   ├── app.py               # Main run loop
│   ├── core/                # Config, exceptions, logging, types
│   ├── providers/           # LLM, search, TTS backends
│   │   ├── llm/             # OpenAI, Anthropic, Google, Ollama
│   │   ├── search/          # DuckDuckGo, Google
│   │   └── tts/             # OpenAI TTS
│   ├── storage/             # ChromaDB, SQLite
│   ├── services/            # Business logic orchestration
│   ├── commands/            # Slash command implementations
│   ├── display/             # Rich console, prompt_toolkit
│   └── resources/           # defaults.yaml, help files
└── tests/                   # Unit, integration, e2e
```

## Code Organisation Requirements

- Root-level AI guidance lives in `AGENTS.md` and `WARP.md`
- Subdirectory `agent.md` files follow the standard in `Project/Spec/technical/TECH_CODE_ORGANISATION.md`
- Each module directory must have a README explaining purpose and extension
- Numpy-format docstrings, type hints on all functions
- Relative imports within package
- Single responsibility per file

## Testing Strategy

- **Unit tests**: Individual functions/classes in isolation with mocked dependencies
- **Integration tests**: Service + storage, command + service combinations
- **E2E tests**: Critical user journeys only (minimal—they're slow and brittle)
- Use pytest with fixtures for test database setup/teardown
- Mock external APIs at HTTP level
- Focus on core functionality, not exhaustive coverage

## Technology Stack

### Required
- Rich (formatting), prompt_toolkit (input)
- ChromaDB, OpenAI Embeddings API
- PyYAML, Pydantic
- pydantic-ai (productivity agent)
- LLM provider SDKs (OpenAI, Anthropic, Google)

### Optional
- OpenAI TTS API
- DuckDuckGo/Google/Bing search
- Ollama (local LLM)

## Development Workflow

- `main` is the stable branch; all work on feature branches
- Branch naming: `feature/<description>` or `fix/<description>`
- CI should be fast (< 5 minutes)
- Releases when meaningful changes accumulate
- Use uv project workflow for isolated environments: `uv sync` creates `.venv` and installs deps, `uv add` manages deps, `uv run` executes commands, and `uv lock` maintains `uv.lock`.

```




**Command Executed:**
```bash
ls -l /home/alex/Documents/repos/Cato/AGENTS.md /home/alex/Documents/repos/Cato/WARP.md
```

**Output:**
```
lrwxrwxrwx 1 alex alex    7 Jan 14 19:45 /home/alex/Documents/repos/Cato/AGENTS.md -> WARP.md
-rw-r--r-- 1 alex alex 6204 Jan 15 20:03 /home/alex/Documents/repos/Cato/WARP.md
```



**Grep Results:**

- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083057-Critically_Review_Repo_Specs.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083151-Design_Project_Architecture_Approach.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083112-Update_WARP_md_With_Spec_Changes.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083124-Design_Project_Architecture_Approach.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_165050-Process_Comments_in_Reports_Summary.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_170144-Create_Command_Line_Args_Specs.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_191803-Run_Cato_Command_Instructions.md**




**Grep Results:**





**Grep Results:**



Updated `Project/Spec/technical/TECH_DEVELOPMENT.md` to document the uv project workflow (`uv sync` creates `.venv`/`uv.lock`, `uv run` for commands, `uv add/remove/lock` for deps, and CI `uv sync --frozen --group dev`), and adjusted the lockfile guidance accordingly. citeturn0search0turn0search3turn0search4turn1search2  
Updated `AGENTS.md` (symlinked to `WARP.md`) with a concise uv workflow note. citeturn0search0turn0search3turn0search4turn1search2

No tests run (docs-only changes).

Want me to update any other spec files (e.g., a dedicated developer onboarding spec or CI docs) with the same uv workflow?

USER:
will cato still be installable with pip?

AGENT:

_Read files error: These files do not exist: /home/alex/Documents/repos/Cato/pyproject.toml _

Short answer: **Yes, as long as Cato has a standard `pyproject.toml` with a build backend** (PEP 517/621). uv doesn’t prevent pip installs.

Right now there’s **no `pyproject.toml` in the repo**, so `pip install .` won’t work yet. Once you add it (as specified in the docs), `pip install .` and `pip install -e .` will work normally.

If you want, I can add a minimal `pyproject.toml` now to make pip installs work.