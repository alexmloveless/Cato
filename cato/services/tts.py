"""
TTS service for text-to-speech functionality.

This module provides the TTSService class which handles text cleaning,
audio generation via TTS providers, and audio playback.
"""

import asyncio
import logging
import platform
import re
import shutil
import time
from pathlib import Path

from cato.core.config import TTSConfig
from cato.core.exceptions import TTSError
from cato.providers.tts.base import TTSProvider

logger = logging.getLogger(__name__)


class TTSService:
    """
    Service for text-to-speech functionality.

    Coordinates text cleaning, TTS generation, and audio playback.

    Parameters
    ----------
    provider : TTSProvider
        TTS provider instance for synthesis.
    config : TTSConfig
        TTS configuration settings.

    Attributes
    ----------
    provider : TTSProvider
        The configured TTS provider.
    config : TTSConfig
        TTS configuration.
    """

    def __init__(self, provider: TTSProvider, config: TTSConfig) -> None:
        self.provider = provider
        self.config = config
        self._audio_dir = Path(config.audio_dir)
        self._audio_dir.mkdir(parents=True, exist_ok=True)
        logger.info(
            f"TTSService initialized with provider={provider.name}, "
            f"voice={config.voice}, model={config.model}"
        )

    def clean_text(self, text: str) -> str:
        """
        Clean text for TTS by removing code blocks and markdown formatting.

        Parameters
        ----------
        text : str
            Raw text with possible markdown formatting.

        Returns
        -------
        str
            Cleaned text suitable for speech synthesis.
        """
        # Remove code blocks (```code```) → "[code block]"
        text = re.sub(r"```[\s\S]*?```", "[code block]", text)

        # Remove markdown links [text](url) → text
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

        # Remove bold (**text** or __text__) → text
        text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
        text = re.sub(r"__([^_]+)__", r"\1", text)

        # Remove italic (*text* or _text_) → text
        text = re.sub(r"\*([^*]+)\*", r"\1", text)
        text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"\1", text)

        # Remove headers (# Header) → Header
        text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)

        # Remove list markers (- item or * item) → item
        text = re.sub(r"^[-*]\s+", "", text, flags=re.MULTILINE)

        # Remove numbered list markers (1. item) → item
        text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)

        # Normalize whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = text.strip()

        return text

    async def speak(
        self,
        text: str,
        voice: str | None = None,
        model: str | None = None,
    ) -> Path:
        """
        Generate TTS audio and save to file.

        Parameters
        ----------
        text : str
            Text to convert to speech.
        voice : str | None, optional
            Voice to use. Defaults to config voice.
        model : str | None, optional
            Model to use. Defaults to config model.

        Returns
        -------
        Path
            Path to the saved audio file.

        Raises
        ------
        TTSError
            If TTS generation fails.
        """
        voice = voice or self.config.voice
        model = model or self.config.model

        cleaned_text = self.clean_text(text)

        logger.debug(f"Generating TTS with voice={voice}, model={model}")
        audio_data = await self.provider.synthesize(cleaned_text, voice, model)

        timestamp = int(time.time())
        audio_path = self._audio_dir / f"cato_tts_{timestamp}.mp3"
        audio_path.write_bytes(audio_data)

        logger.info(f"Audio saved to {audio_path}")
        return audio_path

    async def play_audio(self, path: Path) -> None:
        """
        Play audio file using system audio player.

        Parameters
        ----------
        path : Path
            Path to audio file to play.

        Raises
        ------
        TTSError
            If no audio player is found or playback fails.
        """
        player = self.find_audio_player()
        if not player:
            raise TTSError(
                "No suitable audio player found. "
                "Please install mpg123, ffplay, or another audio player."
            )

        system = platform.system()
        try:
            if system == "Windows":
                process = await asyncio.create_subprocess_exec(
                    "cmd",
                    "/c",
                    "start",
                    "",
                    str(path),
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )
            elif player == "ffplay":
                process = await asyncio.create_subprocess_exec(
                    player,
                    "-nodisp",
                    "-autoexit",
                    str(path),
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )
            else:
                process = await asyncio.create_subprocess_exec(
                    player,
                    str(path),
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )

            await process.wait()

            if process.returncode != 0:
                raise TTSError(f"Audio player exited with code {process.returncode}")

        except FileNotFoundError as e:
            raise TTSError(f"Audio player not found: {e}")
        except Exception as e:
            raise TTSError(f"Failed to play audio: {e}")

    def find_audio_player(self) -> str | None:
        """
        Find an available audio player for the current platform.

        Returns
        -------
        str | None
            Name of available audio player, or None if not found.
        """
        system = platform.system()

        if system == "Darwin":
            if shutil.which("afplay"):
                return "afplay"
        elif system == "Windows":
            return "start"
        else:
            for player in ["mpg123", "ffplay", "aplay", "paplay"]:
                if shutil.which(player):
                    return player

        return None
