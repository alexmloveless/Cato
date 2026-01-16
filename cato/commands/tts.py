"""
TTS commands for text-to-speech functionality.

This module implements commands for speaking assistant responses
using OpenAI's TTS API.
"""

import logging
import os

from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command
from cato.core.config import TTSConfig
from cato.core.exceptions import TTSError, TTSInvalidInputError
from cato.providers.tts.openai import OpenAITTSProvider
from cato.services.tts import TTSService

logger = logging.getLogger(__name__)

VALID_VOICES = ["alloy", "echo", "fable", "nova", "onyx", "shimmer"]
VALID_MODELS = ["tts-1", "tts-1-hd"]


def _get_last_assistant_message(ctx: CommandContext) -> str | None:
    """
    Get the last assistant message from conversation history.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.

    Returns
    -------
    str | None
        Last assistant message content, or None if not found.
    """
    messages = ctx.conversation.messages
    for message in reversed(messages):
        if message.role == "assistant":
            return message.content
    return None


def _create_tts_service(config: TTSConfig) -> TTSService:
    """
    Create TTS service with OpenAI provider.

    Parameters
    ----------
    config : TTSConfig
        TTS configuration.

    Returns
    -------
    TTSService
        Configured TTS service.
    """
    provider = OpenAITTSProvider()
    return TTSService(provider, config)


@command(name="speak", aliases=["s"])
async def speak_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Speak the last assistant response.

    Usage:
      /speak              # Default voice and model
      /speak nova         # Specific voice
      /speak nova tts-1   # Specific voice and model
      /s                  # Alias

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Optional voice and model arguments.

    Returns
    -------
    CommandResult
        Success/failure with message.
    """
    if not ctx.config.tts.enabled:
        return CommandResult(success=False, message="TTS is disabled in configuration")

    if not os.environ.get("OPENAI_API_KEY"):
        return CommandResult(
            success=False, message="OPENAI_API_KEY environment variable not set"
        )

    voice = args[0] if len(args) > 0 else None
    model = args[1] if len(args) > 1 else None

    if voice and voice not in VALID_VOICES:
        return CommandResult(
            success=False,
            message=f"Invalid voice '{voice}'. Valid voices: {', '.join(VALID_VOICES)}",
        )

    if model and model not in VALID_MODELS:
        return CommandResult(
            success=False,
            message=f"Invalid model '{model}'. Valid models: {', '.join(VALID_MODELS)}",
        )

    last_message = _get_last_assistant_message(ctx)
    if not last_message:
        return CommandResult(success=False, message="No assistant response found to speak")

    try:
        tts_service = _create_tts_service(ctx.config.tts)
        display_voice = voice or ctx.config.tts.voice

        ctx.display.show_info(f"🔊 Generating speech using {display_voice} voice...")

        audio_path = await tts_service.speak(last_message, voice, model)
        ctx.display.show_info(f"🎵 Audio saved to: {audio_path}")

        ctx.display.show_info("🎧 Playing audio...")
        await tts_service.play_audio(audio_path)

        return CommandResult(success=True, message="✅ Audio playback completed")

    except TTSInvalidInputError as e:
        return CommandResult(success=False, message=str(e))
    except TTSError as e:
        return CommandResult(success=False, message=f"Failed to generate or play TTS: {e}")
    except Exception as e:
        logger.exception("Unexpected TTS error")
        return CommandResult(success=False, message=f"Failed to generate or play TTS: {e}")


@command(name="speaklike", aliases=["sl"])
async def speaklike_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Speak the last assistant response with custom instructions prepended.

    Usage:
      /speaklike "instructions"
      /sl "Speak slowly and clearly"
      /sl "Read as a news anchor" echo tts-1-hd

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Instructions (required), optional voice and model.

    Returns
    -------
    CommandResult
        Success/failure with message.
    """
    if not ctx.config.tts.enabled:
        return CommandResult(success=False, message="TTS is disabled in configuration")

    if not os.environ.get("OPENAI_API_KEY"):
        return CommandResult(
            success=False, message="OPENAI_API_KEY environment variable not set"
        )

    if len(args) < 1:
        return CommandResult(
            success=False,
            message='Instructions are required. Usage: /speaklike "instructions" [voice] [model]',
        )

    instructions = args[0]
    voice = args[1] if len(args) > 1 else None
    model = args[2] if len(args) > 2 else None

    if voice and voice not in VALID_VOICES:
        return CommandResult(
            success=False,
            message=f"Invalid voice '{voice}'. Valid voices: {', '.join(VALID_VOICES)}",
        )

    if model and model not in VALID_MODELS:
        return CommandResult(
            success=False,
            message=f"Invalid model '{model}'. Valid models: {', '.join(VALID_MODELS)}",
        )

    last_message = _get_last_assistant_message(ctx)
    if not last_message:
        return CommandResult(success=False, message="No assistant response found to speak")

    text_with_instructions = f"{instructions}\n\n{last_message}"

    try:
        tts_service = _create_tts_service(ctx.config.tts)
        display_voice = voice or ctx.config.tts.voice

        ctx.display.show_info(f"🔊 Generating speech using {display_voice} voice...")

        audio_path = await tts_service.speak(text_with_instructions, voice, model)
        ctx.display.show_info(f"🎵 Audio saved to: {audio_path}")

        ctx.display.show_info("🎧 Playing audio...")
        await tts_service.play_audio(audio_path)

        return CommandResult(success=True, message="✅ Audio playback completed")

    except TTSInvalidInputError as e:
        return CommandResult(success=False, message=str(e))
    except TTSError as e:
        return CommandResult(success=False, message=f"Failed to generate or play TTS: {e}")
    except Exception as e:
        logger.exception("Unexpected TTS error")
        return CommandResult(success=False, message=f"Failed to generate or play TTS: {e}")
