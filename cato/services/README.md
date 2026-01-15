# Services Module

This module provides high-level business logic services that orchestrate between lower-level components (providers, storage, display) to implement core application functionality.

## Components

### Conversation (`conversation.py`)
Manages conversation state and message history for chat sessions.

**Key responsibilities:**
- Store system prompt and message history
- Add user and assistant messages
- Format messages for LLM requests
- Token-aware history truncation

**Usage:**
```python
from cato.services.conversation import Conversation

conv = Conversation(system_prompt="You are a helpful assistant.")
conv.add_user_message("Hello!")
conv.add_assistant_message("Hi there!")

# Get messages for LLM (includes system prompt)
messages = conv.to_messages()

# Truncate to fit token limit
conv.truncate_to_tokens(max_tokens=1000, counter=provider.count_tokens)
```

### ChatService (`chat.py`)
Orchestrates LLM interactions with conversation management, retry logic, and system prompt loading.

**Key responsibilities:**
- Manage conversation lifecycle
- Load and compose system prompts from files
- Send messages to LLM with retry logic
- Handle streaming responses
- Token management and truncation

**Usage:**
```python
from cato.services.chat import ChatService

chat = ChatService(provider=llm_provider, config=app_config)

# Send message and get response
result = await chat.send_message("What is Python?")
print(result.content)

# Stream response
async for token in chat.send_message_stream("Explain asyncio"):
    print(token, end="", flush=True)

# Clear conversation history
chat.clear_conversation()
```

**System prompt loading:**
The ChatService supports flexible system prompt composition:

1. **Override mode**: Use only custom base prompt
   ```yaml
   llm:
     base_prompt_file: "~/my_prompt.txt"
     override_base_prompt: true
   ```

2. **Append mode**: Default + custom base
   ```yaml
   llm:
     base_prompt_file: "~/additional.txt"
     override_base_prompt: false
   ```

3. **Additional prompts**: Append multiple files
   ```yaml
   llm:
     system_prompt_files:
       - "~/context1.txt"
       - "~/context2.txt"
   ```

## Architecture

Services sit in the middle of the layered architecture:

```
Commands → Services → Providers/Storage
```

- **Services** orchestrate high-level workflows
- **Providers** handle external APIs (LLM, embedding)
- **Storage** manages persistence (SQLite, ChromaDB)
- **Commands** provide user interface

## Design Patterns

### Dependency Injection
Services receive dependencies via constructor:
```python
chat = ChatService(provider=provider, config=config)
```

### Retry Logic
Automatic retry with exponential backoff for transient failures:
- Rate limits: respect retry-after header
- Connection errors: exponential backoff
- Max 3 retries by default

### Token Management
Conversations automatically truncate to fit context windows:
- Always preserve system prompt
- Keep most recent exchange (last 2 messages)
- Remove oldest messages first

## Error Handling

Services map errors to the CatoError hierarchy and handle retries:
- `LLMRateLimitError`: Automatic retry with backoff
- `LLMConnectionError`: Automatic retry with backoff  
- `LLMAuthenticationError`: Immediate failure (no retry)
- `LLMContextLengthError`: Immediate failure (no retry)

## Testing

Services can be tested with mock providers:
```python
class MockProvider:
    async def complete(self, messages):
        return CompletionResult(content="mock response", model="mock")
    
    def count_tokens(self, text):
        return len(text.split())

chat = ChatService(provider=MockProvider(), config=config)
```
