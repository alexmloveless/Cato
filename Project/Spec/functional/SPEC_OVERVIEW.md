# Cato Functional Specification - Overview

## Application Summary

**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management capabilities, and conversational context through vector storage.

## Purpose

Cato provides a unified terminal interface for:
- Conversational AI interactions with multiple LLM providers
- Personal productivity management (unified list system for todos, shopping, etc.)
- File operations and code management
- Persistent conversational context with retrieval
- Text-to-speech synthesis
- Web search integration

## Core Design Principles

1. **Terminal-First**: All functionality accessible via keyboard in a command-line interface
2. **Rich Output**: Markdown rendering, syntax highlighting, and formatted tables
3. **Unified Experience**: Single interface for chat, productivity, and file operations
4. **Persistent Storage**: Conversation and productivity data persisted across sessions
5. **Extensible Commands**: Slash command system for explicit actions
6. **Graceful Degradation**: Continue operation when individual components fail

## Application Flow

### Startup
1. Load configuration (YAML file → environment variables → CLI overrides)
2. Initialize Rich console for formatted output
3. Display welcome panel with model and profile information
4. Initialize chat session:
   - Set up LLM backend based on configured provider
   - Initialize vector store for conversation memory
   - Initialize productivity system (SQLite storage)
   - Initialize file tools integration
5. Enter interactive REPL loop

### Input Processing Order
User input is processed in the following priority order:

1. **Slash commands**: Input starting with `/` routes to command parser
2. **Regular chat**: All other input sent to LLM with context retrieval

### Session State
- **Session ID**: Unique UUID generated per application launch
- **Thread ID**: Unique UUID for conversation continuity
- **Message history**: List of messages (system, user, assistant)
- **Current directory**: For file operations
- **Context mode**: Debug display mode for showing retrieved context (off/on/summary)

## Specification Documents

This specification is divided into the following functional areas:

| Document | Description |
|----------|-------------|
| SPEC_CORE_CHAT.md | LLM integration, message processing, display |
| SPEC_COMMAND_SYSTEM.md | Slash command framework and all commands |
| SPEC_HELP_SYSTEM.md | Help system behavior and navigation |
| SPEC_LISTS.md | Unified list system (todos, shopping, etc.) |
| SPEC_FILE_OPERATIONS.md | File commands, attach, export, aliases |
| SPEC_VECTOR_STORE.md | Conversation storage, similarity search |
| SPEC_TTS.md | Text-to-speech functionality |
| SPEC_WEB_SEARCH.md | Web search and URL content fetching |
| SPEC_CONFIGURATION.md | All configuration options |
| SPEC_COMMAND_LINE.md | CLI options, modes, and headless behavior |

Canonical references:
- CONFIG_REFERENCE.md (config keys, paths, context semantics)
- DATA_MODELS.md (canonical data models)
- GLOSSARY.md (terminology)

## User Interface

### Welcome Message
The welcome message displays key configuration that affects behaviour (excluding style):

```
─ 🐱 Cato ─────────────────────────────────────────────────
Welcome to Cato - Chat at the Terminal Orchestrator

Type your messages to chat with the LLM.
Type /help to see available commands.
Type /exit to quit the application.

Config: Margaret (~/.config/cato/margaret.yaml)
Model: gpt-4o-mini
Vector Store: enabled (~/.local/share/cato/vectordb)
TTS: enabled
───────────────────────────────────────────────────────────
```

**Required information:**
- Configuration name (`profile_name`) and file path
- Current model
- Behavioural settings that differ from defaults (not style)

**Purpose:** User can scroll to top of session to see exactly what configuration is active without checking files

### Prompt
Default: `🐱 > ` (configurable via `display.prompt_symbol`)

### Response Display
- Assistant responses rendered with clear visual separation (NOT bordered panels)
- Response text must be directly copy-pasteable without formatting artifacts
- Markdown formatting with syntax highlighting for code
- Configurable line width and styling
- Visual delimiter between exchanges

### Status Indicators
- 🔵 Active
- 🟡 In Progress  
- ✅ Completed
- 🗑️ Deleted
- 💭 Context indicator
- 🔊 TTS indicator

## Technology Stack

### Required Dependencies
- **LLM Clients**: OpenAI, Anthropic, Google Generative AI (via provider SDKs)
- **Local LLM**: Ollama (optional)
- **Vector Database**: ChromaDB
- **Embeddings**: OpenAI or Ollama (via embedding provider)
- **Productivity Storage**: SQLite
- **CLI Framework**: Rich (formatting), prompt_toolkit (input)
- **Configuration**: PyYAML, Pydantic (validation)
- **AI Agent**: pydantic-ai (for productivity agent)

### Optional Dependencies
- **TTS**: OpenAI TTS API
- **Audio Playback**: mpg123, ffplay, or system audio player
- **Web Search**: DuckDuckGo, Google, Bing (via HTTP requests)

## Error Handling Philosophy

1. **Non-critical failures**: Log warning, continue with reduced functionality
   - Vector store unavailable → chat continues without context retrieval
   - TTS playback fails → show error, continue chat
   - Web search fails → show error, allow retry

2. **Critical failures**: Log error, show user message, exit gracefully
   - Configuration invalid
   - LLM backend cannot initialize
   - No API key when required

3. **User cancellation**: Ctrl+C interrupts current operation, returns to prompt
