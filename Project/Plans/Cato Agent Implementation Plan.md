# Cato Full Implementation Plan
## Problem Statement
Implement Cato from scratch as a terminal-first LLM chat client with productivity features, following the specifications in `Project/Spec/`. This is a greenfield implementation requiring all architectural layers to be built.
## Guiding Principles
* **Spec-driven**: Functional and technical specs are authoritative
* **Layered architecture**: Core → Storage → Providers → Services → Commands → Presentation
* **No hard-coded defaults**: All defaults in YAML, validated by Pydantic
* **Dependency injection**: Components receive dependencies at construction
* **MVP-first**: Core chat loop functional before productivity/vector features
## Implementation Phases
***
# Phase 1: Project Skeleton & Core
**Goal**: Runnable entry point with config loading and error hierarchy.
## 1.1 Project Setup
* Create `pyproject.toml` with uv/PEP 621 metadata
* Define dependencies: pydantic, pyyaml, rich, prompt_toolkit, httpx, aiosqlite, chromadb, openai, anthropic, google-generativeai, pydantic-ai
* Create directory structure per `TECH_ARCHITECTURE.md (218-325)`
* Create `cato/__init__.py`, `cato/__main__.py`, `cato/main.py`
Files:
* `pyproject.toml`
* `cato/__init__.py`
* `cato/__main__.py`
* `cato/main.py`
## 1.2 Core Module (`cato/core/`)
### 1.2.1 Exception Hierarchy
Implement `CatoError` and all subclasses per `TECH_ERROR_HANDLING.md (36-169)`:
* `ConfigurationError`, `ConfigFileNotFoundError`, `ConfigValidationError`
* `LLMError`, `LLMConnectionError`, `LLMAuthenticationError`, `LLMRateLimitError`, `LLMContextLengthError`, `LLMResponseError`
* `VectorStoreError`, `VectorStoreConnectionError`, `EmbeddingError`
* `StorageError`, `StorageConnectionError`, `StorageQueryError`
* `CommandError`, `CommandNotFoundError`, `CommandArgumentError`, `CommandExecutionError`
* `IOError`, `FileAccessError`, `NetworkError`
* `DisplayError`
Files:
* `cato/core/__init__.py`
* `cato/core/exceptions.py`
* `cato/core/README.md`
### 1.2.2 Logging Setup
Implement logging per `TECH_ERROR_HANDLING.md (239-277)`:
* `setup_logging(config: LoggingConfig)` function
* Console handler (always) + rotating file handler (if configured)
* Module-level `logger = logging.getLogger(__name__)` pattern
Files:
* `cato/core/logging.py`
### 1.2.3 Shared Types
Define data classes per `DATA_MODELS.md` and `TECH_LLM_INTEGRATION.md (13-29)`:
* `Message(role, content)` — Pydantic BaseModel
* `TokenUsage(prompt_tokens, completion_tokens, total_tokens)`
* `CompletionResult(content, model, usage, finish_reason)`
* `ConversationExchange` for vector store
Files:
* `cato/core/types.py`
### 1.2.4 Configuration System
Implement per `TECH_CONFIG_SYSTEM.md` and `SPEC_CONFIGURATION.md`:
* `cato/resources/defaults.yaml` — all defaults with inline docs
* Pydantic models for each config section: `LLMConfig`, `VectorStoreConfig`, `DisplayConfig`, `LoggingConfig`, `StorageConfig`, `TTSConfig`, `WebSearchConfig`, `CommandsConfig`, `PathsConfig`
* Root `CatoConfig` model
* `load_config(path: Path | None) -> CatoConfig` with overlay logic
* Environment variable expansion (`${VAR}` syntax)
* CLI override application
Files:
* `cato/core/config.py`
* `cato/resources/defaults.yaml`
***
# Phase 2: Storage Layer
**Goal**: SQLite database operational for productivity data.
## 2.1 Database Foundation (`cato/storage/`)
Implement per `TECH_STORAGE.md`:
* `Database` class with async SQLite connection via `aiosqlite`
* `connect()`, `close()`, `execute()`, `fetchone()`, `fetchall()`
* Migration system with `Migration` dataclass and `MIGRATIONS` list
* Schema: `tasks`, `lists`, `list_items`, `sessions`, `threads`, `migrations`
Files:
* `cato/storage/__init__.py`
* `cato/storage/README.md`
* `cato/storage/database.py`
* `cato/storage/migrations.py`
## 2.2 Repository Protocol & Implementations
Generic `Repository[T]` protocol per `TECH_STORAGE.md (87-114)`.
Implement:
* `TaskRepository` — CRUD for tasks with filtering/sorting
* `ListRepository` — CRUD for lists
* `ListItemRepository` — CRUD for list items
* `SessionRepository` — session/thread tracking
Files:
* `cato/storage/repositories/__init__.py`
* `cato/storage/repositories/base.py`
* `cato/storage/repositories/tasks.py`
* `cato/storage/repositories/lists.py`
* `cato/storage/repositories/sessions.py`
## 2.3 Storage Service
Unified `Storage` class exposing all repositories per `TECH_STORAGE.md (458-501)`.
* `create_storage(config) -> Storage` factory
Files:
* `cato/storage/service.py`
***
# Phase 3: Provider Layer
**Goal**: LLM providers abstracted and swappable.
## 3.1 LLM Provider Protocol
Define `LLMProvider` protocol per `TECH_LLM_INTEGRATION.md (32-117)`:
* `name`, `model` properties
* `complete(messages, temperature, max_tokens) -> CompletionResult`
* `complete_stream(messages, ...) -> AsyncIterator[str]`
* `count_tokens(text) -> int`
Files:
* `cato/providers/__init__.py`
* `cato/providers/README.md`
* `cato/providers/llm/__init__.py`
* `cato/providers/llm/base.py`
## 3.2 Provider Implementations
Implement each per `TECH_LLM_INTEGRATION.md (122-303)`:
* `OpenAIProvider` — using `openai` SDK
* `AnthropicProvider` — using `anthropic` SDK
* `GoogleProvider` — using `google-generativeai`
* `OllamaProvider` — using `httpx` to local endpoint
Each maps provider-specific errors to `CatoError` hierarchy.
Files:
* `cato/providers/llm/openai.py`
* `cato/providers/llm/anthropic.py`
* `cato/providers/llm/google.py`
* `cato/providers/llm/ollama.py`
## 3.3 Provider Factory
Registry pattern per `TECH_LLM_INTEGRATION.md (306-376)`:
* `@register_provider(name)` decorator
* `create_provider(config) -> LLMProvider`
Files:
* `cato/providers/llm/factory.py`
***
# Phase 4: Display Layer
**Goal**: Rich terminal output and prompt_toolkit input.
## 4.1 Display Protocol
Define `Display` protocol per `TECH_DISPLAY.md (9-132)`:
* `show_message()`, `show_error()`, `show_warning()`, `show_info()`
* `show_markdown()`, `show_code()`, `show_table()`
* `show_spinner() -> SpinnerContext`
* `clear()`, `show_welcome()`
Files:
* `cato/display/__init__.py`
* `cato/display/README.md`
* `cato/display/base.py`
## 4.2 Rich Implementation
Implement `RichDisplay` per `TECH_DISPLAY.md (136-297)`:
* Console setup with theme support
* Built-in themes: `default`, `gruvbox-dark`
* Custom theme loading from `~/.config/cato/themes/`
* `SpinnerContext` context manager
Files:
* `cato/display/console.py`
* `cato/display/themes.py`
## 4.3 Input Handler
Implement per `TECH_DISPLAY.md (337-439)`:
* `InputHandler` using `prompt_toolkit.PromptSession`
* `FileHistory` for command history
* Key bindings: Ctrl+C (cancel), Ctrl+D (exit)
* `get_input()`, `get_multiline_input()`
Files:
* `cato/display/input.py`
## 4.4 Response Formatting
* `ResponseFormatter` for markdown stripping when disabled
* `ContextDisplay` for showing retrieved context
Files:
* `cato/display/formatting.py`
***
# Phase 5: Command Framework
**Goal**: Slash command registration and execution infrastructure.
## 5.1 Command Protocol & Registry
Implement per `TECH_COMMAND_FRAMEWORK.md`:
* `Command` protocol with `name`, `aliases`, `description`, `usage`, `execute()`
* `CommandResult` dataclass
* `CommandContext` dataclass with injected dependencies
* `@command` decorator for registration
* `CommandRegistry` with alias resolution
* `parse_command_input()` using `shlex`
Files:
* `cato/commands/__init__.py`
* `cato/commands/README.md`
* `cato/commands/base.py`
* `cato/commands/registry.py`
* `cato/commands/parser.py`
## 5.2 Command Executor
Implement `CommandExecutor` per `TECH_COMMAND_FRAMEWORK.md (303-365)`:
* Parse input, lookup command, create context, execute
* Error mapping to `CommandResult`
Files:
* `cato/commands/executor.py`
## 5.3 Command Discovery
Auto-import pattern per `TECH_COMMAND_FRAMEWORK.md (530-550)`:
* `discover_commands()` imports all modules in `cato/commands/`
Files:
* Update `cato/commands/__init__.py`
***
# Phase 6: Core Services
**Goal**: Chat service orchestrating LLM interactions.
## 6.1 Conversation Management
Implement `Conversation` class per `TECH_LLM_INTEGRATION.md (380-436)`:
* `system_prompt`, `messages` list
* `add_user_message()`, `add_assistant_message()`
* `to_messages() -> list[Message]`
* `truncate_to_tokens(max_tokens, counter)`
Files:
* `cato/services/__init__.py`
* `cato/services/README.md`
* `cato/services/conversation.py`
## 6.2 Chat Service
Orchestrate LLM calls per `SPEC_CORE_CHAT.md`:
* `ChatService` with injected `LLMProvider`, `VectorStore | None`, config
* `send_message(content) -> str` — context retrieval, API call, history update
* System prompt loading from files
* Retry logic per `TECH_LLM_INTEGRATION.md (463-504)`
Files:
* `cato/services/chat.py`
***
# Phase 7: Application Bootstrap & REPL
**Goal**: Runnable application with basic chat.
## 7.1 Bootstrap Module
Wire all components per `TECH_ARCHITECTURE.md (177-214)`:
* `create_application(config_path) -> Application`
* Instantiate config, providers, storage, services, commands, display
Files:
* `cato/bootstrap.py`
## 7.2 Application Class & REPL
Implement `Application` class:
* `run()` — main REPL loop
* Input routing: slash command vs chat
* Graceful shutdown, Ctrl+C handling
* Welcome message display per `SPEC_OVERVIEW.md (76-99)`
Files:
* `cato/app.py`
## 7.3 CLI Entry Point
Implement per `SPEC_COMMAND_LINE.md`:
* `--config` path override
* `--debug` flag
* `--dummy-mode` for testing
Files:
* Update `cato/main.py`
***
# Phase 8: Core Commands (MVP)
**Goal**: Essential commands for usable chat client.
## 8.1 Core Commands
Implement per `SPEC_COMMAND_SYSTEM.md`:
* `/help` — overview, topics, commands (defer `/help model` to Phase 11)
* `/exit`, `/quit`, `/q` — exit application
* `/clear` — clear history and screen
* `/config` — show current config
Files:
* `cato/commands/core.py`
## 8.2 History Commands
* `/history [n]` — show history
* `/delete [n]` — remove exchanges
* `/model [name]` — show/change model
* `/showsys` — show system prompt
* `/loglevel [level]` — change log level
Files:
* `cato/commands/history.py`
## 8.3 Context Commands
* `/showcontext [on|off|summary]` — toggle context display
* `/casual [on|off]` — toggle casual mode
Files:
* `cato/commands/context.py`
***
# Phase 9: Vector Store Integration
**Goal**: Conversation memory with similarity search.
## 9.1 Vector Store Protocol
Define per `TECH_ARCHITECTURE.md (117-145)` and `TECH_VECTOR_STORE.md`:
* `VectorStore` protocol: `add()`, `search()`, `get()`, `delete()`, `count()`
Files:
* `cato/storage/vector/__init__.py`
* `cato/storage/vector/base.py`
## 9.2 ChromaDB Implementation
* `ChromaDBStore` implementing protocol
* Embedding via configured provider (OpenAI or Ollama)
* Collection management
Files:
* `cato/storage/vector/chromadb.py`
## 9.3 Vector Commands
* `/vadd` — add text to store
* `/vdoc` — add document with chunking
* `/vquery` — query store
* `/vstats` — show statistics
* `/vdelete` — delete by ID
* `/vget` — retrieve by ID/session/thread
Files:
* `cato/commands/vector.py`
## 9.4 Chat Service Integration
Update `ChatService` to:
* Retrieve context before LLM call
* Store exchanges after response
* Respect `context_results`, `similarity_threshold` config
Files:
* Update `cato/services/chat.py`
***
# Phase 10: Productivity System
**Goal**: Task and list management via dedicated agent.
## 10.1 Productivity Service
* `ProductivityService` wrapping task/list repositories
* Query methods with filtering/sorting for `/st` and `/list`
* No agent for MVP read operations — direct repository calls
Files:
* `cato/services/productivity.py`
## 10.2 Productivity Commands
Implement per `SPEC_PRODUCTIVITY.md` and `SPEC_COMMAND_SYSTEM.md (310-336)`:
* `/st` — show tasks with `-s`, `-o`, `-p`, `-c`, `-S` options
* `/list` — show lists or list items
* Display using tables per spec (emoji status indicators)
Files:
* `cato/commands/productivity.py`
## 10.3 Productivity Agent (Optional Enhancement)
If LLM-assisted querying is desired:
* `ProductivityAgent` using pydantic-ai
* Tool functions wrapping repository methods
* Structured output schema for display
* Agent does NOT write to vector store or chat history
Files:
* `cato/services/agents/__init__.py`
* `cato/services/agents/productivity.py`
***
# Phase 11: Help System
**Goal**: Comprehensive in-app help.
## 11.1 Help Content Structure
Create per `TECH_HELP_SYSTEM.md`:
* `cato/resources/help/index.yaml` — navigation + command index
* `cato/resources/help/topics/overview.md`
* `cato/resources/help/topics/commands.md`
* `cato/resources/help/commands/<command>.md` for each command
Files:
* `cato/resources/help/` directory tree
## 11.2 Help Service
* Load and parse `index.yaml`
* Resolve topics, categories, commands
* Render markdown via display layer
Files:
* `cato/services/help.py`
## 11.3 Help Command Completion
* `/help` — render overview
* `/help commands` — render command list from index
* `/help <topic>` — render topic page
* `/help <command>` — render command help
* `/help model "question"` — one-off LLM query against help docs (not added to history)
Files:
* Update `cato/commands/core.py`
***
# Phase 12: File Operations
**Goal**: File commands for context attachment and export.
## 12.1 File Commands
Implement per `SPEC_FILE_OPERATIONS.md` and `SPEC_COMMAND_SYSTEM.md (169-256)`:
* `/attach` — attach files to context
* `/pwd` — show cwd
* `/cd` — change directory
* `/ls` — list directory
* `/cat` — display file
* `/locations` — show aliases
Files:
* `cato/commands/files.py`
## 12.2 Export Commands
* `/writecode` — extract code blocks
* `/writejson` — export to JSON
* `/writemd`, `/w` — export to markdown
* `/writemdall` — export with system prompts
* `/writeresp` — export last exchange
* `/append` — append to file
* `/copy` — copy to clipboard
Files:
* `cato/commands/export.py`
***
# Phase 13: Web & TTS Features
**Goal**: Optional external integrations.
## 13.1 Web Search
Implement per `SPEC_WEB_SEARCH.md`:
* `/web "query" [engine]` — search and add to context
* `/url <url>` — fetch and attach content
* Search provider abstraction (DuckDuckGo, Google, Bing)
Files:
* `cato/providers/search/__init__.py`
* `cato/providers/search/base.py`
* `cato/providers/search/duckduckgo.py`
* `cato/services/web.py`
* `cato/commands/web.py`
## 13.2 TTS
Implement per `SPEC_TTS.md`:
* `/speak [voice] [model]` — speak last response
* `/speaklike "instructions" [voice] [model]` — speak with custom style
* OpenAI TTS provider
Files:
* `cato/providers/tts/__init__.py`
* `cato/providers/tts/base.py`
* `cato/providers/tts/openai.py`
* `cato/services/tts.py`
* `cato/commands/tts.py`
***
# Phase 14: Thread Continuation & Sessions
**Goal**: Resume previous conversations.
## 14.1 Thread Commands
* `/continue <thread_id>` — resume thread from vector store
* Session/thread ID tracking in storage
Files:
* Update `cato/commands/context.py`
* Update `cato/services/chat.py`
***
# Phase 15: Testing & Validation
**Goal**: Test coverage for core functionality.
## 15.1 Test Infrastructure
* `tests/conftest.py` — shared fixtures
* Mock LLM provider, mock vector store, temp SQLite
Files:
* `tests/__init__.py`
* `tests/conftest.py`
## 15.2 Unit Tests
* Config loading and validation
* Exception hierarchy
* Command parsing
* Repository CRUD
Files:
* `tests/unit/test_config.py`
* `tests/unit/test_exceptions.py`
* `tests/unit/test_commands.py`
* `tests/unit/test_repositories.py`
## 15.3 Integration Tests
* Chat service with mock LLM
* Productivity flows with temp DB
* Vector store operations
Files:
* `tests/integration/test_chat.py`
* `tests/integration/test_productivity.py`
* `tests/integration/test_vector.py`
## 15.4 Validation
* Help system consistency checks per `TECH_HELP_SYSTEM.md (82-95)`
* All registered commands have help entries
***
# Phase 16: Documentation & Polish
**Goal**: Production-ready documentation.
## 16.1 Code Documentation
* README.md for each module directory
* NumPy-format docstrings on all public functions/classes
* Inline comments for non-obvious logic
## 16.2 User Documentation
* Top-level README.md with installation, quickstart
* CHANGELOG.md
* CONFIG_REFERENCE.md sync with implementation
## 16.3 AI Navigation
* `AGENTS.md` / `WARP.md` at repo root (already exists)
* `agents.md` in subdirectories per `TECH_CODE_ORGANISATION.md`
***
# Dependency Order Summary
```warp-runnable-command
Phase 1 (Core) → Phase 2 (Storage) → Phase 3 (Providers) → Phase 4 (Display)
       ↓
Phase 5 (Commands) → Phase 6 (Services) → Phase 7 (Bootstrap/REPL)
       ↓
Phase 8 (Core Commands) → [MVP checkpoint: basic chat works]
       ↓
Phase 9 (Vector) → Phase 10 (Productivity) → Phase 11 (Help)
       ↓
Phase 12 (Files) → Phase 13 (Web/TTS) → Phase 14 (Threads)
       ↓
Phase 15 (Tests) → Phase 16 (Docs)
```
***
# Open Decisions
1. **Productivity agent**: Phase 10.3 is optional. MVP can use direct repository calls without LLM. Add agent only if natural-language task queries are needed later.
2. **Vector store embedding provider**: Default to OpenAI `text-embedding-3-small`. Ollama support deferred unless explicitly needed.
3. **Thread continuation**: Phase 14 can be deferred if MVP scope is tight.
4. **TTS/Web**: Phase 13 is optional for MVP.
