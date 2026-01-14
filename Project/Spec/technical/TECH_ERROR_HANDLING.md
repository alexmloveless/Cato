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
- Invalid value type: Warn user, use default for that key
- Value out of range: Warn user, use default

### Example
```python
# On startup with invalid config value
"⚠️ Config warning: 'temperature' must be 0.0-2.0, got 5.0. Using default: 1.0"
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
