# Configuration Specification

## Overview

Ocat uses a layered configuration system with the following precedence (highest to lowest):
1. Command-line arguments
2. Environment variables
3. Configuration file (YAML)
4. Built-in defaults

## Configuration File

### File Locations (checked in order)
1. Path specified via `--config` CLI argument
2. `~/.ocat/config.yaml`
3. `./ocat.yaml` (current directory)
4. `./.ocat.yaml` (current directory, hidden)

### File Format
YAML configuration with nested sections:

```yaml
profile_name: "My Profile"
debug: false

llm:
  model: gpt-4o-mini
  temperature: 1.0
  max_tokens: 4000
  system_prompt_files: []
  base_prompt_file: ""
  override_base_prompt: false

vector_store:
  enabled: true
  path: ./vector_stores/default/
  similarity_threshold: 0.65
  chat_window: 3
  context_results: 5
  search_context_window: 3
  memory_threshold: 0.7
  memory_results: 3

embedding:
  model: text-embedding-3-small
  dimensions: 1536

chunking:
  strategy: semantic
  chunk_size: 1000
  chunk_overlap: 100
  max_chunk_size: 1500
  preserve_sentence_boundaries: true

display:
  user_label: User
  assistant_label: Assistant
  no_rich: false
  no_color: false
  line_width: 80
  response_on_new_line: true
  exchange_delimiter: "─"
  exchange_delimiter_length: 60
  high_contrast: true
  prompt_symbol: "🐱 > "

productivity:
  proactive_memory_suggestions: false
  routing_marker: "%"

file_tools:
  routing_marker: "@"

logging:
  level: WARN
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  show_context: false

tts:
  enabled: true
  voice: nova
  model: tts-1
  audio_dir: /tmp

web_search:
  enabled: true
  default_engine: duckduckgo
  content_threshold: 500
  max_results: 3
  timeout: 10
  engines:
    google: "https://www.google.com/search?q={query}"
    bing: "https://www.bing.com/search?q={query}"
    duckduckgo: "https://duckduckgo.com/html/?q={query}"

locations:
  docs: ~/Documents
  projects: ~/Code/projects
```

## Configuration Sections

### Root Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| profile_name | string | null | Profile name for display |
| debug | bool | false | Enable comprehensive debug mode |

### LLM Configuration (`llm`)

| Setting | Type | Default | Range | Description |
|---------|------|---------|-------|-------------|
| model | string | gpt-4o-mini | - | LLM model identifier |
| temperature | float | 1.0 | 0.0-2.0 | Response randomness |
| max_tokens | int | 4000 | >0 | Maximum response tokens |
| system_prompt_files | list | [] | - | Additional prompt files |
| base_prompt_file | string | (package default) | - | Base prompt file path |
| override_base_prompt | bool | false | - | Skip base prompt (warns user) |

### Vector Store Configuration (`vector_store`)

| Setting | Type | Default | Range | Description |
|---------|------|---------|-------|-------------|
| enabled | bool | true | - | Enable vector store |
| path | string | ./vector_stores/default/ | - | Storage directory |
| similarity_threshold | float | 0.65 | 0.0-1.0 | Minimum similarity for context |
| chat_window | int | 3 | >0 | Recent exchanges for context queries |
| context_results | int | 5 | >0 | Max context exchanges returned |
| search_context_window | int | 3 | >0 | Recent exchanges in search query |
| memory_threshold | float | 0.7 | 0.0-1.0 | Similarity for memory retrieval |
| memory_results | int | 3 | >0 | Max memories returned |

### Embedding Configuration (`embedding`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| model | string | text-embedding-3-small | Embedding model |
| dimensions | int | 1536 | Vector dimensions |

### Chunking Configuration (`chunking`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| strategy | string | semantic | truncate, fixed_size, semantic, hybrid |
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
| response_on_new_line | bool | true | Extra spacing before response |
| exchange_delimiter | string | ─ | Character for separation |
| exchange_delimiter_length | int | 60 | Delimiter line length |
| high_contrast | bool | true | Brighter colors |
| prompt_symbol | string | 🐱 >  | Input prompt |

### Productivity Configuration (`productivity`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| proactive_memory_suggestions | bool | false | Suggest storing personal facts |
| routing_marker | string | % | Prefix for productivity messages |

### File Tools Configuration (`file_tools`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| routing_marker | string | @ | Prefix for file operation messages |

### Logging Configuration (`logging`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| level | string | WARN | DEBUG, INFO, WARN, ERROR |
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

## Command-Line Arguments

### Configuration
| Argument | Description |
|----------|-------------|
| `--config <path>` | Path to configuration file |
| `--profile <name>` | Configuration profile name |

### Model Overrides
| Argument | Description |
|----------|-------------|
| `--model <name>` | LLM model name |
| `--temperature <float>` | Temperature (0.0-2.0) |
| `--max-tokens <int>` | Maximum tokens |

### Vector Store
| Argument | Description |
|----------|-------------|
| `--vector-store-path <path>` | Vector store directory |
| `--no-vector-store` | Disable vector store |
| `--similarity-threshold <float>` | Similarity threshold |

### Display
| Argument | Description |
|----------|-------------|
| `--no-rich` | Disable rich formatting |
| `--no-color` | Disable colors |
| `--line-width <int>` | Terminal width |

### Logging
| Argument | Description |
|----------|-------------|
| `--log-level <level>` | DEBUG, INFO, WARN, ERROR |

### Special Modes
| Argument | Description |
|----------|-------------|
| `--debug` | Enable debug mode |
| `--dummy-mode` | Use mock LLM responses |
| `--casual` | Start in casual mode |

### Headless Operations
| Argument | Description |
|----------|-------------|
| `--add-to-vector-store <path>` | Add document and exit |
| `--query-vector-store <query>` | Query vector store and exit |
| `--vector-store-stats` | Show stats and exit |

### Other
| Argument | Description |
|----------|-------------|
| `--version` | Show version and exit |
| `--help` | Show help and exit |

## Environment Variables

### API Keys
| Variable | Description |
|----------|-------------|
| OPENAI_API_KEY | OpenAI API key (LLM, embeddings, TTS) |
| ANTHROPIC_API_KEY | Anthropic API key |
| GOOGLE_API_KEY | Google API key |

### Configuration Overrides
Environment variables can override config settings using the pattern:
`OCAT_{SECTION}_{SETTING}` (uppercase)

Example:
```bash
export OCAT_LLM_MODEL=gpt-4o
export OCAT_LOGGING_LEVEL=DEBUG
export OCAT_VECTOR_STORE_ENABLED=false
```

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

### Error Handling
- Invalid YAML: Show parse error, exit
- Missing required key: Use default
- Invalid value: Show validation error, exit
- Invalid location alias: Log warning, continue

## Profile System

### Purpose
Profiles allow switching between configurations for different use cases.

### Usage
```bash
ocat --profile work
ocat --profile personal
```

### Profile Identification
The `profile_name` setting is displayed in:
- Welcome panel
- Config display (`/config`)

## Example Configurations

### Minimal Configuration
```yaml
llm:
  model: gpt-4o-mini
```

### Development Configuration
```yaml
profile_name: Development
debug: true

llm:
  model: gpt-4o-mini
  temperature: 0.7

logging:
  level: DEBUG

vector_store:
  path: ./vector_stores/dev/
```

### Production Configuration
```yaml
profile_name: Production

llm:
  model: gpt-4o
  temperature: 1.0
  max_tokens: 8000

vector_store:
  enabled: true
  similarity_threshold: 0.7

logging:
  level: WARN
```

### Local Development (Ollama)
```yaml
profile_name: Local Ollama

llm:
  model: llama2
  temperature: 0.8

vector_store:
  enabled: false  # Optional for local

tts:
  enabled: false
```
