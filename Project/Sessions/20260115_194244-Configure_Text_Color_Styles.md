USER:
i'd like to able to control styles in config e.g. text color

AGENT:

**Command Executed:**
```bash
ls
```

**Output:**
```
20260115_191803-Run_Cato_Command_Instructions.md  AGENTS.md  Project  WARP.md
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





**Files Read:**

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





**Grep Results:**

- **/home/alex/Documents/repos/Cato/Project/Spec/GENERAL_PRINCIPLES.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CODE_ORGANISATION.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_STORAGE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_PRODUCTIVITY.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_COMMAND_FRAMEWORK.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CONFIGURATION.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_TTS.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_165050-Process_Comments_in_Reports_Summary.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CLI.md**
- **/home/alex/Documents/repos/Cato/WARP.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083007-Remove_Memory_Creation_References.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_LINE.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083057-Critically_Review_Repo_Specs.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083135-Create_WARP_md_for_Codebase.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_PERFORMANCE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_FILE_OPERATIONS.md**
- **/home/alex/Documents/repos/Cato/20260115_191803-Run_Cato_Command_Instructions.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_084913-Review_Repo_Specs_with_Critique_Report_GPT-5_2-high.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083124-Design_Project_Architecture_Approach.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083112-Update_WARP_md_With_Spec_Changes.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083219-Read_And_Follow_FULL_SPEC_PROMPT_md.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/CONFIG_REFERENCE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_LLM_INTEGRATION.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_VECTOR_STORE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_VECTOR_STORE.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_171104-Comprehensive_Codebase_Quality_Review.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_170144-Create_Command_Line_Args_Specs.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DISPLAY.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_reports_summary_annotated.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-14_spec_review_claude_opus_4_5.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083151-Design_Project_Architecture_Approach.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_reports_summary.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_WEB_SEARCH.md**
- **/home/alex/Documents/repos/Cato/Project/Notes/Jan 14 at 11-01.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md**




**Files Read:**

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

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DISPLAY.md**
```
# Display Technical Specification

## Overview
Cato uses Rich for formatted output and prompt_toolkit for input handling. The display layer is abstracted through a protocol to enable alternative frontends while maintaining terminal-first design.

## Display Protocol

### Interface Definition
```python
from typing import Protocol
from dataclasses import dataclass

@dataclass
class DisplayMessage:
    """
    Display message.
    
    Note: Uses dataclass as it's internal display data, not external.
    Named DisplayMessage to avoid confusion with LLM Message model.
    """
    role: Literal["user", "assistant", "system", "error", "info"]
    content: str
    timestamp: datetime | None = None


class Display(Protocol):
    """
    Protocol for display implementations.
    
    Abstracts terminal output to enable pluggable frontends.
    """
    
    def show_message(self, message: DisplayMessage) -> None:
        """
        Display a message.
        
        Parameters
        ----------
        message
            Message to display.
        """
        ...
    
    def show_error(self, error: str, details: str | None = None) -> None:
        """
        Display an error message.
        
        Parameters
        ----------
        error
            Error message.
        details
            Optional additional details.
        """
        ...
    
    def show_warning(self, warning: str) -> None:
        """Display a warning message."""
        ...
    
    def show_info(self, info: str) -> None:
        """Display an informational message."""
        ...
    
    def show_markdown(self, content: str) -> None:
        """
        Display markdown-formatted content.
        
        Parameters
        ----------
        content
            Markdown text.
        """
        ...
    
    def show_code(self, code: str, language: str | None = None) -> None:
        """
        Display syntax-highlighted code.
        
        Parameters
        ----------
        code
            Code to display.
        language
            Language for syntax highlighting.
        """
        ...
    
    def show_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        title: str | None = None,
    ) -> None:
        """
        Display a table.
        
        Parameters
        ----------
        headers
            Column headers.
        rows
            Table rows.
        title
            Optional table title.
        """
        ...
    
    def show_spinner(self, message: str) -> SpinnerContext:
        """
        Show a loading spinner.
        
        Parameters
        ----------
        message
            Message to show while loading.
        
        Returns
        -------
        SpinnerContext
            Context manager that stops spinner on exit.
        """
        ...
    
    def clear(self) -> None:
        """Clear the terminal screen."""
        ...
    
    def show_welcome(self) -> None:
        """Display welcome message."""
        ...
```

## Rich Implementation

### Console Setup
```python
from rich.console import Console
from rich.theme import Theme
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live

class RichDisplay:
    """Rich-based terminal display implementation."""
    
    def __init__(self, config: DisplayConfig) -> None:
        self._config = config
        
        # Load theme
        theme = self._load_theme(config.theme)
        
        # Create console
        self._console = Console(
            theme=theme,
            width=config.max_width,
            force_terminal=True,
        )
    
    def _load_theme(self, theme_name: str) -> Theme:
        """Load theme from config or built-in."""
        # Built-in themes
        themes = {
            "default": Theme({
                "user": "bold cyan",
                "assistant": "bold green",
                "system": "dim",
                "error": "bold red",
                "warning": "bold yellow",
                "info": "bold blue",
                "code": "on grey23",
            }),
            "gruvbox-dark": Theme({
                "user": "bold #83a598",      # Blue
                "assistant": "bold #b8bb26", # Green
                "system": "#928374",         # Grey
                "error": "bold #fb4934",     # Red
                "warning": "bold #fabd2f",   # Yellow
                "info": "bold #8ec07c",      # Aqua
                "code": "on #3c3836",        # Dark bg
            }),
        }
        
        if theme_name in themes:
            return themes[theme_name]
        
        # Try to load custom theme from file
        custom_path = Path(f"~/.config/cato/themes/{theme_name}.yaml").expanduser()
        if custom_path.exists():
            return self._load_custom_theme(custom_path)
        
        return themes["default"]
    
    def show_message(self, message: DisplayMessage) -> None:
        """Display a message with role-based styling."""
        prefix = self._get_prefix(message.role)
        style = message.role
        
        if self._config.timestamps and message.timestamp:
            timestamp = message.timestamp.strftime("%H:%M")
            prefix = f"[dim]{timestamp}[/dim] {prefix}"
        
        if message.role == "assistant" and self._config.markdown_enabled:
            self._console.print(prefix, style=style)
            self._console.print(Markdown(message.content))
        else:
            self._console.print(f"{prefix} {message.content}", style=style)
    
    def _get_prefix(self, role: str) -> str:
        """Get display prefix for role."""
        prefixes = {
            "user": "You:",
            "assistant": "Cato:",
            "system": "System:",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
        }
        return prefixes.get(role, "")
    
    def show_error(self, error: str, details: str | None = None) -> None:
        """Display an error message."""
        self._console.print(f"❌ {error}", style="error")
        if details:
            self._console.print(f"   {details}", style="dim")
    
    def show_warning(self, warning: str) -> None:
        """Display a warning."""
        self._console.print(f"⚠️  {warning}", style="warning")
    
    def show_info(self, info: str) -> None:
        """Display info message."""
        self._console.print(f"ℹ️  {info}", style="info")
    
    def show_markdown(self, content: str) -> None:
        """Render and display markdown."""
        md = Markdown(content, code_theme=self._config.code_theme)
        self._console.print(md)
    
    def show_code(self, code: str, language: str | None = None) -> None:
        """Display syntax-highlighted code."""
        syntax = Syntax(
            code,
            language or "text",
            theme=self._config.code_theme,
            line_numbers=True,
            word_wrap=True,
        )
        self._console.print(syntax)
    
    def show_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        title: str | None = None,
    ) -> None:
        """Display a formatted table."""
        table = Table(title=title, show_header=True, header_style="bold")
        
        for header in headers:
            table.add_column(header)
        
        for row in rows:
            table.add_row(*row)
        
        self._console.print(table)
    
    def show_spinner(self, message: str) -> "SpinnerContext":
        """Create spinner context manager."""
        return SpinnerContext(self._console, message, self._config.spinner_style)
    
    def clear(self) -> None:
        """Clear terminal."""
        self._console.clear()
    
    def show_welcome(self) -> None:
        """Display welcome banner."""
        panel = Panel(
            "[bold]Cato[/bold] - Chat at the Terminal Orchestrator\n"
            "Type [cyan]/help[/cyan] for commands, [cyan]/exit[/cyan] to quit",
            title="Welcome",
            border_style="dim",
        )
        self._console.print(panel)
```

### Spinner Context
```python
from contextlib import contextmanager

class SpinnerContext:
    """Context manager for loading spinner."""
    
    def __init__(self, console: Console, message: str, style: str) -> None:
        self._console = console
        self._message = message
        self._style = style
        self._live: Live | None = None
    
    def __enter__(self) -> "SpinnerContext":
        spinner = Spinner(self._style, text=self._message)
        self._live = Live(spinner, console=self._console, refresh_per_second=10)
        self._live.__enter__()
        return self
    
    def __exit__(self, *args) -> None:
        if self._live:
            self._live.__exit__(*args)
    
    def update(self, message: str) -> None:
        """Update spinner message."""
        if self._live:
            self._live.update(Spinner(self._style, text=message))


# Usage
async def send_message(self, content: str) -> str:
    with self._display.show_spinner("Thinking..."):
        response = await self._llm.complete(messages)
    return response.content
```

## Input Handling

### Prompt Toolkit Setup
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings

class InputHandler:
    """Handle user input with prompt_toolkit."""
    
    def __init__(self, config: DisplayConfig, history_path: Path) -> None:
        self._config = config
        
        # Custom key bindings
        bindings = KeyBindings()
        
        @bindings.add("c-c")
        def _(event):
            """Handle Ctrl+C gracefully."""
            event.app.exit(result=None)
        
        @bindings.add("c-d")
        def _(event):
            """Handle Ctrl+D for exit."""
            raise EOFError()
        
        # Create session
        self._session = PromptSession(
            history=FileHistory(str(history_path)),
            auto_suggest=AutoSuggestFromHistory(),
            key_bindings=bindings,
            style=self._get_style(),
            multiline=False,
            enable_history_search=True,
        )
    
    def _get_style(self) -> Style:
        """Get prompt style based on theme."""
        if self._config.theme == "gruvbox-dark":
            return Style.from_dict({
                "prompt": "#83a598 bold",
                "": "#ebdbb2",
            })
        return Style.from_dict({
            "prompt": "cyan bold",
            "": "",
        })
    
    async def get_input(self, prompt: str | None = None) -> str | None:
        """
        Get user input.
        
        Parameters
        ----------
        prompt
            Prompt string.
        
        Returns
        -------
        str | None
            User input or None if cancelled.
        """
        try:
            return await self._session.prompt_async(prompt or self._config.prompt_symbol)
        except (EOFError, KeyboardInterrupt):
            return None
    
    async def get_multiline_input(self, prompt: str | None = None) -> str | None:
        """
        Get multiline input (ends with blank line).
        
        Parameters
        ----------
        prompt
            Prompt string.
        
        Returns
        -------
        str | None
            Combined input or None if cancelled.
        """
        lines = []
        continuation = "... "
        
        try:
            while True:
                base_prompt = prompt or self._config.prompt_symbol
                p = base_prompt if not lines else continuation
                line = await self._session.prompt_async(p)
                
                if not line and lines:
                    break
                lines.append(line)
            
            return "\n".join(lines)
        except (EOFError, KeyboardInterrupt):
            return None
```

## Theming

### Theme Configuration
```yaml
display:
  theme: "gruvbox-dark"
  markdown_enabled: true
  code_theme: "monokai"
  max_width: null       # null = terminal width
  timestamps: false
  spinner_style: "dots"
  prompt_symbol: "🐱 > "
  line_width: 80
  exchange_delimiter: "─"
  exchange_delimiter_length: 60
```

### Custom Theme File
```yaml
# ~/.config/cato/themes/custom.yaml
colors:
  user: "#61afef"
  assistant: "#98c379"
  system: "#5c6370"
  error: "#e06c75"
  warning: "#e5c07b"
  info: "#56b6c2"
  code_background: "#282c34"
```

### Theme Loading
```python
def _load_custom_theme(self, path: Path) -> Theme:
    """Load theme from YAML file."""
    with open(path) as f:
        data = yaml.safe_load(f)
    
    colors = data.get("colors", {})
    return Theme({
        "user": f"bold {colors.get('user', 'cyan')}",
        "assistant": f"bold {colors.get('assistant', 'green')}",
        "system": colors.get("system", "dim"),
        "error": f"bold {colors.get('error', 'red')}",
        "warning": f"bold {colors.get('warning', 'yellow')}",
        "info": f"bold {colors.get('info', 'blue')}",
        "code": f"on {colors.get('code_background', 'grey23')}",
    })
```

## Context Display
Context display is a debug-only view. Context injection into the LLM request always occurs when vector store retrieval passes the similarity threshold.

### Retrieved Context
```python
class ContextDisplay:
    """Display retrieved context from vector store."""
    
    def __init__(self, display: Display) -> None:
        self._display = display
    
    def show_context(
        self,
        context_items: list[str],
        scores: list[float] | None = None,
    ) -> None:
        """
        Display context excerpts.
        
        Parameters
        ----------
        context_items
            Retrieved context strings.
        scores
            Optional similarity scores.
        """
        self._display.show_info(f"Found {len(context_items)} relevant context items:")
        
        for i, item in enumerate(context_items):
            score_str = f" (score: {scores[i]:.2f})" if scores else ""
            
            # Truncate long items
            preview = item[:200] + "..." if len(item) > 200 else item
            preview = preview.replace("\n", " ")
            
            self._display.show_info(f"  [{i+1}]{score_str} {preview}")
```

## Output Formatting

### Response Formatter
```python
class ResponseFormatter:
    """Format assistant responses for display."""
    
    def __init__(self, config: DisplayConfig) -> None:
        self._config = config
    
    def format(self, content: str) -> str:
        """
        Format response content.
        
        Parameters
        ----------
        content
            Raw response content.
        
        Returns
        -------
        str
            Formatted content.
        """
        if not self._config.markdown_enabled:
            return self._strip_markdown(content)
        return content
    
    def _strip_markdown(self, content: str) -> str:
        """Remove markdown formatting for plain text display."""
        # Basic markdown stripping
        import re
        
        # Remove code blocks (keep content)
        content = re.sub(r"```\w*\n?", "", content)
        
        # Remove inline code backticks
        content = re.sub(r"`([^`]+)`", r"\1", content)
        
        # Remove bold/italic
        content = re.sub(r"\*\*([^*]+)\*\*", r"\1", content)
        content = re.sub(r"\*([^*]+)\*", r"\1", content)
        content = re.sub(r"__([^_]+)__", r"\1", content)
        content = re.sub(r"_([^_]+)_", r"\1", content)
        
        # Remove headers
        content = re.sub(r"^#+\s+", "", content, flags=re.MULTILINE)
        
        return content
```

## Progress Display

### Progress Bar
```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

class ProgressDisplay:
    """Display progress for long operations."""
    
    def __init__(self, console: Console) -> None:
        self._console = console
    
    @contextmanager
    def progress(self, description: str, total: int | None = None):
        """
        Create progress context.
        
        Parameters
        ----------
        description
            Progress description.
        total
            Total items (None for indeterminate).
        """
        if total:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=self._console,
            ) as progress:
                task = progress.add_task(description, total=total)
                yield lambda n=1: progress.update(task, advance=n)
        else:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self._console,
            ) as progress:
                progress.add_task(description, total=None)
                yield lambda: None


# Usage
with display.progress("Processing documents", total=len(files)) as advance:
    for file in files:
        process(file)
        advance()
```

## Configuration

### Display Config
```python
class DisplayConfig(BaseModel):
    """Display configuration."""
    
    theme: str = "default"
    markdown_enabled: bool = True
    code_theme: str = "monokai"
    max_width: int | None = Field(ge=40, default=None)
    timestamps: bool = False
    spinner_style: str = "dots"  # dots, line, moon, etc.
    prompt_symbol: str = "🐱 > "
    line_width: int = 80
    exchange_delimiter: str = "─"
    exchange_delimiter_length: int = 60
```

## Integration

### Bootstrap
```python
def create_display(config: CatoConfig) -> Display:
    """
    Create display instance.
    
    Parameters
    ----------
    config
        Application configuration.
    
    Returns
    -------
    Display
        Configured display instance.
    """
    return RichDisplay(config.display)


def create_input_handler(config: CatoConfig) -> InputHandler:
    """
    Create input handler.
    
    Parameters
    ----------
    config
        Application configuration.
    
    Returns
    -------
    InputHandler
        Configured input handler.
    """
    history_path = expand_path(config.commands.history_file)
    history_path.parent.mkdir(parents=True, exist_ok=True)
    return InputHandler(config.display, history_path)
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





**File Glob Results:**





**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/agents.md**
```
This directory contains the project specs

```




**Command Executed:**
```bash
git --no-pager status -sb
```

**Output:**
```
## main...origin/main [ahead 1]
?? 20260115_191803-Run_Cato_Command_Instructions.md
```


**Command Executed:**
```bash
git checkout -b feature/display-style-config
```

**Output:**
```
Switched to a new branch 'feature/display-style-config'
```



**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CONFIGURATION.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CONFIGURATION.md
@@ -119,6 +119,9 @@
 | line_width | int | 80 | Terminal width for response formatting (chars) |
 | exchange_delimiter | string | ─ | Character for separation |
 | exchange_delimiter_length | int | 60 | Delimiter line length |
+| style_overrides | dict | {} | Rich style overrides keyed by role (user, assistant, system, error, warning, info, code) |
+| prompt_style | string | null | prompt_toolkit style for the prompt (null uses theme/default) |
+| input_style | string | null | prompt_toolkit style for input text (null uses theme/default) |
 
 
 ### Logging Configuration (`logging`)

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/CONFIG_REFERENCE.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/CONFIG_REFERENCE.md
@@ -71,6 +71,9 @@
 - `line_width`
 - `exchange_delimiter`
 - `exchange_delimiter_length`
+- `style_overrides`
+- `prompt_style`
+- `input_style`
 
 ### Logging (`logging`)
 - `level` (`DEBUG | INFO | WARNING | ERROR`)

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DISPLAY.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DISPLAY.md
@@ -184,15 +184,24 @@
             }),
         }
         
+        theme = themes.get("default")
         if theme_name in themes:
-            return themes[theme_name]
+            theme = themes[theme_name]
         
         # Try to load custom theme from file
         custom_path = Path(f"~/.config/cato/themes/{theme_name}.yaml").expanduser()
         if custom_path.exists():
-            return self._load_custom_theme(custom_path)
+            theme = self._load_custom_theme(custom_path)
         
-        return themes["default"]
+        return self._apply_style_overrides(theme, self._config.style_overrides)
+
+    def _apply_style_overrides(self, theme: Theme, overrides: dict[str, str]) -> Theme:
+        """Apply style overrides to a base theme."""
+        if not overrides:
+            return theme
+        merged = dict(theme.styles)
+        merged.update(overrides)
+        return Theme(merged)
     
     def show_message(self, message: DisplayMessage) -> None:
         """Display a message with role-based styling."""
@@ -364,6 +373,11 @@
     
     def _get_style(self) -> Style:
         """Get prompt style based on theme."""
+        if self._config.prompt_style or self._config.input_style:
+            return Style.from_dict({
+                "prompt": self._config.prompt_style or "cyan bold",
+                "": self._config.input_style or "",
+            })
         if self._config.theme == "gruvbox-dark":
             return Style.from_dict({
                 "prompt": "#83a598 bold",
@@ -440,6 +454,11 @@
   line_width: 80
   exchange_delimiter: "─"
   exchange_delimiter_length: 60
+  style_overrides:
+    assistant: "bold #b8bb26"
+    system: "#928374"
+  prompt_style: "#83a598 bold"
+  input_style: "#ebdbb2"
 ```
 
 ### Custom Theme File
@@ -631,6 +650,9 @@
     line_width: int = 80
     exchange_delimiter: str = "─"
     exchange_delimiter_length: int = 60
+    style_overrides: dict[str, str] = Field(default_factory=dict)
+    prompt_style: str | None = None
+    input_style: str | None = None
 ```
 
 ## Integration

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md
@@ -188,6 +188,9 @@
     line_width: int
     exchange_delimiter: str
     exchange_delimiter_length: int
+    style_overrides: dict[str, str]
+    prompt_style: str | None
+    input_style: str | None
 ```
 
 ### Logging Configuration
@@ -519,6 +522,9 @@
   line_width: 80
   exchange_delimiter: "─"
   exchange_delimiter_length: 60
+  style_overrides: {}
+  prompt_style: null
+  input_style: null
 
 commands:
   prefix: "/"

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DISPLAY.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DISPLAY.md
@@ -461,6 +461,8 @@
   input_style: "#ebdbb2"
 ```
 
+`style_overrides` is applied after the base theme (built-in or custom theme file). Keys should match the display role styles used by Rich (`user`, `assistant`, `system`, `error`, `warning`, `info`, `code`).
+
 ### Custom Theme File
 ```yaml
 # ~/.config/cato/themes/custom.yaml

```




**Command Executed:**
```bash
git --no-pager status -sb
```

**Output:**
```
## feature/display-style-config
 M Project/Spec/CONFIG_REFERENCE.md
 M Project/Spec/functional/SPEC_CONFIGURATION.md
 M Project/Spec/technical/TECH_CONFIG_SYSTEM.md
 M Project/Spec/technical/TECH_DISPLAY.md
?? Project/Sessions/20260115_191803-Run_Cato_Command_Instructions.md
```

I’ve updated the specs to let you control styles directly in config via `display.style_overrides` (Rich role styles) plus `display.prompt_style` and `display.input_style` (prompt_toolkit). Default config in the spec now includes these keys, and style overrides are applied after the base theme.

Example config:

```yaml
display:
  theme: "gruvbox-dark"
  style_overrides:
    user: "bold #83a598"
    assistant: "bold #b8bb26"
    system: "#928374"
    error: "bold #fb4934"
  prompt_style: "#83a598 bold"
  input_style: "#ebdbb2"
```
Do you want different key names or additional style hooks beyond the role/prompt/input styles?

Summary: Updated the configuration and display specs to support inline style overrides and prompt/input styling in config.