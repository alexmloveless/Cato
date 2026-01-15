USER:
is there anything in the specs relating to the test framework, creating and maintaining tests, test prardigm?

AGENT:


**Grep Results:**

- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083124-Design_Project_Architecture_Approach.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_084913-Review_Repo_Specs_with_Critique_Report_GPT-5_2-high.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-15_171104-Comprehensive_Codebase_Quality_Review.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083057-Critically_Review_Repo_Specs.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_170144-Create_Command_Line_Args_Specs.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_WEB_SEARCH.md**
- **/home/alex/Documents/repos/Cato/WARP.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083135-Create_WARP_md_for_Codebase.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-14_spec_review_claude_opus_4_5.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083112-Update_WARP_md_With_Spec_Changes.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083219-Read_And_Follow_FULL_SPEC_PROMPT_md.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083007-Remove_Memory_Creation_References.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_083151-Design_Project_Architecture_Approach.md**
- **/home/alex/Documents/repos/Cato/Project/Sessions/20260115_165050-Process_Comments_in_Reports_Summary.md**




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



Yes—testing is specified fairly explicitly. The key spec is `Project/Spec/technical/TECH_DEVELOPMENT.md`, and there are supporting notes in `Project/Spec/technical/TECH_ARCHITECTURE.md`.

**Highlights from the specs:**
- **Test framework**: **pytest** (with `pytest-cov` and `pytest-asyncio` in dev deps).  
  See `TECH_DEVELOPMENT.md` → *Unit Tests*, *Running Tests*, and *pyproject.toml* sections.
- **Test paradigm**: **test pyramid** (many unit, some integration, few E2E).  
  See `TECH_DEVELOPMENT.md` → *Test Pyramid*.
- **What to test**: unit tests for config validation, command parsing, utilities; integration tests for service+storage and command+service; E2E for core REPL flows.  
  See `TECH_DEVELOPMENT.md` → *Unit Tests*, *Integration Tests*, *End-to-End Tests*.
- **What not to test**: third‑party internals, brittle formatting, exhaustive error paths, perf benchmarks (initially).  
  See `TECH_DEVELOPMENT.md` → *What NOT to Test*.
- **Test organization**: `tests/unit`, `tests/integration`, `tests/e2e`, shared `conftest.py`.  
  See `TECH_DEVELOPMENT.md` → *Test Organisation*.
- **Maintenance/CI**: fast CI (<5 min), run unit+integration on PRs, E2E only on `main`.  
  See `TECH_DEVELOPMENT.md` → *Continuous Integration*.
- **Testability principle**: dependency injection + protocols to make components easy to mock.  
  See `TECH_ARCHITECTURE.md` → *Design Goals* and *Protocol-Based Abstractions*.

If you want, I can pull specific excerpts or point you to exact line ranges.