"""Configuration system with YAML overlay and Pydantic validation."""

import logging
import os
import re
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic_core import ValidationInfo

from cato.core.exceptions import (
    ConfigFileNotFoundError,
    ConfigurationError,
    ConfigValidationError,
)

logger = logging.getLogger(__name__)


# Provider-specific configurations
class OpenAIConfig(BaseModel):
    """OpenAI provider configuration."""
    
    api_key: str


class AnthropicConfig(BaseModel):
    """Anthropic provider configuration."""
    
    api_key: str


class GoogleConfig(BaseModel):
    """Google provider configuration."""
    
    api_key: str


class OllamaConfig(BaseModel):
    """Ollama provider configuration."""
    
    base_url: str = "http://localhost:11434"


# Main configuration sections
class LLMConfig(BaseModel):
    """LLM provider configuration."""
    
    provider: Literal["openai", "anthropic", "google", "ollama"]
    model: str
    temperature: float = Field(ge=0.0, le=2.0)
    max_tokens: int = Field(ge=1, le=200000)
    timeout_seconds: int = Field(ge=1, le=300)
    system_prompt_files: list[Path] = Field(default_factory=list)
    base_prompt_file: Path | None = None
    override_base_prompt: bool = False
    
    # Provider-specific settings
    openai: OpenAIConfig | None = None
    anthropic: AnthropicConfig | None = None
    google: GoogleConfig | None = None
    ollama: OllamaConfig | None = None


class VectorStoreConfig(BaseModel):
    """Vector store configuration."""
    
    enabled: bool
    backend: Literal["chromadb"]
    path: Path
    collection_name: str
    context_results: int = Field(ge=1)
    search_context_window: int = Field(ge=1)
    similarity_threshold: float = Field(ge=0.0, le=1.0)
    dynamic_threshold: bool
    retrieval_strategy: str
    chat_window: int
    embedding_provider: Literal["openai", "ollama"]
    embedding_model: str
    embedding_dimensions: int = Field(ge=1)
    chunking_strategy: Literal["truncate", "fixed_size", "semantic", "hybrid"]
    chunk_size: int = Field(ge=100, le=10000)
    chunk_overlap: int = Field(ge=0)
    max_chunk_size: int = Field(ge=100, le=10000)
    preserve_sentence_boundaries: bool
    
    @field_validator("chunk_overlap")
    @classmethod
    def overlap_less_than_size(cls, v: int, info: ValidationInfo) -> int:
        """Validate chunk_overlap is less than chunk_size."""
        if info.data and "chunk_size" in info.data and v >= info.data["chunk_size"]:
            raise ValueError("chunk_overlap must be less than chunk_size")
        return v


class StorageConfig(BaseModel):
    """SQLite storage configuration."""
    
    database_path: Path
    backup_enabled: bool
    backup_frequency_hours: int = Field(ge=1)


class DisplayConfig(BaseModel):
    """Display and UI configuration."""
    
    theme: str
    markdown_enabled: bool
    code_theme: str
    max_width: int | None = Field(ge=40, default=None)
    timestamps: bool
    spinner_style: str
    prompt_symbol: str
    line_width: int
    exchange_delimiter: str
    exchange_delimiter_length: int
    style_overrides: dict[str, str] = Field(default_factory=dict)
    prompt_style: str | None = None
    input_style: str | None = None


class LoggingConfig(BaseModel):
    """Logging configuration."""
    
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]
    file_path: Path | None
    format: str
    max_file_size_mb: int = Field(ge=1)
    backup_count: int = Field(ge=0)


class CommandConfig(BaseModel):
    """Command system configuration."""
    
    prefix: str
    history_file: Path


class PathConfig(BaseModel):
    """Base application paths."""
    
    data_dir: Path
    config_dir: Path
    cache_dir: Path


class TTSConfig(BaseModel):
    """Text-to-speech configuration."""
    
    enabled: bool
    voice: str
    model: str
    audio_dir: Path


class WebSearchConfig(BaseModel):
    """Web search configuration."""
    
    enabled: bool
    default_engine: str
    content_threshold: int = Field(ge=1)
    max_results: int = Field(ge=1, le=10)
    timeout: int = Field(ge=1)
    engines: dict[str, str] = Field(default_factory=dict)


class CatoConfig(BaseModel):
    """
    Root configuration model.
    
    All configuration is validated through Pydantic. Unknown keys are ignored
    with a warning.
    """
    
    model_config = ConfigDict(extra="ignore")
    
    profile_name: str | None = None
    debug: bool = False
    llm: LLMConfig
    vector_store: VectorStoreConfig
    storage: StorageConfig
    display: DisplayConfig
    commands: CommandConfig
    logging: LoggingConfig
    paths: PathConfig
    tts: TTSConfig
    web_search: WebSearchConfig
    locations: dict[str, str] = Field(default_factory=dict)


def get_default_config_path() -> Path:
    """
    Get path to packaged default configuration.
    
    Returns
    -------
    Path
        Path to defaults.yaml in the package resources.
    """
    return Path(__file__).parent.parent / "resources" / "defaults.yaml"


def get_user_config_path() -> Path:
    """
    Get default user configuration path.
    
    Returns
    -------
    Path
        Path to ~/.config/cato/config.yaml (may not exist).
    """
    return Path.home() / ".config" / "cato" / "config.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    """
    Load YAML file into dictionary.
    
    Parameters
    ----------
    path : Path
        Path to YAML file.
    
    Returns
    -------
    dict[str, Any]
        Parsed YAML content.
    
    Raises
    ------
    ConfigFileNotFoundError
        If the file does not exist.
    ConfigurationError
        If YAML parsing fails.
    """
    if not path.exists():
        raise ConfigFileNotFoundError(f"Config file not found: {path}")
    
    try:
        with path.open("r") as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Invalid YAML in {path}: {e}")


def deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    """
    Deep merge overlay dict into base dict.
    
    Overlay values replace base values. Nested dicts are merged recursively.
    
    Parameters
    ----------
    base : dict[str, Any]
        Base configuration dictionary.
    overlay : dict[str, Any]
        Overlay configuration dictionary.
    
    Returns
    -------
    dict[str, Any]
        Merged configuration.
    """
    result = base.copy()
    
    for key, value in overlay.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def expand_env_vars(value: Any) -> Any:
    """
    Recursively expand ${VAR} environment variables in strings.
    
    Parameters
    ----------
    value : Any
        Value to process (string, dict, list, or other).
    
    Returns
    -------
    Any
        Value with environment variables expanded.
    """
    if isinstance(value, str):
        # Find ${VAR} patterns and replace with environment variable value
        pattern = re.compile(r"\$\{([^}]+)\}")
        
        def replace_var(match: re.Match[str]) -> str:
            var_name = match.group(1)
            return os.environ.get(var_name, match.group(0))  # Keep original if not found
        
        return pattern.sub(replace_var, value)
    elif isinstance(value, dict):
        return {k: expand_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [expand_env_vars(item) for item in value]
    else:
        return value


def expand_paths(config: dict[str, Any]) -> dict[str, Any]:
    """
    Expand ~ in path strings throughout config.
    
    Parameters
    ----------
    config : dict[str, Any]
        Configuration dictionary.
    
    Returns
    -------
    dict[str, Any]
        Configuration with expanded paths.
    """
    # Recursively expand paths - look for keys ending in _path, _dir, _file
    result = {}
    
    for key, value in config.items():
        if isinstance(value, dict):
            result[key] = expand_paths(value)
        elif isinstance(value, str) and any(
            key.endswith(suffix) for suffix in ["_path", "_dir", "_file"]
        ):
            result[key] = str(Path(value).expanduser())
        else:
            result[key] = value
    
    return result


def apply_env_overrides(config: dict[str, Any]) -> dict[str, Any]:
    """
    Apply CATO_* environment variables as config overrides.
    
    Environment variables in format CATO_SECTION_KEY=value will override
    the corresponding config value.
    
    Parameters
    ----------
    config : dict[str, Any]
        Configuration dictionary to modify.
    
    Returns
    -------
    dict[str, Any]
        Configuration with environment overrides applied.
    """
    prefix = "CATO_"
    
    for key, value in os.environ.items():
        if not key.startswith(prefix):
            continue
        
        # Parse key path: CATO_LLM_MODEL -> ["llm", "model"]
        parts = key[len(prefix) :].lower().split("_")
        
        # Navigate to nested location and set value
        current = config
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set the final value (try to parse as int/float/bool if possible)
        final_key = parts[-1]
        current[final_key] = _parse_env_value(value)
    
    return config


def _parse_env_value(value: str) -> Any:
    """
    Parse environment variable value to appropriate type.
    
    Parameters
    ----------
    value : str
        Environment variable value.
    
    Returns
    -------
    Any
        Parsed value (int, float, bool, or str).
    """
    # Try bool
    if value.lower() in ("true", "yes", "1"):
        return True
    if value.lower() in ("false", "no", "0"):
        return False
    
    # Try int
    try:
        return int(value)
    except ValueError:
        pass
    
    # Try float
    try:
        return float(value)
    except ValueError:
        pass
    
    # Return as string
    return value


def load_config(user_path: Path | None = None) -> CatoConfig:
    """
    Load configuration with overlay system.
    
    Loads default config, overlays user config, applies environment overrides,
    and validates with Pydantic.
    
    Parameters
    ----------
    user_path : Path | None, optional
        Optional custom path to user config. If None, checks CATO_CONFIG_FILE
        environment variable, then default location.
    
    Returns
    -------
    CatoConfig
        Validated configuration object.
    
    Raises
    ------
    ConfigurationError
        If configuration loading or validation fails.
    """
    try:
        # 1. Load defaults (required)
        defaults = load_yaml(get_default_config_path())
        
        # 2. Determine user config path
        if user_path is None:
            env_path = os.environ.get("CATO_CONFIG_FILE")
            if env_path:
                user_path = Path(env_path)
            else:
                user_path = get_user_config_path()
        
        # 3. Load user config if exists
        merged = defaults
        if user_path.exists():
            user_config = load_yaml(user_path)
            merged = deep_merge(defaults, user_config)
            logger.info(f"Loaded user config from {user_path}")
        else:
            logger.info("No user config found, using defaults")
        
        # 4. Expand environment variables in strings (${VAR})
        merged = expand_env_vars(merged)
        
        # 5. Expand ~ in paths
        merged = expand_paths(merged)
        
        # 6. Apply CATO_* environment overrides
        merged = apply_env_overrides(merged)
        
        # 7. Validate with Pydantic
        config = CatoConfig.model_validate(merged)
        
        return config
        
    except ConfigFileNotFoundError:
        raise
    except ConfigurationError:
        raise
    except Exception as e:
        raise ConfigValidationError(f"Config validation failed: {e}")
