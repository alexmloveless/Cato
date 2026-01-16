# /continue

Resume a previous conversation thread from the vector store.

## Usage

```
/continue <session_id>    # Resume thread by session ID
/cont <session_id>        # Alias
```

## Description

The `/continue` command allows you to resume a previous conversation by loading all message exchanges from a specific session. This is useful for:

- Continuing long-running conversations across multiple sessions
- Revisiting and building upon past discussions
- Maintaining context across application restarts

The command retrieves all exchanges from the vector store for the specified session ID and reconstructs the conversation history in chronological order. Your current conversation will be replaced with the loaded thread, and the session ID will be updated to match the continued thread.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| session_id | Yes | The unique identifier for the session/thread to resume |

## Requirements

- Vector store must be enabled in configuration (`vector_store.enabled: true`)
- The session ID must exist in the vector store
- At least one message exchange must be stored for the session

## Finding Session IDs

You can find session IDs by:
- Checking previous session logs (displayed at Cato startup)
- Using `/vstats` to view vector store statistics
- Using `/vquery` to search for relevant past conversations
- Looking at the session_id in vector store metadata

## Examples

```
# Resume a previous session
/continue a1b2c3d4

# Use the alias
/cont a1b2c3d4
```

## Output

On success:
```
✓ Loaded 15 message exchange(s) from session: a1b2c3d4
You can now continue the conversation from where it left off.
```

On error:
```
No conversation found for session: a1b2c3d4
```

## Configuration

Ensure vector store is enabled in your configuration:

```yaml
vector_store:
  enabled: true
  type: chromadb
  path: ~/.local/share/cato/chroma
```

## See Also

- [/clear](clear.md) - Clear current conversation
- [/vquery](vquery.md) - Search vector store for past conversations
- [/vstats](vstats.md) - View vector store statistics
