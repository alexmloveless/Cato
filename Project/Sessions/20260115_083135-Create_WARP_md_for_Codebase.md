USER:
/init

AGENT:

**Command Executed:**
```bash
ls -la /home/alex/Documents/repos/Cato
```

**Output:**
```
total 16
drwxr-xr-x 4 alex alex 4096 Jan 13 11:47 .
drwxr-xr-x 7 alex alex 4096 Jan 13 11:46 ..
drwxr-xr-x 7 alex alex 4096 Jan 14 18:20 .git
drwxr-xr-x 4 alex alex 4096 Jan 14 12:59 Project
```


**Command Executed:**
```bash
ls -laR /home/alex/Documents/repos/Cato/Project
```

**Output:**
```
/home/alex/Documents/repos/Cato/Project:
total 16
drwxr-xr-x 4 alex alex 4096 Jan 14 12:59 .
drwxr-xr-x 4 alex alex 4096 Jan 13 11:47 ..
drwxr-xr-x 2 alex alex 4096 Jan 14 13:00 Notes
drwxr-xr-x 4 alex alex 4096 Jan 14 18:17 Spec

/home/alex/Documents/repos/Cato/Project/Notes:
total 28
drwxr-xr-x 2 alex alex  4096 Jan 14 13:00  .
drwxr-xr-x 4 alex alex  4096 Jan 14 12:59  ..
-rw-r--r-- 1 alex alex 19426 Jan 14 13:00 'Jan 14 at 11-01.md'

/home/alex/Documents/repos/Cato/Project/Spec:
total 24
drwxr-xr-x 4 alex alex 4096 Jan 14 18:17 .
drwxr-xr-x 4 alex alex 4096 Jan 14 12:59 ..
drwxr-xr-x 2 alex alex 4096 Jan 14 18:18 functional
-rw-r--r-- 1 alex alex 4904 Jan 14 18:17 GENERAL_PRINCIPLES.md
drwxr-xr-x 2 alex alex 4096 Jan 14 18:18 technical

/home/alex/Documents/repos/Cato/Project/Spec/functional:
total 100
drwxr-xr-x 2 alex alex 4096 Jan 14 18:18 .
drwxr-xr-x 4 alex alex 4096 Jan 14 18:17 ..
-rw-r--r-- 1 alex alex 6865 Jan 14 18:20 FUNCTIONAL_SPECIFICATION_OVERVIEW.md
-rw-r--r-- 1 alex alex 9201 Jan 14 18:20 SPEC_COMMAND_SYSTEM.md
-rw-r--r-- 1 alex alex 8485 Jan 14 18:18 SPEC_CONFIGURATION.md
-rw-r--r-- 1 alex alex 7560 Jan 14 18:19 SPEC_CORE_CHAT.md
-rw-r--r-- 1 alex alex 7541 Jan 14 18:18 SPEC_FILE_OPERATIONS.md
-rw-r--r-- 1 alex alex 5804 Jan 14 18:20 SPEC_OVERVIEW.md
-rw-r--r-- 1 alex alex 6467 Jan 14 18:18 SPEC_PRODUCTIVITY.md
-rw-r--r-- 1 alex alex 5101 Jan 14 18:18 SPEC_TTS.md
-rw-r--r-- 1 alex alex 9704 Jan 14 18:19 SPEC_VECTOR_STORE.md
-rw-r--r-- 1 alex alex 6562 Jan 14 18:18 SPEC_WEB_SEARCH.md

/home/alex/Documents/repos/Cato/Project/Spec/technical:
total 20
drwxr-xr-x 2 alex alex 4096 Jan 14 18:18 .
drwxr-xr-x 4 alex alex 4096 Jan 14 18:17 ..
-rw-r--r-- 1 alex alex 2817 Jan 14 18:17 TECH_CODE_ORGANISATION.md
-rw-r--r-- 1 alex alex 3558 Jan 14 18:17 TECH_ERROR_HANDLING.md
-rw-r--r-- 1 alex alex 2452 Jan 14 18:18 TECH_PERFORMANCE.md
```



**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/GENERAL_PRINCIPLES.md**
```
# Cato General Principles

## Purpose
Cato (Chat at the Terminal Orchestrator) exists to provide maximum control over LLM interactions, tailored to specific user needs and idiosyncrasies. It is a chat client first, productivity client second.

## Core Philosophy

### Terminal-First
- Cato is a terminal application. Alternative frontends should use terminal paradigms.
- Separation of logic and display enables pluggable terminal frontends.
- Style configuration should be kept separate unless very specific to a frontend paradigm.

### Single User Focus
- Built for a single user on a single machine.
- Designed for users who are highly changeable, like to tinker and experiment.
- Configuration and architecture should be as flexible as possible.
- Multiple instances may run with different configurations simultaneously - users should manage collisions manually.

### Quality Over Convenience
- No tolerance for poor design decisions, bad architecture, or lazy coding.
- Core architecture must remain flexible and modular.
- Any component should be easily unplugged or switched out.
- Highest engineering standards required.

## Specification-Driven Development
- The functional specification is the bible for all development.
- The specification is not static - it must be kept updated at all times.
- Any decision that adds to or alters the specification must be documented with what changed and when.
- All development, design, and architecture decisions must be logged.

## Configuration Philosophy
- Configuration file driven as much as possible.
- YAML format with extensive inline documentation.
- **No hard-coded inline values** - all defaults stored in YAML, not as function/method defaults.
- User configuration overlays default configuration - only override what differs.
- A single key-value pair in user config is sufficient; all other values fall back to defaults.
- Use Pydantic extensively for validation.
- Unrecognised config items should warn but not crash - continue with defaults.

## Dependency Management
- Favour the Pydantic stack for API interactions (pydantic-ai over LangChain).
- Minimise external library dependencies where existing approved dependencies suffice.
- Do not code natively what can be done with approved dependencies.
- Do not add new dependencies outside the approved stack without explicit approval.

## Agent Architecture
- Cato is NOT an agent - it is a chat and productivity client.
- Agent-like features for specific tasks may be added later but are not in initial scope.
- Natural language interface to productivity/commands is explicitly NOT wanted - commands use slash syntax.

## Documentation Philosophy

### Codebase Self-Documentation
- Separated modules (especially in directories) should contain a README explaining:
  - What is in the directory
  - What it is used for
  - Pointers to common functions/classes/methods
  - How to add legitimate elements
- An `agent.txt` file should exist at root to help any model/agent quickly navigate the codebase.
- Goal: minimise code scanning by models/agents to understand the system.

### User Documentation
- In-app help must be extensive, robust, and always kept up to date.
- Help system should be easy to navigate without relying on the model.
- The model does not need to know how Cato works unless explicitly asked via `/help model`.

### System Prompt
- Base/master system prompt contains minimum needed for model to do its job.
- Master prompt is sacrosanct - changes treated as code changes.
- User system prompt is appended to master prompt.
- Model does not need awareness of UI mechanics.

## Error Handling Philosophy
- Atomic exception handling - as specific as possible.
- No broad exception catching.
- Favour catching exceptions over returning error messages from Python.
- Clear, human-readable error messages.
- Errors should be expensive and visible - don't hide problems.
- Application should almost diagnose itself.

### Logging Modes
- **Debug mode**: Extremely chatty, comprehensive logging throughout stack.
- **Warn mode**: Chatty but only relevant to user experience.
- Never do anything silently - report failures to user clearly.

## Performance Requirements
- Boot as quickly as possible - effectively instantaneous.
- All database interactions in real-time - no data caching outside context.
- **Never load entire vector store into memory**.
- No gradual streamed output required, but show waiting indicator for long responses.

## Multi-Provider Support
- Assume multiple models from multiple providers will be used.
- Assume multiple agents from multiple providers will be used.
- Architecture must support any combination.

## Future Considerations
- Architecture should allow for multimodal elements (not in initial spec).
- Headless mode for one-shot queries (limited functionality).
- Real-time context retrieval from vector store as conversation topics change.

```

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md**
```
# Cato Functional Specification - Overview

## Application Summary

**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management capabilities, and conversational memory through vector storage.

## Purpose

Cato provides a unified terminal interface for:
- Conversational AI interactions with multiple LLM providers
- Personal productivity management (tasks, lists, time tracking, memories)
- File operations and code management
- Persistent conversational memory with context retrieval
- Text-to-speech synthesis
- Web search integration

## Core Design Principles

1. **Terminal-First**: All functionality accessible via keyboard in a command-line interface
2. **Rich Output**: Markdown rendering, syntax highlighting, and formatted tables
3. **Unified Experience**: Single interface for chat, productivity, and file operations
4. **Persistent Memory**: Conversation and productivity data persisted across sessions
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

1. **Memory prompts**: If awaiting yes/no response for memory storage suggestion
2. **Slash commands**: Input starting with `/` routes to command parser
3. **Productivity routing**: Input starting with `%` routes to productivity agent
4. **File routing**: Input starting with `@` routes to file tools agent
5. **Regular chat**: All other input sent to LLM with context retrieval

### Session State
- **Session ID**: Unique UUID generated per application launch
- **Thread ID**: Unique UUID for conversation continuity
- **Message history**: List of messages (system, user, assistant)
- **Current directory**: For file operations
- **Context mode**: Controls display of retrieved context (on/off/summary)

## Specification Documents

This specification is divided into the following functional areas:

| Document | Description |
|----------|-------------|
| SPEC_CORE_CHAT.md | LLM integration, message processing, display |
| SPEC_COMMAND_SYSTEM.md | Slash command framework and all commands |
| SPEC_PRODUCTIVITY.md | Tasks, lists, timelog, memories |
| SPEC_FILE_OPERATIONS.md | File commands, attach, export, aliases |
| SPEC_VECTOR_STORE.md | Conversation storage, similarity search |
| SPEC_TTS.md | Text-to-speech functionality |
| SPEC_WEB_SEARCH.md | Web search and URL content fetching |
| SPEC_CONFIGURATION.md | All configuration options |

## User Interface

### Welcome Message
The welcome message displays key configuration that affects behaviour (excluding style):

```
─ 🐱 Cato ─────────────────────────────────────────────────
Welcome to Cato - Chat at the Terminal Orchestrator

Type your messages to chat with the LLM.
Type /help to see available commands.
Type /exit to quit the application.

Config: Margaret (~/.cato/margaret.yaml)
Model: gpt-4o-mini
Vector Store: enabled (./vector_stores/default/)
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
- 🧠 Memory recall indicator
- 💭 Context indicator
- 🔊 TTS indicator

## Technology Stack

### Required Dependencies
- **LLM Clients**: OpenAI, Anthropic, Google Generative AI (via provider SDKs)
- **Local LLM**: Ollama (optional)
- **Vector Database**: ChromaDB
- **Embeddings**: OpenAI Embeddings API
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
   - Vector store unavailable → chat continues without memory
   - TTS playback fails → show error, continue chat
   - Web search fails → show error, allow retry

2. **Critical failures**: Log error, show user message, exit gracefully
   - Configuration invalid
   - LLM backend cannot initialize
   - No API key when required

3. **User cancellation**: Ctrl+C interrupts current operation, returns to prompt

```

**/home/alex/Documents/repos/Cato/Project/Spec/functional/FUNCTIONAL_SPECIFICATION_OVERVIEW.md**
```
# Cato Functional Specification

## Overview

**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management capabilities, and conversational memory through vector storage.

## Core Chat Functionality

### LLM Integration
- **Multi-Provider Support**: OpenAI (GPT models), Anthropic (Claude), Google (Gemini), Ollama (local models)
- **Configurable Parameters**: Model selection, temperature, max tokens, system prompts
- **Rich UI**: Markdown rendering, syntax highlighting, configurable display themes

### Conversation Management
- **History Navigation**: Arrow key navigation through command history
- **Context Control**: Toggle context display (`/showcontext on|off|summary`)
- **Session Persistence**: Vector storage for conversation memory and retrieval
- **Thread Continuity**: Continue previous conversations by thread ID
- **Message Export**: JSON, Markdown formats with various export options

## Productivity System

### Task Management
- **Task Organization**: Categories, priorities (urgent/high/medium/low), due dates
- **Task Status**: Active, in-progress, completed tracking
- **Task Display**: Rich table with sorting, filtering by status/category/priority

### List Management
- **Named Lists**: Create and manage multiple lists (shopping, projects, etc.)
- **List Items**: Add, categorize, and status track items within lists
- **List Overview**: Show all lists with item counts or specific list contents


## File Operations

### File Integration
- **Attach to Context**: Include file contents in conversation context
- **Code Extraction**: Extract code blocks from responses to files
- **Vector Storage**: Add file contents to vector store for future reference
- **Export Operations**: Save conversations and responses in various formats

### Location Aliases
- **Custom Shortcuts**: Configure aliases for frequently accessed paths
- **Alias Resolution**: Use `alias:filename` syntax in commands
- **Configuration**: Define in YAML configuration file

## Vector Store & Memory

### Conversation Storage
- **Automatic Storage**: Store all conversation exchanges for future reference  
- **Similarity Search**: Find relevant past conversations based on current context
- **Context Retrieval**: Automatically include relevant past exchanges in responses

### Document Management
- **File Indexing**: Add documents to vector store with intelligent chunking
- **Text Addition**: Direct text addition to vector store via commands
- **Search & Retrieval**: Query vector store for similar content
- **Statistics**: Monitor vector store usage and performance

## Web Search Integration

### Search Functionality
- **Multi-Engine Support**: DuckDuckGo (default), Google, Bing
- **Content Processing**: Intelligent content extraction and cleaning
- **Context Integration**: Automatically add search results to conversation context
- **Result Filtering**: Focus on main content, skip non-text files

### Search Commands
- **Web Search**: `/web "query" [engine]` - search and integrate results
- **URL Fetch**: `/url <url>` - fetch content from specific URL
- **Smart Processing**: Content truncation, relevance filtering

## Text-to-Speech

### Speech Synthesis
- **OpenAI TTS**: Multiple voices (alloy, echo, fable, nova, onyx, shimmer)
- **Model Selection**: Standard (tts-1) and HD quality (tts-1-hd)
- **Custom Instructions**: Modify speaking style with `/speaklike`
- **Audio Management**: Automatic playback with file retention

### Speech Commands
- **Basic Speech**: `/speak [voice] [model]` - speak last response
- **Custom Speech**: `/speaklike "instructions" [voice] [model]`
- **Content Cleaning**: Automatic markdown and code block filtering

## Command System

### Slash Commands
- **Core Commands**: `/help`, `/clear`, `/exit`, `/config`, `/history`
- **File Commands**: `/file read/write/list/search`, `/cd`, `/pwd`, `/ls`, `/cat`
- **Productivity Commands**: `/st`, `/list`, `/at`, `/ct`
- **Vector Commands**: `/vadd`, `/vdoc`, `/vget`, `/vquery`, `/vstats`
- **Export Commands**: `/writejson`, `/writemd`, `/writecode`, `/copy`
- **TTS Commands**: `/speak`, `/speaklike`
- **Web Commands**: `/web`, `/url`


## Configuration & Customization

### Configuration File
- **YAML Format**: Comprehensive configuration in `cato.yaml`
- **Environment Variables**: Support for API keys and overrides
- **Overlay System**: User config overlays defaults, only specify differences
- **Location Aliases**: Custom path shortcuts

### CLI Options
- **Model Overrides**: Change model, temperature, max tokens
- **Vector Store Control**: Enable/disable, path configuration, similarity thresholds
- **Display Options**: Line width, color schemes, rich text control
- **Special Modes**: Debug mode, dummy mode, casual mode

### Display Customization
- **Rich Formatting**: Markdown rendering, syntax highlighting, color themes
- **Layout Control**: Line width, response positioning, delimiter customization
- **Accessibility**: High contrast mode, configurable labels and prompts
- **Migration Tools**: Headless mode operations for data management

## Quality Features

### Error Handling
- **Graceful Degradation**: Continue operation when individual components fail
- **User Feedback**: Clear error messages and recovery suggestions
- **Debug Support**: Comprehensive logging and debug mode
- **Fallback Modes**: Mock responses for testing, offline operation support

### Performance Features
- **Async Operations**: Non-blocking LLM requests and file operations
- **Timeout Handling**: Request timeouts with cancellation support

### User Experience
- **Rich Interface**: Beautiful terminal UI with colors and formatting
- **History Navigation**: Command history with autocomplete suggestions
- **Progress Indicators**: Visual feedback for long operations
- **Keyboard Shortcuts**: Efficient navigation and operation cancellation

## Technical Architecture

### Core Components
- **Chat Engine**: Async conversation management with multi-provider LLM support
- **Productivity Engine**: Task, list
- **File Engine**: File operations with location alias support
- **Vector Store**: ChromaDB-based conversation and document storage
- **Command System**: Extensible slash command framework

### Data Storage
- **Vector Store**: ChromaDB for embeddings and similarity search
- **Productivity Data**: SQLite database for structured productivity information
- **Configuration**: YAML-based configuration with environment variable support
- **File System**: Direct file system operations with alias resolution

### Integration Points
- **LLM Providers**: OpenAI, Anthropic, Google, Ollama APIs
- **TTS Services**: OpenAI text-to-speech API
- **Search Engines**: DuckDuckGo, Google, Bing web search APIs
- **Audio Players**: System audio playback (mpg123, afplay, etc.)


```

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CODE_ORGANISATION.md**
```
# Code Organisation Technical Specification

## Overview
Cato's codebase must be organised to minimise the effort required for any developer or AI model to understand, navigate, and modify the system.

## Directory Structure

### Root Level
- `agent.txt` - Navigation file for AI models/agents explaining codebase structure and common tasks
- `README.md` - Standard project readme
- `pyproject.toml` / `setup.py` - Package configuration
- `cato/` - Main package directory

### Module Directories
Each significant module directory must contain:
- `README.md` explaining:
  - Purpose of the module
  - Key classes/functions and their roles
  - How to extend the module (e.g., adding new commands)
  - Dependencies and relationships with other modules

### Command System Organisation
Commands should be organised for easy addition:
- Individual command files or grouped by functional area
- Clear registration mechanism (decorator-based)
- Adding a new command should require:
  1. Creating/editing one file
  2. No manual registration in other files

## agent.txt Specification
The root `agent.txt` file should provide:
1. Brief description of Cato
2. Directory structure overview
3. Quick navigation to common tasks:
   - Adding a new command
   - Modifying configuration
   - Adding vector store functionality
   - Modifying display/UI
4. Pointers to relevant documentation
5. List of approved dependencies

## File Organisation Principles

### Single Responsibility
- Each file should have a clear, single purpose
- Avoid monolithic files with mixed concerns

### Logical Grouping
- Group related functionality in directories
- Use clear, descriptive names

### Import Structure
- Use relative imports within package
- Avoid circular imports through proper layering

## Code Documentation

### Module-Level Docstrings
Every module should have a docstring explaining:
- What the module does
- Key classes/functions exported
- Usage examples where helpful

### Function/Class Documentation
- All public functions and classes must have docstrings (numpy format)
- Type hints required for all function signatures
- Inline comments for non-obvious logic

## Extensibility Patterns

### Command Registration
```python
# Example pattern - commands register themselves
@command(name="example", aliases=["ex"])
class ExampleCommand(BaseCommand):
    """Docstring explaining the command."""
    async def execute(self, args: list[str]) -> CommandResult:
        ...
```

### Strategy Pattern for Pluggable Components
- Vector store retrieval strategies
- Chunking strategies
- Similarity algorithms
- All should follow a common interface for easy swapping

## Configuration Integration
- No hard-coded defaults in code
- All configurable values loaded from config system
- Config values accessed through typed config objects

```





**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CONFIGURATION.md**
```
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

## Configuration File

### File Locations (checked in order)
1. Path specified via `--config` CLI argument
2. `~/.cato/config.yaml`
3. `./cato.yaml` (current directory)
4. `./.cato.yaml` (current directory, hidden)

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
| model | string | gpt-4o-mini | - | LLM model identifier |
| temperature | float | 1.0 | 0.0-2.0 | Response randomness |
| max_tokens | int | 4000 | >0 | Maximum response tokens |
| system_prompt_files | list | [] | - | Additional prompt files |
| base_prompt_file | string | (package default) | - | Alternative prompt file path |
| override_base_prompt | bool | false | - | Only has an effect if base_prompt_file is populated. If true will override the base in its entirety. If false, it will append. |

### Vector Store Configuration (`vector_store`)

| Setting | Type | Default | Range | Description |
|---------|------|---------|-------|-------------|
| enabled | bool | true | - | Enable vector store |
| path | string | ./vector_stores/default/ | - | Storage directory |
| chat_window | int | -1 | >0 | The number of recent exchanges to maintain in the current chat. This is to limit the size of of the context. A value of -1 means keep all exchanges, |
| context_results | int | 5 | >0 | Max context exchanges returned |
| context_similarity_threshold | float | 0.65 | 0.0-1.0 | Minimum similarity for context (static threshold) |
| dynamic_threshold | bool | true | - | Enable dynamic similarity thresholding based on context length |
| retrieval_strategy | string | default | - | Similarity retrieval strategy (see SPEC_VECTOR_STORE.md) |
| search_context_window | int | 3 | >0 | The number of recent exchanges to use in the vector for the similarity search |

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
| exchange_delimiter | string | ─ | Character for separation |
| exchange_delimiter_length | int | 60 | Delimiter line length |
| prompt_symbol | string | 🐱 >  | Input prompt (supports Unicode/emoji) |
| spinner_icon | string | ⠋ | Waiting indicator icon (spinner character) |


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


### Logging
| Argument | Description |
|----------|-------------|
| `--log-level <level>` | DEBUG, INFO, WARN, ERROR |

### Special Modes
| Argument | Description |
|----------|-------------|
| `--debug` | Enable debug mode |
| `--dummy-mode` | Use mock LLM responses |

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

```

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md**
```
# Error Handling Technical Specification

## Philosophy
Errors should be visible, clear, and actionable. The application should almost diagnose itself.

## Exception Handling Patterns

### Atomic Exceptions
- Catch specific exceptions, not broad `Exception` or `BaseException`
- Each try/except block should handle one logical error scenario

```python
# GOOD - specific exception handling
try:
    config = load_yaml(path)
except FileNotFoundError:
    logger.warning(f"Config file not found at {path}, using defaults")
    config = default_config
except yaml.YAMLError as e:
    logger.error(f"Invalid YAML in config file: {e}")
    raise ConfigurationError(f"Cannot parse {path}: {e}")

# BAD - broad exception handling
try:
    config = load_yaml(path)
except Exception as e:
    logger.error(f"Config error: {e}")
```

### Exception vs Return Value
- Prefer raising exceptions for errors over returning error tuples/dicts
- Use custom exception classes for domain-specific errors
- Exceptions should carry enough context for debugging

### Custom Exception Hierarchy
```python
class CatoError(Exception):
    """Base exception for Cato errors."""
    pass

class ConfigurationError(CatoError):
    """Configuration-related errors."""
    pass

class VectorStoreError(CatoError):
    """Vector store operation errors."""
    pass

class CommandError(CatoError):
    """Command execution errors."""
    pass
```

## User-Facing Error Messages

### Format
- Clear, human-readable language
- Include what went wrong
- Include actionable guidance where possible
- Use emoji indicators for visual clarity

```python
# Error display format
"❌ Command error: File not found: /path/to/file.txt"
"⚠️ Warning: Unrecognised config key 'foo', ignoring"
"❌ API error: OpenAI rate limit exceeded. Try again in 60 seconds."
```

### Information Levels
- **User message**: What happened and what to do
- **Log message**: Technical details for debugging
- Don't expose stack traces to user unless in debug mode

## Configuration Error Handling

### Validation Behaviour
- Invalid YAML syntax: Log error, exit
- Missing config file: Use defaults, log info
- Unrecognised config key: Warn user, ignore key, continue
- Invalid value type: Warn user, use default for that key
- Value out of range: Warn user, use default

### Example
```python
# On startup with invalid config value
"⚠️ Config warning: 'temperature' must be 0.0-2.0, got 5.0. Using default: 1.0"
```

## Graceful Degradation

### Component Failures
When a non-critical component fails:
1. Log the error appropriately
2. Inform the user clearly
3. Continue with reduced functionality

```python
# Vector store unavailable
"⚠️ Vector store could not initialise: {error}. Continuing without memory features."

# TTS unavailable
"⚠️ TTS failed: {error}. Speech features disabled for this session."
```

### Network/API Failures
- Implement reasonable timeouts
- Provide clear feedback on timeout
- Allow retry where appropriate

## Logging Integration

### Error Logging
- All errors must be logged
- Log level appropriate to severity:
  - DEBUG: Detailed diagnostic info
  - INFO: Notable events
  - WARNING: Recoverable issues
  - ERROR: Failures requiring attention

### Context in Logs
- Include relevant context (operation being attempted, relevant parameters)
- Don't log sensitive data (API keys, passwords)

## Never Silent Failures
- Never swallow exceptions without logging
- Never retry infinitely without user feedback
- Always inform user when something doesn't work as expected

```

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_PERFORMANCE.md**
```
# Performance Technical Specification

## Startup Performance

### Target
Cato should start effectively instantaneously. User should see the prompt within 1-2 seconds maximum.

### Requirements
- **No eager data loading**: Do not load vector store contents into memory at startup
- **Lazy initialisation**: Initialise components only when first needed where possible
- **Minimal imports**: Use lazy imports for heavy dependencies if necessary

### Prohibited Patterns
```python
# NEVER do this - loads entire vector store
class VectorStore:
    def __init__(self):
        self.all_embeddings = self.db.get_all()  # BAD

# Instead - query on demand
class VectorStore:
    def query(self, text: str, k: int):
        return self.db.query(text, k)  # GOOD
```

## Runtime Performance

### Database Interactions
- All database queries should be real-time
- No caching of database contents outside current conversation context
- Use appropriate indices for common query patterns

### Vector Store Queries
- Query performance should scale reasonably with store size
- Use efficient similarity search algorithms (cosine similarity via ChromaDB)
- Limit result sets appropriately (`context_results` config)

### Context Management
- Maintain only current conversation in memory
- Retrieved context from vector store is transient
- Clear context appropriately on `/clear`

## Response Generation

### Waiting Indicator
- Display spinner while waiting for LLM response
- Spinner icon configurable via `display.spinner_icon`
- Show cancellation hint (Ctrl+C)

### Timeout Handling
- Default API timeout: 120 seconds
- Graceful cancellation on Ctrl+C
- Clear feedback on timeout

## Memory Management

### What to Keep in Memory
- Current conversation messages
- Active configuration
- Session metadata (IDs, state flags)

### What NOT to Keep in Memory
- Historical conversations
- Vector store contents
- Productivity database contents

## Async Operations
- Use async/await for I/O bound operations
- LLM API calls should be async
- File operations can be sync (typically fast enough)
- Vector store operations should not block UI

## Startup Sequence (Optimised)
1. Parse CLI arguments
2. Load and validate configuration
3. Initialise display (Rich console)
4. Display welcome message
5. **Lazy init**: Vector store connection (don't load data)
6. **Lazy init**: LLM backend
7. Enter REPL loop
8. First vector store query triggers any necessary index loading

```



Now I have a good understanding of the project. Let me check for any existing WARP.md, CLAUDE.md, README.md, or other rules files.


**File Glob Results:**

- **/home/alex/Documents/repos/Cato/Project/Notes/Jan 14 at 11-01.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/GENERAL_PRINCIPLES.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/FUNCTIONAL_SPECIFICATION_OVERVIEW.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CONFIGURATION.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_FILE_OPERATIONS.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_PRODUCTIVITY.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_TTS.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_VECTOR_STORE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_WEB_SEARCH.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CODE_ORGANISATION.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_PERFORMANCE.md**



**Command Executed:**
```bash
ls -la /home/alex/Documents/repos/Cato/.github/copilot-instructions.md /home/alex/Documents/repos/Cato/.cursor/rules/ 2>/dev/null || echo "No copilot or cursor rules found"
```

**Output:**
```
No copilot or cursor rules found
```

This is a new project with only specification documents. Based on my analysis, I'll create a WARP.md file that captures the essential guidance for future Warp sessions.


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/WARP.md
+++ /home/alex/Documents/repos/Cato/WARP.md
@@ -0,0 +1,65 @@
+# WARP.md
+
+This file provides guidance to WARP (warp.dev) when working with code in this repository.
+
+## Project Overview
+
+**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management, conversational memory via vector storage, TTS, and web search.
+
+**Status**: Pre-implementation - specification documents exist in `Project/Spec/`
+
+## Before Starting Development
+
+Read the specification documents in order:
+1. `Project/Spec/GENERAL_PRINCIPLES.md` - Core philosophy and constraints
+2. `Project/Spec/functional/SPEC_OVERVIEW.md` - Application flow and UI
+3. Relevant functional specs in `Project/Spec/functional/`
+4. Technical specs in `Project/Spec/technical/`
+
+## Key Architectural Decisions
+
+### Configuration
+- YAML-driven configuration with overlay system (user config overlays defaults)
+- **No hard-coded defaults in code** - all defaults in default YAML file
+- Pydantic for all validation
+- Unrecognised config keys warn but don't crash
+
+### Multi-Provider LLM
+- Must support OpenAI, Anthropic, Google, Ollama
+- Use pydantic-ai over LangChain for agent/API interactions
+
+### Storage
+- ChromaDB for vector store (embeddings, similarity search)
+- SQLite for productivity data (tasks, lists, memories)
+- **Never load entire vector store into memory**
+
+### Command System
+- Slash commands (`/help`, `/speak`, `/web`, etc.) for explicit actions
+- Decorator-based registration - adding a command requires only one file
+- **No natural language command interface** - commands use explicit syntax
+
+### Error Handling
+- Atomic exception handling (specific exceptions, not broad catches)
+- Custom exception hierarchy (CatoError base class)
+- Graceful degradation for non-critical failures
+- Never silent failures
+
+## Code Organisation Requirements
+
+When implementation begins:
+- Create `agent.txt` at root for AI navigation
+- Each module directory must have a README explaining purpose and extension
+- Numpy-format docstrings, type hints on all functions
+- Relative imports within package
+
+## Technology Stack
+
+### Required
+- Rich (formatting), prompt_toolkit (input)
+- ChromaDB, OpenAI Embeddings API
+- PyYAML, Pydantic
+- pydantic-ai (productivity agent)
+
+### Optional
+- OpenAI TTS API
+- DuckDuckGo/Google/Bing search

```



Created `WARP.md` with the essential guidance distilled from the specification documents. It captures:

- Project purpose and current status (pre-implementation)
- Reading order for specs before development
- Critical architectural constraints (no hard-coded defaults, never load full vector store, no natural language commands)
- Technology stack and preferences (pydantic-ai over LangChain)
- Code organisation requirements

The file is concise and focuses on decisions that aren't obvious from the code structure itself.

USER:
extract the information regarding purpose, use, intent, users and add to the description in the WARP.md file 

AGENT:


**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/GENERAL_PRINCIPLES.md**
```
# Cato General Principles

## Purpose
Cato (Chat at the Terminal Orchestrator) exists to provide maximum control over LLM interactions, tailored to specific user needs and idiosyncrasies. It is a chat client first, productivity client second.

## Core Philosophy

### Terminal-First
- Cato is a terminal application. Alternative frontends should use terminal paradigms.
- Separation of logic and display enables pluggable terminal frontends.
- Style configuration should be kept separate unless very specific to a frontend paradigm.

### Single User Focus
- Built for a single user on a single machine.
- Designed for users who are highly changeable, like to tinker and experiment.
- Configuration and architecture should be as flexible as possible.
- Multiple instances may run with different configurations simultaneously - users should manage collisions manually.

### Quality Over Convenience
- No tolerance for poor design decisions, bad architecture, or lazy coding.
- Core architecture must remain flexible and modular.
- Any component should be easily unplugged or switched out.
- Highest engineering standards required.

## Specification-Driven Development
- The functional specification is the bible for all development.
- The specification is not static - it must be kept updated at all times.
- Any decision that adds to or alters the specification must be documented with what changed and when.
- All development, design, and architecture decisions must be logged.

## Configuration Philosophy
- Configuration file driven as much as possible.
- YAML format with extensive inline documentation.
- **No hard-coded inline values** - all defaults stored in YAML, not as function/method defaults.
- User configuration overlays default configuration - only override what differs.
- A single key-value pair in user config is sufficient; all other values fall back to defaults.
- Use Pydantic extensively for validation.
- Unrecognised config items should warn but not crash - continue with defaults.

## Dependency Management
- Favour the Pydantic stack for API interactions (pydantic-ai over LangChain).
- Minimise external library dependencies where existing approved dependencies suffice.
- Do not code natively what can be done with approved dependencies.
- Do not add new dependencies outside the approved stack without explicit approval.

## Agent Architecture
- Cato is NOT an agent - it is a chat and productivity client.
- Agent-like features for specific tasks may be added later but are not in initial scope.
- Natural language interface to productivity/commands is explicitly NOT wanted - commands use slash syntax.

## Documentation Philosophy

### Codebase Self-Documentation
- Separated modules (especially in directories) should contain a README explaining:
  - What is in the directory
  - What it is used for
  - Pointers to common functions/classes/methods
  - How to add legitimate elements
- An `agent.txt` file should exist at root to help any model/agent quickly navigate the codebase.
- Goal: minimise code scanning by models/agents to understand the system.

### User Documentation
- In-app help must be extensive, robust, and always kept up to date.
- Help system should be easy to navigate without relying on the model.
- The model does not need to know how Cato works unless explicitly asked via `/help model`.

### System Prompt
- Base/master system prompt contains minimum needed for model to do its job.
- Master prompt is sacrosanct - changes treated as code changes.
- User system prompt is appended to master prompt.
- Model does not need awareness of UI mechanics.

## Error Handling Philosophy
- Atomic exception handling - as specific as possible.
- No broad exception catching.
- Favour catching exceptions over returning error messages from Python.
- Clear, human-readable error messages.
- Errors should be expensive and visible - don't hide problems.
- Application should almost diagnose itself.

### Logging Modes
- **Debug mode**: Extremely chatty, comprehensive logging throughout stack.
- **Warn mode**: Chatty but only relevant to user experience.
- Never do anything silently - report failures to user clearly.

## Performance Requirements
- Boot as quickly as possible - effectively instantaneous.
- All database interactions in real-time - no data caching outside context.
- **Never load entire vector store into memory**.
- No gradual streamed output required, but show waiting indicator for long responses.

## Multi-Provider Support
- Assume multiple models from multiple providers will be used.
- Assume multiple agents from multiple providers will be used.
- Architecture must support any combination.

## Future Considerations
- Architecture should allow for multimodal elements (not in initial spec).
- Headless mode for one-shot queries (limited functionality).
- Real-time context retrieval from vector store as conversation topics change.

```

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md**
```
# Cato Functional Specification - Overview

## Application Summary

**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management capabilities, and conversational memory through vector storage.

## Purpose

Cato provides a unified terminal interface for:
- Conversational AI interactions with multiple LLM providers
- Personal productivity management (tasks, lists, time tracking, memories)
- File operations and code management
- Persistent conversational memory with context retrieval
- Text-to-speech synthesis
- Web search integration

## Core Design Principles

1. **Terminal-First**: All functionality accessible via keyboard in a command-line interface
2. **Rich Output**: Markdown rendering, syntax highlighting, and formatted tables
3. **Unified Experience**: Single interface for chat, productivity, and file operations
4. **Persistent Memory**: Conversation and productivity data persisted across sessions
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

1. **Memory prompts**: If awaiting yes/no response for memory storage suggestion
2. **Slash commands**: Input starting with `/` routes to command parser
3. **Productivity routing**: Input starting with `%` routes to productivity agent
4. **File routing**: Input starting with `@` routes to file tools agent
5. **Regular chat**: All other input sent to LLM with context retrieval

### Session State
- **Session ID**: Unique UUID generated per application launch
- **Thread ID**: Unique UUID for conversation continuity
- **Message history**: List of messages (system, user, assistant)
- **Current directory**: For file operations
- **Context mode**: Controls display of retrieved context (on/off/summary)

## Specification Documents

This specification is divided into the following functional areas:

| Document | Description |
|----------|-------------|
| SPEC_CORE_CHAT.md | LLM integration, message processing, display |
| SPEC_COMMAND_SYSTEM.md | Slash command framework and all commands |
| SPEC_PRODUCTIVITY.md | Tasks, lists, timelog, memories |
| SPEC_FILE_OPERATIONS.md | File commands, attach, export, aliases |
| SPEC_VECTOR_STORE.md | Conversation storage, similarity search |
| SPEC_TTS.md | Text-to-speech functionality |
| SPEC_WEB_SEARCH.md | Web search and URL content fetching |
| SPEC_CONFIGURATION.md | All configuration options |

## User Interface

### Welcome Message
The welcome message displays key configuration that affects behaviour (excluding style):

```
─ 🐱 Cato ─────────────────────────────────────────────────
Welcome to Cato - Chat at the Terminal Orchestrator

Type your messages to chat with the LLM.
Type /help to see available commands.
Type /exit to quit the application.

Config: Margaret (~/.cato/margaret.yaml)
Model: gpt-4o-mini
Vector Store: enabled (./vector_stores/default/)
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
- 🧠 Memory recall indicator
- 💭 Context indicator
- 🔊 TTS indicator

## Technology Stack

### Required Dependencies
- **LLM Clients**: OpenAI, Anthropic, Google Generative AI (via provider SDKs)
- **Local LLM**: Ollama (optional)
- **Vector Database**: ChromaDB
- **Embeddings**: OpenAI Embeddings API
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
   - Vector store unavailable → chat continues without memory
   - TTS playback fails → show error, continue chat
   - Web search fails → show error, allow retry

2. **Critical failures**: Log error, show user message, exit gracefully
   - Configuration invalid
   - LLM backend cannot initialize
   - No API key when required

3. **User cancellation**: Ctrl+C interrupts current operation, returns to prompt

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/WARP.md
+++ /home/alex/Documents/repos/Cato/WARP.md
@@ -8,6 +8,23 @@
 
 **Status**: Pre-implementation - specification documents exist in `Project/Spec/`
 
+### Purpose
+Cato exists to provide maximum control over LLM interactions, tailored to specific user needs and idiosyncrasies. It is a chat client first, productivity client second.
+
+### Intent
+Cato provides a unified terminal interface for:
+- Conversational AI interactions with multiple LLM providers
+- Personal productivity management (tasks, lists, time tracking, memories)
+- File operations and code management
+- Persistent conversational memory with context retrieval
+- Text-to-speech synthesis and web search integration
+
+### Target User
+- Single user on a single machine
+- Users who are highly changeable, like to tinker and experiment
+- Users who want flexible, modular architecture they can customise
+- Multiple instances may run with different configurations simultaneously
+
 ## Before Starting Development
 
 Read the specification documents in order:

```



Added Purpose, Intent, and Target User sections to the Project Overview, drawn from the GENERAL_PRINCIPLES.md and SPEC_OVERVIEW.md documents.