# /showcontext

Toggle or set context display mode.

## Usage

```
/showcontext          # Toggle through modes: off -> summary -> on
/showcontext on       # Enable full context display
/showcontext off      # Disable context display
/showcontext summary  # Show only count
```

## Description

Controls whether and how retrieved context from the vector store is displayed before each response. Context is always injected into prompts when the vector store is enabled and similarity thresholds are met, but this command controls whether you see it.

## Display Modes

- **off** (default): Context is injected into prompts but not displayed to you
- **summary**: Shows count of context items retrieved (e.g., "📚 Retrieved 3 context items")
- **on**: Displays full context excerpts in a panel before each response

## Requirements

- Vector store must be enabled (`vector_store.enabled: true` in config)
- Context is only displayed when items are actually retrieved

## Examples

```
# Toggle to next mode
> /showcontext
✓ Context display: summary
Context count will be shown before responses

# Enable full context display
> /showcontext on
✓ Context display: on
Full context excerpts will be displayed before responses

# Disable display
> /showcontext off
✓ Context display: off
Context is injected into prompts but not displayed
```

## Notes

- Mode persists for the duration of the session
- Does not affect context injection into prompts
- Useful for understanding what prior conversations are influencing responses
