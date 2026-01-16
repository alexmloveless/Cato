"""
Unit tests for exception hierarchy.

Tests cover:
- Base CatoError functionality
- Context handling
- String representation
- Inheritance hierarchy
- Special exception attributes (e.g., retry_after)
"""

import pytest

from cato.core.exceptions import (
    CatoError,
    # Configuration
    ConfigurationError,
    ConfigFileNotFoundError,
    ConfigValidationError,
    # LLM
    LLMError,
    LLMConnectionError,
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMContextLengthError,
    LLMResponseError,
    # Vector Store
    VectorStoreError,
    VectorStoreConnectionError,
    EmbeddingError,
    # Storage
    StorageError,
    StorageConnectionError,
    StorageQueryError,
    # Commands
    CommandError,
    CommandNotFoundError,
    CommandArgumentError,
    CommandExecutionError,
    # I/O
    IOError,
    FileAccessError,
    NetworkError,
    # TTS
    TTSError,
    TTSConnectionError,
    TTSAuthenticationError,
    TTSRateLimitError,
    TTSInvalidInputError,
    # Display
    DisplayError,
)


class TestCatoError:
    """Test base CatoError class."""

    def test_basic_error(self):
        """Test creating basic error with message."""
        error = CatoError("Something went wrong")
        assert str(error) == "Something went wrong"
        assert error.message == "Something went wrong"
        assert error.context == {}

    def test_error_with_context(self):
        """Test error with contextual information."""
        error = CatoError(
            "Operation failed",
            context={"file": "test.txt", "line": 42}
        )
        assert error.message == "Operation failed"
        assert error.context == {"file": "test.txt", "line": 42}
        assert "file='test.txt'" in str(error)
        assert "line=42" in str(error)

    def test_error_inheritance(self):
        """Test that CatoError inherits from Exception."""
        error = CatoError("test")
        assert isinstance(error, Exception)

    def test_catching_cato_error(self):
        """Test catching CatoError as base exception."""
        try:
            raise CatoError("test error")
        except CatoError as e:
            assert e.message == "test error"
        except Exception:
            pytest.fail("Should catch CatoError")


class TestConfigurationExceptions:
    """Test configuration exception hierarchy."""

    def test_configuration_error_inheritance(self):
        """Test ConfigurationError inherits from CatoError."""
        error = ConfigurationError("config error")
        assert isinstance(error, CatoError)
        assert isinstance(error, Exception)

    def test_config_file_not_found_error(self):
        """Test ConfigFileNotFoundError."""
        error = ConfigFileNotFoundError("config.yaml not found")
        assert isinstance(error, ConfigurationError)
        assert isinstance(error, CatoError)
        assert "config.yaml" in str(error)

    def test_config_validation_error(self):
        """Test ConfigValidationError."""
        error = ConfigValidationError(
            "Invalid temperature value",
            context={"value": 3.0, "max": 2.0}
        )
        assert isinstance(error, ConfigurationError)
        assert "temperature" in str(error)

    def test_catch_config_errors(self):
        """Test catching all config errors with base class."""
        errors = [
            ConfigurationError("base"),
            ConfigFileNotFoundError("not found"),
            ConfigValidationError("invalid"),
        ]

        for error in errors:
            try:
                raise error
            except ConfigurationError:
                pass  # Successfully caught
            except Exception:
                pytest.fail(f"Should catch {type(error).__name__} as ConfigurationError")


class TestLLMExceptions:
    """Test LLM exception hierarchy."""

    def test_llm_error_inheritance(self):
        """Test LLMError inherits from CatoError."""
        error = LLMError("LLM error")
        assert isinstance(error, CatoError)

    def test_llm_connection_error(self):
        """Test LLMConnectionError."""
        error = LLMConnectionError("Cannot connect to OpenAI")
        assert isinstance(error, LLMError)
        assert "connect" in str(error).lower()

    def test_llm_authentication_error(self):
        """Test LLMAuthenticationError."""
        error = LLMAuthenticationError("Invalid API key")
        assert isinstance(error, LLMError)

    def test_llm_rate_limit_error(self):
        """Test LLMRateLimitError with retry_after."""
        error = LLMRateLimitError(
            "Rate limit exceeded",
            retry_after=60
        )
        assert isinstance(error, LLMError)
        assert error.retry_after == 60

    def test_llm_rate_limit_error_no_retry(self):
        """Test LLMRateLimitError without retry_after."""
        error = LLMRateLimitError("Rate limit exceeded")
        assert error.retry_after is None

    def test_llm_context_length_error(self):
        """Test LLMContextLengthError."""
        error = LLMContextLengthError(
            "Input too long",
            context={"tokens": 10000, "max": 8000}
        )
        assert isinstance(error, LLMError)
        assert "tokens" in error.context

    def test_llm_response_error(self):
        """Test LLMResponseError."""
        error = LLMResponseError("Empty response")
        assert isinstance(error, LLMError)

    def test_catch_all_llm_errors(self):
        """Test catching all LLM errors with base class."""
        errors = [
            LLMError("base"),
            LLMConnectionError("connection"),
            LLMAuthenticationError("auth"),
            LLMRateLimitError("rate limit"),
            LLMContextLengthError("context"),
            LLMResponseError("response"),
        ]

        for error in errors:
            try:
                raise error
            except LLMError:
                pass  # Successfully caught
            except Exception:
                pytest.fail(f"Should catch {type(error).__name__} as LLMError")


class TestVectorStoreExceptions:
    """Test vector store exception hierarchy."""

    def test_vector_store_error(self):
        """Test VectorStoreError."""
        error = VectorStoreError("Vector store error")
        assert isinstance(error, CatoError)

    def test_vector_store_connection_error(self):
        """Test VectorStoreConnectionError."""
        error = VectorStoreConnectionError("Cannot connect to ChromaDB")
        assert isinstance(error, VectorStoreError)

    def test_embedding_error(self):
        """Test EmbeddingError."""
        error = EmbeddingError("Failed to generate embeddings")
        assert isinstance(error, VectorStoreError)


class TestStorageExceptions:
    """Test storage exception hierarchy."""

    def test_storage_error(self):
        """Test StorageError."""
        error = StorageError("Database error")
        assert isinstance(error, CatoError)

    def test_storage_connection_error(self):
        """Test StorageConnectionError."""
        error = StorageConnectionError("Cannot open database")
        assert isinstance(error, StorageError)

    def test_storage_query_error(self):
        """Test StorageQueryError."""
        error = StorageQueryError(
            "Query failed",
            context={"query": "SELECT * FROM tasks"}
        )
        assert isinstance(error, StorageError)
        assert "query" in error.context


class TestCommandExceptions:
    """Test command exception hierarchy."""

    def test_command_error(self):
        """Test CommandError."""
        error = CommandError("Command error")
        assert isinstance(error, CatoError)

    def test_command_not_found_error(self):
        """Test CommandNotFoundError."""
        error = CommandNotFoundError(
            "Unknown command",
            context={"command": "unknowncmd"}
        )
        assert isinstance(error, CommandError)

    def test_command_argument_error(self):
        """Test CommandArgumentError."""
        error = CommandArgumentError("Missing required argument")
        assert isinstance(error, CommandError)

    def test_command_execution_error(self):
        """Test CommandExecutionError."""
        error = CommandExecutionError("Command execution failed")
        assert isinstance(error, CommandError)


class TestIOExceptions:
    """Test I/O exception hierarchy."""

    def test_io_error(self):
        """Test IOError."""
        error = IOError("I/O error")
        assert isinstance(error, CatoError)

    def test_file_access_error(self):
        """Test FileAccessError."""
        error = FileAccessError(
            "Permission denied",
            context={"path": "/etc/secret"}
        )
        assert isinstance(error, IOError)

    def test_network_error(self):
        """Test NetworkError."""
        error = NetworkError("Connection timeout")
        assert isinstance(error, IOError)


class TestTTSExceptions:
    """Test TTS exception hierarchy."""

    def test_tts_error(self):
        """Test TTSError."""
        error = TTSError("TTS error")
        assert isinstance(error, CatoError)

    def test_tts_connection_error(self):
        """Test TTSConnectionError."""
        error = TTSConnectionError("Cannot connect to TTS service")
        assert isinstance(error, TTSError)

    def test_tts_authentication_error(self):
        """Test TTSAuthenticationError."""
        error = TTSAuthenticationError("Invalid API key")
        assert isinstance(error, TTSError)

    def test_tts_rate_limit_error(self):
        """Test TTSRateLimitError with retry_after."""
        error = TTSRateLimitError("Rate limit exceeded", retry_after=120)
        assert isinstance(error, TTSError)
        assert error.retry_after == 120

    def test_tts_invalid_input_error(self):
        """Test TTSInvalidInputError."""
        error = TTSInvalidInputError(
            "Invalid voice",
            context={"voice": "unknown_voice"}
        )
        assert isinstance(error, TTSError)


class TestDisplayExceptions:
    """Test display exception hierarchy."""

    def test_display_error(self):
        """Test DisplayError."""
        error = DisplayError("Rendering failed")
        assert isinstance(error, CatoError)


class TestExceptionCatching:
    """Test catching exceptions at different levels."""

    def test_catch_specific_exception(self):
        """Test catching specific exception type."""
        try:
            raise LLMConnectionError("connection failed")
        except LLMConnectionError as e:
            assert "connection" in str(e)
        except Exception:
            pytest.fail("Should catch LLMConnectionError")

    def test_catch_category_exception(self):
        """Test catching exception category."""
        try:
            raise LLMAuthenticationError("auth failed")
        except LLMError as e:
            assert isinstance(e, LLMAuthenticationError)
        except Exception:
            pytest.fail("Should catch as LLMError")

    def test_catch_base_exception(self):
        """Test catching any Cato exception."""
        exceptions = [
            ConfigurationError("config"),
            LLMError("llm"),
            VectorStoreError("vector"),
            StorageError("storage"),
            CommandError("command"),
            IOError("io"),
            TTSError("tts"),
            DisplayError("display"),
        ]

        for exc in exceptions:
            try:
                raise exc
            except CatoError:
                pass  # Successfully caught
            except Exception:
                pytest.fail(f"Should catch {type(exc).__name__} as CatoError")


class TestExceptionRepresentation:
    """Test exception string representations."""

    def test_simple_message(self):
        """Test simple error message."""
        error = CatoError("Simple error")
        assert str(error) == "Simple error"

    def test_message_with_context(self):
        """Test error message includes context."""
        error = CatoError(
            "Error occurred",
            context={"key": "value", "count": 5}
        )
        result = str(error)
        assert "Error occurred" in result
        assert "key='value'" in result
        assert "count=5" in result

    def test_nested_context_values(self):
        """Test context with complex values."""
        error = CatoError(
            "Failed",
            context={"data": {"nested": "value"}}
        )
        result = str(error)
        assert "Failed" in result
        assert "data=" in result
