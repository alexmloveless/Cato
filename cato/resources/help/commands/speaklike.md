# /speaklike

Speak the last assistant response with custom instructions prepended.

## Usage

```
/speaklike "instructions"
/speaklike "instructions" voice
/speaklike "instructions" voice model
/sl "instructions"
```

## Description

The `/speaklike` command works like `/speak`, but allows you to provide custom instructions that are prepended to the response text before TTS generation. This can modify how the content is spoken.

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| instructions | Yes | - | Custom speaking instructions (quoted) |
| voice | No | nova | Voice selection |
| model | No | tts-1 | Model selection |

## Voices

| Voice | Description |
|-------|-------------|
| alloy | Neutral, balanced |
| echo | Warm, conversational |
| fable | Expressive, dynamic |
| nova | Friendly, natural |
| onyx | Deep, authoritative |
| shimmer | Bright, energetic |

## Models

| Model | Quality | Speed |
|-------|---------|-------|
| tts-1 | Standard | Faster |
| tts-1-hd | High Definition | Slower |

## Requirements

- `OPENAI_API_KEY` environment variable must be set
- Audio player: mpg123, ffplay, afplay (macOS), or Windows default player

## Examples

```
/speaklike "Speak slowly and clearly"
/sl "Read as if explaining to a 5-year-old"
/sl "Read as a formal news broadcast" onyx tts-1-hd
```

## See Also

- [/speak](speak.md) - Speak without custom instructions
