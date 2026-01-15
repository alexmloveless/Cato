# Configuration Specification

## Overview

Cato uses a layered configuration system with the following precedence (highest to lowest):
1. Command-line arguments
2. Environment variables
3. User configuration file (YAML)
4. Default configuration file (YAML with extensive inline documentation)

## Configuration Philosophy

### Overlay Behaviour
The user configuration file **overlays** the default configuration:
- User config only needs to specify values that differ from defaults
- A single key-value pair in user config is sufficient
- All unspecified values fall back to defaults
- No hard-coded defaults in code - all defaults stored in default YAML file

### Default Configuration File
The package includes a default configuration file with:
- All configuration options
- Sensible default values
- Extensive inline comments documenting each option
- This serves as both default values and user documentation

See CONFIG_REFERENCE.md for canonical keys, defaults, and paths.

## Configuration File

### File Locations (checked in order)
1. Path specified via `--config` CLI argument
2. `CATO_CONFIG_FILE` environment variable
3. `~/.config/cato/config.yaml`

### File Format
YAML configuration with nested sections:

```yaml
profile_name: "My Profile"
debug: false

section_1:
  value_1: whatever
  value_2: 1.0

section_2:
  value_3: whatever
  value_4: 1.0
```

## Configuration Sections

### Root Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| profile_name | string | null | Human-readable name for this configuration (e.g. "Work", "Personal") |
| debug | bool | false | Enable comprehensive debug mode |

### LLM Configuration (`llm`)

| Setting | Type | Default | Range | Description |
|---------|------|---------|-------|-------------|
| provider | string | openai | openai, anthropic, google, ollama | LLM provider selection |
| model | string | gpt-4o-mini | - | LLM model identifier |
| temperature | float | 1.0 | 0.0-2.0 | Response randomness |
| max_tokens | int | 4000 | >0 | Maximum response tokens |
| system_prompt_files | list | [] | - | Additional prompt files |
| base_prompt_file | string | (package default) | - | Alternative prompt file path |
| override_base_prompt | bool | false | - | Only has an effect if base_prompt_file is populated. If true will override the base in its entirety. If false, it will append. |

### Vector Store Configuration (`vector_store`)
See CONFIG_REFERENCE.md for canonical structure.

| Setting | Type | Default | Range | Description |
|---------|------|---------|-------|-------------|
| enabled | bool | true | - | Enable vector store |
| backend | string | chromadb | - | Vector store backend |
| path | string | ~/.local/share/cato/vectordb | - | Storage directory |
| collection_name | string | cato_memory | - | Collection name |
| chat_window | int | -1 | >0 | Max recent exchanges to retain in memory (-1 = all) |
| context_results | int | 5 | >0 | Max context exchanges returned |
| similarity_threshold | float | 0.65 | 0.0-1.0 | Minimum similarity score |
| dynamic_threshold | bool | true | - | Enable dynamic similarity thresholding |
| retrieval_strategy | string | default | - | Similarity retrieval strategy (see SPEC_VECTOR_STORE.md) |
| search_context_window | int | 3 | >0 | Recent exchanges used to build the search query |

**Embedding settings** (within `vector_store`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| embedding_provider | string | openai | openai, ollama |
| embedding_model | string | text-embedding-3-small | Embedding model |
| embedding_dimensions | int | 1536 | Vector dimensions |

**Chunking settings** (within `vector_store`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| chunking_strategy | string | semantic | truncate, fixed_size, semantic, hybrid |
| chunk_size | int | 1000 | Target chunk size (chars) |
| chunk_overlap | int | 100 | Overlap between chunks (chars) |
| max_chunk_size | int | 1500 | Maximum chunk size |
| preserve_sentence_boundaries | bool | true | Avoid mid-sentence splits |

### Display Configuration (`display`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| user_label | string | User | Label for user messages |
| assistant_label | string | Assistant | Label for assistant messages |
| no_rich | bool | false | Disable rich text formatting |
| no_color | bool | false | Disable ANSI colors |
| line_width | int | 80 | Terminal width (chars) |
| exchange_delimiter | string | ─ | Character for separation |
| exchange_delimiter_length | int | 60 | Delimiter line length |
| prompt_symbol | string | 🐱 >  | Input prompt (supports Unicode/emoji) |
| spinner_icon | string | ⠋ | Waiting indicator icon (spinner character) |


### Logging Configuration (`logging`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| level | string | WARNING | DEBUG, INFO, WARNING, ERROR |
| format | string | (standard format) | Log message format |
| show_context | bool | false | Show context in INFO logs |

### TTS Configuration (`tts`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| enabled | bool | true | Enable TTS functionality |
| voice | string | nova | Default voice |
| model | string | tts-1 | Default TTS model |
| audio_dir | string | /tmp | Audio file directory |

### Web Search Configuration (`web_search`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| enabled | bool | true | Enable web search |
| default_engine | string | duckduckgo | Default search engine |
| content_threshold | int | 500 | Max words per page |
| max_results | int | 3 | Max results to process (≤10) |
| timeout | int | 10 | Request timeout (seconds) |
| engines | dict | (built-in) | Search engine URLs |

### Location Aliases (`locations`)

Key-value pairs mapping alias names to paths:
```yaml
locations:
  docs: ~/Documents
  projects: ~/Code/projects
  config: ~/.config
```

## Command-Line Interface

CLI options, modes (including headless), and outputs are specified in `SPEC_COMMAND_LINE.md`. This document focuses on configuration data and precedence; CLI overrides remain the highest-precedence layer in the configuration stack.

## Environment Variables

### API Keys
| Variable | Description |
|----------|-------------|
| OPENAI_API_KEY | OpenAI API key (LLM, embeddings, TTS) |
| ANTHROPIC_API_KEY | Anthropic API key |
| GOOGLE_API_KEY | Google API key |

### Configuration Overrides

| Variable | Description |
|----------|-------------|
| CATO_CONFIG_FILE |  The path to the config file to use if one wasn't passed in the cmd args|

## Validation

### On Startup
1. Load configuration file (if found)
2. Parse YAML structure
3. Validate using Pydantic models:
   - Type checking
   - Range validation
   - Enum validation
4. Validate location aliases (paths exist)
5. Apply environment variable overrides
6. Apply CLI argument overrides
7. Report validation errors

If there is an appropriate existing parser or validator in pydantic (e.g. for file location validation) the you should use that in preference to creating a native one.

### Error Handling
- Invalid YAML: Show parse error, exit
- Missing required key: Use default
- Invalid value: Warn the user and fall back to default
- Invalid location alias: Log warning, continue


## Example Configurations

### Minimal Configuration
```yaml
llm:
  provider: openai
  model: gpt-4o-mini
```

### Development Configuration
```yaml
profile_name: Development
debug: true

llm:
  provider: openai
  model: gpt-4o-mini
  temperature: 0.7

logging:
  level: DEBUG

vector_store:
  path: ~/.local/share/cato/vectordb-dev
```

### Production Configuration
```yaml
profile_name: Production

llm:
  provider: openai
  model: gpt-4o
  temperature: 1.0
  max_tokens: 8000

vector_store:
  enabled: true
  similarity_threshold: 0.7

logging:
  level: WARNING
```

### Local Development (Ollama)
```yaml
profile_name: Local Ollama

llm:
  provider: ollama
  model: llama2
  temperature: 0.8

vector_store:
  enabled: false  # Optional for local

tts:
  enabled: false
```
