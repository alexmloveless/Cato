USER:
tell me how cato will be run

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



Per the specs, Cato is a terminal CLI app. It will be run via the package entry point—either `python -m cato` (from `cato/__main__.py`) or a `cato` CLI entry point (from `cato/main.py`). On startup it loads config in this order: YAML file → environment variables → CLI overrides, initializes the Rich console, shows a welcome panel, wires providers/services/storage via `bootstrap.py`, then enters an interactive REPL where `/` commands are handled before regular chat input.

If you want the exact run command or flags as implemented (once code exists), point me to the relevant spec or code file and I’ll confirm.

USER:
how will cato be installed on other machines?

AGENT:


**Grep Results:**

- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083057-Critically_Review_Repo_Specs.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083135-Create_WARP_md_for_Codebase.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DISPLAY.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_VECTOR_STORE.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_084913-Review_Repo_Specs_with_Critique_Report_GPT-5_2-high.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-14_spec_review_claude_opus_4_5.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_165050-Process_Comments_in_Reports_Summary.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_170144-Create_Command_Line_Args_Specs.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_TTS.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083112-Update_WARP_md_With_Spec_Changes.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_PERFORMANCE.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_reports_summary_annotated.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_171104-Comprehensive_Codebase_Quality_Review.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_VECTOR_STORE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_LINE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_LLM_INTEGRATION.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/CONFIG_REFERENCE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md**
- **/home/alex/Documents/repos/Cato/WARP.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083151-Design_Project_Architecture_Approach.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/GENERAL_PRINCIPLES.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_FILE_OPERATIONS.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_STORAGE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_WEB_SEARCH.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_reports_summary.md**
- **/home/alex/Documents/repos/Cato/Project/Notes/Jan 14 at 11-01.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CLI.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CODE_ORGANISATION.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_COMMAND_FRAMEWORK.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083007-Remove_Memory_Creation_References.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083124-Design_Project_Architecture_Approach.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083219-Read_And_Follow_FULL_SPEC_PROMPT_md.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CONFIGURATION.md**




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
| system_prompt_files | list | [] | - | Additional prompt files |
| base_prompt_file | string | (package default) | - | Alternative prompt file path |
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
| user_label | string | User | Label for user messages |
| assistant_label | string | Assistant | Label for assistant messages |
| no_rich | bool | false | Disable rich text formatting |
| no_color | bool | false | Disable ANSI colors |
| line_width | int | 80 | Terminal width (chars) |
| exchange_delimiter | string | ─ | Character for separation |
| exchange_delimiter_length | int | 60 | Delimiter line length |
| prompt_symbol | string | 🐱 >  | Input prompt (supports Unicode/emoji) |
| spinner_icon | string | ⠋ | Waiting indicator icon (spinner character) |


### Logging Configuration (`logging`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| level | string | WARNING | DEBUG, INFO, WARNING, ERROR |
| format | string | (standard format) | Log message format |
| show_context | bool | false | Show context in INFO logs |

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
1. Load configuration file (if found)
2. Parse YAML structure
3. Validate using Pydantic models:
   - Type checking
   - Range validation
   - Enum validation
4. Validate location aliases (paths exist)
5. Apply environment variable overrides
6. Apply CLI argument overrides
7. Report validation errors

If there is an appropriate existing parser or validator in pydantic (e.g. for file location validation) the you should use that in preference to creating a native one.

### Error Handling
- Invalid YAML: Show parse error, exit
- Missing required key: Use default
- Invalid value: Warn the user and fall back to default
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



Per `Project/Spec/technical/TECH_DEVELOPMENT.md`, Cato won’t be published to PyPI initially. Installation on other machines is expected to be from git (or a local checkout) and then installed into a Python environment using **uv**.

Minimal install options from the spec:

- **From git** (no PyPI):
```bash
uv pip install git+https://github.com/user/cato.git
```
- **Local checkout (editable)**:
```bash
git clone https://github.com/user/cato.git
cd cato
uv pip install -e .
```
If you want the exact repo URL or a non-editable install flow, tell me the preferred distribution target (private git, tarball, etc.).

USER:
can it be installed with just pip?

AGENT:
Yes. The specs explicitly mention using `pip install git+https://...` or `pip install -e .` for local installs, even though uv is the preferred tool. If you want to forbid pip, that would need a spec change.

USER:
what is the process for making changes, creating releases, building and deploying?

AGENT:
From `Project/Spec/technical/TECH_DEVELOPMENT.md`:

**Making changes**
- Work on feature branches only (`feature/<desc>` or `fix/<desc>`); no direct commits to `main`.
- Merge back to `main` via PR or direct merge for solo workflow.

**Release process**
- SemVer (`MAJOR.MINOR.PATCH`, pre‑1.0 uses `0.x.y`).
- Checklist:
  1) Ensure tests pass on `main`
  2) Bump version in `pyproject.toml`
  3) Update `CHANGELOG.md`
  4) Tag release (`git tag -a vX.Y.Z -m "Release X.Y.Z"`)
  5) Push tag

**Build / deploy**
- No PyPI publishing initially. Distribution is **from git** or local editable install.
- Build system is `hatchling` (via `pyproject.toml`) but there’s no separate deploy pipeline specified.

**CI**
- GitHub Actions runs lint (ruff), type checks (mypy), unit + integration tests; E2E tests only on `main`.

If you want a formal “deployment” step (e.g., PyPI, container, or release artifacts), that’s not in the spec yet and would need to be added.

USER:
will the data stores be created the first time cato is run?

AGENT:


**Grep Results:**

- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CLI.md**
- **/home/alex/Documents/repos/Cato/WARP.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_FILE_OPERATIONS.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_TTS.md**
- **/home/alex/Documents/repos/Cato/Project/Notes/Jan 14 at 11-01.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083219-Read_And_Follow_FULL_SPEC_PROMPT_md.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CONFIGURATION.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_reports_summary.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_COMMAND_FRAMEWORK.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083007-Remove_Memory_Creation_References.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_165050-Process_Comments_in_Reports_Summary.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_171104-Comprehensive_Codebase_Quality_Review.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_WEB_SEARCH.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_084913-Review_Repo_Specs_with_Critique_Report_GPT-5_2-high.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/DATA_MODELS.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/CONFIG_REFERENCE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_STORAGE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_LINE.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083112-Update_WARP_md_With_Spec_Changes.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_PERFORMANCE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_VECTOR_STORE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/GENERAL_PRINCIPLES.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_VECTOR_STORE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_LLM_INTEGRATION.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083151-Design_Project_Architecture_Approach.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083135-Create_WARP_md_for_Codebase.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_170144-Create_Command_Line_Args_Specs.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_PRODUCTIVITY.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_reports_summary_annotated.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083124-Design_Project_Architecture_Approach.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/GLOSSARY.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083057-Critically_Review_Repo_Specs.md**
- **/home/alex/Documents/repos/Cato/Project/Notes/agents.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DISPLAY.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-14_spec_review_claude_opus_4_5.md**




**Files Read:**

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





**Files Read:**

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





**Files Read:**

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
        chunk_overlap: int = 200,
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
  similarity_threshold: 0.7
  dynamic_threshold: true
  retrieval_strategy: "default"

  # Embedding settings
  embedding_provider: "openai"
  embedding_model: "text-embedding-3-small"
  embedding_dimensions: 1536

  # Chunking settings
  chunking_strategy: "semantic"
  chunk_size: 1000
  chunk_overlap: 200
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
        chunk_overlap: int = 200,
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
  similarity_threshold: 0.7
  dynamic_threshold: true
  retrieval_strategy: "default"

  # Embedding settings
  embedding_provider: "openai"
  embedding_model: "text-embedding-3-small"
  embedding_dimensions: 1536

  # Chunking settings
  chunking_strategy: "semantic"
  chunk_size: 1000
  chunk_overlap: 200
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



Yes—per the specs:

- **SQLite (productivity + sessions)**: On startup, storage connects and **creates the parent directory and runs migrations**, so the `~/.local/share/cato/cato.db` file and tables are created on first run if missing.  
- **Vector store (ChromaDB)**: When enabled, the vector store initializes a **PersistentClient** and calls **`get_or_create_collection`**, so the on‑disk store/collection is created if it doesn’t exist. It remains empty until exchanges/documents are added (and exchanges are not stored in dummy mode).

If vector store is disabled in config, it won’t be created.

USER:
what is the default loc for the vector store?

AGENT:
Default vector store path is `~/.local/share/cato/vectordb` (from `SPEC_CONFIGURATION.md`).

USER:
/ex

AGENT:
What do you want `/ex` to do?