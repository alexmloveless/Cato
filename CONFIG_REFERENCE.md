# Configuration Reference

Complete guide to configuring Cato.

## Table of Contents

- [Configuration System](#configuration-system)
- [LLM Provider](#llm-provider)
- [Vector Store](#vector-store)
- [Storage](#storage)
- [Display](#display)
- [Logging](#logging)
- [Commands](#commands)
- [Paths](#paths)
- [Text-to-Speech](#text-to-speech)
- [Web Search](#web-search)
- [Location Aliases](#location-aliases)
- [Environment Variables](#environment-variables)

## Configuration System

Cato uses a layered configuration approach:

1. **Package defaults** - `cato/resources/defaults.yaml` (always loaded)
2. **User config** - `~/.config/cato/config.yaml` (overlays defaults)
3. **Environment variables** - `CATO_*` variables (override config file)
4. **CLI flags** - `--config`, `--debug` (override everything)

### Configuration Files

**Default location**: `~/.config/cato/config.yaml`

**Alternative location**: Set `CATO_CONFIG_FILE` environment variable

**Format**: YAML with Pydantic validation

### Creating a Config File

```bash
# Create config directory
mkdir -p ~/.config/cato

# Copy defaults as template
cp cato/resources/defaults.yaml ~/.config/cato/config.yaml

# Edit to customize
nano ~/.config/cato/config.yaml
```

**Important**: Only include settings you want to change from defaults.

## LLM Provider

Configure LLM provider and model selection.

### Basic Settings

```yaml
llm:
  provider: "openai"           # openai, anthropic, google, ollama
  model: "gpt-4o-mini"        # Provider-specific model ID
  temperature: 1.0            # 0.0 (deterministic) to 2.0 (random)
  max_tokens: 4000            # Maximum response length
  timeout_seconds: 60         # Request timeout
```

### Provider-Specific Configuration

#### OpenAI

```yaml
llm:
  provider: "openai"
  model: "gpt-4"              # gpt-4, gpt-4-turbo, gpt-3.5-turbo, etc.
  openai:
    api_key: "${OPENAI_API_KEY}"
```

**Recommended models**:
- `gpt-4` - Most capable
- `gpt-4-turbo` - Faster, cheaper
- `gpt-4o-mini` - Fastest, cheapest
- `gpt-3.5-turbo` - Legacy, very fast

#### Anthropic

```yaml
llm:
  provider: "anthropic"
  model: "claude-sonnet-4"
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
```

**Recommended models**:
- `claude-sonnet-4` - Best balance
- `claude-opus-4` - Most capable
- `claude-haiku-4` - Fastest, cheapest

#### Google Gemini

```yaml
llm:
  provider: "google"
  model: "gemini-pro"
  google:
    api_key: "${GOOGLE_API_KEY}"
```

**Recommended models**:
- `gemini-pro` - Standard model
- `gemini-pro-vision` - With image support

#### Ollama (Local)

```yaml
llm:
  provider: "ollama"
  model: "llama3"             # Any model you've pulled
  ollama:
    base_url: "http://localhost:11434"
```

**Setup Ollama**:
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3

# Start server (if not auto-started)
ollama serve
```

### System Prompts

Customize the system prompt:

```yaml
llm:
  # Additional prompts to append to default
  system_prompt_files:
    - ~/my_custom_prompt.txt
    - ~/.config/cato/expert_mode.txt

  # Replace default prompt entirely
  base_prompt_file: ~/.config/cato/my_base_prompt.txt
  override_base_prompt: true    # If true, ignore package default
```

## Vector Store

Configure conversation memory and semantic search.

### Basic Settings

```yaml
vector_store:
  enabled: true
  backend: "chromadb"
  path: "~/.local/share/cato/vectordb"
  collection_name: "cato_memory"
```

### Context Retrieval

```yaml
vector_store:
  # Number of similar exchanges to retrieve
  context_results: 5

  # Recent exchanges used to build search query
  search_context_window: 3

  # Minimum similarity score (0.0-1.0, lower = more similar)
  similarity_threshold: 0.65

  # Dynamically adjust threshold
  dynamic_threshold: true

  # Retrieval strategy
  retrieval_strategy: "default"

  # Max recent exchanges in memory (-1 = all)
  chat_window: -1
```

**Tuning similarity_threshold**:
- `0.5-0.7` - More permissive (retrieves more context)
- `0.7-0.9` - Balanced (default range)
- `0.9-1.0` - Very strict (only exact matches)

### Embedding Configuration

```yaml
vector_store:
  # Embedding provider
  embedding_provider: "openai"    # openai or ollama

  # Model for embeddings
  embedding_model: "text-embedding-3-small"

  # Vector dimensions (must match model)
  embedding_dimensions: 1536
```

**Embedding models**:
- OpenAI `text-embedding-3-small` - 1536 dims, fast, cheap
- OpenAI `text-embedding-3-large` - 3072 dims, more accurate
- Ollama - Use any model pulled locally

### Document Chunking

```yaml
vector_store:
  # Chunking strategy
  chunking_strategy: "semantic"   # truncate, fixed_size, semantic, hybrid

  # Target chunk size (characters)
  chunk_size: 1000

  # Overlap between chunks
  chunk_overlap: 100

  # Maximum chunk size
  max_chunk_size: 1500

  # Preserve sentence boundaries
  preserve_sentence_boundaries: true
```

**Chunking strategies**:
- `truncate` - Simply cut at limit
- `fixed_size` - Split into equal chunks
- `semantic` - Split at sentence/paragraph boundaries
- `hybrid` - Combine semantic and fixed-size

## Storage

Configure SQLite database for tasks, lists, and sessions.

```yaml
storage:
  # Database file path
  database_path: "~/.local/share/cato/cato.db"

  # Enable automatic backups
  backup_enabled: false

  # Backup frequency (hours)
  backup_frequency_hours: 24
```

**Database location**: Can be changed to sync with cloud storage:
```yaml
storage:
  database_path: "~/Dropbox/cato/cato.db"
```

## Display

Configure terminal UI appearance.

### Theme

```yaml
display:
  theme: "default"              # default, gruvbox-dark, or custom theme name
  markdown_enabled: true        # Render markdown formatting
  code_theme: "monokai"        # Syntax highlighting theme
  max_width: null              # Max width (null = terminal width)
```

**Built-in themes**:
- `default` - Clean, minimal
- `gruvbox-dark` - Retro, warm dark theme

**Custom themes**: Place in `~/.config/cato/themes/<name>.yaml`

### Formatting

```yaml
display:
  timestamps: false             # Show message timestamps
  spinner_style: "dots"         # Loading spinner
  prompt_symbol: "🐱 > "       # Input prompt (supports emoji)
  line_width: 80               # Formatting width
  exchange_delimiter: "─"      # Exchange separator character
  exchange_delimiter_length: 60
```

### Style Overrides

```yaml
display:
  style_overrides:
    user: "bold cyan"
    assistant: "green"
    system: "dim yellow"
    error: "bold red"
    warning: "yellow"
    info: "blue"
    code: "magenta"
```

**Rich style format**: `[modifier] [color] [on background]`

Examples:
- `bold cyan`
- `dim yellow on black`
- `italic green`

## Logging

Configure application logging.

```yaml
logging:
  level: "WARNING"              # DEBUG, INFO, WARNING, ERROR
  file_path: "~/.local/share/cato/cato.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  max_file_size_mb: 10
  backup_count: 3              # Number of rotated log files
```

**Log levels**:
- `DEBUG` - Everything (very verbose)
- `INFO` - General information
- `WARNING` - Warnings and errors only (default)
- `ERROR` - Errors only

**Disable file logging**:
```yaml
logging:
  file_path: null
```

## Commands

Configure command system behavior.

```yaml
commands:
  prefix: "/"                   # Command prefix
  history_file: "~/.local/share/cato/command_history"
```

**Change command prefix** (not recommended):
```yaml
commands:
  prefix: "!"    # Use ! instead of /
```

## Paths

Configure application directories.

```yaml
paths:
  data_dir: "~/.local/share/cato"
  config_dir: "~/.config/cato"
  cache_dir: "~/.cache/cato"
```

**Custom locations**:
```yaml
paths:
  data_dir: "~/Dropbox/cato/data"
  config_dir: "~/Dropbox/cato/config"
  cache_dir: "/tmp/cato-cache"
```

## Text-to-Speech

Configure OpenAI TTS integration.

### Basic Settings

```yaml
tts:
  enabled: true
  voice: "nova"                 # Default voice
  model: "tts-1"               # tts-1 or tts-1-hd
  audio_dir: "/tmp"            # Temporary audio files
```

### Voice Options

**Available voices**:
- `alloy` - Neutral, balanced
- `echo` - Warm, conversational
- `fable` - Expressive, dynamic
- `nova` - Friendly, natural (default)
- `onyx` - Deep, authoritative
- `shimmer` - Bright, energetic

### Model Options

- `tts-1` - Standard quality, faster
- `tts-1-hd` - High definition, slower, higher quality

**Example**:
```yaml
tts:
  enabled: true
  voice: "onyx"
  model: "tts-1-hd"
  audio_dir: "~/Music/cato-audio"
```

**Requirements**:
- `OPENAI_API_KEY` environment variable
- Audio player: mpg123 (Linux), ffplay (cross-platform), or afplay (macOS)

## Web Search

Configure web search and content extraction.

### Basic Settings

```yaml
web_search:
  enabled: true
  default_engine: "duckduckgo"
  content_threshold: 500        # Max words per result
  max_results: 3               # Number of results to process
  timeout: 10                  # Request timeout (seconds)
```

### Search Engines

```yaml
web_search:
  engines:
    duckduckgo: "https://duckduckgo.com/html/?q={query}"
    google: "https://www.google.com/search?q={query}"
    bing: "https://www.bing.com/search?q={query}"
```

**Add custom search engine**:
```yaml
web_search:
  engines:
    custom: "https://example.com/search?q={query}"
```

## Location Aliases

Define shortcuts for file operations.

```yaml
locations:
  docs: ~/Documents
  projects: ~/Code/projects
  notes: ~/Dropbox/Notes
  config: ~/.config
```

**Usage**:
```bash
/cd docs              # Navigate to ~/Documents
/ls projects          # List ~/Code/projects
/cat config/file.txt  # View ~/.config/file.txt
```

## Environment Variables

Override any configuration value with environment variables.

### Format

```bash
export CATO_SECTION_KEY="value"
```

### Examples

```bash
# LLM configuration
export CATO_LLM_MODEL="gpt-4"
export CATO_LLM_TEMPERATURE="0.8"

# Vector store
export CATO_VECTOR_STORE_ENABLED="true"
export CATO_VECTOR_STORE_CONTEXT_RESULTS="10"

# Display
export CATO_DISPLAY_THEME="gruvbox-dark"
export CATO_DISPLAY_MARKDOWN_ENABLED="true"

# Logging
export CATO_LOGGING_LEVEL="DEBUG"

# General
export CATO_DEBUG="true"
```

### API Keys

```bash
# Required for providers
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
```

### Variable Expansion

Use `${VAR}` syntax in config files:

```yaml
llm:
  openai:
    api_key: "${OPENAI_API_KEY}"

paths:
  data_dir: "${HOME}/.local/share/cato"
  custom_path: "${MY_CUSTOM_DIR}/cato"
```

## Configuration Examples

### Minimal Config (OpenAI)

```yaml
llm:
  provider: "openai"
  model: "gpt-4o-mini"
  openai:
    api_key: "${OPENAI_API_KEY}"
```

### Full-Featured Config

```yaml
llm:
  provider: "anthropic"
  model: "claude-sonnet-4"
  temperature: 0.8
  max_tokens: 8000
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"

vector_store:
  enabled: true
  context_results: 10
  similarity_threshold: 0.7

display:
  theme: "gruvbox-dark"
  markdown_enabled: true
  max_width: 120
  timestamps: true
  prompt_symbol: "💬 "

logging:
  level: "INFO"
  file_path: "~/.local/share/cato/logs/cato.log"

tts:
  enabled: true
  voice: "nova"
  model: "tts-1-hd"

web_search:
  enabled: true
  max_results: 5

locations:
  docs: ~/Documents
  code: ~/Code
  notes: ~/Dropbox/Notes
```

### Offline/Local Config (Ollama)

```yaml
llm:
  provider: "ollama"
  model: "llama3"
  ollama:
    base_url: "http://localhost:11434"

vector_store:
  enabled: true
  embedding_provider: "ollama"
  embedding_model: "nomic-embed-text"

tts:
  enabled: false    # Requires OpenAI API

web_search:
  enabled: false    # Optional for offline use
```

## Validation

Cato uses Pydantic for configuration validation. Invalid values will be rejected on startup with helpful error messages.

**Common validation errors**:
- Temperature out of range (0.0-2.0)
- Invalid provider name
- Missing required API keys
- Invalid file paths
- Chunk overlap >= chunk size

## Troubleshooting

### Config not loading

```bash
# Check config file location
ls -la ~/.config/cato/config.yaml

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('~/.config/cato/config.yaml'))"

# Run with debug
cato --debug
```

### API key errors

```bash
# Check environment variables
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Reset to defaults

```bash
# Backup current config
mv ~/.config/cato/config.yaml ~/.config/cato/config.yaml.bak

# Cato will use package defaults
cato
```

## See Also

- [README.md](README.md) - Installation and quick start
- [CHANGELOG.md](CHANGELOG.md) - Version history
- `/help config` - In-app configuration help
- `/config` - View current configuration
