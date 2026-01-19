# /clear

Clear the conversation history and terminal screen.

## Usage

```
/clear
```

## Description

Removes all user and assistant messages from the current conversation, keeping only the system prompt. The terminal screen is cleared and the welcome message is displayed.

This is useful when you want to:
- Start a fresh conversation on a new topic
- Clear the context window to reduce token usage
- Remove sensitive information from the conversation history

## Aliases

- `/cls`

## Behavior

1. Clears all messages from conversation history (system prompt is preserved)
2. Clears the terminal screen
3. Displays the welcome message
4. The next message will start a fresh conversation

## Examples

```
/clear
```

## Related Commands

- `/history` - View conversation history before clearing
- `/delete` - Remove specific exchanges without clearing everything
