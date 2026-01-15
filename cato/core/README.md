# Core Module

This module contains foundational components used throughout Cato.

## Components

### `exceptions.py`
Complete exception hierarchy for the application. All exceptions inherit from `CatoError` base class.

**Exception categories:**
- **Configuration**: Config loading and validation errors
- **LLM**: Provider API errors (connection, auth, rate limits, etc.)
- **Vector Store**: ChromaDB and embedding errors
- **Storage**: SQLite database errors
- **Commands**: Command parsing and execution errors
- **I/O**: File and network access errors
- **Display**: Terminal rendering errors

### `logging.py`
Logging setup with console and optional file handlers.

### `config.py`
Configuration loading using YAML overlay system with Pydantic validation.

### `types.py`
Shared data classes used across modules (`Message`, `TokenUsage`, `CompletionResult`, etc.).

## Usage

```python
from cato.core import CatoError, LLMError, ConfigurationError
from cato.core.config import load_config
from cato.core.types import Message
```

## Design Principles

- **Single responsibility**: Each module has one clear purpose
- **Type safety**: Full type hints on all functions
- **No external dependencies on other Cato modules**: Core is the foundation layer
