# /loglevel

Show or change the current logging level.

## Usage

```
/loglevel           # Show current level
/loglevel WARNING   # Set to WARNING
/log ERROR          # Alias, set to ERROR
```

## Description

The `/loglevel` command controls the verbosity of Cato's logging output. Lower log levels show more messages, while higher levels only show critical information.

This affects both console output and log file entries (if file logging is enabled).

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| level | No | Log level to set (DEBUG, INFO, WARNING, ERROR) |

## Log Levels

| Level | Description |
|-------|-------------|
| DEBUG | Everything - very verbose, for troubleshooting |
| INFO | General information about operations |
| WARNING | Warnings and errors only (recommended) |
| ERROR | Errors only - minimal output |

## Examples

```
# Check current level
/loglevel

# Reduce verbosity (recommended)
/loglevel WARNING

# Enable detailed logging for debugging
/loglevel DEBUG

# Only show errors
/loglevel ERROR

# Use alias
/log WARNING
```

## Output

When showing current level:
```
Current log level: **WARNING**

Available levels: DEBUG, INFO, WARNING, ERROR
Usage: /loglevel <level>
```

When setting level:
```
✓ Log level set to **WARNING**
```

## Notes

- Changes take effect immediately for the current session
- Log level resets to config default when restarting Cato
- For persistent changes, update your configuration file:
  ```yaml
  logging:
    level: "WARNING"
  ```
- Or set environment variable:
  ```bash
  export CATO_LOGGING_LEVEL="WARNING"
  ```

## See Also

- [/config](config.md) - View current configuration
- [Configuration Reference](../../CONFIG_REFERENCE.md) - Logging configuration
