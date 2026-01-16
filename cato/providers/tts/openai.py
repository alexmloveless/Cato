"""OpenAI TTS provider implementation."""

import logging
import os

import openai
from openai import AsyncOpenAI

from cato.core.exceptions import (
    TTSAuthenticationError,
    TTSConnectionError,
    TTSInvalidInputError,
    TTSRateLimitError,
)

logger = logging.getLogger(__name__)


class OpenAITTSProvider:
    """
    OpenAI TTS API provider implementation.

    Supports text-to-speech synthesis via OpenAI's async client.

    Parameters
    ----------
    api_key : str | None, optional
        OpenAI API key. If not provided, reads from OPENAI_API_KEY environment variable.
    timeout : int, optional
        Request timeout in seconds. Defaults to 60.

    Raises
    ------
    TTSAuthenticationError
        If no API key is provided or found in environment.
    """

    VALID_VOICES: list[str] = ["alloy", "echo", "fable", "nova", "onyx", "shimmer"]
    VALID_MODELS: list[str] = ["tts-1", "tts-1-hd"]

    def __init__(
        self,
        api_key: str | None = None,
        timeout: int = 60,
    ) -> None:
        resolved_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not resolved_key:
            raise TTSAuthenticationError("OPENAI_API_KEY environment variable not set")

        self._client = AsyncOpenAI(api_key=resolved_key, timeout=timeout)

    @property
    def name(self) -> str:
        """Provider name."""
        return "openai"

    async def synthesize(self, text: str, voice: str, model: str) -> bytes:
        """
        Synthesize speech from text using OpenAI TTS API.

        Parameters
        ----------
        text : str
            Text to convert to speech.
        voice : str
            Voice identifier (alloy, echo, fable, nova, onyx, shimmer).
        model : str
            Model identifier (tts-1, tts-1-hd).

        Returns
        -------
        bytes
            MP3 audio data.

        Raises
        ------
        TTSInvalidInputError
            Invalid voice, model, or empty text.
        TTSAuthenticationError
            Invalid API key.
        TTSConnectionError
            Cannot reach OpenAI.
        TTSRateLimitError
            Rate limit exceeded.
        """
        if voice not in self.VALID_VOICES:
            raise TTSInvalidInputError(
                f"Invalid voice '{voice}'. Valid voices: {', '.join(self.VALID_VOICES)}"
            )

        if model not in self.VALID_MODELS:
            raise TTSInvalidInputError(
                f"Invalid model '{model}'. Valid models: {', '.join(self.VALID_MODELS)}"
            )

        if not text or not text.strip():
            raise TTSInvalidInputError("No readable text found after cleaning")

        try:
            response = await self._client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                response_format="mp3",
            )
            return bytes(response.content)

        except openai.AuthenticationError as e:
            logger.error(f"OpenAI TTS authentication failed: {e}")
            raise TTSAuthenticationError(f"OpenAI authentication failed: {e}")
        except openai.RateLimitError as e:
            retry_after = self._parse_retry_after(e)
            logger.warning(f"OpenAI TTS rate limit hit, retry after: {retry_after}s")
            raise TTSRateLimitError(
                f"Rate limit exceeded: {e}", retry_after=retry_after
            )
        except openai.APIConnectionError as e:
            logger.error(f"OpenAI TTS connection error: {e}")
            raise TTSConnectionError(f"Failed to connect to OpenAI: {e}")
        except openai.BadRequestError as e:
            logger.error(f"OpenAI TTS bad request: {e}")
            raise TTSInvalidInputError(f"Bad request: {e}")
        except Exception as e:
            logger.error(f"Unexpected OpenAI TTS error: {e}")
            raise TTSConnectionError(f"Failed to generate TTS: {e}")

    def _parse_retry_after(self, error: openai.RateLimitError) -> int | None:
        """Extract retry-after value from rate limit error."""
        return None
