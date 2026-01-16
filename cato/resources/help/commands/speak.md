# /speak

Convert and speak the last assistant response using text-to-speech.

## Usage

```
/speak              # Default voice and model
/speak nova         # Specific voice
/speak nova tts-1   # Specific voice and model
/s                  # Alias
```

## Description

The `/speak` command converts the most recent assistant response to audio using OpenAI's TTS API and plays it through your system's audio player.

Before synthesis, markdown formatting is cleaned from the text:
- Code blocks are replaced with "[code block]"
- Markdown links become plain text
- Bold/italic markers are removed
- Headers and list markers are normalized

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
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

## Configuration

```yaml
tts:
  enabled: true
  voice: nova
  model: tts-1
  audio_dir: /tmp
```

## Examples

```
/speak
/speak onyx
/speak nova tts-1-hd
/s
```

## See Also

- [/speaklike](speaklike.md) - Speak with custom instructions
