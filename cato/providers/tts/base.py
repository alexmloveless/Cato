"""TTS provider protocol definition."""

from typing import ClassVar, Protocol


class TTSProvider(Protocol):
    """
    Protocol for text-to-speech provider implementations.

    Any class implementing these methods can be used as a TTS provider.
    Providers are responsible for converting text to audio bytes.
    """

    VALID_VOICES: ClassVar[list[str]]
    VALID_MODELS: ClassVar[list[str]]

    @property
    def name(self) -> str:
        """
        Provider identifier.

        Returns
        -------
        str
            Provider name (e.g., 'openai').
        """
        ...

    async def synthesize(self, text: str, voice: str, model: str) -> bytes:
        """
        Synthesize speech from text.

        Parameters
        ----------
        text : str
            Text to convert to speech.
        voice : str
            Voice identifier to use for synthesis.
        model : str
            Model identifier to use for synthesis.

        Returns
        -------
        bytes
            MP3 audio data.

        Raises
        ------
        TTSError
            Base TTS error.
        TTSAuthenticationError
            Invalid API key.
        TTSConnectionError
            Cannot reach the provider.
        TTSRateLimitError
            Rate limit exceeded.
        TTSInvalidInputError
            Invalid voice, model, or text input.
        """
        ...
