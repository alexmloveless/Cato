# Providers Module

This module contains provider implementations for external services (LLM, search, TTS).

## Components

### `llm/`
LLM provider implementations with unified protocol.

**Providers:**
- `OpenAIProvider`: OpenAI API (GPT models)
- `AnthropicProvider`: Anthropic Claude API
- `GoogleProvider`: Google Gemini API
- `OllamaProvider`: Local Ollama models

**Key features:**
- Protocol-based abstraction for swappable providers
- Automatic error mapping to `CatoError` hierarchy
- Streaming support for real-time responses
- Token counting per provider

### `search/` (Phase 13)
Web search provider implementations.

### `tts/` (Phase 13)
Text-to-speech provider implementations.

## Usage

```python
from cato.providers import create_provider
from cato.core.config import load_config

config = load_config()
provider = create_provider(config)

# Use provider
result = await provider.complete(messages, temperature=0.7)
print(result.content)
```

## Design Principles

- **Protocol-based**: Providers implement `LLMProvider` protocol
- **Provider-agnostic**: Application code doesn't depend on specific providers
- **Error mapping**: Provider-specific errors mapped to generic exceptions
- **Configuration-driven**: Provider selection via config file
