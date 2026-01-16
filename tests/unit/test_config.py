"""
Unit tests for configuration system.

Tests cover:
- Loading from YAML files
- Deep merging of configurations
- Environment variable expansion
- Path expansion
- Pydantic validation
- Error handling
"""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from cato.core.config import (
    CatoConfig,
    LLMConfig,
    VectorStoreConfig,
    load_config,
    deep_merge,
    expand_env_vars,
    expand_paths,
    apply_env_overrides,
    _parse_env_value,
    get_default_config_path,
)
from cato.core.exceptions import (
    ConfigFileNotFoundError,
    ConfigValidationError,
    ConfigurationError,
)


class TestDeepMerge:
    """Test deep merge functionality."""

    def test_simple_merge(self):
        """Test merging two simple dictionaries."""
        base = {"a": 1, "b": 2}
        overlay = {"b": 3, "c": 4}
        result = deep_merge(base, overlay)

        assert result == {"a": 1, "b": 3, "c": 4}

    def test_nested_merge(self):
        """Test merging nested dictionaries."""
        base = {"section": {"key1": "value1", "key2": "value2"}}
        overlay = {"section": {"key2": "new_value2", "key3": "value3"}}
        result = deep_merge(base, overlay)

        assert result == {
            "section": {
                "key1": "value1",
                "key2": "new_value2",
                "key3": "value3",
            }
        }

    def test_list_override(self):
        """Test that lists are replaced, not merged."""
        base = {"items": [1, 2, 3]}
        overlay = {"items": [4, 5]}
        result = deep_merge(base, overlay)

        assert result == {"items": [4, 5]}

    def test_deep_nested_merge(self):
        """Test merging deeply nested structures."""
        base = {
            "level1": {
                "level2": {
                    "key1": "value1",
                    "key2": "value2",
                }
            }
        }
        overlay = {
            "level1": {
                "level2": {
                    "key2": "new_value",
                },
                "new_key": "new_value",
            }
        }
        result = deep_merge(base, overlay)

        assert result == {
            "level1": {
                "level2": {
                    "key1": "value1",
                    "key2": "new_value",
                },
                "new_key": "new_value",
            }
        }


class TestEnvVarExpansion:
    """Test environment variable expansion."""

    def test_expand_single_var(self, monkeypatch):
        """Test expanding a single environment variable."""
        monkeypatch.setenv("TEST_VAR", "test_value")
        result = expand_env_vars("${TEST_VAR}")
        assert result == "test_value"

    def test_expand_multiple_vars(self, monkeypatch):
        """Test expanding multiple variables in one string."""
        monkeypatch.setenv("VAR1", "value1")
        monkeypatch.setenv("VAR2", "value2")
        result = expand_env_vars("${VAR1}_${VAR2}")
        assert result == "value1_value2"

    def test_expand_in_nested_dict(self, monkeypatch):
        """Test expanding variables in nested structures."""
        monkeypatch.setenv("API_KEY", "secret123")
        config = {
            "provider": {
                "api_key": "${API_KEY}",
                "url": "https://api.example.com",
            }
        }
        result = expand_env_vars(config)
        assert result["provider"]["api_key"] == "secret123"
        assert result["provider"]["url"] == "https://api.example.com"

    def test_expand_in_list(self, monkeypatch):
        """Test expanding variables in lists."""
        monkeypatch.setenv("PATH1", "/path/1")
        monkeypatch.setenv("PATH2", "/path/2")
        config = {"paths": ["${PATH1}", "${PATH2}"]}
        result = expand_env_vars(config)
        assert result["paths"] == ["/path/1", "/path/2"]

    def test_missing_var_unchanged(self):
        """Test that missing variables are left unchanged."""
        result = expand_env_vars("${NONEXISTENT_VAR}")
        assert result == "${NONEXISTENT_VAR}"


class TestPathExpansion:
    """Test path expansion functionality."""

    def test_expand_tilde_in_path(self):
        """Test expanding ~ in path strings."""
        config = {"database_path": "~/cato/data.db"}
        result = expand_paths(config)
        assert str(Path.home()) in result["database_path"]
        assert "~" not in result["database_path"]

    def test_expand_nested_paths(self):
        """Test expanding paths in nested structures."""
        config = {
            "section": {
                "log_file": "~/.cato/logs/app.log",
                "data_dir": "~/cato/data",
            }
        }
        result = expand_paths(config)
        assert "~" not in result["section"]["log_file"]
        assert "~" not in result["section"]["data_dir"]

    def test_non_path_keys_unchanged(self):
        """Test that non-path keys are not expanded."""
        config = {
            "name": "~/this/is/not/a/path",
            "config_file": "~/this/is/a/path",
        }
        result = expand_paths(config)
        assert result["name"] == "~/this/is/not/a/path"  # Not expanded
        assert "~" not in result["config_file"]  # Expanded


class TestEnvOverrides:
    """Test environment variable override system."""

    def test_simple_override(self, monkeypatch):
        """Test simple config override via environment."""
        monkeypatch.setenv("CATO_DEBUG", "true")
        config = {"debug": False}
        result = apply_env_overrides(config)
        assert result["debug"] is True

    def test_nested_override(self, monkeypatch):
        """Test nested config override."""
        monkeypatch.setenv("CATO_LLM_MODEL", "gpt-4")
        config = {"llm": {"model": "gpt-3.5-turbo"}}
        result = apply_env_overrides(config)
        assert result["llm"]["model"] == "gpt-4"

    def test_create_missing_section(self, monkeypatch):
        """Test creating missing config section via environment."""
        monkeypatch.setenv("CATO_NEW_SECTION_KEY", "value")
        config = {}
        result = apply_env_overrides(config)
        assert result["new"]["section"]["key"] == "value"

    def test_type_parsing(self, monkeypatch):
        """Test automatic type parsing of env values."""
        monkeypatch.setenv("CATO_INT_VAL", "42")
        monkeypatch.setenv("CATO_FLOAT_VAL", "3.14")
        monkeypatch.setenv("CATO_BOOL_VAL", "true")
        monkeypatch.setenv("CATO_STR_VAL", "text")

        config = {}
        result = apply_env_overrides(config)

        assert result["int"]["val"] == 42
        assert result["float"]["val"] == 3.14
        assert result["bool"]["val"] is True
        assert result["str"]["val"] == "text"


class TestParseEnvValue:
    """Test environment value parsing."""

    def test_parse_bool_true(self):
        """Test parsing boolean true values."""
        assert _parse_env_value("true") is True
        assert _parse_env_value("TRUE") is True
        assert _parse_env_value("yes") is True
        assert _parse_env_value("1") is True

    def test_parse_bool_false(self):
        """Test parsing boolean false values."""
        assert _parse_env_value("false") is False
        assert _parse_env_value("FALSE") is False
        assert _parse_env_value("no") is False
        assert _parse_env_value("0") is False

    def test_parse_int(self):
        """Test parsing integer values."""
        assert _parse_env_value("42") == 42
        assert _parse_env_value("-10") == -10

    def test_parse_float(self):
        """Test parsing float values."""
        assert _parse_env_value("3.14") == 3.14
        assert _parse_env_value("-0.5") == -0.5

    def test_parse_string(self):
        """Test that non-numeric strings remain strings."""
        assert _parse_env_value("hello") == "hello"
        assert _parse_env_value("gpt-4") == "gpt-4"


class TestConfigLoading:
    """Test full configuration loading."""

    def test_load_default_config(self):
        """Test loading default configuration."""
        # Should load defaults from package
        config = load_config(Path("/nonexistent/config.yaml"))
        assert isinstance(config, CatoConfig)
        assert config.llm is not None
        assert config.storage is not None

    def test_load_with_user_config(self, temp_dir):
        """Test loading with user config overlay."""
        # Create user config that overrides model
        user_config = temp_dir / "config.yaml"
        user_config.write_text(
            yaml.dump({"llm": {"model": "custom-model"}})
        )

        config = load_config(user_config)
        assert config.llm.model == "custom-model"

    def test_load_nonexistent_default(self, monkeypatch):
        """Test that missing default config raises error."""
        # Make default config path invalid
        def mock_get_default():
            return Path("/nonexistent/defaults.yaml")

        monkeypatch.setattr(
            "cato.core.config.get_default_config_path",
            mock_get_default,
        )

        with pytest.raises(ConfigFileNotFoundError):
            load_config()

    def test_env_var_precedence(self, temp_dir, monkeypatch):
        """Test that environment variables override file config."""
        # Create user config
        user_config = temp_dir / "config.yaml"
        user_config.write_text(
            yaml.dump({"debug": False})
        )

        # Override with environment
        monkeypatch.setenv("CATO_DEBUG", "true")

        config = load_config(user_config)
        assert config.debug is True

    def test_invalid_yaml(self, temp_dir):
        """Test that invalid YAML raises error."""
        invalid_config = temp_dir / "invalid.yaml"
        invalid_config.write_text("{ invalid yaml ]")

        with pytest.raises(ConfigurationError):
            load_config(invalid_config)


class TestConfigValidation:
    """Test Pydantic validation."""

    def test_valid_llm_config(self):
        """Test creating valid LLM config."""
        config = LLMConfig(
            provider="openai",
            model="gpt-4",
            temperature=0.7,
            max_tokens=2000,
            timeout_seconds=30,
        )
        assert config.provider == "openai"
        assert config.model == "gpt-4"

    def test_invalid_temperature(self):
        """Test that invalid temperature is rejected."""
        with pytest.raises(Exception):  # ValidationError
            LLMConfig(
                provider="openai",
                model="gpt-4",
                temperature=3.0,  # Out of range
                max_tokens=2000,
                timeout_seconds=30,
            )

    def test_invalid_provider(self):
        """Test that invalid provider is rejected."""
        with pytest.raises(Exception):  # ValidationError
            LLMConfig(
                provider="invalid_provider",
                model="gpt-4",
                temperature=0.7,
                max_tokens=2000,
                timeout_seconds=30,
            )

    def test_vector_store_chunk_overlap_validation(self):
        """Test that chunk_overlap must be less than chunk_size."""
        with pytest.raises(Exception):  # ValidationError
            VectorStoreConfig(
                enabled=True,
                backend="chromadb",
                path=Path("/tmp"),
                collection_name="test",
                context_results=5,
                search_context_window=10,
                similarity_threshold=0.8,
                dynamic_threshold=False,
                retrieval_strategy="default",
                chat_window=10,
                embedding_provider="openai",
                embedding_model="text-embedding-3-small",
                embedding_dimensions=1536,
                chunking_strategy="fixed_size",
                chunk_size=1000,
                chunk_overlap=1500,  # Invalid: >= chunk_size
                max_chunk_size=2000,
                preserve_sentence_boundaries=True,
            )


class TestConfigPaths:
    """Test configuration path utilities."""

    def test_get_default_config_path(self):
        """Test getting default config path."""
        path = get_default_config_path()
        assert path.name == "defaults.yaml"
        assert path.exists()

    def test_default_config_is_valid(self):
        """Test that default config file is valid YAML and parseable."""
        path = get_default_config_path()
        with path.open() as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict)
        assert "llm" in data
        assert "storage" in data
