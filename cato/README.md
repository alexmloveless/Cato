# Cato Package

This is the main Python package for Cato, a terminal-first LLM chat client with productivity features.

## Package Structure

```
cato/
├── __init__.py           # Package initialization
├── __main__.py           # Entry point for `python -m cato`
├── main.py               # CLI entry point
├── app.py                # Main application and REPL loop
├── bootstrap.py          # Dependency injection and setup
│
├── commands/             # Slash command implementations
│   ├── base.py          # Command protocols
│   ├── registry.py      # Command registration
│   ├── parser.py        # Command input parsing
│   ├── executor.py      # Command execution
│   ├── core.py          # Core commands (/help, /exit, etc.)
│   ├── context.py       # Context commands (/continue)
│   ├── productivity.py  # Task/list commands
│   ├── vector.py        # Vector store commands
│   ├── web.py           # Web search commands
│   └── tts.py           # Text-to-speech commands
│
├── core/                 # Core abstractions
│   ├── config.py        # Configuration system
│   ├── exceptions.py    # Exception hierarchy
│   ├── types.py         # Shared data types
│   └── logging.py       # Logging setup
│
├── display/              # Terminal UI
│   ├── base.py          # Display protocol
│   ├── console.py       # Rich console implementation
│   ├── input.py         # Input handling
│   ├── themes.py        # Theme definitions
│   └── formatting.py    # Response formatting
│
├── providers/            # External service providers
│   ├── llm/             # LLM provider implementations
│   │   ├── base.py      # LLM protocol
│   │   ├── factory.py   # Provider factory
│   │   ├── openai.py    # OpenAI provider
│   │   ├── anthropic.py # Anthropic provider
│   │   ├── google.py    # Google Gemini provider
│   │   └── ollama.py    # Ollama provider
│   ├── search/          # Web search providers
│   │   ├── base.py      # Search protocol
│   │   └── duckduckgo.py
│   └── tts/             # Text-to-speech providers
│       ├── base.py      # TTS protocol
│       └── openai.py    # OpenAI TTS
│
├── resources/            # Static resources
│   ├── defaults.yaml    # Default configuration
│   ├── system_prompt.txt # Default system prompt
│   ├── help/            # Help documentation
│   │   ├── index.yaml   # Help navigation
│   │   ├── topics/      # Help topics
│   │   └── commands/    # Command help files
│   └── themes/          # Custom themes
│
├── services/             # Business logic
│   ├── chat.py          # Chat orchestration
│   ├── conversation.py  # Conversation management
│   ├── help.py          # Help system
│   ├── productivity.py  # Task/list management
│   ├── web.py           # Web search service
│   └── tts.py           # TTS service
│
└── storage/              # Data persistence
    ├── database.py      # SQLite connection
    ├── migrations.py    # Schema migrations
    ├── repositories/    # Data repositories
    │   ├── base.py      # Repository protocols
    │   ├── tasks.py     # Task repository
    │   ├── lists.py     # List repository
    │   └── sessions.py  # Session repository
    ├── vector/          # Vector store
    │   ├── base.py      # Vector store protocol
    │   └── chromadb.py  # ChromaDB implementation
    └── embedding/       # Embedding providers
        ├── base.py      # Embedding protocol
        └── openai.py    # OpenAI embeddings
```

## Architecture

Cato follows a layered architecture where each layer depends only on layers below it:

```
┌─────────────────────────────┐
│   Presentation Layer        │  app.py, main.py
│   (CLI, REPL)              │
└─────────────────────────────┘
            ↓
┌─────────────────────────────┐
│   Command Layer             │  commands/
│   (Slash commands)          │
└─────────────────────────────┘
            ↓
┌─────────────────────────────┐
│   Service Layer             │  services/
│   (Business logic)          │
└─────────────────────────────┘
            ↓
┌─────────────────────────────┐
│   Provider Layer            │  providers/
│   (External APIs)           │
└─────────────────────────────┘
            ↓
┌─────────────────────────────┐
│   Storage Layer             │  storage/
│   (Database, Vector store)  │
└─────────────────────────────┘
            ↓
┌─────────────────────────────┐
│   Core Layer                │  core/
│   (Config, Types, Errors)   │
└─────────────────────────────┘
```

## Key Patterns

### Dependency Injection

Components receive dependencies at construction rather than instantiating them:

```python
# Good: Dependencies injected
service = ChatService(
    provider=llm_provider,
    config=config,
    vector_store=vector_store,
)

# Bad: Internal instantiation
service = ChatService()  # Creates own dependencies
```

### Protocol-Based Design

Use protocols for interfaces, not abstract base classes:

```python
from typing import Protocol

class LLMProvider(Protocol):
    async def complete(self, messages: list[Message]) -> CompletionResult:
        ...
```

### Factory Pattern

Use factories for object creation with registration:

```python
@register_provider("openai")
class OpenAIProvider:
    ...

provider = create_provider(config)  # Returns registered provider
```

### Repository Pattern

Data access abstracted behind repositories:

```python
task_repo = TaskRepository(database)
tasks = await task_repo.filter_by(status="pending")
```

## Development

### Adding a New Command

1. Create command function in appropriate module
2. Register with `@command` decorator
3. Add help file in `resources/help/commands/`
4. Update `resources/help/index.yaml`

Example:

```python
from cato.commands.registry import command
from cato.commands.base import CommandContext, CommandResult

@command(name="mycommand", aliases=["mc"], description="My command")
async def my_command(ctx: CommandContext, *args: str) -> CommandResult:
    # Implementation
    return CommandResult(success=True, message="Done!")
```

### Adding a New Provider

1. Implement provider protocol in `providers/`
2. Register with factory decorator
3. Add configuration section in `core/config.py`
4. Update `resources/defaults.yaml`

### Adding a New Service

1. Create service class in `services/`
2. Inject dependencies in constructor
3. Expose via bootstrap module
4. Add to `CommandContext` if needed

## Testing

Tests are organized by type:

- `tests/unit/` - Unit tests for individual components
- `tests/integration/` - Integration tests for workflows
- `tests/conftest.py` - Shared fixtures and mocks

Run tests:

```bash
pytest                # All tests
pytest tests/unit/    # Unit tests only
pytest -v             # Verbose output
pytest --cov=cato     # With coverage
```

## Code Style

- **Formatting**: ruff (line length: 100)
- **Type checking**: mypy with strict mode
- **Docstrings**: NumPy format
- **Imports**: Organized by stdlib, third-party, local

## See Also

- [Project README](../README.md) - Installation and usage
- [CONFIG_REFERENCE.md](../CONFIG_REFERENCE.md) - Configuration guide
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [Project Specs](../Project/Spec/) - Technical specifications
