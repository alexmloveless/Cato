# LLM Integration Technical Specification

## Overview
Cato supports multiple LLM providers through a unified protocol-based abstraction. Providers are interchangeable at runtime via configuration.

## Provider Protocol

### Interface Definition
```python
from typing import Protocol, AsyncIterator
from dataclasses import dataclass

@dataclass
class Message:
    """Normalised message format."""
    role: Literal["system", "user", "assistant"]
    content: str

@dataclass
class CompletionResult:
    """Result from LLM completion."""
    content: str
    model: str
    usage: TokenUsage | None = None
    finish_reason: str | None = None

@dataclass
class TokenUsage:
    """Token usage statistics."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class LLMProvider(Protocol):
    """
    Protocol for LLM provider implementations.
    
    Any class implementing these methods can be used as a provider.
    """
    
    @property
    def name(self) -> str:
        """Provider identifier (e.g., 'openai', 'anthropic')."""
        ...
    
    @property
    def model(self) -> str:
        """Currently configured model."""
        ...
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        """
        Generate a completion for the given messages.
        
        Parameters
        ----------
        messages
            Conversation history in normalised format.
        temperature
            Override configured temperature.
        max_tokens
            Override configured max tokens.
        
        Returns
        -------
        CompletionResult
            The model's response with metadata.
        
        Raises
        ------
        LLMConnectionError
            Cannot reach the provider.
        LLMAuthenticationError
            Invalid API key.
        LLMRateLimitError
            Rate limit exceeded.
        LLMContextLengthError
            Input exceeds context window.
        """
        ...
    
    async def complete_stream(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream completion tokens as they arrive.
        
        Yields
        ------
        str
            Individual tokens or token chunks.
        """
        ...
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text for this provider's tokenizer.
        
        Parameters
        ----------
        text
            Text to tokenize.
        
        Returns
        -------
        int
            Token count.
        """
        ...
```

## Provider Implementations

### OpenAI Provider
```python
class OpenAIProvider:
    """OpenAI API provider implementation."""
    
    def __init__(self, config: OpenAIConfig) -> None:
        self._config = config
        self._client = AsyncOpenAI(api_key=config.api_key)
        self._model = config.model
    
    @property
    def name(self) -> str:
        return "openai"
    
    @property
    def model(self) -> str:
        return self._model
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[self._to_openai_message(m) for m in messages],
                temperature=temperature or self._config.temperature,
                max_tokens=max_tokens or self._config.max_tokens,
            )
            return self._to_result(response)
        except openai.AuthenticationError as e:
            raise LLMAuthenticationError(str(e))
        except openai.RateLimitError as e:
            raise LLMRateLimitError(str(e), retry_after=self._parse_retry(e))
        except openai.APIConnectionError as e:
            raise LLMConnectionError(str(e))
    
    def _to_openai_message(self, msg: Message) -> dict:
        return {"role": msg.role, "content": msg.content}
    
    def _to_result(self, response) -> CompletionResult:
        choice = response.choices[0]
        return CompletionResult(
            content=choice.message.content,
            model=response.model,
            usage=TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            finish_reason=choice.finish_reason,
        )
```

### Anthropic Provider
```python
class AnthropicProvider:
    """Anthropic Claude API provider implementation."""
    
    def __init__(self, config: AnthropicConfig) -> None:
        self._config = config
        self._client = AsyncAnthropic(api_key=config.api_key)
        self._model = config.model
    
    @property
    def name(self) -> str:
        return "anthropic"
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        # Extract system message (Anthropic handles it separately)
        system_msg = None
        chat_messages = []
        for msg in messages:
            if msg.role == "system":
                system_msg = msg.content
            else:
                chat_messages.append({"role": msg.role, "content": msg.content})
        
        try:
            response = await self._client.messages.create(
                model=self._model,
                system=system_msg,
                messages=chat_messages,
                temperature=temperature or self._config.temperature,
                max_tokens=max_tokens or self._config.max_tokens,
            )
            return self._to_result(response)
        except anthropic.AuthenticationError as e:
            raise LLMAuthenticationError(str(e))
        except anthropic.RateLimitError as e:
            raise LLMRateLimitError(str(e))
```

### Google Provider
```python
class GoogleProvider:
    """Google Gemini API provider implementation."""
    
    def __init__(self, config: GoogleConfig) -> None:
        self._config = config
        genai.configure(api_key=config.api_key)
        self._model = genai.GenerativeModel(config.model)
    
    @property
    def name(self) -> str:
        return "google"
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        # Convert to Gemini format
        history = self._build_history(messages[:-1])
        chat = self._model.start_chat(history=history)
        
        response = await chat.send_message_async(
            messages[-1].content,
            generation_config=genai.GenerationConfig(
                temperature=temperature or self._config.temperature,
                max_output_tokens=max_tokens or self._config.max_tokens,
            ),
        )
        return CompletionResult(
            content=response.text,
            model=self._config.model,
        )
```

### Ollama Provider
```python
class OllamaProvider:
    """Ollama local model provider implementation."""
    
    def __init__(self, config: OllamaConfig) -> None:
        self._config = config
        self._base_url = config.base_url or "http://localhost:11434"
        self._model = config.model
    
    @property
    def name(self) -> str:
        return "ollama"
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/api/chat",
                json={
                    "model": self._model,
                    "messages": [{"role": m.role, "content": m.content} for m in messages],
                    "options": {
                        "temperature": temperature or self._config.temperature,
                        "num_predict": max_tokens or self._config.max_tokens,
                    },
                    "stream": False,
                },
                timeout=self._config.timeout_seconds,
            )
            response.raise_for_status()
            data = response.json()
            return CompletionResult(
                content=data["message"]["content"],
                model=self._model,
            )
```

## Provider Factory

### Registration and Creation
```python
from typing import Callable

# Provider registry: maps name to factory function
_PROVIDERS: dict[str, Callable[[CatoConfig], LLMProvider]] = {}


def register_provider(name: str) -> Callable:
    """
    Decorator to register a provider factory.
    
    Parameters
    ----------
    name
        Provider identifier (must match config value).
    """
    def decorator(factory: Callable[[CatoConfig], LLMProvider]) -> Callable:
        _PROVIDERS[name] = factory
        return factory
    return decorator


@register_provider("openai")
def create_openai(config: CatoConfig) -> LLMProvider:
    return OpenAIProvider(config.llm.openai)


@register_provider("anthropic")
def create_anthropic(config: CatoConfig) -> LLMProvider:
    return AnthropicProvider(config.llm.anthropic)


@register_provider("google")
def create_google(config: CatoConfig) -> LLMProvider:
    return GoogleProvider(config.llm.google)


@register_provider("ollama")
def create_ollama(config: CatoConfig) -> LLMProvider:
    return OllamaProvider(config.llm.ollama)


def create_provider(config: CatoConfig) -> LLMProvider:
    """
    Create the configured LLM provider.
    
    Parameters
    ----------
    config
        Application configuration.
    
    Returns
    -------
    LLMProvider
        Configured provider instance.
    
    Raises
    ------
    ConfigurationError
        Unknown provider name.
    """
    provider_name = config.llm.provider
    if provider_name not in _PROVIDERS:
        raise ConfigurationError(
            f"Unknown LLM provider: {provider_name}",
            context={"available": list(_PROVIDERS.keys())},
        )
    return _PROVIDERS[provider_name](config)
```

## Message Normalisation

### Conversation History
```python
@dataclass
class Conversation:
    """Manages conversation state and history."""
    
    system_prompt: str
    messages: list[Message] = field(default_factory=list)
    
    def add_user_message(self, content: str) -> None:
        """Add a user message to history."""
        self.messages.append(Message(role="user", content=content))
    
    def add_assistant_message(self, content: str) -> None:
        """Add an assistant response to history."""
        self.messages.append(Message(role="assistant", content=content))
    
    def to_messages(self) -> list[Message]:
        """
        Get full message list for LLM request.
        
        Returns
        -------
        list[Message]
            System prompt followed by conversation history.
        """
        return [Message(role="system", content=self.system_prompt)] + self.messages
    
    def truncate_to_tokens(self, max_tokens: int, counter: Callable[[str], int]) -> None:
        """
        Truncate history to fit within token limit.
        
        Removes oldest messages (after system prompt) until within limit.
        Always keeps system prompt and most recent exchange.
        
        Parameters
        ----------
        max_tokens
            Maximum allowed tokens.
        counter
            Function to count tokens in text.
        """
        while self._count_tokens(counter) > max_tokens and len(self.messages) > 2:
            self.messages.pop(0)  # Remove oldest message
    
    def _count_tokens(self, counter: Callable[[str], int]) -> int:
        total = counter(self.system_prompt)
        for msg in self.messages:
            total += counter(msg.content)
        return total
```

## Error Handling

### Provider-Specific to Generic Mapping
Each provider implementation maps its specific exceptions to the generic hierarchy:

```python
# Exception mapping pattern
OPENAI_EXCEPTION_MAP = {
    openai.AuthenticationError: LLMAuthenticationError,
    openai.RateLimitError: LLMRateLimitError,
    openai.APIConnectionError: LLMConnectionError,
    openai.BadRequestError: LLMContextLengthError,  # Often context length
}

def map_exception(e: Exception, mapping: dict) -> CatoError:
    """Map provider exception to Cato exception."""
    for provider_exc, cato_exc in mapping.items():
        if isinstance(e, provider_exc):
            return cato_exc(str(e))
    return LLMError(str(e))
```

### Retry Logic
```python
async def complete_with_retry(
    provider: LLMProvider,
    messages: list[Message],
    max_retries: int = 3,
) -> CompletionResult:
    """
    Complete with automatic retry on transient failures.
    
    Parameters
    ----------
    provider
        LLM provider to use.
    messages
        Messages to send.
    max_retries
        Maximum retry attempts.
    
    Returns
    -------
    CompletionResult
        Successful completion result.
    
    Raises
    ------
    LLMError
        After all retries exhausted.
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            return await provider.complete(messages)
        except LLMRateLimitError as e:
            last_error = e
            if e.retry_after:
                await asyncio.sleep(e.retry_after)
            else:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        except LLMConnectionError as e:
            last_error = e
            await asyncio.sleep(2 ** attempt)
    
    raise last_error or LLMError("Max retries exceeded")
```

## Configuration

### Provider-Specific Config
```yaml
llm:
  provider: "openai"  # Which provider to use
  model: "gpt-4"
  temperature: 1.0
  max_tokens: 4096
  timeout_seconds: 60
  
  # Provider-specific settings (only relevant one is used)
  openai:
    api_key: "${OPENAI_API_KEY}"
    organization: null
    
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    
  google:
    api_key: "${GOOGLE_API_KEY}"
    
  ollama:
    base_url: "http://localhost:11434"
```

## Adding New Providers

To add a new provider:

1. Create `cato/providers/<name>.py`
2. Implement the `LLMProvider` protocol
3. Register with `@register_provider("<name>")`
4. Add config model to `cato/core/config.py`
5. Add to config schema validation

```python
# cato/providers/newprovider.py
from cato.providers.base import LLMProvider, register_provider

@register_provider("newprovider")
def create_newprovider(config: CatoConfig) -> LLMProvider:
    return NewProvider(config.llm.newprovider)

class NewProvider:
    """New provider implementation."""
    
    def __init__(self, config: NewProviderConfig) -> None:
        # Setup
        pass
    
    # Implement protocol methods...
```
