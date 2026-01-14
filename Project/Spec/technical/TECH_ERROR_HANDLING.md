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

### Custom Exception Hierarchy
```python
class CatoError(Exception):
    """Base exception for Cato errors."""
    pass

class ConfigurationError(CatoError):
    """Configuration-related errors."""
    pass

class VectorStoreError(CatoError):
    """Vector store operation errors."""
    pass

class CommandError(CatoError):
    """Command execution errors."""
    pass
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

## Logging Integration

### Error Logging
- All errors must be logged
- Log level appropriate to severity:
  - DEBUG: Detailed diagnostic info
  - INFO: Notable events
  - WARNING: Recoverable issues
  - ERROR: Failures requiring attention

### Context in Logs
- Include relevant context (operation being attempted, relevant parameters)
- Don't log sensitive data (API keys, passwords)

## Never Silent Failures
- Never swallow exceptions without logging
- Never retry infinitely without user feedback
- Always inform user when something doesn't work as expected
