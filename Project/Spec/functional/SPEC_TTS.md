# Text-to-Speech Specification

## Overview

Ocat provides text-to-speech functionality using OpenAI's TTS API to convert assistant responses to spoken audio.

## Requirements

### API Key
- Requires `OPENAI_API_KEY` environment variable
- Uses same key as LLM and embeddings

### Audio Player
One of the following must be available:
- **Linux**: mpg123, ffplay, aplay, or paplay
- **macOS**: afplay (built-in)
- **Windows**: Default media player via `start` command

## Commands

### /speak, /s
Convert and speak the last assistant response.

```
/speak              # Default voice and model
/speak nova         # Specific voice
/speak nova tts-1   # Specific voice and model
/s                  # Alias
```

**Arguments:**
| Position | Name | Default | Description |
|----------|------|---------|-------------|
| 1 | voice | nova (config) | Voice selection |
| 2 | model | tts-1 (config) | Model selection |

### /speaklike, /sl
Speak with custom instructions prepended.

```
/speaklike "instructions" [voice] [model]
/sl "Speak slowly and clearly"
/sl "Read as a news anchor" echo tts-1-hd
```

**Arguments:**
| Position | Name | Required | Description |
|----------|------|----------|-------------|
| 1 | instructions | Yes | Custom speaking instructions |
| 2 | voice | No | Voice selection |
| 3 | model | No | Model selection |

**Behavior:**
Instructions are prepended to the response text before TTS generation.

## Voices

| Voice | Description |
|-------|-------------|
| alloy | Neutral, balanced |
| echo | Warm, conversational |
| fable | Expressive, dynamic |
| nova | Friendly, natural |
| onyx | Deep, authoritative |
| shimmer | Bright, energetic |

Default: `nova` (configurable)

## Models

| Model | Quality | Speed | Cost |
|-------|---------|-------|------|
| tts-1 | Standard | Faster | Lower |
| tts-1-hd | High Definition | Slower | Higher |

Default: `tts-1` (configurable)

## Text Processing

### Content Cleaning
Before TTS generation, content is cleaned:

1. **Code blocks removed**: ````code```` → `[code block]`
2. **Inline code preserved**: `code` → code
3. **Markdown links**: `[text](url)` → text
4. **Bold/Italic removed**: `**bold**` → bold
5. **Headers simplified**: `# Header` → Header
6. **List markers removed**: `- item` → item
7. **Extra whitespace normalized**

### Empty Content
If no readable text remains after cleaning:
- Error: "No readable text found after cleaning"

## Audio Output

### File Storage
```yaml
tts:
  audio_dir: /tmp
```

Audio files are saved to configured directory:
- Filename: `cato_tts_{timestamp}.mp3`
- Files persist after playback (not auto-deleted)

### Playback Flow
1. Generate TTS audio via OpenAI API
2. Save MP3 to `audio_dir`
3. Display save confirmation
4. Play audio using system player
5. Wait for playback completion
6. Display completion message

### Progress Display
```
🔊 Generating speech using nova voice...
🎵 Audio saved to: /tmp/ocat_tts_1705123456.mp3
🎧 Playing audio...
✅ Audio playback completed
```

## Configuration

### TTS Settings
```yaml
tts:
  enabled: true
  voice: nova
  model: tts-1
  audio_dir: /tmp
```

| Setting | Default | Description |
|---------|---------|-------------|
| enabled | true | Enable TTS functionality |
| voice | nova | Default voice |
| model | tts-1 | Default model |
| audio_dir | /tmp | Directory for audio files |

### Disabling TTS
```yaml
tts:
  enabled: false
```

When disabled, `/speak` and `/speaklike` commands return error.

## Error Handling

### API Errors
- Invalid API key: "OPENAI_API_KEY environment variable not set"
- API failure: "Failed to generate or play TTS: {error}"

### Audio Player Errors
- No player found: "No suitable audio player found. Please install mpg123, ffplay, or another audio player."
- Playback failure: "Audio player exited with code {code}"

### Content Errors
- No assistant response: "No assistant response found to speak"
- Empty after cleaning: "No readable text found after cleaning"

### Command Errors
- TTS disabled: "TTS is disabled in configuration"
- Invalid voice: "Invalid voice '{voice}'. Valid voices: alloy, echo, fable, nova, onyx, shimmer"
- Invalid model: "Invalid model '{model}'. Valid models: tts-1, tts-1-hd"
- Missing instructions: "Instructions are required. Usage: /speaklike \"instructions\" [voice] [model]"

## Platform-Specific Behavior

### Linux
Searches for audio players in order:
1. mpg123
2. ffplay (with `-nodisp -autoexit` flags)
3. aplay
4. paplay

### macOS
Uses built-in `afplay` command.

### Windows
Uses `start` command to open with default media player.

## Usage Examples

### Basic Speech
```
/speak
```
Speaks last response with default settings.

### Voice Selection
```
/speak onyx
```
Speaks with deep, authoritative voice.

### High Quality
```
/speak nova tts-1-hd
```
Speaks with HD audio quality.

### Custom Instructions
```
/speaklike "Speak as if explaining to a 5-year-old"
```
Adds context before the response text.

### News Style
```
/sl "Read this as a formal news broadcast" onyx tts-1-hd
```
Professional news anchor style with HD audio.
