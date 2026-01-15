"""Provider factory with registration system."""

import logging
from typing import Callable

from cato.core.config import CatoConfig
from cato.core.exceptions import ConfigurationError
from cato.providers.llm.anthropic import AnthropicProvider
from cato.providers.llm.base import LLMProvider
from cato.providers.llm.google import GoogleProvider
from cato.providers.llm.ollama import OllamaProvider
from cato.providers.llm.openai import OpenAIProvider

logger = logging.getLogger(__name__)

# Provider registry maps provider name to factory function
_PROVIDERS: dict[str, Callable[[CatoConfig], LLMProvider]] = {}


def register_provider(name: str) -> Callable[[Callable[[CatoConfig], LLMProvider]], Callable[[CatoConfig], LLMProvider]]:
    """
    Decorator to register a provider factory.
    
    Parameters
    ----------
    name : str
        Provider identifier (must match config value).
    
    Returns
    -------
    Callable
        Decorator function.
    
    Examples
    --------
    >>> @register_provider("openai")
    ... def create_openai(config: CatoConfig) -> LLMProvider:
    ...     return OpenAIProvider(config.llm.openai)
    """
    def decorator(factory: Callable[[CatoConfig], LLMProvider]) -> Callable[[CatoConfig], LLMProvider]:
        _PROVIDERS[name] = factory
        logger.debug(f"Registered LLM provider: {name}")
        return factory
    return decorator


@register_provider("openai")
def create_openai(config: CatoConfig) -> LLMProvider:
    """
    Create OpenAI provider.
    
    Parameters
    ----------
    config : CatoConfig
        Application configuration.
    
    Returns
    -------
    LLMProvider
        Configured OpenAI provider.
    """
    if not config.llm.openai:
        raise ConfigurationError("OpenAI configuration missing")
    
    return OpenAIProvider(
        config=config.llm.openai,
        model=config.llm.model,
        temperature=config.llm.temperature,
        max_tokens=config.llm.max_tokens,
        timeout=config.llm.timeout_seconds,
    )


@register_provider("anthropic")
def create_anthropic(config: CatoConfig) -> LLMProvider:
    """
    Create Anthropic provider.
    
    Parameters
    ----------
    config : CatoConfig
        Application configuration.
    
    Returns
    -------
    LLMProvider
        Configured Anthropic provider.
    """
    if not config.llm.anthropic:
        raise ConfigurationError("Anthropic configuration missing")
    
    return AnthropicProvider(
        config=config.llm.anthropic,
        model=config.llm.model,
        temperature=config.llm.temperature,
        max_tokens=config.llm.max_tokens,
        timeout=config.llm.timeout_seconds,
    )


@register_provider("google")
def create_google(config: CatoConfig) -> LLMProvider:
    """
    Create Google provider.
    
    Parameters
    ----------
    config : CatoConfig
        Application configuration.
    
    Returns
    -------
    LLMProvider
        Configured Google provider.
    """
    if not config.llm.google:
        raise ConfigurationError("Google configuration missing")
    
    return GoogleProvider(
        config=config.llm.google,
        model=config.llm.model,
        temperature=config.llm.temperature,
        max_tokens=config.llm.max_tokens,
        timeout=config.llm.timeout_seconds,
    )


@register_provider("ollama")
def create_ollama(config: CatoConfig) -> LLMProvider:
    """
    Create Ollama provider.
    
    Parameters
    ----------
    config : CatoConfig
        Application configuration.
    
    Returns
    -------
    LLMProvider
        Configured Ollama provider.
    """
    if not config.llm.ollama:
        raise ConfigurationError("Ollama configuration missing")
    
    return OllamaProvider(
        config=config.llm.ollama,
        model=config.llm.model,
        temperature=config.llm.temperature,
        max_tokens=config.llm.max_tokens,
        timeout=config.llm.timeout_seconds,
    )


def create_provider(config: CatoConfig) -> LLMProvider:
    """
    Create the configured LLM provider.
    
    Factory function that instantiates the appropriate provider based
    on the configuration's provider selection.
    
    Parameters
    ----------
    config : CatoConfig
        Application configuration containing LLM settings.
    
    Returns
    -------
    LLMProvider
        Configured provider instance ready for use.
    
    Raises
    ------
    ConfigurationError
        Unknown provider name or missing provider configuration.
    
    Examples
    --------
    >>> config = load_config()
    >>> provider = create_provider(config)
    >>> result = await provider.complete(messages)
    """
    provider_name = config.llm.provider
    
    if provider_name not in _PROVIDERS:
        available = ", ".join(_PROVIDERS.keys())
        raise ConfigurationError(
            f"Unknown LLM provider: {provider_name}",
            context={"available_providers": available},
        )
    
    logger.info(f"Creating LLM provider: {provider_name} with model {config.llm.model}")
    return _PROVIDERS[provider_name](config)
