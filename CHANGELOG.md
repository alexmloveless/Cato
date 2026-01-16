# Changelog

All notable changes to Cato will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Phase 16: Documentation & Polish (2026-01-16)

#### Added
- Comprehensive README.md with installation, quickstart, and feature documentation
- CHANGELOG.md documenting all implementation phases
- CONFIG_REFERENCE.md for complete configuration guide
- Module-level documentation files

#### Changed
- Enhanced code documentation with NumPy-style docstrings
- Improved inline comments for complex logic

### Phase 15: Testing & Validation (2026-01-16)

#### Added
- Comprehensive test suite with 128+ passing tests
- Unit tests for configuration system (20+ tests)
- Unit tests for exception hierarchy (40+ tests)
- Unit tests for command parsing (30+ tests)
- Unit tests for repositories (25+ tests)
- Integration tests for chat service (15+ tests)
- Integration tests for productivity workflows (6+ tests)
- Integration tests for vector store operations (8+ tests)
- Help system validation tests
- Mock LLM provider and vector store for testing
- pytest fixtures for async testing
- Test infrastructure with conftest.py

#### Documentation
- Test coverage documentation
- Testing guidelines and patterns

### Phase 14: Thread Continuation & Sessions (2026-01-16)

#### Added
- `/continue` command to resume previous conversation threads
- `/cont` alias for continue command
- `ChatService.continue_thread()` method
- Thread loading from vector store by session ID
- Chronological reconstruction of conversation history
- Help documentation for thread continuation
- Session ID tracking and management

#### Changed
- Enhanced vector store querying with session filtering
- Updated help index with continue command

### Phase 13: Web Search and TTS Features (2026-01-16)

#### Added
- `/web` command for web search with content extraction
- `/url` command to fetch and attach URL content
- `/url_store` command to save URL content to vector store
- `/speak` command for text-to-speech of last response
- `/speaklike` command for TTS with custom instructions
- OpenAI TTS provider integration
- Web search provider abstraction
- DuckDuckGo search integration
- Voice selection (alloy, echo, fable, nova, onyx, shimmer)
- TTS model selection (tts-1, tts-1-hd)
- Markdown cleaning for TTS output
- Audio playback support (mpg123, ffplay, afplay)

#### Configuration
- `tts.enabled`, `tts.voice`, `tts.model`, `tts.audio_dir` settings
- `web_search.enabled`, `web_search.default_engine` settings

### Phase 11: Help System (2026-01-16)

#### Added
- Comprehensive in-app help system
- `cato/resources/help/index.yaml` navigation structure
- Help topics and categories
- Command-specific help files
- `/help model "question"` for LLM-assisted help queries
- Help content organization by category

#### Documentation
- Complete help files for all commands
- Help system architecture documentation

### Phase 10: Productivity System (2026-01-16)

#### Added
- `/st` command for task management
  - Status filtering (`-s`)
  - Priority filtering (`-p`)
  - Category filtering (`-c`)
  - Sorting options (`-o`)
  - Search functionality (`-S`)
- `/list` command for list management
- Task repository with CRUD operations
- List repository with CRUD operations
- SQLite-based productivity data storage
- Emoji status indicators
- Rich table formatting for task/list display

#### Configuration
- Storage configuration for database paths
- Task and list schemas in migrations

### Phase 9: Vector Store Integration (2026-01-16)

#### Added
- ChromaDB vector store integration
- `/vadd` command to add text to vector store
- `/vdoc` command to add documents with chunking
- `/vquery` command for similarity search
- `/vstats` command for store statistics
- `/vdelete` command to remove documents
- `/vget` command to retrieve by ID
- Automatic conversation exchange storage
- Context retrieval for chat messages
- OpenAI embedding provider
- Semantic search with cosine similarity

#### Configuration
- `vector_store.enabled`, `vector_store.backend`
- `vector_store.path`, `vector_store.collection_name`
- `vector_store.context_results`, `vector_store.similarity_threshold`
- Chunking strategy configuration
- Embedding provider settings

### Phase 8: Core Commands (MVP) (2026-01-16)

#### Added
- `/help` command for help system
- `/exit`, `/quit`, `/q` commands
- `/clear` command to clear conversation
- `/config` command to show configuration
- `/history` command to view message history
- `/delete` command to remove exchanges
- `/model` command to change LLM model
- `/showsys` command to display system prompt
- `/loglevel` command to change log level
- `/showcontext` command to toggle context display
- `/casual` command to toggle casual mode

### Phase 7: Application Bootstrap & REPL (2026-01-15)

#### Added
- Main application entry point (`cato/main.py`)
- Application class with REPL loop (`cato/app.py`)
- Bootstrap module for dependency injection (`cato/bootstrap.py`)
- CLI argument parsing (--config, --debug, --dummy-mode)
- Welcome message display
- Graceful shutdown handling
- Ctrl+C interrupt handling
- Input routing (commands vs chat)

### Phase 6: Core Services (2026-01-15)

#### Added
- `ChatService` for LLM interaction orchestration
- `Conversation` class for message management
- System prompt loading from files
- Conversation history truncation
- Token counting integration
- Retry logic for transient failures
- Exponential backoff for rate limits
- Message exchange tracking

#### Features
- Context window management
- Temperature and max_tokens overrides
- Streaming response support

### Phase 5: Command Framework (2026-01-15)

#### Added
- `Command` protocol definition
- `@command` decorator for registration
- `CommandRegistry` for lookup and execution
- `CommandExecutor` for command execution
- `CommandContext` for dependency injection
- Command parser with shlex tokenization
- Alias resolution system
- Automatic command discovery

#### Features
- Shell-like argument parsing
- Quoted string support
- Error handling and mapping

### Phase 4: Display Layer (2026-01-15)

#### Added
- `Display` protocol for terminal output
- `RichDisplay` implementation using Rich library
- Built-in themes (default, gruvbox-dark)
- Custom theme loading support
- `InputHandler` using prompt_toolkit
- File history for command persistence
- Key bindings (Ctrl+C, Ctrl+D)
- `ResponseFormatter` for markdown processing
- `ContextDisplay` for retrieved context
- Spinner context manager for loading states

#### Configuration
- `display.theme`, `display.markdown_enabled`
- `display.code_theme`, `display.max_width`
- `display.timestamps`, `display.spinner_style`

### Phase 3: Provider Layer (2026-01-15)

#### Added
- `LLMProvider` protocol
- OpenAI provider implementation
- Anthropic provider implementation
- Google Gemini provider implementation
- Ollama provider implementation
- Provider factory with registration system
- Error mapping to `CatoError` hierarchy
- Token counting support

#### Features
- Streaming completion support
- Provider-specific configuration
- API key management

### Phase 2: Storage Layer (2026-01-15)

#### Added
- `Database` class with async SQLite support
- Migration system with versioning
- `Repository` protocol for CRUD operations
- `TaskRepository` for task management
- `ListRepository` for list management
- `SessionRepository` for session tracking
- `Storage` service facade
- Database schema for tasks, lists, sessions

#### Features
- Automatic migrations on startup
- Transaction support
- Connection pooling

### Phase 1: Project Skeleton & Core (2026-01-15)

#### Added
- Project structure and organization
- `CatoError` exception hierarchy
- Configuration system with YAML overlay
- Pydantic models for validation
- Environment variable expansion (${VAR})
- Path expansion (~)
- CATO_* environment overrides
- Logging setup with rotation
- Core data types (Message, TokenUsage, CompletionResult)

#### Configuration
- `cato/resources/defaults.yaml` with comprehensive defaults
- Configuration overlay system
- Provider-specific config sections

## Initial Setup (2026-01-15)

#### Added
- Basic project structure
- pyproject.toml with dependencies
- Development tooling (pytest, ruff, mypy)
- Git repository initialization

---

## Version History

**Current Version**: 0.1.0 (Development)

All phases completed represent the MVP (Minimum Viable Product) implementation of Cato.
