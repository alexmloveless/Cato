# Cato

A terminal-first LLM chat client with productivity features, designed for maximum control over LLM interactions.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Cato is a powerful, configuration-driven chat client that brings LLM interactions to your terminal with integrated productivity tools. Built for developers and power users who want full control over their AI workflows.

### Key Features

- 🤖 **Multi-Provider Support**: OpenAI, Anthropic Claude, Google Gemini, and Ollama
- 🧠 **Vector Store Integration**: ChromaDB-powered semantic memory for conversation context
- ✅ **Productivity System**: Built-in task and list management with SQLite backend
- 🎨 **Rich Terminal UI**: Beautiful markdown rendering with customizable themes
- 🔍 **Web Search Integration**: DuckDuckGo search with content extraction
- 🔊 **Text-to-Speech**: OpenAI TTS integration for audio responses
- 📝 **Comprehensive Help**: In-app documentation with LLM-assisted search
- ⚙️ **Highly Configurable**: YAML-based configuration with environment variable support

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cato.git
cd cato

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

### Configuration

1. Set up your API keys:
```bash
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
# Or add to ~/.bashrc or ~/.zshrc
```

2. (Optional) Create a custom config:
```bash
mkdir -p ~/.config/cato
cp cato/resources/defaults.yaml ~/.config/cato/config.yaml
# Edit ~/.config/cato/config.yaml to customize
```

### First Run

```bash
# Start Cato
cato

# Or with debug mode
cato --debug
```

## Core Principles

- **Chat client first, productivity second** — Commands are explicit; no natural-language command layer
- **Modular and flexible architecture** — Components can be swapped or removed without rewrites
- **Spec-driven development** — Functional and technical specs are the source of truth
- **Configuration-driven** — YAML defaults with overlays; avoid hard-coded values
- **Robust, navigable help** — Documentation is comprehensive and kept up to date

## Features in Detail

### Multi-Provider LLM Support

Switch between providers and models seamlessly:

```bash
# Change model
/model gpt-4

# Or configure in config.yaml
llm:
  provider: anthropic
  model: claude-sonnet-4
```

Supported providers:
- **OpenAI**: GPT-4, GPT-3.5, etc.
- **Anthropic**: Claude 3.5 Sonnet, Claude 3 Opus
- **Google**: Gemini Pro
- **Ollama**: Any locally hosted model

### Vector Store Memory

Automatic conversation storage and retrieval:

```yaml
vector_store:
  enabled: true
  backend: chromadb
  context_results: 5
  similarity_threshold: 0.8
```

Commands:
- `/vadd <text>` - Add content to vector store
- `/vdoc <path>` - Add document with chunking
- `/vquery <query>` - Search stored content
- `/vstats` - View store statistics
- `/continue <session_id>` - Resume previous conversation

### Productivity System

Built-in task and list management:

```bash
# View tasks
/st                    # Show all tasks
/st -s pending         # Filter by status
/st -p high            # Filter by priority

# Manage lists
/list                  # Show all lists
/list shopping         # Show items in shopping list
```

### Web Search

Integrated web search with content extraction:

```bash
# Search and add to context
/web "machine learning best practices"

# Fetch URL content
/url https://example.com/article

# Store URL in vector store
/url_store
```

### Text-to-Speech

Convert responses to audio:

```bash
# Speak last response
/speak

# With specific voice
/speak nova

# With custom instructions
/speaklike "speak like a pirate"
```

### Comprehensive Help System

```bash
# Get help
/help                  # Show overview
/help commands         # List all commands
/help <command>        # Command-specific help
/help model "question" # Ask LLM about Cato
```

## Command Reference

### Core Commands
- `/help` - Display help information
- `/exit`, `/quit`, `/q` - Exit application
- `/clear` - Clear conversation history
- `/config` - Show current configuration

### History & Context
- `/history [n]` - Show conversation history
- `/delete [n]` - Remove exchanges
- `/model [name]` - Show/change model
- `/showsys` - Display system prompt
- `/continue <id>` - Resume previous thread

### Vector Store
- `/vadd <text>` - Add text to store
- `/vdoc <path>` - Add document file
- `/vquery <query>` - Search store
- `/vstats` - Show statistics
- `/vdelete <id>` - Delete document
- `/vget <id>` - Retrieve document

### Productivity
- `/st [options]` - Show tasks
- `/list [name]` - Show lists/items

### Web & Search
- `/web "query" [engine]` - Search web
- `/url <url>` - Fetch URL content
- `/url_store` - Store URL in vector store

### Text-to-Speech
- `/speak [voice] [model]` - Speak last response
- `/speaklike "instructions"` - Speak with style

## Configuration

Cato uses a layered configuration system:

1. **Package defaults** (`cato/resources/defaults.yaml`)
2. **User config** (`~/.config/cato/config.yaml`)
3. **Environment variables** (`CATO_*`)
4. **CLI flags** (`--debug`, `--config`)

### Configuration File Example

```yaml
llm:
  provider: openai
  model: gpt-4
  temperature: 0.7
  max_tokens: 2000

vector_store:
  enabled: true
  backend: chromadb
  path: ~/.local/share/cato/chroma
  context_results: 5
  similarity_threshold: 0.8

display:
  theme: gruvbox-dark
  markdown_enabled: true
  max_width: 120

logging:
  level: INFO
  file_path: ~/.local/share/cato/logs/cato.log
```

See [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md) for complete configuration documentation.

### Environment Variables

Override any config value with environment variables:

```bash
export CATO_LLM_MODEL="gpt-4"
export CATO_VECTOR_STORE_ENABLED="true"
export CATO_DEBUG="true"
```

## Development

### Setup

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=cato

# Linting
ruff check .

# Type checking
mypy cato
```

### Project Structure

```
cato/
├── commands/          # Slash command implementations
├── core/             # Core exceptions, config, types
├── display/          # Terminal UI and rendering
├── providers/        # LLM, TTS, search providers
├── resources/        # Default config, help docs
├── services/         # Chat, help, productivity services
└── storage/          # Database and vector store

tests/
├── unit/             # Unit tests
└── integration/      # Integration tests
```

### Architecture

Cato follows a layered architecture:

```
Presentation Layer (display/)
    ↓
Command Layer (commands/)
    ↓
Service Layer (services/)
    ↓
Provider Layer (providers/)
    ↓
Storage Layer (storage/)
    ↓
Core Layer (core/)
```

## Documentation

- [Configuration Reference](CONFIG_REFERENCE.md) - Complete configuration guide
- [CHANGELOG](CHANGELOG.md) - Version history and changes
- [Project Specs](Project/Spec/) - Functional and technical specifications
- [Implementation Plan](Project/Plans/) - Development roadmap
- In-app help: `/help` command

## Requirements

- Python 3.11 or higher
- API keys for your chosen LLM provider(s)
- Optional: Local Ollama installation for offline models

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Cato is currently a personal project focused on single-user workflows. While not actively seeking contributions, bug reports and feature suggestions are welcome via GitHub issues.

## Acknowledgments

Built with:
- [Rich](https://github.com/Textualize/rich) - Terminal rendering
- [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - Interactive prompts
- [Pydantic](https://github.com/pydantic/pydantic) - Configuration validation
- [ChromaDB](https://github.com/chroma-core/chroma) - Vector store
- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python) - Claude API
- [OpenAI SDK](https://github.com/openai/openai-python) - OpenAI API

## Support

For issues, questions, or feature requests, please open a GitHub issue.
