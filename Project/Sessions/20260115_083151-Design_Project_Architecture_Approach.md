USER:
suggest an approach to start designing the architecture and technical specs for this project

AGENT:
I'll read the existing specification documents to understand what's already defined before suggesting an approach.

**Command Executed:**
```bash
ls -la /home/alex/Documents/repos/Cato/Project/
```

**Output:**
```
total 16
drwxr-xr-x 4 alex alex 4096 Jan 14 12:59 .
drwxr-xr-x 4 alex alex 4096 Jan 14 19:45 ..
drwxr-xr-x 2 alex alex 4096 Jan 14 13:00 Notes
drwxr-xr-x 4 alex alex 4096 Jan 14 18:17 Spec
```


**Command Executed:**
```bash
find /home/alex/Documents/repos/Cato/Project/Spec -type f -name "*.md" | sort
```

**Output:**
```
/home/alex/Documents/repos/Cato/Project/Spec/functional/FUNCTIONAL_SPECIFICATION_OVERVIEW.md
/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md
/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CONFIGURATION.md
/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md
/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_FILE_OPERATIONS.md
/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md
/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_PRODUCTIVITY.md
/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_TTS.md
/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_VECTOR_STORE.md
/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_WEB_SEARCH.md
/home/alex/Documents/repos/Cato/Project/Spec/GENERAL_PRINCIPLES.md
/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CODE_ORGANISATION.md
/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md
/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_PERFORMANCE.md
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



Let me also check the other technical specs and a few key functional specs to understand the full scope.


**Files Read:**

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

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md**
```
# Command System Specification

## Overview

Cato uses a slash command system for explicit actions. Commands start with `/` and are parsed before any other input processing.

## Command Framework

### Command Detection
Input is treated as a command if it starts with `/` (after whitespace trimming).

### Command Parsing
Commands are parsed using shell-like tokenization:
- Command name extracted after `/`
- Arguments split by whitespace
- Quoted arguments preserved as single tokens

Example:
```
/web "search query with spaces" google
```
Parses to: command=`web`, args=`["search query with spaces", "google"]`

### Command Result
Each command returns a result with:
- `success`: Boolean indicating success/failure
- `message`: User-facing message
- `data`: Optional structured data for further processing

## Command Reference

### Core Commands

#### /help
Display help information.
```
/help                    # Show overview
/help commands           # Show all commands
/help productivity       # Show productivity help
/help files              # Show file operations help
/help websearch          # Show web search help
/help speak              # Show TTS help
/help config             # Show configuration help
/help model "question"   # Ask the model about Cato (see below)
```

##### /help model
Ask the model for help with Cato functionality.
```
/help model "how do I add a new command?"
/help model "what configuration options affect the vector store?"
```

**Behavior:**
1. Loads all user help files into context
2. Creates a one-off message to the model with:
   - Help file contents
   - Instruction to derive response from help documentation
   - The user's question
3. Model responds based solely on help documentation
4. This exchange is NOT added to the conversation history
5. Does not affect the main conversation context

#### /exit, /quit, /q
Exit the application.
```
/exit
/quit
/q
```

#### /clear
Clear conversation history and screen.
```
/clear
```
Behavior:
- Removes all user/assistant messages
- Preserves system messages
- Clears terminal screen
- Displays welcome message

#### /config
Show current configuration settings.
```
/config
```
Displays table with:
- Model, temperature, max tokens
- Vector store settings
- Display settings
- Logging level

### History Commands

#### /history
Show conversation history.
```
/history        # Show all messages
/history 10     # Show last 10 messages
```

#### /delete
Remove recent exchanges from history.
```
/delete         # Remove last exchange
/delete 3       # Remove last 3 exchanges
```

#### /model
Change or display the current LLM model. This overrides the setting in the user config file.
```
/model                  # Show current model
/model gpt-4o           # Change to gpt-4o
/model claude-3-sonnet  # Change to Claude
```

#### /showsys
Display the current system prompt.
```
/showsys
```

#### /loglevel
Change logging verbosity.
```
/loglevel           # Show current level
/loglevel DEBUG     # Set to DEBUG
/loglevel INFO      # Set to INFO
/loglevel WARN      # Set to WARN
/loglevel ERROR     # Set to ERROR
```

### Context Commands

#### /showcontext
Toggle context display mode for all future exchanges.
```
/showcontext        # Toggle on/off (shows new state)
/showcontext on     # Enable context display with excerpts
/showcontext off    # Disable context display
```

**Behavior:**
- Acts as a **toggle** - calling `/showcontext` without arguments flips the current state
- When **on**: Context excerpts displayed before each response
- When **off**: No context information displayed (default)
- State persists for the duration of the session

#### /continue, /cont
Continue an existing conversation thread.
```
/continue <thread_id>
/cont <thread_id>
```

#### /casual
Toggle casual conversation mode.
```
/casual on      # Enable casual mode
/casual off     # Disable casual mode
```

### File Commands

#### /attach
Attach files as conversation context.
```
/attach file1.txt                    # Attach single file
/attach file1.txt file2.py file3.md  # Attach multiple (max 5)
```

#### /pwd
Show current working directory.
```
/pwd
```

#### /cd
Change current directory.
```
/cd /path/to/directory
/cd ..
/cd ~
```

#### /ls
List directory contents (alias for `/file list`).
```
/ls              # List current directory
/ls /path/to     # List specific directory
```

#### /cat
Display file contents (alias for `/file read`).
```
/cat filename.txt
/cat alias:filename.txt
```

#### /locations
Show configured location aliases.
```
/locations
```

### Export Commands

#### /writecode
Extract code blocks from last response.
```
/writecode output.py
```
Extracts all code blocks (from markdown fences) and saves to file.

#### /writejson
Export conversation to JSON.
```
/writejson conversation.json
```
Exports:
- All messages with roles and content
- Configuration metadata (model, temperature)

#### /writemd, /w
Export conversation thread to Markdown.
```
/writemd output.md
/w output.md
```
Exports user/assistant exchanges (excludes system prompts).

#### /writemdall
Export full conversation to Markdown (includes system prompts).
```
/writemdall output.md
```

#### /writeresp
Export last exchange to file.
```
/writeresp output.txt           # Plain text
/writeresp output.json json     # JSON format
/writeresp output.md md         # Markdown format
```

#### /append
Append to an existing file.
```
/append notes.txt "Additional content"
/append notes.txt                       # Append last exchange
```

### Clipboard Commands

#### /copy
Copy last assistant response to clipboard.
```
/copy
```

### Vector Store Commands

See SPEC_VECTOR_STORE.md for detailed vector store documentation.

#### /vadd
Add text directly to vector store.
```
/vadd This is important information to remember
```

#### /vdoc
Add a document file to vector store with chunking.
```
/vdoc /path/to/document.txt
/vdoc alias:document.md
```

#### /vdelete
Delete an exchange from vector store.
```
/vdelete <exchange_id>
```

#### /vget
Retrieve exchanges by ID, session, or thread.
```
/vget <exchange_id>      # Get specific exchange
/vget session            # Get current session exchanges
/vget thread             # Get current thread exchanges
```

#### /vquery
Query vector store for similar content.
```
/vquery "search query"       # Default results
/vquery "search query" 10    # Return 10 results
```

#### /vstats
Display vector store statistics.
```
/vstats
```

### Memory Commands

### Productivity Commands

See SPEC_PRODUCTIVITY.md for detailed productivity documentation.

#### /st, /show-tasks, /tasks
Show open tasks.
```
/st                         # Show all open tasks
/st work                    # Filter by category
/st -p high                 # Filter by priority
/st -s priority -o desc     # Sort by priority descending
/st --status=completed      # Show completed tasks
```

**Options:**
- `-s, --sort=<field>`: Sort by created, priority, category, due, id, status
- `-o, --order=<asc|desc>`: Sort order
- `-p, --priority=<level>`: Filter by priority
- `-c, --category=<name>`: Filter by category
- `-S, --status=<status>`: Filter by status (active, in_progress, completed)

#### /list, /lists, /show-lists
Show lists and list items.
```
/list                   # Show all lists with counts
/list shopping          # Show items in shopping list
```

### Web Commands

See SPEC_WEB_SEARCH.md for detailed web search documentation.

#### /web
Search the web and add results to context.
```
/web "search query"                  # Use default engine
/web "search query" google           # Use specific engine
/web "search query" duckduckgo       # Use DuckDuckGo
```

#### /url
Fetch and attach content from a URL.
```
/url https://example.com/page.html
```

### TTS Commands

See SPEC_TTS.md for detailed TTS documentation.

#### /speak, /s
Speak the last assistant response.
```
/speak              # Default voice and model
/speak nova         # Specific voice
/speak nova tts-1   # Specific voice and model
/s                  # Alias
```

**Available Voices:** alloy, echo, fable, nova, onyx, shimmer

**Available Models:** tts-1, tts-1-hd

#### /speaklike, /sl
Speak with custom instructions.
```
/speaklike "Speak slowly and clearly"
/speaklike "Read as a news anchor" nova tts-1-hd
```

## Command Aliases

| Command | Aliases |
|---------|---------|
| /exit | /quit, /q |
| /continue | /cont |
| /speak | /s |
| /speaklike | /sl |
| /remember | /rem, /r |
| /st | /show-tasks, /tasks |
| /list | /lists, /show-lists |
| /timelog | /tl, /time |
| /writemd | /w |

## Error Handling

Commands return appropriate error messages for:
- Missing required arguments
- Invalid argument values
- File not found / permission denied
- Feature disabled in configuration
- External service failures (API, network)

Example error display:
```
❌ Command error: No file path specified. Usage: /file read <path>
```

## Command Extension

The command system is designed for extensibility:
- Commands registered via `@command` decorator
- BaseCommand abstract class for implementation
- CommandRegistry for lookup and alias resolution
- Async execute method for each command

```



Now I have a solid understanding of the existing specifications. Let me check what's in the Notes directory to see if there's any additional context.

**Command Executed:**
```bash
ls -la /home/alex/Documents/repos/Cato/Project/Notes/
```

**Output:**
```
total 28
drwxr-xr-x 2 alex alex  4096 Jan 14 13:00  .
drwxr-xr-x 4 alex alex  4096 Jan 14 12:59  ..
-rw-r--r-- 1 alex alex 19426 Jan 14 13:00 'Jan 14 at 11-01.md'
```

Based on my review of your existing specification documents, here's a suggested approach:

## Recommended Approach

### 1. Gap Analysis First
Your functional specs are well-developed. The technical side needs expansion. Missing technical specs:
- **TECH_CONFIG_SYSTEM.md** - YAML loading, overlay mechanism, Pydantic schemas
- **TECH_LLM_INTEGRATION.md** - Provider abstraction, multi-provider architecture
- **TECH_VECTOR_STORE.md** - ChromaDB integration, embedding strategy, query patterns
- **TECH_STORAGE.md** - SQLite schema for productivity, data access patterns
- **TECH_COMMAND_FRAMEWORK.md** - Decorator registration, command lifecycle, result handling
- **TECH_DISPLAY.md** - Rich integration, prompt_toolkit setup, theming

### 2. Design Sequence
Start with foundational components that others depend on:

1. **Configuration system** → Everything else reads from it
2. **Error/Logging framework** → Cross-cutting concern needed early
3. **LLM provider abstraction** → Core functionality depends on it
4. **Command framework** → Shell for all user interactions
5. **Vector store** → Complex, benefits from early design attention
6. **Display layer** → Touches everything but can be refined later

### 3. For Each Technical Spec
- Define interfaces/protocols before implementation details
- Include component diagrams showing dependencies
- Specify test strategy for the component
- Add configuration keys the component will need

### 4. Practical Starting Point
I'd suggest beginning with the **Configuration System** tech spec since:
- GENERAL_PRINCIPLES already defines the philosophy clearly
- It's foundational—nothing works without config
- It's contained enough to design completely before moving on
- Forces you to define the Pydantic model structure early

Would you like me to draft a technical spec for the configuration system, or would you prefer to start with a different component?

USER:
turn this into a plan

AGENT:


**Documents Created:**

**Document 5d3664ce-a5f5-48eb-bf3a-c296889d8a5f**
```
# Cato Technical Architecture Design Plan
## Objective
Create comprehensive technical specifications for all major Cato components, establishing clear interfaces, dependencies, and implementation patterns before coding begins.
## Current State
* Functional specifications exist for all major features in `Project/Spec/functional/`
* General principles and philosophy documented in `GENERAL_PRINCIPLES.md`
* Three technical specs exist: Code Organisation, Error Handling, Performance
* No implementation code yet
## Missing Technical Specifications
The following specs need to be created in `Project/Spec/technical/`:
1. **TECH_CONFIG_SYSTEM.md** - YAML loading, overlay mechanism, Pydantic validation schemas
2. **TECH_LLM_INTEGRATION.md** - Provider abstraction layer, multi-provider architecture
3. **TECH_VECTOR_STORE.md** - ChromaDB integration, embedding strategy, query patterns
4. **TECH_STORAGE.md** - SQLite schema for productivity data, data access layer
5. **TECH_COMMAND_FRAMEWORK.md** - Decorator-based registration, command lifecycle
6. **TECH_DISPLAY.md** - Rich/prompt_toolkit integration, theming system
## Design Sequence
Ordered by dependency (foundational components first):
### Phase 1: Core Infrastructure
**1. Configuration System** (TECH_CONFIG_SYSTEM.md)
* YAML file loading and merging logic
* Default config structure
* User overlay mechanism
* Pydantic models for all config sections
* Environment variable overrides
* CLI argument overrides
* Validation and error messaging for invalid config
**2. Error and Logging Framework** (expand TECH_ERROR_HANDLING.md)
* Complete custom exception hierarchy
* Logging configuration and setup
* Debug vs Warn mode implementation
* User-facing error formatting
### Phase 2: Core Functionality
**3. LLM Provider Integration** (TECH_LLM_INTEGRATION.md)
* Provider abstraction interface/protocol
* OpenAI, Anthropic, Google, Ollama implementations
* Message format normalisation
* Streaming vs non-streaming handling
* Token counting and context management
* Timeout and retry patterns
**4. Command Framework** (TECH_COMMAND_FRAMEWORK.md)
* BaseCommand abstract class
* @command decorator implementation
* CommandRegistry and alias resolution
* Argument parsing (shell-like tokenization)
* CommandResult structure
* Async execution pattern
### Phase 3: Data Layer
**5. Vector Store Integration** (TECH_VECTOR_STORE.md)
* ChromaDB setup and connection
* Embedding generation (OpenAI API)
* Collection schema for conversations
* Chunking strategies for documents
* Query and similarity search patterns
* Metadata schema for exchanges
**6. Productivity Storage** (TECH_STORAGE.md)
* SQLite database schema (tasks, lists, timelog, memories)
* Data access layer patterns
* Migration strategy
* Query patterns for common operations
### Phase 4: Presentation
**7. Display Layer** (TECH_DISPLAY.md)
* Rich console setup
* prompt_toolkit input configuration
* Markdown rendering pipeline
* Syntax highlighting setup
* Spinner/waiting indicators
* Theme/style configuration separation
## Spec Template
Each technical spec should include:
* **Purpose**: What problem this component solves
* **Dependencies**: Other components this relies on
* **Interface**: Public API/protocol definition
* **Configuration**: Config keys this component uses
* **Implementation Notes**: Key patterns and constraints
* **Error Handling**: Specific exceptions and degradation behaviour
* **Testing Strategy**: How to test this component
## Next Steps
1. Begin with TECH_CONFIG_SYSTEM.md - foundational for everything else
2. Review and expand TECH_ERROR_HANDLING.md with complete exception hierarchy
3. Proceed through phases sequentially
4. After all specs complete, create `agent.txt` and module READMEs
5. Begin implementation

```



Plan created. It outlines the 6 missing technical specs organised into 4 phases by dependency order, with a template structure for each spec. Ready to begin with the configuration system when you are.

USER:
Execute this plan

AGENT:
I'll execute this plan by creating each technical specification. Let me start by reading the existing functional specs that inform the technical designs.
UpdateTodos: 7 items

USER:
I'd like to understand the wider desigh and architetural principles first. How will the code be organised to achieve my objectives, particularly in terms of modularity and flexibility

AGENT:
Good question—let me outline the architectural approach before diving into individual specs.

## Core Architecture Principles

### 1. Layered Architecture
```
┌─────────────────────────────────────┐
│           Presentation              │  ← Rich console, prompt_toolkit
├─────────────────────────────────────┤
│           Commands                  │  ← Slash commands, input routing
├─────────────────────────────────────┤
│           Services                  │  ← Chat, Productivity, TTS, Web
├─────────────────────────────────────┤
│           Providers                 │  ← LLM providers, Search engines
├─────────────────────────────────────┤
│           Storage                   │  ← ChromaDB, SQLite
├─────────────────────────────────────┤
│           Core                      │  ← Config, Errors, Logging
└─────────────────────────────────────┘
```
Each layer only depends on layers below it. This means you can swap out the presentation layer without touching services, or change LLM providers without affecting commands.

### 2. Protocol-Based Abstractions
Instead of concrete classes, key interfaces defined as Python `Protocol`s:

```python
class LLMProvider(Protocol):
    async def complete(self, messages: list[Message]) -> Response: ...
    async def stream(self, messages: list[Message]) -> AsyncIterator[str]: ...

class StorageBackend(Protocol):
    def query(self, text: str, k: int) -> list[Result]: ...
    def store(self, content: str, metadata: dict) -> str: ...
```
Any class implementing the protocol is valid—no inheritance required. Want to swap ChromaDB for Pinecone later? Implement the protocol, change one config line.

### 3. Dependency Injection via Config
Components receive their dependencies, they don't create them:

```python
# NOT this (hard coupling)
class ChatService:
    def __init__(self):
        self.llm = OpenAIProvider()  # locked to OpenAI

# THIS (injected)
class ChatService:
    def __init__(self, llm: LLMProvider, vector_store: StorageBackend):
        self.llm = llm
        self.vector_store = vector_store
```
A factory/bootstrap module reads config and wires everything together at startup.

### 4. Proposed Directory Structure
```
cato/
├── __main__.py           # Entry point
├── bootstrap.py          # Wiring/DI, component initialisation
├── core/
│   ├── config.py         # Pydantic models, YAML loading
│   ├── errors.py         # Exception hierarchy
│   └── logging.py        # Logging setup
├── providers/
│   ├── base.py           # LLMProvider protocol
│   ├── openai.py
│   ├── anthropic.py
│   ├── google.py
│   └── ollama.py
├── storage/
│   ├── vector.py         # VectorStore protocol + ChromaDB impl
│   └── productivity.py   # SQLite for tasks/lists/etc
├── services/
│   ├── chat.py           # Main chat orchestration
│   ├── productivity.py   # Task/list/memory logic
│   ├── tts.py
│   └── web.py
├── commands/
│   ├── base.py           # BaseCommand, registry, decorator
│   ├── core.py           # /help, /exit, /clear, /config
│   ├── history.py        # /history, /delete, /model
│   ├── files.py          # /attach, /cd, /ls, /cat
│   ├── export.py         # /writemd, /writecode, etc
│   ├── vector.py         # /vadd, /vquery, /vstats
│   ├── productivity.py   # /st, /list, /timelog
│   ├── tts.py            # /speak, /speaklike
│   └── web.py            # /web, /url
├── display/
│   ├── console.py        # Rich setup, output formatting
│   ├── input.py          # prompt_toolkit setup
│   └── themes.py         # Style definitions
└── repl.py               # Main REPL loop
```
### 5. Key Flexibility Points

| Want to... | How |
|------------|-----|
| Add a new LLM provider | Create `providers/newprovider.py` implementing `LLMProvider` protocol, add to config |
| Add a new command | Create decorated function/class in `commands/`, auto-registered |
| Change vector DB | Implement `StorageBackend` protocol, swap in config |
| Modify display style | Edit `display/themes.py` or user config—no code changes |
| Run multiple configs | Launch with different `--config` paths |

### 6. What This Achieves

- **Modularity**: Each directory is a self-contained concern
- **Testability**: Protocols allow easy mocking
- **Swappability**: Config-driven component selection
- **Extensibility**: Adding commands/providers doesn't touch existing code
- **Tinkering-friendly**: Most behaviour adjustable via YAML

---

Should I create a technical spec that captures this architecture (something like `TECH_ARCHITECTURE.md`) before proceeding with the individual component specs? This would serve as the reference for how everything fits together.

USER:
yes, create that and then pause so that I can review

AGENT:


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md
@@ -0,0 +1,409 @@
+# Architecture Technical Specification
+
+## Overview
+This document defines Cato's core architectural patterns, component organisation, and the principles that enable modularity and flexibility.
+
+## Design Goals
+1. **Swappable components**: Any major component (LLM provider, storage backend, display) replaceable via configuration
+2. **Easy extension**: Adding commands, providers, or features requires minimal changes to existing code
+3. **Testability**: All components testable in isolation through dependency injection
+4. **Configuration-driven**: Behaviour controlled by YAML, not code changes
+5. **Clear boundaries**: Each module has a single responsibility with explicit interfaces
+
+## Layered Architecture
+
+```
+┌─────────────────────────────────────────────────────────────┐
+│                      Presentation                           │
+│              (Rich console, prompt_toolkit)                 │
+├─────────────────────────────────────────────────────────────┤
+│                        Commands                             │
+│           (Slash commands, input routing, REPL)             │
+├─────────────────────────────────────────────────────────────┤
+│                        Services                             │
+│          (Chat, Productivity, TTS, Web Search)              │
+├─────────────────────────────────────────────────────────────┤
+│                        Providers                            │
+│       (LLM backends, Search engines, TTS engines)           │
+├─────────────────────────────────────────────────────────────┤
+│                        Storage                              │
+│              (ChromaDB, SQLite, File I/O)                   │
+├─────────────────────────────────────────────────────────────┤
+│                          Core                               │
+│              (Config, Errors, Logging, Types)               │
+└─────────────────────────────────────────────────────────────┘
+```
+
+### Layer Rules
+- Each layer may only import from layers below it
+- No circular dependencies between layers
+- Cross-cutting concerns (logging, errors) live in Core and are available to all layers
+
+### Layer Responsibilities
+
+#### Core
+- Configuration loading, validation, and access
+- Custom exception hierarchy
+- Logging setup and configuration
+- Shared type definitions and data classes
+
+#### Storage
+- Vector store operations (ChromaDB)
+- Productivity data persistence (SQLite)
+- File operations for attachments and exports
+- No business logic—pure data access
+
+#### Providers
+- LLM API integration (OpenAI, Anthropic, Google, Ollama)
+- Search engine integration (DuckDuckGo, Google, Bing)
+- TTS engine integration (OpenAI TTS)
+- Each provider implements a common protocol
+
+#### Services
+- Business logic orchestration
+- Chat service: message handling, context retrieval, response generation
+- Productivity service: task/list/memory operations
+- TTS service: text processing, audio generation
+- Web service: search execution, URL fetching
+
+#### Commands
+- Slash command parsing and dispatch
+- Command registration and discovery
+- Input routing (commands vs chat vs productivity)
+- REPL loop management
+
+#### Presentation
+- Console output formatting (Rich)
+- User input handling (prompt_toolkit)
+- Theming and styling
+- Spinners and progress indicators
+
+## Protocol-Based Abstractions
+
+Key interfaces are defined as Python `Protocol` classes, enabling duck typing without inheritance.
+
+### LLM Provider Protocol
+```python
+from typing import Protocol, AsyncIterator
+
+class LLMProvider(Protocol):
+    """Protocol for LLM backend implementations."""
+    
+    @property
+    def model_name(self) -> str:
+        """Return the current model identifier."""
+        ...
+    
+    async def complete(
+        self, 
+        messages: list[Message], 
+        temperature: float | None = None,
+        max_tokens: int | None = None
+    ) -> CompletionResponse:
+        """Generate a completion for the given messages."""
+        ...
+    
+    async def stream(
+        self, 
+        messages: list[Message],
+        temperature: float | None = None,
+        max_tokens: int | None = None
+    ) -> AsyncIterator[str]:
+        """Stream a completion token by token."""
+        ...
+```
+
+### Vector Store Protocol
+```python
+class VectorStore(Protocol):
+    """Protocol for vector storage backends."""
+    
+    def store(
+        self, 
+        content: str, 
+        metadata: dict[str, Any],
+        embedding: list[float] | None = None
+    ) -> str:
+        """Store content and return its ID."""
+        ...
+    
+    def query(
+        self, 
+        text: str, 
+        k: int = 5,
+        filters: dict[str, Any] | None = None
+    ) -> list[QueryResult]:
+        """Query for similar content."""
+        ...
+    
+    def delete(self, ids: list[str]) -> int:
+        """Delete items by ID, return count deleted."""
+        ...
+```
+
+### Benefits of Protocols
+- No base class inheritance required
+- Any class with matching methods satisfies the protocol
+- Easy to create test mocks
+- Swap implementations by changing config, not code
+
+## Dependency Injection
+
+Components receive their dependencies at construction time rather than creating them internally.
+
+### Pattern
+```python
+# Services receive providers via constructor
+class ChatService:
+    def __init__(
+        self,
+        llm: LLMProvider,
+        vector_store: VectorStore,
+        config: ChatConfig
+    ):
+        self._llm = llm
+        self._vector_store = vector_store
+        self._config = config
+
+# NOT this - creates tight coupling
+class ChatService:
+    def __init__(self):
+        self._llm = OpenAIProvider()  # Locked to OpenAI
+```
+
+### Bootstrap Module
+A dedicated `bootstrap.py` module handles component wiring:
+1. Load configuration
+2. Instantiate providers based on config
+3. Instantiate services with their dependencies
+4. Instantiate commands with service references
+5. Return fully-wired application instance
+
+```python
+def create_application(config_path: Path | None = None) -> Application:
+    """Wire up all components and return runnable application."""
+    config = load_config(config_path)
+    
+    # Create providers based on config
+    llm = create_llm_provider(config.llm)
+    vector_store = create_vector_store(config.vector_store)
+    productivity_db = create_productivity_db(config.storage)
+    
+    # Create services with dependencies
+    chat_service = ChatService(llm, vector_store, config.chat)
+    productivity_service = ProductivityService(productivity_db, config.productivity)
+    
+    # Create command registry with services
+    commands = create_command_registry(
+        chat=chat_service,
+        productivity=productivity_service,
+        config=config
+    )
+    
+    # Create display layer
+    display = create_display(config.display)
+    
+    return Application(
+        commands=commands,
+        display=display,
+        config=config
+    )
+```
+
+## Directory Structure
+
+```
+cato/
+├── __init__.py
+├── __main__.py              # Entry point: python -m cato
+├── bootstrap.py             # Component wiring and initialisation
+├── app.py                   # Application class, main run loop
+│
+├── core/
+│   ├── __init__.py
+│   ├── README.md            # Module documentation
+│   ├── config.py            # Config loading, Pydantic models
+│   ├── errors.py            # CatoError hierarchy
+│   ├── logging.py           # Logging setup
+│   └── types.py             # Shared data classes (Message, etc.)
+│
+├── providers/
+│   ├── __init__.py
+│   ├── README.md
+│   ├── llm/
+│   │   ├── __init__.py
+│   │   ├── base.py          # LLMProvider protocol
+│   │   ├── openai.py
+│   │   ├── anthropic.py
+│   │   ├── google.py
+│   │   └── ollama.py
+│   ├── search/
+│   │   ├── __init__.py
+│   │   ├── base.py          # SearchProvider protocol
+│   │   ├── duckduckgo.py
+│   │   └── google.py
+│   └── tts/
+│       ├── __init__.py
+│       ├── base.py          # TTSProvider protocol
+│       └── openai.py
+│
+├── storage/
+│   ├── __init__.py
+│   ├── README.md
+│   ├── vector/
+│   │   ├── __init__.py
+│   │   ├── base.py          # VectorStore protocol
+│   │   └── chromadb.py
+│   └── productivity/
+│       ├── __init__.py
+│       ├── base.py          # ProductivityStore protocol
+│       ├── sqlite.py
+│       └── schema.sql       # Table definitions
+│
+├── services/
+│   ├── __init__.py
+│   ├── README.md
+│   ├── chat.py              # Chat orchestration
+│   ├── productivity.py      # Task/list/memory logic
+│   ├── tts.py               # TTS orchestration
+│   └── web.py               # Web search orchestration
+│
+├── commands/
+│   ├── __init__.py
+│   ├── README.md
+│   ├── base.py              # BaseCommand, @command decorator, registry
+│   ├── core.py              # /help, /exit, /clear, /config
+│   ├── history.py           # /history, /delete, /model, /showsys
+│   ├── context.py           # /showcontext, /continue, /casual
+│   ├── files.py             # /attach, /cd, /ls, /cat, /pwd
+│   ├── export.py            # /writemd, /writecode, /writejson, etc.
+│   ├── vector.py            # /vadd, /vdoc, /vquery, /vstats, /vdelete
+│   ├── productivity.py      # /st, /list, /timelog, /remember
+│   ├── tts.py               # /speak, /speaklike
+│   └── web.py               # /web, /url
+│
+├── display/
+│   ├── __init__.py
+│   ├── README.md
+│   ├── console.py           # Rich console, output formatting
+│   ├── input.py             # prompt_toolkit setup
+│   ├── markdown.py          # Markdown rendering
+│   └── themes.py            # Style definitions
+│
+└── resources/
+    ├── defaults.yaml        # Default configuration
+    └── help/                # Help text files
+        ├── overview.md
+        ├── commands.md
+        └── ...
+```
+
+## Extension Points
+
+### Adding a New LLM Provider
+1. Create `cato/providers/llm/newprovider.py`
+2. Implement the `LLMProvider` protocol
+3. Register in provider factory (one line)
+4. Add config schema for provider-specific options
+5. User selects via `llm.provider: newprovider` in config
+
+### Adding a New Command
+1. Create or edit file in `cato/commands/`
+2. Use `@command` decorator:
+```python
+@command(name="mycommand", aliases=["mc"])
+async def my_command(ctx: CommandContext, args: list[str]) -> CommandResult:
+    """Help text for the command."""
+    # Implementation
+    return CommandResult(success=True, message="Done")
+```
+3. No other registration needed—decorator handles it
+
+### Adding a New Storage Backend
+1. Create implementation in `cato/storage/`
+2. Implement relevant protocol (VectorStore or ProductivityStore)
+3. Register in storage factory
+4. User selects via config
+
+## Configuration Integration
+
+All components receive configuration through typed Pydantic models:
+
+```python
+# Components don't read config files directly
+# They receive pre-validated config objects
+
+class ChatService:
+    def __init__(self, config: ChatConfig):
+        self._temperature = config.temperature  # Already validated
+        self._max_tokens = config.max_tokens
+```
+
+This ensures:
+- No hard-coded defaults in implementation code
+- Type safety throughout
+- Single source of truth (YAML files)
+- Easy testing with custom config objects
+
+## Error Propagation
+
+Errors flow upward through layers:
+1. **Storage/Provider layer**: Raise specific exceptions (e.g., `VectorStoreError`, `ProviderAPIError`)
+2. **Service layer**: Catch, log, optionally wrap in service-specific exception or re-raise
+3. **Command layer**: Catch service exceptions, convert to user-friendly `CommandResult`
+4. **Presentation layer**: Display error to user appropriately
+
+```python
+# Storage layer
+def query(self, text: str) -> list[Result]:
+    try:
+        return self._client.query(text)
+    except chromadb.errors.InvalidCollectionException as e:
+        raise VectorStoreError(f"Collection not found: {e}") from e
+
+# Service layer
+async def get_context(self, query: str) -> list[str]:
+    try:
+        results = self._vector_store.query(query)
+        return [r.content for r in results]
+    except VectorStoreError:
+        logger.warning("Vector store unavailable, continuing without context")
+        return []  # Graceful degradation
+
+# Command layer
+async def execute(self, args: list[str]) -> CommandResult:
+    try:
+        context = await self._chat.get_context(args[0])
+        return CommandResult(success=True, data=context)
+    except CatoError as e:
+        return CommandResult(success=False, message=str(e))
+```
+
+## Testing Strategy
+
+### Unit Tests
+- Test each component in isolation
+- Use protocol-based mocks for dependencies
+- Test config validation separately
+
+### Integration Tests
+- Test service + storage combinations
+- Test command + service combinations
+- Use test fixtures for database state
+
+### End-to-End Tests
+- Test full REPL interactions
+- Use subprocess or pytest fixtures
+- Verify user-visible behaviour
+
+## Flexibility Summary
+
+| Requirement | How Achieved |
+|-------------|--------------|
+| Swap LLM providers | Protocol abstraction + config selection |
+| Add commands easily | Decorator-based registration |
+| Customise appearance | Config-driven theming, separate display layer |
+| Run multiple configs | CLI `--config` flag, isolated instances |
+| Test components | Dependency injection, protocol mocks |
+| Extend storage | Protocol abstraction + factory pattern |
+| Modify without breaking | Layered architecture, explicit interfaces |

```



Created `Project/Spec/technical/TECH_ARCHITECTURE.md`. This covers:

- **Layered architecture** with clear dependency rules
- **Protocol-based abstractions** for LLM providers and storage backends
- **Dependency injection** pattern with a bootstrap module for wiring
- **Complete directory structure** showing where each component lives
- **Extension points** for adding providers, commands, and storage backends
- **Error propagation** flow through layers
- **Testing strategy** outline

Review it and let me know if you'd like any changes before I continue with the individual component specs.

USER:
ll Project/Spec/technical/

USER:
ll Project/Spec/technical/

USER:
document the approach to development releases, CI and testing

AGENT:


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
@@ -0,0 +1,404 @@
+# Development, Testing and Release Technical Specification
+
+## Overview
+This document defines the development workflow, testing strategy, continuous integration, and release process for Cato.
+
+## Development Philosophy
+
+### Single User, Local First
+- Cato is developed for a single user on a single machine
+- No multi-user deployment considerations
+- Local development and testing is the primary workflow
+- CI exists to catch regressions, not for complex deployment pipelines
+
+### Minimal Ceremony
+- Lightweight processes that don't impede rapid iteration
+- Testing focused on core functionality, not exhaustive coverage
+- Releases when meaningful changes accumulate, not on fixed schedules
+
+## Branch Strategy
+
+### Main Branch
+- `main` is the stable branch
+- All development work happens on feature branches
+- Direct commits to `main` are prohibited
+
+### Feature Branches
+- Create a new branch for each feature or bug fix
+- Branch naming: `feature/<short-description>` or `fix/<short-description>`
+- Keep branches short-lived where possible
+- Merge to `main` via pull request (or direct merge for solo development)
+
+```bash
+# Starting new work
+git checkout main
+git pull
+git checkout -b feature/add-anthropic-provider
+
+# After completion
+git checkout main
+git merge feature/add-anthropic-provider
+git branch -d feature/add-anthropic-provider
+```
+
+## Testing Strategy
+
+### Test Pyramid
+```
+        /\
+       /  \     E2E Tests (few)
+      /----\    - Full REPL interactions
+     /      \   - Critical user journeys
+    /--------\  Integration Tests (moderate)
+   /          \ - Service + storage
+  /------------\- Command + service
+ /              \
+/----------------\  Unit Tests (many)
+                    - Individual functions
+                    - Config validation
+                    - Protocol implementations
+```
+
+### Unit Tests
+**Scope**: Individual functions, classes, and methods in isolation
+
+**What to test**:
+- Configuration loading and validation
+- Command argument parsing
+- Message formatting
+- Utility functions
+- Protocol implementations with mocked dependencies
+
+**Tools**: pytest
+
+```python
+# Example: testing config validation
+def test_temperature_must_be_in_range():
+    with pytest.raises(ValidationError):
+        LLMConfig(temperature=5.0)  # Invalid: must be 0-2
+
+def test_valid_config_loads():
+    config = LLMConfig(provider="openai", model="gpt-4o")
+    assert config.provider == "openai"
+```
+
+### Integration Tests
+**Scope**: Multiple components working together
+
+**What to test**:
+- Service layer with real storage (test database)
+- Command execution with mocked services
+- Provider implementations with mocked API responses
+
+**Approach**:
+- Use pytest fixtures for test database setup/teardown
+- Mock external APIs (OpenAI, Anthropic, etc.) at HTTP level
+- Test realistic workflows
+
+```python
+# Example: testing chat service with vector store
+@pytest.fixture
+def test_vector_store(tmp_path):
+    """Create a temporary ChromaDB instance."""
+    return ChromaDBStore(path=tmp_path / "test_vectors")
+
+def test_context_retrieval(test_vector_store):
+    # Store some content
+    test_vector_store.store("Python is a programming language", {})
+    
+    # Query should find it
+    results = test_vector_store.query("What is Python?", k=1)
+    assert len(results) == 1
+    assert "Python" in results[0].content
+```
+
+### End-to-End Tests
+**Scope**: Full application behaviour from user perspective
+
+**What to test**:
+- Application startup and shutdown
+- Critical command flows (/help, /exit, /clear)
+- Basic chat interaction (with mocked LLM)
+- Error handling and graceful degradation
+
+**Approach**:
+- Use subprocess or pexpect to drive the REPL
+- Mock LLM responses at API level
+- Keep E2E tests minimal—they're slow and brittle
+
+```python
+# Example: testing /help command
+def test_help_command(cato_process):
+    cato_process.sendline("/help")
+    output = cato_process.expect_output(timeout=5)
+    assert "Available commands" in output
+```
+
+### What NOT to Test
+- Third-party library internals (Rich, ChromaDB, etc.)
+- Exact output formatting (too brittle)
+- Every error path (focus on critical ones)
+- Performance benchmarks (not initially)
+
+### Test Organisation
+```
+tests/
+├── conftest.py           # Shared fixtures
+├── unit/
+│   ├── test_config.py
+│   ├── test_commands.py
+│   ├── test_message_parsing.py
+│   └── ...
+├── integration/
+│   ├── test_chat_service.py
+│   ├── test_vector_store.py
+│   ├── test_productivity.py
+│   └── ...
+└── e2e/
+    ├── test_startup.py
+    ├── test_basic_chat.py
+    └── test_commands.py
+```
+
+### Running Tests
+```bash
+# Run all tests
+pytest
+
+# Run only unit tests
+pytest tests/unit/
+
+# Run with coverage
+pytest --cov=cato --cov-report=term-missing
+
+# Run specific test file
+pytest tests/unit/test_config.py
+
+# Run tests matching pattern
+pytest -k "test_config"
+```
+
+## Continuous Integration
+
+### CI Philosophy
+- CI should be fast (< 5 minutes)
+- Fail fast on obvious issues
+- Don't block on non-critical checks
+
+### GitHub Actions Workflow
+```yaml
+# .github/workflows/ci.yml
+name: CI
+
+on:
+  push:
+    branches: [main]
+  pull_request:
+    branches: [main]
+
+jobs:
+  test:
+    runs-on: ubuntu-latest
+    strategy:
+      matrix:
+        python-version: ["3.11", "3.12"]
+    
+    steps:
+      - uses: actions/checkout@v4
+      
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: ${{ matrix.python-version }}
+      
+      - name: Install dependencies
+        run: |
+          pip install uv
+          uv pip install -e ".[dev]"
+      
+      - name: Run linting
+        run: ruff check cato/
+      
+      - name: Run type checking
+        run: mypy cato/
+      
+      - name: Run tests
+        run: pytest tests/unit tests/integration --tb=short
+
+  # E2E tests run separately, only on main
+  e2e:
+    runs-on: ubuntu-latest
+    if: github.ref == 'refs/heads/main'
+    needs: test
+    
+    steps:
+      - uses: actions/checkout@v4
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.12"
+      - name: Install dependencies
+        run: |
+          pip install uv
+          uv pip install -e ".[dev]"
+      - name: Run E2E tests
+        run: pytest tests/e2e --tb=short
+```
+
+### CI Checks
+1. **Linting** (ruff): Code style and common errors
+2. **Type checking** (mypy): Static type verification
+3. **Unit tests**: Fast, isolated tests
+4. **Integration tests**: Component interaction tests
+5. **E2E tests**: Full application tests (main branch only)
+
+### Pre-commit Hooks (Optional)
+```yaml
+# .pre-commit-config.yaml
+repos:
+  - repo: https://github.com/astral-sh/ruff-pre-commit
+    rev: v0.1.0
+    hooks:
+      - id: ruff
+        args: [--fix]
+      - id: ruff-format
+```
+
+## Code Quality Tools
+
+### Linting: Ruff
+```toml
+# pyproject.toml
+[tool.ruff]
+line-length = 100
+target-version = "py311"
+
+[tool.ruff.lint]
+select = [
+    "E",    # pycodestyle errors
+    "W",    # pycodestyle warnings
+    "F",    # pyflakes
+    "I",    # isort
+    "B",    # flake8-bugbear
+    "UP",   # pyupgrade
+]
+```
+
+### Type Checking: Mypy
+```toml
+# pyproject.toml
+[tool.mypy]
+python_version = "3.11"
+strict = true
+warn_return_any = true
+warn_unused_ignores = true
+```
+
+### Test Coverage
+- Aim for ~70-80% coverage on core modules
+- Don't chase 100%—diminishing returns
+- Focus coverage on business logic, not boilerplate
+
+## Release Process
+
+### Versioning
+Semantic versioning: `MAJOR.MINOR.PATCH`
+- **MAJOR**: Breaking changes to config or commands
+- **MINOR**: New features, new commands
+- **PATCH**: Bug fixes, minor improvements
+
+Pre-1.0: `0.x.y` where breaking changes are expected
+
+### Release Checklist
+1. Ensure all tests pass on `main`
+2. Update version in `pyproject.toml`
+3. Update CHANGELOG.md with notable changes
+4. Create git tag: `git tag -a v0.1.0 -m "Release 0.1.0"`
+5. Push tag: `git push origin v0.1.0`
+
+### Changelog Format
+```markdown
+# Changelog
+
+## [0.2.0] - 2026-01-20
+### Added
+- Anthropic provider support
+- /speaklike command for custom TTS instructions
+
+### Changed
+- Improved context retrieval performance
+
+### Fixed
+- Vector store connection error on startup
+
+## [0.1.0] - 2026-01-14
+- Initial release
+```
+
+### No PyPI Publishing (Initially)
+- Cato is for personal use
+- Install from git: `pip install git+https://github.com/user/cato.git`
+- Or local editable install: `pip install -e .`
+
+## Development Environment
+
+### Setup
+```bash
+# Clone repository
+git clone https://github.com/user/cato.git
+cd cato
+
+# Create conda environment (per user preference)
+conda create -n cato python=3.12
+conda activate cato
+
+# Install in editable mode with dev dependencies
+uv pip install -e ".[dev]"
+
+# Install pre-commit hooks (optional)
+pre-commit install
+```
+
+### Dev Dependencies
+```toml
+# pyproject.toml
+[project.optional-dependencies]
+dev = [
+    "pytest>=8.0",
+    "pytest-cov>=4.0",
+    "pytest-asyncio>=0.23",
+    "mypy>=1.8",
+    "ruff>=0.1",
+    "pre-commit>=3.0",
+]
+```
+
+### Running Locally
+```bash
+# Run from source
+python -m cato
+
+# Run with specific config
+python -m cato --config ~/.cato/dev.yaml
+
+# Run with debug logging
+python -m cato --log-level DEBUG
+```
+
+## Documentation
+
+### Code Documentation
+- Numpy-format docstrings on all public functions
+- Type hints on all function signatures
+- README.md in each module directory
+- `agent.txt` at repo root for AI navigation
+
+### User Documentation
+- In-app help system (`/help`)
+- Help files in `cato/resources/help/`
+- Keep help in sync with implementation
+
+### Specification Maintenance
+- Update specs when implementation diverges
+- Log significant decisions in specs
+- Specs are living documents, not write-once

```



Created `TECH_DEVELOPMENT.md` covering:

- **Branch strategy**: Feature branches, no direct commits to main
- **Testing pyramid**: Unit → Integration → E2E with clear scope for each
- **CI workflow**: GitHub Actions with linting, type checking, and tests
- **Code quality tools**: Ruff for linting, mypy for types
- **Release process**: Semantic versioning, changelog format, git tags
- **Development environment setup**: Conda + uv workflow

Ready for your review. Let me know if you'd like changes before continuing with the component specs.

USER:
go ahead and build the technical specs

AGENT:
I'll continue building the remaining technical specs. Let me check the current TODO list and proceed.
Starting with the config system spec.


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





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md
@@ -0,0 +1,394 @@
+# Configuration System Technical Specification
+
+## Overview
+Cato uses a layered YAML configuration system where user settings overlay defaults. All configurable values live in YAML files—no hard-coded defaults in code.
+
+## Configuration Hierarchy
+```
+defaults.yaml          # Shipped with Cato, never modified by user
+    ↓
+user_config.yaml       # User overrides, sparse (only differences)
+    ↓
+environment vars       # CATO_* env vars for secrets/runtime overrides
+    ↓
+CLI arguments          # Highest precedence, session-specific
+```
+
+## File Locations
+```
+~/.config/cato/
+├── config.yaml        # User configuration
+├── prompts/           # Custom system prompts
+└── themes/            # Custom display themes
+
+$PACKAGE/
+└── defaults/
+    ├── defaults.yaml  # Default configuration
+    ├── prompts/       # Default prompts
+    └── themes/        # Default themes
+```
+
+## Configuration Loading
+
+### Load Sequence
+```python
+def load_config(user_path: Path | None = None) -> CatoConfig:
+    """
+    Load configuration with overlay system.
+    
+    Parameters
+    ----------
+    user_path
+        Optional custom path to user config. If None, uses default location.
+    
+    Returns
+    -------
+    CatoConfig
+        Validated configuration object.
+    """
+    # 1. Load defaults (always present, shipped with package)
+    defaults = load_yaml(get_default_config_path())
+    
+    # 2. Load user config if exists
+    user_config = {}
+    if user_path and user_path.exists():
+        user_config = load_yaml(user_path)
+    elif default_user_path().exists():
+        user_config = load_yaml(default_user_path())
+    
+    # 3. Deep merge: user overlays defaults
+    merged = deep_merge(defaults, user_config)
+    
+    # 4. Apply environment variable overrides
+    merged = apply_env_overrides(merged)
+    
+    # 5. Validate with Pydantic
+    return CatoConfig.model_validate(merged)
+```
+
+### Deep Merge Behaviour
+```python
+# defaults.yaml
+llm:
+  provider: "openai"
+  model: "gpt-4"
+  temperature: 1.0
+  max_tokens: 4096
+
+# user_config.yaml
+llm:
+  model: "gpt-4-turbo"
+
+# Result after merge
+llm:
+  provider: "openai"        # from defaults
+  model: "gpt-4-turbo"      # from user (override)
+  temperature: 1.0          # from defaults
+  max_tokens: 4096          # from defaults
+```
+
+## Pydantic Schema
+
+### Root Configuration
+```python
+class CatoConfig(BaseModel):
+    """Root configuration model."""
+    
+    model_config = ConfigDict(extra="forbid")  # Warn on unknown keys
+    
+    llm: LLMConfig
+    vector_store: VectorStoreConfig
+    storage: StorageConfig
+    display: DisplayConfig
+    commands: CommandConfig
+    logging: LoggingConfig
+    paths: PathConfig
+```
+
+### LLM Configuration
+```python
+class LLMConfig(BaseModel):
+    """LLM provider configuration."""
+    
+    provider: Literal["openai", "anthropic", "google", "ollama"]
+    model: str
+    temperature: float = Field(ge=0.0, le=2.0)
+    max_tokens: int = Field(ge=1, le=200000)
+    timeout_seconds: int = Field(ge=1, le=300)
+    
+    # Provider-specific settings
+    openai: OpenAIConfig | None = None
+    anthropic: AnthropicConfig | None = None
+    google: GoogleConfig | None = None
+    ollama: OllamaConfig | None = None
+```
+
+### Vector Store Configuration
+```python
+class VectorStoreConfig(BaseModel):
+    """Vector store configuration."""
+    
+    enabled: bool
+    backend: Literal["chromadb"]
+    path: Path
+    collection_name: str
+    embedding_model: str
+    chunk_size: int = Field(ge=100, le=10000)
+    chunk_overlap: int = Field(ge=0)
+    
+    @field_validator("chunk_overlap")
+    @classmethod
+    def overlap_less_than_size(cls, v: int, info: ValidationInfo) -> int:
+        if "chunk_size" in info.data and v >= info.data["chunk_size"]:
+            raise ValueError("chunk_overlap must be less than chunk_size")
+        return v
+```
+
+### Storage Configuration
+```python
+class StorageConfig(BaseModel):
+    """SQLite storage configuration."""
+    
+    database_path: Path
+    backup_enabled: bool
+    backup_frequency_hours: int = Field(ge=1)
+```
+
+### Display Configuration
+```python
+class DisplayConfig(BaseModel):
+    """Display and UI configuration."""
+    
+    theme: str
+    markdown_enabled: bool
+    code_theme: str
+    max_width: int | None = Field(ge=40, default=None)
+    timestamps: bool
+    spinner_style: str
+```
+
+### Logging Configuration
+```python
+class LoggingConfig(BaseModel):
+    """Logging configuration."""
+    
+    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]
+    file_path: Path | None
+    format: str
+    max_file_size_mb: int = Field(ge=1)
+    backup_count: int = Field(ge=0)
+```
+
+## Environment Variable Overrides
+
+### Naming Convention
+```
+CATO_<SECTION>_<KEY>=value
+CATO_<SECTION>_<SUBSECTION>_<KEY>=value
+```
+
+### Examples
+```bash
+# Override LLM model
+CATO_LLM_MODEL="claude-3-opus"
+
+# Override logging level
+CATO_LOGGING_LEVEL="DEBUG"
+
+# API keys (primary use case)
+CATO_OPENAI_API_KEY="sk-..."
+CATO_ANTHROPIC_API_KEY="sk-ant-..."
+```
+
+### Implementation
+```python
+def apply_env_overrides(config: dict) -> dict:
+    """
+    Apply CATO_* environment variables as config overrides.
+    
+    Parameters
+    ----------
+    config
+        Configuration dict to modify.
+    
+    Returns
+    -------
+    dict
+        Configuration with env overrides applied.
+    """
+    prefix = "CATO_"
+    for key, value in os.environ.items():
+        if not key.startswith(prefix):
+            continue
+        
+        # Parse key path: CATO_LLM_MODEL -> ["llm", "model"]
+        parts = key[len(prefix):].lower().split("_")
+        
+        # Navigate to nested location and set value
+        set_nested(config, parts, parse_env_value(value))
+    
+    return config
+```
+
+## CLI Argument Overrides
+```python
+@click.command()
+@click.option("--config", type=Path, help="Path to config file")
+@click.option("--model", help="Override LLM model")
+@click.option("--debug", is_flag=True, help="Enable debug logging")
+def main(config: Path | None, model: str | None, debug: bool) -> None:
+    """Cato entry point."""
+    cfg = load_config(config)
+    
+    # CLI overrides (highest precedence)
+    if model:
+        cfg.llm.model = model
+    if debug:
+        cfg.logging.level = "DEBUG"
+```
+
+## Validation Behaviour
+
+### Unknown Keys
+```python
+class CatoConfig(BaseModel):
+    model_config = ConfigDict(extra="forbid")
+
+# During validation
+try:
+    config = CatoConfig.model_validate(data)
+except ValidationError as e:
+    for error in e.errors():
+        if error["type"] == "extra_forbidden":
+            key = ".".join(str(loc) for loc in error["loc"])
+            logger.warning(f"Unknown config key '{key}', ignoring")
+    # Re-validate with extra="ignore" to continue
+    config = CatoConfig.model_validate(data, strict=False)
+```
+
+### Invalid Values
+```python
+def validate_with_fallback(data: dict, defaults: dict) -> CatoConfig:
+    """
+    Validate config, falling back to defaults for invalid values.
+    
+    Parameters
+    ----------
+    data
+        User configuration data.
+    defaults
+        Default configuration data.
+    
+    Returns
+    -------
+    CatoConfig
+        Validated configuration, with defaults substituted for invalid values.
+    """
+    try:
+        return CatoConfig.model_validate(data)
+    except ValidationError as e:
+        for error in e.errors():
+            path = list(error["loc"])
+            logger.warning(
+                f"Invalid config value at '{'.'.join(map(str, path))}': "
+                f"{error['msg']}. Using default."
+            )
+            # Reset to default value
+            set_nested(data, path, get_nested(defaults, path))
+        
+        return CatoConfig.model_validate(data)
+```
+
+## Default Configuration File
+```yaml
+# defaults.yaml - Shipped with Cato, do not modify
+
+llm:
+  provider: "openai"
+  model: "gpt-4"
+  temperature: 1.0
+  max_tokens: 4096
+  timeout_seconds: 60
+
+vector_store:
+  enabled: true
+  backend: "chromadb"
+  path: "~/.local/share/cato/vectordb"
+  collection_name: "cato_memory"
+  embedding_model: "text-embedding-3-small"
+  chunk_size: 1000
+  chunk_overlap: 200
+
+storage:
+  database_path: "~/.local/share/cato/cato.db"
+  backup_enabled: true
+  backup_frequency_hours: 24
+
+display:
+  theme: "default"
+  markdown_enabled: true
+  code_theme: "monokai"
+  max_width: null
+  timestamps: false
+  spinner_style: "dots"
+
+commands:
+  prefix: "/"
+  history_file: "~/.local/share/cato/command_history"
+
+logging:
+  level: "WARNING"
+  file_path: "~/.local/share/cato/cato.log"
+  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
+  max_file_size_mb: 10
+  backup_count: 3
+
+paths:
+  data_dir: "~/.local/share/cato"
+  config_dir: "~/.config/cato"
+  cache_dir: "~/.cache/cato"
+```
+
+## User Configuration Example
+```yaml
+# ~/.config/cato/config.yaml
+# Only specify values that differ from defaults
+
+llm:
+  model: "gpt-4-turbo"
+  temperature: 0.7
+
+display:
+  theme: "gruvbox-dark"
+  timestamps: true
+
+logging:
+  level: "DEBUG"
+```
+
+## Runtime Configuration Access
+```python
+# Configuration is loaded once at startup and passed via dependency injection
+class ChatService:
+    def __init__(self, config: CatoConfig, llm: LLMProvider) -> None:
+        self._config = config
+        self._llm = llm
+    
+    async def send_message(self, message: str) -> str:
+        return await self._llm.complete(
+            message,
+            temperature=self._config.llm.temperature,
+            max_tokens=self._config.llm.max_tokens,
+        )
+```
+
+## Path Expansion
+All paths in configuration support:
+- `~` for home directory
+- Environment variables via `${VAR}`
+
+```python
+def expand_path(path: str | Path) -> Path:
+    """Expand ~ and environment variables in path."""
+    return Path(os.path.expandvars(os.path.expanduser(str(path))))
+```

```



MarkAsCompleted: 1 items
Now expanding the error handling spec with the complete exception hierarchy and logging setup.


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md
@@ -32,23 +32,152 @@
 - Use custom exception classes for domain-specific errors
 - Exceptions should carry enough context for debugging
 
-### Custom Exception Hierarchy
+## Custom Exception Hierarchy
+
+### Base Exception
 ```python
 class CatoError(Exception):
-    """Base exception for Cato errors."""
-    pass
+    """
+    Base exception for all Cato errors.
+    
+    All custom exceptions inherit from this to enable catching
+    any Cato-specific error with a single except clause when needed.
+    
+    Parameters
+    ----------
+    message
+        Human-readable error description.
+    context
+        Optional dict of contextual data for debugging.
+    """
+    
+    def __init__(self, message: str, context: dict[str, Any] | None = None) -> None:
+        super().__init__(message)
+        self.message = message
+        self.context = context or {}
+    
+    def __str__(self) -> str:
+        if self.context:
+            ctx = ", ".join(f"{k}={v!r}" for k, v in self.context.items())
+            return f"{self.message} ({ctx})"
+        return self.message
+```
 
+### Complete Hierarchy
+```python
+# Configuration
 class ConfigurationError(CatoError):
-    """Configuration-related errors."""
+    """Configuration loading or validation error."""
     pass
 
+class ConfigFileNotFoundError(ConfigurationError):
+    """Required configuration file missing."""
+    pass
+
+class ConfigValidationError(ConfigurationError):
+    """Configuration value failed validation."""
+    pass
+
+# LLM Provider
+class LLMError(CatoError):
+    """LLM provider or API error."""
+    pass
+
+class LLMConnectionError(LLMError):
+    """Cannot connect to LLM provider."""
+    pass
+
+class LLMAuthenticationError(LLMError):
+    """API key invalid or missing."""
+    pass
+
+class LLMRateLimitError(LLMError):
+    """Rate limit exceeded."""
+    
+    def __init__(self, message: str, retry_after: int | None = None, **kwargs) -> None:
+        super().__init__(message, **kwargs)
+        self.retry_after = retry_after
+
+class LLMContextLengthError(LLMError):
+    """Input exceeds model context window."""
+    pass
+
+class LLMResponseError(LLMError):
+    """Invalid or unexpected response from LLM."""
+    pass
+
+# Vector Store
 class VectorStoreError(CatoError):
-    """Vector store operation errors."""
+    """Vector store operation error."""
+    pass
+
+class VectorStoreConnectionError(VectorStoreError):
+    """Cannot connect to vector store."""
+    pass
+
+class EmbeddingError(VectorStoreError):
+    """Error generating embeddings."""
     pass
 
+# Storage (SQLite)
+class StorageError(CatoError):
+    """Database storage error."""
+    pass
+
+class StorageConnectionError(StorageError):
+    """Cannot connect to database."""
+    pass
+
+class StorageQueryError(StorageError):
+    """Database query failed."""
+    pass
+
+# Commands
 class CommandError(CatoError):
-    """Command execution errors."""
+    """Command execution error."""
+    pass
+
+class CommandNotFoundError(CommandError):
+    """Unknown command."""
+    pass
+
+class CommandArgumentError(CommandError):
+    """Invalid command arguments."""
+    pass
+
+class CommandExecutionError(CommandError):
+    """Command failed during execution."""
+    pass
+
+# Input/Output
+class IOError(CatoError):
+    """File or network I/O error."""
+    pass
+
+class FileAccessError(IOError):
+    """Cannot read or write file."""
+    pass
+
+class NetworkError(IOError):
+    """Network operation failed."""
     pass
+
+# Display
+class DisplayError(CatoError):
+    """Display/rendering error."""
+    pass
+```
+
+### Exception Location
+All exceptions defined in `cato/core/exceptions.py` and imported where needed:
+```python
+from cato.core.exceptions import (
+    CatoError,
+    ConfigurationError,
+    LLMError,
+    LLMRateLimitError,
+    # ... etc
+)
 ```
 
 ## User-Facing Error Messages

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md
@@ -236,19 +236,133 @@
 - Provide clear feedback on timeout
 - Allow retry where appropriate
 
-## Logging Integration
+## Logging System
+
+### Logger Setup
+```python
+import logging
+from logging.handlers import RotatingFileHandler
+from pathlib import Path
+
+def setup_logging(config: LoggingConfig) -> None:
+    """
+    Configure application-wide logging.
+    
+    Parameters
+    ----------
+    config
+        Logging configuration from main config.
+    """
+    root_logger = logging.getLogger("cato")
+    root_logger.setLevel(config.level)
+    
+    # Console handler (always present)
+    console = logging.StreamHandler()
+    console.setLevel(config.level)
+    console.setFormatter(logging.Formatter(
+        "%(levelname)s: %(message)s"
+    ))
+    root_logger.addHandler(console)
+    
+    # File handler (if configured)
+    if config.file_path:
+        file_handler = RotatingFileHandler(
+            config.file_path,
+            maxBytes=config.max_file_size_mb * 1024 * 1024,
+            backupCount=config.backup_count,
+        )
+        file_handler.setLevel(logging.DEBUG)  # File gets everything
+        file_handler.setFormatter(logging.Formatter(config.format))
+        root_logger.addHandler(file_handler)
+```
+
+### Module Loggers
+Each module creates its own logger:
+```python
+# In cato/providers/openai.py
+import logging
+
+logger = logging.getLogger(__name__)  # "cato.providers.openai"
+
+class OpenAIProvider:
+    async def complete(self, prompt: str) -> str:
+        logger.debug(f"Sending completion request, prompt length: {len(prompt)}")
+        try:
+            response = await self._client.complete(prompt)
+            logger.debug(f"Received response, length: {len(response)}")
+            return response
+        except RateLimitError as e:
+            logger.warning(f"Rate limited, retry after: {e.retry_after}s")
+            raise LLMRateLimitError(str(e), retry_after=e.retry_after)
+```
+
+### Log Levels
+
+| Level | Use Case | Example |
+|-------|----------|--------|
+| DEBUG | Detailed diagnostic info | "Sending request to OpenAI, model=gpt-4" |
+| INFO | Notable events | "Vector store initialised with 1,234 documents" |
+| WARNING | Recoverable issues | "Config key 'foo' unrecognised, ignoring" |
+| ERROR | Failures requiring attention | "Failed to connect to database" |
+
+### Debug Mode
+When `logging.level: DEBUG`:
+- All layers emit detailed logs
+- Request/response payloads logged (truncated)
+- Timing information for operations
+- Stack traces for all exceptions
+
+```python
+logger.debug(
+    f"LLM request: provider={provider}, model={model}, "
+    f"temperature={temp}, tokens={len(messages)}"
+)
+```
+
+### Warn Mode
+When `logging.level: WARNING`:
+- Only issues affecting user experience
+- Degraded functionality notifications
+- Performance warnings
 
-### Error Logging
+### Sensitive Data
+Never log:
+- API keys (even partial)
+- User credentials
+- Full conversation content (log lengths instead)
+
+```python
+# GOOD
+logger.debug(f"API request with key ending in ...{api_key[-4:]}")
+logger.debug(f"Processing message, length: {len(content)} chars")
+
+# BAD
+logger.debug(f"API key: {api_key}")
+logger.debug(f"User message: {content}")
+```
+
+## Error Logging
 - All errors must be logged
-- Log level appropriate to severity:
-  - DEBUG: Detailed diagnostic info
-  - INFO: Notable events
-  - WARNING: Recoverable issues
-  - ERROR: Failures requiring attention
+- Log level appropriate to severity
+- Include context for debugging
 
-### Context in Logs
-- Include relevant context (operation being attempted, relevant parameters)
-- Don't log sensitive data (API keys, passwords)
+```python
+try:
+    result = await provider.complete(prompt)
+except LLMRateLimitError as e:
+    logger.warning(
+        f"Rate limit hit",
+        extra={"provider": provider.name, "retry_after": e.retry_after}
+    )
+    raise
+except LLMError as e:
+    logger.error(
+        f"LLM request failed: {e}",
+        extra={"provider": provider.name, "model": model},
+        exc_info=True  # Include stack trace
+    )
+    raise
+```
 
 ## Never Silent Failures
 - Never swallow exceptions without logging

```



MarkAsCompleted: 1 items
Now creating the LLM integration spec.


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_LLM_INTEGRATION.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_LLM_INTEGRATION.md
@@ -0,0 +1,555 @@
+# LLM Integration Technical Specification
+
+## Overview
+Cato supports multiple LLM providers through a unified protocol-based abstraction. Providers are interchangeable at runtime via configuration.
+
+## Provider Protocol
+
+### Interface Definition
+```python
+from typing import Protocol, AsyncIterator
+from dataclasses import dataclass
+
+@dataclass
+class Message:
+    """Normalised message format."""
+    role: Literal["system", "user", "assistant"]
+    content: str
+
+@dataclass
+class CompletionResult:
+    """Result from LLM completion."""
+    content: str
+    model: str
+    usage: TokenUsage | None = None
+    finish_reason: str | None = None
+
+@dataclass
+class TokenUsage:
+    """Token usage statistics."""
+    prompt_tokens: int
+    completion_tokens: int
+    total_tokens: int
+
+
+class LLMProvider(Protocol):
+    """
+    Protocol for LLM provider implementations.
+    
+    Any class implementing these methods can be used as a provider.
+    """
+    
+    @property
+    def name(self) -> str:
+        """Provider identifier (e.g., 'openai', 'anthropic')."""
+        ...
+    
+    @property
+    def model(self) -> str:
+        """Currently configured model."""
+        ...
+    
+    async def complete(
+        self,
+        messages: list[Message],
+        *,
+        temperature: float | None = None,
+        max_tokens: int | None = None,
+    ) -> CompletionResult:
+        """
+        Generate a completion for the given messages.
+        
+        Parameters
+        ----------
+        messages
+            Conversation history in normalised format.
+        temperature
+            Override configured temperature.
+        max_tokens
+            Override configured max tokens.
+        
+        Returns
+        -------
+        CompletionResult
+            The model's response with metadata.
+        
+        Raises
+        ------
+        LLMConnectionError
+            Cannot reach the provider.
+        LLMAuthenticationError
+            Invalid API key.
+        LLMRateLimitError
+            Rate limit exceeded.
+        LLMContextLengthError
+            Input exceeds context window.
+        """
+        ...
+    
+    async def complete_stream(
+        self,
+        messages: list[Message],
+        *,
+        temperature: float | None = None,
+        max_tokens: int | None = None,
+    ) -> AsyncIterator[str]:
+        """
+        Stream completion tokens as they arrive.
+        
+        Yields
+        ------
+        str
+            Individual tokens or token chunks.
+        """
+        ...
+    
+    def count_tokens(self, text: str) -> int:
+        """
+        Count tokens in text for this provider's tokenizer.
+        
+        Parameters
+        ----------
+        text
+            Text to tokenize.
+        
+        Returns
+        -------
+        int
+            Token count.
+        """
+        ...
+```
+
+## Provider Implementations
+
+### OpenAI Provider
+```python
+class OpenAIProvider:
+    """OpenAI API provider implementation."""
+    
+    def __init__(self, config: OpenAIConfig) -> None:
+        self._config = config
+        self._client = AsyncOpenAI(api_key=config.api_key)
+        self._model = config.model
+    
+    @property
+    def name(self) -> str:
+        return "openai"
+    
+    @property
+    def model(self) -> str:
+        return self._model
+    
+    async def complete(
+        self,
+        messages: list[Message],
+        *,
+        temperature: float | None = None,
+        max_tokens: int | None = None,
+    ) -> CompletionResult:
+        try:
+            response = await self._client.chat.completions.create(
+                model=self._model,
+                messages=[self._to_openai_message(m) for m in messages],
+                temperature=temperature or self._config.temperature,
+                max_tokens=max_tokens or self._config.max_tokens,
+            )
+            return self._to_result(response)
+        except openai.AuthenticationError as e:
+            raise LLMAuthenticationError(str(e))
+        except openai.RateLimitError as e:
+            raise LLMRateLimitError(str(e), retry_after=self._parse_retry(e))
+        except openai.APIConnectionError as e:
+            raise LLMConnectionError(str(e))
+    
+    def _to_openai_message(self, msg: Message) -> dict:
+        return {"role": msg.role, "content": msg.content}
+    
+    def _to_result(self, response) -> CompletionResult:
+        choice = response.choices[0]
+        return CompletionResult(
+            content=choice.message.content,
+            model=response.model,
+            usage=TokenUsage(
+                prompt_tokens=response.usage.prompt_tokens,
+                completion_tokens=response.usage.completion_tokens,
+                total_tokens=response.usage.total_tokens,
+            ),
+            finish_reason=choice.finish_reason,
+        )
+```
+
+### Anthropic Provider
+```python
+class AnthropicProvider:
+    """Anthropic Claude API provider implementation."""
+    
+    def __init__(self, config: AnthropicConfig) -> None:
+        self._config = config
+        self._client = AsyncAnthropic(api_key=config.api_key)
+        self._model = config.model
+    
+    @property
+    def name(self) -> str:
+        return "anthropic"
+    
+    async def complete(
+        self,
+        messages: list[Message],
+        *,
+        temperature: float | None = None,
+        max_tokens: int | None = None,
+    ) -> CompletionResult:
+        # Extract system message (Anthropic handles it separately)
+        system_msg = None
+        chat_messages = []
+        for msg in messages:
+            if msg.role == "system":
+                system_msg = msg.content
+            else:
+                chat_messages.append({"role": msg.role, "content": msg.content})
+        
+        try:
+            response = await self._client.messages.create(
+                model=self._model,
+                system=system_msg,
+                messages=chat_messages,
+                temperature=temperature or self._config.temperature,
+                max_tokens=max_tokens or self._config.max_tokens,
+            )
+            return self._to_result(response)
+        except anthropic.AuthenticationError as e:
+            raise LLMAuthenticationError(str(e))
+        except anthropic.RateLimitError as e:
+            raise LLMRateLimitError(str(e))
+```
+
+### Google Provider
+```python
+class GoogleProvider:
+    """Google Gemini API provider implementation."""
+    
+    def __init__(self, config: GoogleConfig) -> None:
+        self._config = config
+        genai.configure(api_key=config.api_key)
+        self._model = genai.GenerativeModel(config.model)
+    
+    @property
+    def name(self) -> str:
+        return "google"
+    
+    async def complete(
+        self,
+        messages: list[Message],
+        *,
+        temperature: float | None = None,
+        max_tokens: int | None = None,
+    ) -> CompletionResult:
+        # Convert to Gemini format
+        history = self._build_history(messages[:-1])
+        chat = self._model.start_chat(history=history)
+        
+        response = await chat.send_message_async(
+            messages[-1].content,
+            generation_config=genai.GenerationConfig(
+                temperature=temperature or self._config.temperature,
+                max_output_tokens=max_tokens or self._config.max_tokens,
+            ),
+        )
+        return CompletionResult(
+            content=response.text,
+            model=self._config.model,
+        )
+```
+
+### Ollama Provider
+```python
+class OllamaProvider:
+    """Ollama local model provider implementation."""
+    
+    def __init__(self, config: OllamaConfig) -> None:
+        self._config = config
+        self._base_url = config.base_url or "http://localhost:11434"
+        self._model = config.model
+    
+    @property
+    def name(self) -> str:
+        return "ollama"
+    
+    async def complete(
+        self,
+        messages: list[Message],
+        *,
+        temperature: float | None = None,
+        max_tokens: int | None = None,
+    ) -> CompletionResult:
+        async with httpx.AsyncClient() as client:
+            response = await client.post(
+                f"{self._base_url}/api/chat",
+                json={
+                    "model": self._model,
+                    "messages": [{"role": m.role, "content": m.content} for m in messages],
+                    "options": {
+                        "temperature": temperature or self._config.temperature,
+                        "num_predict": max_tokens or self._config.max_tokens,
+                    },
+                    "stream": False,
+                },
+                timeout=self._config.timeout_seconds,
+            )
+            response.raise_for_status()
+            data = response.json()
+            return CompletionResult(
+                content=data["message"]["content"],
+                model=self._model,
+            )
+```
+
+## Provider Factory
+
+### Registration and Creation
+```python
+from typing import Callable
+
+# Provider registry: maps name to factory function
+_PROVIDERS: dict[str, Callable[[CatoConfig], LLMProvider]] = {}
+
+
+def register_provider(name: str) -> Callable:
+    """
+    Decorator to register a provider factory.
+    
+    Parameters
+    ----------
+    name
+        Provider identifier (must match config value).
+    """
+    def decorator(factory: Callable[[CatoConfig], LLMProvider]) -> Callable:
+        _PROVIDERS[name] = factory
+        return factory
+    return decorator
+
+
+@register_provider("openai")
+def create_openai(config: CatoConfig) -> LLMProvider:
+    return OpenAIProvider(config.llm.openai)
+
+
+@register_provider("anthropic")
+def create_anthropic(config: CatoConfig) -> LLMProvider:
+    return AnthropicProvider(config.llm.anthropic)
+
+
+@register_provider("google")
+def create_google(config: CatoConfig) -> LLMProvider:
+    return GoogleProvider(config.llm.google)
+
+
+@register_provider("ollama")
+def create_ollama(config: CatoConfig) -> LLMProvider:
+    return OllamaProvider(config.llm.ollama)
+
+
+def create_provider(config: CatoConfig) -> LLMProvider:
+    """
+    Create the configured LLM provider.
+    
+    Parameters
+    ----------
+    config
+        Application configuration.
+    
+    Returns
+    -------
+    LLMProvider
+        Configured provider instance.
+    
+    Raises
+    ------
+    ConfigurationError
+        Unknown provider name.
+    """
+    provider_name = config.llm.provider
+    if provider_name not in _PROVIDERS:
+        raise ConfigurationError(
+            f"Unknown LLM provider: {provider_name}",
+            context={"available": list(_PROVIDERS.keys())},
+        )
+    return _PROVIDERS[provider_name](config)
+```
+
+## Message Normalisation
+
+### Conversation History
+```python
+@dataclass
+class Conversation:
+    """Manages conversation state and history."""
+    
+    system_prompt: str
+    messages: list[Message] = field(default_factory=list)
+    
+    def add_user_message(self, content: str) -> None:
+        """Add a user message to history."""
+        self.messages.append(Message(role="user", content=content))
+    
+    def add_assistant_message(self, content: str) -> None:
+        """Add an assistant response to history."""
+        self.messages.append(Message(role="assistant", content=content))
+    
+    def to_messages(self) -> list[Message]:
+        """
+        Get full message list for LLM request.
+        
+        Returns
+        -------
+        list[Message]
+            System prompt followed by conversation history.
+        """
+        return [Message(role="system", content=self.system_prompt)] + self.messages
+    
+    def truncate_to_tokens(self, max_tokens: int, counter: Callable[[str], int]) -> None:
+        """
+        Truncate history to fit within token limit.
+        
+        Removes oldest messages (after system prompt) until within limit.
+        Always keeps system prompt and most recent exchange.
+        
+        Parameters
+        ----------
+        max_tokens
+            Maximum allowed tokens.
+        counter
+            Function to count tokens in text.
+        """
+        while self._count_tokens(counter) > max_tokens and len(self.messages) > 2:
+            self.messages.pop(0)  # Remove oldest message
+    
+    def _count_tokens(self, counter: Callable[[str], int]) -> int:
+        total = counter(self.system_prompt)
+        for msg in self.messages:
+            total += counter(msg.content)
+        return total
+```
+
+## Error Handling
+
+### Provider-Specific to Generic Mapping
+Each provider implementation maps its specific exceptions to the generic hierarchy:
+
+```python
+# Exception mapping pattern
+OPENAI_EXCEPTION_MAP = {
+    openai.AuthenticationError: LLMAuthenticationError,
+    openai.RateLimitError: LLMRateLimitError,
+    openai.APIConnectionError: LLMConnectionError,
+    openai.BadRequestError: LLMContextLengthError,  # Often context length
+}
+
+def map_exception(e: Exception, mapping: dict) -> CatoError:
+    """Map provider exception to Cato exception."""
+    for provider_exc, cato_exc in mapping.items():
+        if isinstance(e, provider_exc):
+            return cato_exc(str(e))
+    return LLMError(str(e))
+```
+
+### Retry Logic
+```python
+async def complete_with_retry(
+    provider: LLMProvider,
+    messages: list[Message],
+    max_retries: int = 3,
+) -> CompletionResult:
+    """
+    Complete with automatic retry on transient failures.
+    
+    Parameters
+    ----------
+    provider
+        LLM provider to use.
+    messages
+        Messages to send.
+    max_retries
+        Maximum retry attempts.
+    
+    Returns
+    -------
+    CompletionResult
+        Successful completion result.
+    
+    Raises
+    ------
+    LLMError
+        After all retries exhausted.
+    """
+    last_error = None
+    for attempt in range(max_retries):
+        try:
+            return await provider.complete(messages)
+        except LLMRateLimitError as e:
+            last_error = e
+            if e.retry_after:
+                await asyncio.sleep(e.retry_after)
+            else:
+                await asyncio.sleep(2 ** attempt)  # Exponential backoff
+        except LLMConnectionError as e:
+            last_error = e
+            await asyncio.sleep(2 ** attempt)
+    
+    raise last_error or LLMError("Max retries exceeded")
+```
+
+## Configuration
+
+### Provider-Specific Config
+```yaml
+llm:
+  provider: "openai"  # Which provider to use
+  model: "gpt-4"
+  temperature: 1.0
+  max_tokens: 4096
+  timeout_seconds: 60
+  
+  # Provider-specific settings (only relevant one is used)
+  openai:
+    api_key: "${OPENAI_API_KEY}"
+    organization: null
+    
+  anthropic:
+    api_key: "${ANTHROPIC_API_KEY}"
+    
+  google:
+    api_key: "${GOOGLE_API_KEY}"
+    
+  ollama:
+    base_url: "http://localhost:11434"
+```
+
+## Adding New Providers
+
+To add a new provider:
+
+1. Create `cato/providers/<name>.py`
+2. Implement the `LLMProvider` protocol
+3. Register with `@register_provider("<name>")`
+4. Add config model to `cato/core/config.py`
+5. Add to config schema validation
+
+```python
+# cato/providers/newprovider.py
+from cato.providers.base import LLMProvider, register_provider
+
+@register_provider("newprovider")
+def create_newprovider(config: CatoConfig) -> LLMProvider:
+    return NewProvider(config.llm.newprovider)
+
+class NewProvider:
+    """New provider implementation."""
+    
+    def __init__(self, config: NewProviderConfig) -> None:
+        # Setup
+        pass
+    
+    # Implement protocol methods...
+```

```



MarkAsCompleted: 1 items
Creating the command framework spec. Let me first check the existing command system spec for reference.


**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md**
```
# Command System Specification

## Overview

Cato uses a slash command system for explicit actions. Commands start with `/` and are parsed before any other input processing.

## Command Framework

### Command Detection
Input is treated as a command if it starts with `/` (after whitespace trimming).

### Command Parsing
Commands are parsed using shell-like tokenization:
- Command name extracted after `/`
- Arguments split by whitespace
- Quoted arguments preserved as single tokens

Example:
```
/web "search query with spaces" google
```
Parses to: command=`web`, args=`["search query with spaces", "google"]`

### Command Result
Each command returns a result with:
- `success`: Boolean indicating success/failure
- `message`: User-facing message
- `data`: Optional structured data for further processing

## Command Reference

### Core Commands

#### /help
Display help information.
```
/help                    # Show overview
/help commands           # Show all commands
/help productivity       # Show productivity help
/help files              # Show file operations help
/help websearch          # Show web search help
/help speak              # Show TTS help
/help config             # Show configuration help
/help model "question"   # Ask the model about Cato (see below)
```

##### /help model
Ask the model for help with Cato functionality.
```
/help model "how do I add a new command?"
/help model "what configuration options affect the vector store?"
```

**Behavior:**
1. Loads all user help files into context
2. Creates a one-off message to the model with:
   - Help file contents
   - Instruction to derive response from help documentation
   - The user's question
3. Model responds based solely on help documentation
4. This exchange is NOT added to the conversation history
5. Does not affect the main conversation context

#### /exit, /quit, /q
Exit the application.
```
/exit
/quit
/q
```

#### /clear
Clear conversation history and screen.
```
/clear
```
Behavior:
- Removes all user/assistant messages
- Preserves system messages
- Clears terminal screen
- Displays welcome message

#### /config
Show current configuration settings.
```
/config
```
Displays table with:
- Model, temperature, max tokens
- Vector store settings
- Display settings
- Logging level

### History Commands

#### /history
Show conversation history.
```
/history        # Show all messages
/history 10     # Show last 10 messages
```

#### /delete
Remove recent exchanges from history.
```
/delete         # Remove last exchange
/delete 3       # Remove last 3 exchanges
```

#### /model
Change or display the current LLM model. This overrides the setting in the user config file.
```
/model                  # Show current model
/model gpt-4o           # Change to gpt-4o
/model claude-3-sonnet  # Change to Claude
```

#### /showsys
Display the current system prompt.
```
/showsys
```

#### /loglevel
Change logging verbosity.
```
/loglevel           # Show current level
/loglevel DEBUG     # Set to DEBUG
/loglevel INFO      # Set to INFO
/loglevel WARN      # Set to WARN
/loglevel ERROR     # Set to ERROR
```

### Context Commands

#### /showcontext
Toggle context display mode for all future exchanges.
```
/showcontext        # Toggle on/off (shows new state)
/showcontext on     # Enable context display with excerpts
/showcontext off    # Disable context display
```

**Behavior:**
- Acts as a **toggle** - calling `/showcontext` without arguments flips the current state
- When **on**: Context excerpts displayed before each response
- When **off**: No context information displayed (default)
- State persists for the duration of the session

#### /continue, /cont
Continue an existing conversation thread.
```
/continue <thread_id>
/cont <thread_id>
```

#### /casual
Toggle casual conversation mode.
```
/casual on      # Enable casual mode
/casual off     # Disable casual mode
```

### File Commands

#### /attach
Attach files as conversation context.
```
/attach file1.txt                    # Attach single file
/attach file1.txt file2.py file3.md  # Attach multiple (max 5)
```

#### /pwd
Show current working directory.
```
/pwd
```

#### /cd
Change current directory.
```
/cd /path/to/directory
/cd ..
/cd ~
```

#### /ls
List directory contents (alias for `/file list`).
```
/ls              # List current directory
/ls /path/to     # List specific directory
```

#### /cat
Display file contents (alias for `/file read`).
```
/cat filename.txt
/cat alias:filename.txt
```

#### /locations
Show configured location aliases.
```
/locations
```

### Export Commands

#### /writecode
Extract code blocks from last response.
```
/writecode output.py
```
Extracts all code blocks (from markdown fences) and saves to file.

#### /writejson
Export conversation to JSON.
```
/writejson conversation.json
```
Exports:
- All messages with roles and content
- Configuration metadata (model, temperature)

#### /writemd, /w
Export conversation thread to Markdown.
```
/writemd output.md
/w output.md
```
Exports user/assistant exchanges (excludes system prompts).

#### /writemdall
Export full conversation to Markdown (includes system prompts).
```
/writemdall output.md
```

#### /writeresp
Export last exchange to file.
```
/writeresp output.txt           # Plain text
/writeresp output.json json     # JSON format
/writeresp output.md md         # Markdown format
```

#### /append
Append to an existing file.
```
/append notes.txt "Additional content"
/append notes.txt                       # Append last exchange
```

### Clipboard Commands

#### /copy
Copy last assistant response to clipboard.
```
/copy
```

### Vector Store Commands

See SPEC_VECTOR_STORE.md for detailed vector store documentation.

#### /vadd
Add text directly to vector store.
```
/vadd This is important information to remember
```

#### /vdoc
Add a document file to vector store with chunking.
```
/vdoc /path/to/document.txt
/vdoc alias:document.md
```

#### /vdelete
Delete an exchange from vector store.
```
/vdelete <exchange_id>
```

#### /vget
Retrieve exchanges by ID, session, or thread.
```
/vget <exchange_id>      # Get specific exchange
/vget session            # Get current session exchanges
/vget thread             # Get current thread exchanges
```

#### /vquery
Query vector store for similar content.
```
/vquery "search query"       # Default results
/vquery "search query" 10    # Return 10 results
```

#### /vstats
Display vector store statistics.
```
/vstats
```

### Memory Commands

### Productivity Commands

See SPEC_PRODUCTIVITY.md for detailed productivity documentation.

#### /st, /show-tasks, /tasks
Show open tasks.
```
/st                         # Show all open tasks
/st work                    # Filter by category
/st -p high                 # Filter by priority
/st -s priority -o desc     # Sort by priority descending
/st --status=completed      # Show completed tasks
```

**Options:**
- `-s, --sort=<field>`: Sort by created, priority, category, due, id, status
- `-o, --order=<asc|desc>`: Sort order
- `-p, --priority=<level>`: Filter by priority
- `-c, --category=<name>`: Filter by category
- `-S, --status=<status>`: Filter by status (active, in_progress, completed)

#### /list, /lists, /show-lists
Show lists and list items.
```
/list                   # Show all lists with counts
/list shopping          # Show items in shopping list
```

### Web Commands

See SPEC_WEB_SEARCH.md for detailed web search documentation.

#### /web
Search the web and add results to context.
```
/web "search query"                  # Use default engine
/web "search query" google           # Use specific engine
/web "search query" duckduckgo       # Use DuckDuckGo
```

#### /url
Fetch and attach content from a URL.
```
/url https://example.com/page.html
```

### TTS Commands

See SPEC_TTS.md for detailed TTS documentation.

#### /speak, /s
Speak the last assistant response.
```
/speak              # Default voice and model
/speak nova         # Specific voice
/speak nova tts-1   # Specific voice and model
/s                  # Alias
```

**Available Voices:** alloy, echo, fable, nova, onyx, shimmer

**Available Models:** tts-1, tts-1-hd

#### /speaklike, /sl
Speak with custom instructions.
```
/speaklike "Speak slowly and clearly"
/speaklike "Read as a news anchor" nova tts-1-hd
```

## Command Aliases

| Command | Aliases |
|---------|---------|
| /exit | /quit, /q |
| /continue | /cont |
| /speak | /s |
| /speaklike | /sl |
| /remember | /rem, /r |
| /st | /show-tasks, /tasks |
| /list | /lists, /show-lists |
| /timelog | /tl, /time |
| /writemd | /w |

## Error Handling

Commands return appropriate error messages for:
- Missing required arguments
- Invalid argument values
- File not found / permission denied
- Feature disabled in configuration
- External service failures (API, network)

Example error display:
```
❌ Command error: No file path specified. Usage: /file read <path>
```

## Command Extension

The command system is designed for extensibility:
- Commands registered via `@command` decorator
- BaseCommand abstract class for implementation
- CommandRegistry for lookup and alias resolution
- Async execute method for each command

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_COMMAND_FRAMEWORK.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_COMMAND_FRAMEWORK.md
@@ -0,0 +1,648 @@
+# Command Framework Technical Specification
+
+## Overview
+Cato uses a decorator-based command registration system. Commands are self-contained modules that register themselves on import, enabling easy addition of new commands without modifying core code.
+
+## Command Protocol
+
+### Base Interface
+```python
+from typing import Protocol
+from dataclasses import dataclass
+
+@dataclass
+class CommandResult:
+    """Result from command execution."""
+    success: bool
+    message: str
+    data: dict | None = None
+
+
+class Command(Protocol):
+    """
+    Protocol for command implementations.
+    
+    Commands are stateless—all state accessed via injected dependencies.
+    """
+    
+    @property
+    def name(self) -> str:
+        """Primary command name (without slash)."""
+        ...
+    
+    @property
+    def aliases(self) -> list[str]:
+        """Alternative names for the command."""
+        ...
+    
+    @property
+    def description(self) -> str:
+        """Brief description for help text."""
+        ...
+    
+    @property
+    def usage(self) -> str:
+        """Usage pattern string."""
+        ...
+    
+    async def execute(
+        self,
+        args: list[str],
+        context: CommandContext,
+    ) -> CommandResult:
+        """
+        Execute the command.
+        
+        Parameters
+        ----------
+        args
+            Parsed arguments (command name excluded).
+        context
+            Execution context with dependencies.
+        
+        Returns
+        -------
+        CommandResult
+            Result with success status and message.
+        """
+        ...
+```
+
+### Command Context
+```python
+@dataclass
+class CommandContext:
+    """
+    Execution context providing access to application services.
+    
+    Injected at runtime—commands should not instantiate dependencies.
+    """
+    
+    config: CatoConfig
+    conversation: Conversation
+    llm: LLMProvider
+    vector_store: VectorStore | None
+    storage: Storage
+    display: Display
+    
+    # Current state
+    cwd: Path  # Current working directory
+    session_id: str
+    thread_id: str | None
+```
+
+## Command Registration
+
+### Decorator Pattern
+```python
+from typing import Callable, Type
+
+# Global command registry
+_COMMANDS: dict[str, Type[Command]] = {}
+_ALIASES: dict[str, str] = {}  # alias -> primary name
+
+
+def command(
+    name: str,
+    aliases: list[str] | None = None,
+    description: str = "",
+    usage: str = "",
+) -> Callable[[Type], Type]:
+    """
+    Decorator to register a command class.
+    
+    Parameters
+    ----------
+    name
+        Primary command name (without slash).
+    aliases
+        Alternative names.
+    description
+        Brief description for help.
+    usage
+        Usage pattern string.
+    
+    Returns
+    -------
+    Callable
+        Decorator that registers the class.
+    
+    Example
+    -------
+    @command("help", aliases=["h", "?"], description="Show help")
+    class HelpCommand:
+        async def execute(self, args, context):
+            ...
+    """
+    def decorator(cls: Type) -> Type:
+        # Attach metadata to class
+        cls._cmd_name = name
+        cls._cmd_aliases = aliases or []
+        cls._cmd_description = description
+        cls._cmd_usage = usage
+        
+        # Register
+        _COMMANDS[name] = cls
+        for alias in (aliases or []):
+            _ALIASES[alias] = name
+        
+        return cls
+    return decorator
+```
+
+### Registry Access
+```python
+class CommandRegistry:
+    """
+    Central registry for command lookup and execution.
+    
+    Commands are discovered automatically when their modules are imported.
+    """
+    
+    def __init__(self) -> None:
+        self._commands = _COMMANDS
+        self._aliases = _ALIASES
+    
+    def get(self, name: str) -> Type[Command] | None:
+        """
+        Look up a command by name or alias.
+        
+        Parameters
+        ----------
+        name
+            Command name (with or without slash).
+        
+        Returns
+        -------
+        Type[Command] | None
+            Command class if found.
+        """
+        # Strip leading slash if present
+        name = name.lstrip("/")
+        
+        # Check aliases first
+        if name in self._aliases:
+            name = self._aliases[name]
+        
+        return self._commands.get(name)
+    
+    def list_commands(self) -> list[tuple[str, str, list[str]]]:
+        """
+        List all registered commands.
+        
+        Returns
+        -------
+        list[tuple[str, str, list[str]]]
+            List of (name, description, aliases) tuples.
+        """
+        return [
+            (name, cls._cmd_description, cls._cmd_aliases)
+            for name, cls in sorted(self._commands.items())
+        ]
+    
+    def resolve_alias(self, name: str) -> str:
+        """Resolve an alias to its primary command name."""
+        return self._aliases.get(name.lstrip("/"), name.lstrip("/"))
+```
+
+## Command Parsing
+
+### Input Tokenization
+```python
+import shlex
+
+def parse_command_input(input_text: str) -> tuple[str, list[str]] | None:
+    """
+    Parse user input into command name and arguments.
+    
+    Parameters
+    ----------
+    input_text
+        Raw user input.
+    
+    Returns
+    -------
+    tuple[str, list[str]] | None
+        (command_name, args) if input is a command, None otherwise.
+    
+    Examples
+    --------
+    >>> parse_command_input("/help")
+    ("help", [])
+    >>> parse_command_input('/web "search query" google')
+    ("web", ["search query", "google"])
+    >>> parse_command_input("hello")
+    None
+    """
+    text = input_text.strip()
+    
+    # Must start with /
+    if not text.startswith("/"):
+        return None
+    
+    # Remove leading slash
+    text = text[1:]
+    
+    # Handle empty command
+    if not text:
+        return None
+    
+    try:
+        # Use shlex for shell-like tokenization
+        tokens = shlex.split(text)
+    except ValueError:
+        # Unbalanced quotes - treat rest as single argument
+        parts = text.split(maxsplit=1)
+        tokens = [parts[0], parts[1]] if len(parts) > 1 else [parts[0]]
+    
+    command_name = tokens[0].lower()
+    args = tokens[1:] if len(tokens) > 1 else []
+    
+    return (command_name, args)
+```
+
+### Argument Parsing
+Commands can use argument parsers for complex arguments:
+
+```python
+from argparse import ArgumentParser, Namespace
+
+class TaskCommand:
+    """Show tasks with filtering and sorting."""
+    
+    def __init__(self) -> None:
+        self._parser = ArgumentParser(prog="/st", add_help=False)
+        self._parser.add_argument("category", nargs="?", default=None)
+        self._parser.add_argument("-p", "--priority", choices=["low", "medium", "high"])
+        self._parser.add_argument("-s", "--sort", default="created")
+        self._parser.add_argument("-o", "--order", choices=["asc", "desc"], default="asc")
+        self._parser.add_argument("-S", "--status", default="active")
+    
+    async def execute(self, args: list[str], context: CommandContext) -> CommandResult:
+        try:
+            parsed = self._parser.parse_args(args)
+        except SystemExit:
+            return CommandResult(
+                success=False,
+                message=f"Invalid arguments. Usage: {self._cmd_usage}",
+            )
+        
+        # Use parsed.category, parsed.priority, etc.
+        ...
+```
+
+## Command Execution
+
+### Execution Flow
+```python
+class CommandExecutor:
+    """
+    Executes commands with proper context and error handling.
+    """
+    
+    def __init__(
+        self,
+        registry: CommandRegistry,
+        context_factory: Callable[[], CommandContext],
+    ) -> None:
+        self._registry = registry
+        self._context_factory = context_factory
+    
+    async def execute(self, input_text: str) -> CommandResult | None:
+        """
+        Parse and execute a command from user input.
+        
+        Parameters
+        ----------
+        input_text
+            Raw user input.
+        
+        Returns
+        -------
+        CommandResult | None
+            Result if input was a command, None if not a command.
+        
+        Raises
+        ------
+        CommandNotFoundError
+            Unknown command name.
+        CommandExecutionError
+            Command failed during execution.
+        """
+        parsed = parse_command_input(input_text)
+        if parsed is None:
+            return None  # Not a command
+        
+        command_name, args = parsed
+        
+        # Look up command
+        command_cls = self._registry.get(command_name)
+        if command_cls is None:
+            raise CommandNotFoundError(
+                f"Unknown command: /{command_name}",
+                context={"available": [c[0] for c in self._registry.list_commands()]},
+            )
+        
+        # Create instance and execute
+        command = command_cls()
+        context = self._context_factory()
+        
+        try:
+            return await command.execute(args, context)
+        except CatoError:
+            raise  # Let Cato errors propagate
+        except Exception as e:
+            raise CommandExecutionError(
+                f"Command /{command_name} failed: {e}",
+                context={"command": command_name, "args": args},
+            ) from e
+```
+
+## Command Implementation Examples
+
+### Simple Command
+```python
+@command("clear", description="Clear conversation and screen")
+class ClearCommand:
+    """Clear conversation history and terminal screen."""
+    
+    @property
+    def name(self) -> str:
+        return "clear"
+    
+    @property
+    def aliases(self) -> list[str]:
+        return []
+    
+    @property
+    def description(self) -> str:
+        return "Clear conversation and screen"
+    
+    @property
+    def usage(self) -> str:
+        return "/clear"
+    
+    async def execute(
+        self,
+        args: list[str],
+        context: CommandContext,
+    ) -> CommandResult:
+        # Clear conversation (keep system prompt)
+        context.conversation.messages.clear()
+        
+        # Clear screen
+        context.display.clear()
+        context.display.show_welcome()
+        
+        return CommandResult(success=True, message="Conversation cleared")
+```
+
+### Command with Arguments
+```python
+@command(
+    "history",
+    aliases=["h"],
+    description="Show conversation history",
+    usage="/history [count]",
+)
+class HistoryCommand:
+    """Display conversation history."""
+    
+    @property
+    def name(self) -> str:
+        return "history"
+    
+    @property
+    def aliases(self) -> list[str]:
+        return ["h"]
+    
+    @property
+    def description(self) -> str:
+        return "Show conversation history"
+    
+    @property
+    def usage(self) -> str:
+        return "/history [count]"
+    
+    async def execute(
+        self,
+        args: list[str],
+        context: CommandContext,
+    ) -> CommandResult:
+        # Parse optional count argument
+        count = None
+        if args:
+            try:
+                count = int(args[0])
+                if count < 1:
+                    raise ValueError()
+            except ValueError:
+                return CommandResult(
+                    success=False,
+                    message=f"Invalid count: {args[0]}. Must be a positive integer.",
+                )
+        
+        # Get messages
+        messages = context.conversation.messages
+        if count:
+            messages = messages[-count:]
+        
+        # Format and display
+        for msg in messages:
+            context.display.show_message(msg.role, msg.content)
+        
+        return CommandResult(
+            success=True,
+            message=f"Showing {len(messages)} messages",
+        )
+```
+
+### Command with Subcommands
+```python
+@command(
+    "help",
+    aliases=["h", "?"],
+    description="Show help information",
+    usage="/help [topic]",
+)
+class HelpCommand:
+    """Display help information."""
+    
+    # Subcommand handlers
+    _TOPICS = {
+        "commands": "_show_commands",
+        "productivity": "_show_productivity",
+        "files": "_show_files",
+        "model": "_ask_model",
+    }
+    
+    async def execute(
+        self,
+        args: list[str],
+        context: CommandContext,
+    ) -> CommandResult:
+        if not args:
+            return await self._show_overview(context)
+        
+        topic = args[0].lower()
+        handler_name = self._TOPICS.get(topic)
+        
+        if handler_name:
+            handler = getattr(self, handler_name)
+            return await handler(args[1:], context)
+        
+        return CommandResult(
+            success=False,
+            message=f"Unknown help topic: {topic}",
+            data={"available": list(self._TOPICS.keys())},
+        )
+    
+    async def _show_overview(self, context: CommandContext) -> CommandResult:
+        # Show general help
+        ...
+    
+    async def _ask_model(
+        self,
+        args: list[str],
+        context: CommandContext,
+    ) -> CommandResult:
+        # Special handling for /help model "question"
+        if not args:
+            return CommandResult(
+                success=False,
+                message='Usage: /help model "your question"',
+            )
+        
+        question = " ".join(args)
+        # Load help docs, query model, return response
+        ...
+```
+
+## Command Discovery
+
+### Auto-Import Pattern
+Commands are discovered by importing all modules in `cato/commands/`:
+
+```python
+# cato/commands/__init__.py
+import importlib
+import pkgutil
+from pathlib import Path
+
+def discover_commands() -> None:
+    """
+    Import all command modules to trigger registration.
+    
+    Called once at startup after core is initialised.
+    """
+    package_dir = Path(__file__).parent
+    
+    for module_info in pkgutil.iter_modules([str(package_dir)]):
+        if not module_info.name.startswith("_"):
+            importlib.import_module(f"cato.commands.{module_info.name}")
+```
+
+### File Structure
+```
+cato/commands/
+├── __init__.py          # discover_commands()
+├── base.py              # Command protocol, decorator, registry
+├── core.py              # /help, /exit, /clear, /config
+├── history.py           # /history, /delete, /showsys
+├── files.py             # /attach, /pwd, /cd, /ls, /cat
+├── export.py            # /writecode, /writemd, /writejson
+├── vector.py            # /vadd, /vdoc, /vquery, /vstats
+├── productivity.py      # /st, /list, /timelog
+├── web.py               # /web, /url
+└── tts.py               # /speak, /speaklike
+```
+
+## Adding New Commands
+
+To add a new command:
+
+1. Create file in `cato/commands/` (or add to existing related file)
+2. Import decorator: `from cato.commands.base import command`
+3. Implement class with `@command` decorator
+4. Command is auto-discovered on next startup
+
+```python
+# cato/commands/mycommand.py
+from cato.commands.base import command, CommandContext, CommandResult
+
+@command(
+    "mycommand",
+    aliases=["mc"],
+    description="Do something useful",
+    usage="/mycommand <arg>",
+)
+class MyCommand:
+    """Implementation of mycommand."""
+    
+    @property
+    def name(self) -> str:
+        return "mycommand"
+    
+    @property
+    def aliases(self) -> list[str]:
+        return ["mc"]
+    
+    @property
+    def description(self) -> str:
+        return "Do something useful"
+    
+    @property
+    def usage(self) -> str:
+        return "/mycommand <arg>"
+    
+    async def execute(
+        self,
+        args: list[str],
+        context: CommandContext,
+    ) -> CommandResult:
+        if not args:
+            return CommandResult(
+                success=False,
+                message="Missing required argument",
+            )
+        
+        # Do the thing
+        result = await self._do_something(args[0], context)
+        
+        return CommandResult(
+            success=True,
+            message=f"Done: {result}",
+            data={"result": result},
+        )
+```
+
+## Error Handling
+
+Commands should:
+- Validate arguments before execution
+- Return `CommandResult(success=False, ...)` for user errors
+- Raise `CommandArgumentError` for invalid argument types
+- Let other exceptions propagate (caught by executor)
+
+```python
+async def execute(self, args: list[str], context: CommandContext) -> CommandResult:
+    # Validate required args
+    if len(args) < 1:
+        return CommandResult(
+            success=False,
+            message=f"Missing required argument. Usage: {self.usage}",
+        )
+    
+    # Validate argument types
+    try:
+        count = int(args[0])
+    except ValueError:
+        raise CommandArgumentError(
+            f"Expected integer, got: {args[0]}",
+            context={"argument": "count", "value": args[0]},
+        )
+    
+    # Execute - let other errors propagate
+    result = await context.storage.get_items(count)
+    return CommandResult(success=True, message="OK", data={"items": result})
+```

```



MarkAsCompleted: 1 items
Good progress. Creating the vector store spec now.


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_VECTOR_STORE.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_VECTOR_STORE.md
@@ -0,0 +1,716 @@
+# Vector Store Technical Specification
+
+## Overview
+Cato uses ChromaDB for persistent vector storage, enabling semantic search over conversation history and documents. The vector store is query-only at runtime—never load the full store into memory.
+
+## Vector Store Protocol
+
+### Interface Definition
+```python
+from typing import Protocol
+from dataclasses import dataclass
+
+@dataclass
+class VectorDocument:
+    """Document stored in vector store."""
+    id: str
+    content: str
+    metadata: dict
+    embedding: list[float] | None = None  # May not always be returned
+
+
+@dataclass
+class SearchResult:
+    """Result from similarity search."""
+    document: VectorDocument
+    score: float  # Distance/similarity score
+
+
+class VectorStore(Protocol):
+    """
+    Protocol for vector store implementations.
+    
+    All operations are async to support potential remote backends.
+    """
+    
+    async def add(
+        self,
+        documents: list[VectorDocument],
+    ) -> list[str]:
+        """
+        Add documents to the store.
+        
+        Parameters
+        ----------
+        documents
+            Documents to add (embeddings generated if not provided).
+        
+        Returns
+        -------
+        list[str]
+            IDs of added documents.
+        """
+        ...
+    
+    async def search(
+        self,
+        query: str,
+        n_results: int = 5,
+        filter: dict | None = None,
+    ) -> list[SearchResult]:
+        """
+        Search for similar documents.
+        
+        Parameters
+        ----------
+        query
+            Search query (will be embedded).
+        n_results
+            Maximum results to return.
+        filter
+            Metadata filter (ChromaDB where clause).
+        
+        Returns
+        -------
+        list[SearchResult]
+            Matching documents with scores.
+        """
+        ...
+    
+    async def get(
+        self,
+        ids: list[str],
+    ) -> list[VectorDocument]:
+        """
+        Retrieve documents by ID.
+        
+        Parameters
+        ----------
+        ids
+            Document IDs to retrieve.
+        
+        Returns
+        -------
+        list[VectorDocument]
+            Retrieved documents.
+        """
+        ...
+    
+    async def delete(
+        self,
+        ids: list[str],
+    ) -> None:
+        """
+        Delete documents by ID.
+        
+        Parameters
+        ----------
+        ids
+            Document IDs to delete.
+        """
+        ...
+    
+    async def count(self) -> int:
+        """Return total document count."""
+        ...
+```
+
+## ChromaDB Implementation
+
+### Setup and Initialisation
+```python
+import chromadb
+from chromadb.config import Settings
+
+class ChromaVectorStore:
+    """ChromaDB-backed vector store implementation."""
+    
+    def __init__(
+        self,
+        config: VectorStoreConfig,
+        embedding_provider: EmbeddingProvider,
+    ) -> None:
+        self._config = config
+        self._embedder = embedding_provider
+        
+        # Persistent client (disk-backed)
+        self._client = chromadb.PersistentClient(
+            path=str(config.path),
+            settings=Settings(
+                anonymized_telemetry=False,
+                allow_reset=False,
+            ),
+        )
+        
+        # Get or create collection
+        self._collection = self._client.get_or_create_collection(
+            name=config.collection_name,
+            metadata={"hnsw:space": "cosine"},  # Cosine similarity
+        )
+    
+    async def add(self, documents: list[VectorDocument]) -> list[str]:
+        """Add documents with embeddings."""
+        # Generate embeddings for documents without them
+        texts_to_embed = [
+            (i, doc.content)
+            for i, doc in enumerate(documents)
+            if doc.embedding is None
+        ]
+        
+        if texts_to_embed:
+            embeddings = await self._embedder.embed_batch(
+                [t[1] for t in texts_to_embed]
+            )
+            for (i, _), embedding in zip(texts_to_embed, embeddings):
+                documents[i].embedding = embedding
+        
+        # Add to ChromaDB
+        self._collection.add(
+            ids=[doc.id for doc in documents],
+            embeddings=[doc.embedding for doc in documents],
+            documents=[doc.content for doc in documents],
+            metadatas=[doc.metadata for doc in documents],
+        )
+        
+        return [doc.id for doc in documents]
+    
+    async def search(
+        self,
+        query: str,
+        n_results: int = 5,
+        filter: dict | None = None,
+    ) -> list[SearchResult]:
+        """Search by semantic similarity."""
+        # Embed query
+        query_embedding = await self._embedder.embed(query)
+        
+        # Query ChromaDB
+        results = self._collection.query(
+            query_embeddings=[query_embedding],
+            n_results=n_results,
+            where=filter,
+            include=["documents", "metadatas", "distances"],
+        )
+        
+        # Convert to SearchResult
+        search_results = []
+        for i in range(len(results["ids"][0])):
+            doc = VectorDocument(
+                id=results["ids"][0][i],
+                content=results["documents"][0][i],
+                metadata=results["metadatas"][0][i],
+            )
+            search_results.append(SearchResult(
+                document=doc,
+                score=results["distances"][0][i],
+            ))
+        
+        return search_results
+```
+
+## Embedding Provider
+
+### OpenAI Embeddings
+```python
+class OpenAIEmbeddingProvider:
+    """OpenAI API embeddings."""
+    
+    def __init__(self, config: EmbeddingConfig) -> None:
+        self._client = AsyncOpenAI(api_key=config.api_key)
+        self._model = config.model  # e.g., "text-embedding-3-small"
+    
+    async def embed(self, text: str) -> list[float]:
+        """
+        Generate embedding for single text.
+        
+        Parameters
+        ----------
+        text
+            Text to embed.
+        
+        Returns
+        -------
+        list[float]
+            Embedding vector.
+        """
+        response = await self._client.embeddings.create(
+            model=self._model,
+            input=text,
+        )
+        return response.data[0].embedding
+    
+    async def embed_batch(
+        self,
+        texts: list[str],
+        batch_size: int = 100,
+    ) -> list[list[float]]:
+        """
+        Generate embeddings for multiple texts.
+        
+        Parameters
+        ----------
+        texts
+            Texts to embed.
+        batch_size
+            Max texts per API call.
+        
+        Returns
+        -------
+        list[list[float]]
+            Embedding vectors in same order.
+        """
+        embeddings = []
+        
+        for i in range(0, len(texts), batch_size):
+            batch = texts[i:i + batch_size]
+            response = await self._client.embeddings.create(
+                model=self._model,
+                input=batch,
+            )
+            embeddings.extend([d.embedding for d in response.data])
+        
+        return embeddings
+```
+
+## Document Chunking
+
+### Text Splitter
+```python
+class TextChunker:
+    """
+    Split documents into chunks for embedding.
+    
+    Uses recursive character splitting with overlap.
+    """
+    
+    def __init__(
+        self,
+        chunk_size: int = 1000,
+        chunk_overlap: int = 200,
+        separators: list[str] | None = None,
+    ) -> None:
+        self._chunk_size = chunk_size
+        self._chunk_overlap = chunk_overlap
+        self._separators = separators or ["\n\n", "\n", ". ", " ", ""]
+    
+    def split(self, text: str) -> list[str]:
+        """
+        Split text into chunks.
+        
+        Parameters
+        ----------
+        text
+            Text to split.
+        
+        Returns
+        -------
+        list[str]
+            Text chunks with overlap.
+        """
+        return self._split_recursive(text, self._separators)
+    
+    def _split_recursive(
+        self,
+        text: str,
+        separators: list[str],
+    ) -> list[str]:
+        """Recursively split using separators in order."""
+        if not text:
+            return []
+        
+        # If text fits in chunk, return it
+        if len(text) <= self._chunk_size:
+            return [text]
+        
+        # Find separator to use
+        separator = separators[-1]  # Default to last (empty string)
+        for sep in separators:
+            if sep in text:
+                separator = sep
+                break
+        
+        # Split and merge
+        splits = text.split(separator) if separator else list(text)
+        return self._merge_splits(splits, separator, separators)
+    
+    def _merge_splits(
+        self,
+        splits: list[str],
+        separator: str,
+        separators: list[str],
+    ) -> list[str]:
+        """Merge splits into chunks with overlap."""
+        chunks = []
+        current_chunk = []
+        current_length = 0
+        
+        for split in splits:
+            split_length = len(split) + len(separator)
+            
+            if current_length + split_length > self._chunk_size and current_chunk:
+                # Save current chunk
+                chunk_text = separator.join(current_chunk)
+                chunks.append(chunk_text)
+                
+                # Start new chunk with overlap
+                overlap_length = 0
+                while current_chunk and overlap_length < self._chunk_overlap:
+                    overlap_length += len(current_chunk[-1]) + len(separator)
+                    if overlap_length > self._chunk_overlap:
+                        current_chunk.pop(0)
+                        break
+                    current_chunk.pop(0)
+                
+                current_length = sum(len(s) for s in current_chunk) + len(separator) * len(current_chunk)
+            
+            current_chunk.append(split)
+            current_length += split_length
+        
+        # Don't forget last chunk
+        if current_chunk:
+            chunks.append(separator.join(current_chunk))
+        
+        return chunks
+```
+
+### Document Processor
+```python
+class DocumentProcessor:
+    """Process documents for vector storage."""
+    
+    def __init__(
+        self,
+        chunker: TextChunker,
+        vector_store: VectorStore,
+    ) -> None:
+        self._chunker = chunker
+        self._store = vector_store
+    
+    async def add_document(
+        self,
+        content: str,
+        source: str,
+        metadata: dict | None = None,
+    ) -> list[str]:
+        """
+        Process and add a document to the vector store.
+        
+        Parameters
+        ----------
+        content
+            Document content.
+        source
+            Source identifier (filename, URL, etc.).
+        metadata
+            Additional metadata.
+        
+        Returns
+        -------
+        list[str]
+            IDs of created chunks.
+        """
+        # Split into chunks
+        chunks = self._chunker.split(content)
+        
+        # Create documents
+        base_metadata = metadata or {}
+        base_metadata["source"] = source
+        base_metadata["total_chunks"] = len(chunks)
+        
+        documents = [
+            VectorDocument(
+                id=f"{source}:{i}",
+                content=chunk,
+                metadata={
+                    **base_metadata,
+                    "chunk_index": i,
+                },
+            )
+            for i, chunk in enumerate(chunks)
+        ]
+        
+        # Add to store
+        return await self._store.add(documents)
+```
+
+## Exchange Storage
+
+### Conversation Exchange Format
+```python
+@dataclass
+class Exchange:
+    """A user/assistant exchange for storage."""
+    id: str
+    session_id: str
+    thread_id: str | None
+    user_message: str
+    assistant_message: str
+    timestamp: datetime
+    metadata: dict
+
+
+class ExchangeStore:
+    """Store conversation exchanges in vector store."""
+    
+    def __init__(self, vector_store: VectorStore) -> None:
+        self._store = vector_store
+    
+    async def add_exchange(self, exchange: Exchange) -> str:
+        """
+        Add a conversation exchange.
+        
+        Parameters
+        ----------
+        exchange
+            Exchange to store.
+        
+        Returns
+        -------
+        str
+            Exchange ID.
+        """
+        # Combine user and assistant messages for embedding
+        combined_content = (
+            f"User: {exchange.user_message}\n\n"
+            f"Assistant: {exchange.assistant_message}"
+        )
+        
+        doc = VectorDocument(
+            id=exchange.id,
+            content=combined_content,
+            metadata={
+                "type": "exchange",
+                "session_id": exchange.session_id,
+                "thread_id": exchange.thread_id or "",
+                "timestamp": exchange.timestamp.isoformat(),
+                "user_message": exchange.user_message[:500],  # Truncated for metadata
+                **exchange.metadata,
+            },
+        )
+        
+        await self._store.add([doc])
+        return exchange.id
+    
+    async def search_exchanges(
+        self,
+        query: str,
+        n_results: int = 5,
+        session_id: str | None = None,
+        thread_id: str | None = None,
+    ) -> list[SearchResult]:
+        """
+        Search exchanges by semantic similarity.
+        
+        Parameters
+        ----------
+        query
+            Search query.
+        n_results
+            Max results.
+        session_id
+            Filter to specific session.
+        thread_id
+            Filter to specific thread.
+        
+        Returns
+        -------
+        list[SearchResult]
+            Matching exchanges.
+        """
+        filter_clause = {"type": "exchange"}
+        if session_id:
+            filter_clause["session_id"] = session_id
+        if thread_id:
+            filter_clause["thread_id"] = thread_id
+        
+        return await self._store.search(
+            query=query,
+            n_results=n_results,
+            filter=filter_clause,
+        )
+```
+
+## Context Retrieval
+
+### Automatic Context
+```python
+class ContextRetriever:
+    """Retrieve relevant context for conversations."""
+    
+    def __init__(
+        self,
+        exchange_store: ExchangeStore,
+        config: VectorStoreConfig,
+    ) -> None:
+        self._store = exchange_store
+        self._config = config
+    
+    async def get_relevant_context(
+        self,
+        query: str,
+        max_results: int = 3,
+        max_tokens: int = 2000,
+        token_counter: Callable[[str], int] | None = None,
+    ) -> list[str]:
+        """
+        Retrieve context relevant to the query.
+        
+        Parameters
+        ----------
+        query
+            User's message/query.
+        max_results
+            Maximum context items.
+        max_tokens
+            Maximum total tokens in context.
+        token_counter
+            Function to count tokens.
+        
+        Returns
+        -------
+        list[str]
+            Relevant context excerpts.
+        """
+        results = await self._store.search_exchanges(
+            query=query,
+            n_results=max_results * 2,  # Get extra for filtering
+        )
+        
+        context = []
+        total_tokens = 0
+        counter = token_counter or (lambda x: len(x) // 4)  # Rough estimate
+        
+        for result in results:
+            content = result.document.content
+            tokens = counter(content)
+            
+            if total_tokens + tokens > max_tokens:
+                continue
+            
+            context.append(content)
+            total_tokens += tokens
+            
+            if len(context) >= max_results:
+                break
+        
+        return context
+```
+
+## Configuration
+
+### Vector Store Config
+```yaml
+vector_store:
+  enabled: true
+  backend: "chromadb"
+  path: "~/.local/share/cato/vectordb"
+  collection_name: "cato_memory"
+  
+  # Embedding settings
+  embedding_model: "text-embedding-3-small"
+  embedding_dimensions: 1536
+  
+  # Chunking settings
+  chunk_size: 1000
+  chunk_overlap: 200
+  
+  # Query settings
+  default_results: 5
+  max_results: 20
+  similarity_threshold: 0.7  # Minimum similarity score
+```
+
+## Initialisation
+
+### Bootstrap Integration
+```python
+def create_vector_store(config: CatoConfig) -> VectorStore | None:
+    """
+    Create vector store if enabled.
+    
+    Parameters
+    ----------
+    config
+        Application configuration.
+    
+    Returns
+    -------
+    VectorStore | None
+        Configured vector store or None if disabled.
+    """
+    if not config.vector_store.enabled:
+        logger.info("Vector store disabled in configuration")
+        return None
+    
+    try:
+        embedding_provider = OpenAIEmbeddingProvider(
+            EmbeddingConfig(
+                api_key=os.environ.get("OPENAI_API_KEY"),
+                model=config.vector_store.embedding_model,
+            )
+        )
+        
+        store = ChromaVectorStore(
+            config=config.vector_store,
+            embedding_provider=embedding_provider,
+        )
+        
+        logger.info(
+            f"Vector store initialised: {config.vector_store.path}, "
+            f"collection={config.vector_store.collection_name}"
+        )
+        return store
+        
+    except Exception as e:
+        logger.warning(f"Failed to initialise vector store: {e}")
+        return None  # Continue without vector store
+```
+
+## Performance Considerations
+
+### Memory Management
+- **Never load full store**: Always use queries with limits
+- **Batch embeddings**: Use batch API for multiple documents
+- **Lazy loading**: Don't initialise until first use if startup time critical
+
+### Query Optimisation
+```python
+# Use metadata filters to reduce search space
+results = await store.search(
+    query="python error handling",
+    n_results=5,
+    filter={
+        "type": "exchange",
+        "session_id": current_session,  # Limit to current session first
+    },
+)
+```
+
+### Caching
+```python
+from functools import lru_cache
+
+class CachedEmbeddingProvider:
+    """Embedding provider with caching for repeated queries."""
+    
+    def __init__(self, provider: EmbeddingProvider, max_cache: int = 1000) -> None:
+        self._provider = provider
+        self._cache: dict[str, list[float]] = {}
+        self._max_cache = max_cache
+    
+    async def embed(self, text: str) -> list[float]:
+        # Check cache
+        cache_key = text[:500]  # Truncate for key
+        if cache_key in self._cache:
+            return self._cache[cache_key]
+        
+        # Generate and cache
+        embedding = await self._provider.embed(text)
+        
+        if len(self._cache) >= self._max_cache:
+            # Simple eviction: remove oldest
+            self._cache.pop(next(iter(self._cache)))
+        
+        self._cache[cache_key] = embedding
+        return embedding
+```

```



MarkAsCompleted: 1 items
Two specs remaining. Creating the SQLite storage spec now.


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_STORAGE.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_STORAGE.md
@@ -0,0 +1,657 @@
+# Storage Technical Specification
+
+## Overview
+Cato uses SQLite for structured data storage (tasks, lists, time logs, memories). The database provides persistent storage for productivity features with a simple data access layer.
+
+## Database Location
+```
+~/.local/share/cato/cato.db
+```
+
+Configurable via `storage.database_path` in config.
+
+## Schema
+
+### Tasks Table
+```sql
+CREATE TABLE IF NOT EXISTS tasks (
+    id TEXT PRIMARY KEY,
+    title TEXT NOT NULL,
+    description TEXT,
+    status TEXT NOT NULL DEFAULT 'active',  -- active, in_progress, completed
+    priority TEXT DEFAULT 'medium',          -- low, medium, high
+    category TEXT,
+    due_date TEXT,                           -- ISO 8601 format
+    created_at TEXT NOT NULL,                -- ISO 8601 format
+    updated_at TEXT NOT NULL,                -- ISO 8601 format
+    completed_at TEXT,                       -- ISO 8601 format
+    metadata TEXT                            -- JSON for extensibility
+);
+
+CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
+CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
+CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
+CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
+```
+
+### Lists Table
+```sql
+CREATE TABLE IF NOT EXISTS lists (
+    id TEXT PRIMARY KEY,
+    name TEXT NOT NULL UNIQUE,
+    description TEXT,
+    created_at TEXT NOT NULL,
+    updated_at TEXT NOT NULL,
+    metadata TEXT
+);
+
+CREATE TABLE IF NOT EXISTS list_items (
+    id TEXT PRIMARY KEY,
+    list_id TEXT NOT NULL,
+    content TEXT NOT NULL,
+    checked INTEGER NOT NULL DEFAULT 0,
+    position INTEGER NOT NULL DEFAULT 0,
+    created_at TEXT NOT NULL,
+    updated_at TEXT NOT NULL,
+    metadata TEXT,
+    FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE
+);
+
+CREATE INDEX IF NOT EXISTS idx_list_items_list_id ON list_items(list_id);
+```
+
+### Time Logs Table
+```sql
+CREATE TABLE IF NOT EXISTS time_logs (
+    id TEXT PRIMARY KEY,
+    task_id TEXT,                            -- Optional link to task
+    description TEXT NOT NULL,
+    category TEXT,
+    start_time TEXT NOT NULL,                -- ISO 8601 format
+    end_time TEXT,                           -- ISO 8601 format (NULL if running)
+    duration_seconds INTEGER,                -- Computed on stop
+    created_at TEXT NOT NULL,
+    metadata TEXT,
+    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL
+);
+
+CREATE INDEX IF NOT EXISTS idx_time_logs_task_id ON time_logs(task_id);
+CREATE INDEX IF NOT EXISTS idx_time_logs_start_time ON time_logs(start_time);
+CREATE INDEX IF NOT EXISTS idx_time_logs_category ON time_logs(category);
+```
+
+### Memories Table
+```sql
+CREATE TABLE IF NOT EXISTS memories (
+    id TEXT PRIMARY KEY,
+    content TEXT NOT NULL,
+    category TEXT,
+    source TEXT,                             -- 'user', 'conversation', 'import'
+    importance INTEGER DEFAULT 1,            -- 1-5 scale
+    created_at TEXT NOT NULL,
+    last_accessed TEXT,
+    access_count INTEGER DEFAULT 0,
+    metadata TEXT
+);
+
+CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
+CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance);
+```
+
+### Sessions Table
+```sql
+CREATE TABLE IF NOT EXISTS sessions (
+    id TEXT PRIMARY KEY,
+    started_at TEXT NOT NULL,
+    ended_at TEXT,
+    message_count INTEGER DEFAULT 0,
+    metadata TEXT
+);
+
+CREATE TABLE IF NOT EXISTS threads (
+    id TEXT PRIMARY KEY,
+    session_id TEXT NOT NULL,
+    name TEXT,
+    created_at TEXT NOT NULL,
+    metadata TEXT,
+    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
+);
+```
+
+## Data Access Layer
+
+### Repository Protocol
+```python
+from typing import Protocol, TypeVar, Generic
+from dataclasses import dataclass
+
+T = TypeVar("T")
+
+class Repository(Protocol[T]):
+    """Generic repository protocol for CRUD operations."""
+    
+    async def get(self, id: str) -> T | None:
+        """Get entity by ID."""
+        ...
+    
+    async def get_all(self, **filters) -> list[T]:
+        """Get all entities, optionally filtered."""
+        ...
+    
+    async def create(self, entity: T) -> str:
+        """Create entity, return ID."""
+        ...
+    
+    async def update(self, entity: T) -> None:
+        """Update existing entity."""
+        ...
+    
+    async def delete(self, id: str) -> None:
+        """Delete entity by ID."""
+        ...
+```
+
+### Task Repository
+```python
+@dataclass
+class Task:
+    """Task entity."""
+    id: str
+    title: str
+    description: str | None
+    status: Literal["active", "in_progress", "completed"]
+    priority: Literal["low", "medium", "high"]
+    category: str | None
+    due_date: datetime | None
+    created_at: datetime
+    updated_at: datetime
+    completed_at: datetime | None
+    metadata: dict
+
+
+class TaskRepository:
+    """SQLite-backed task repository."""
+    
+    def __init__(self, db: Database) -> None:
+        self._db = db
+    
+    async def get(self, id: str) -> Task | None:
+        """
+        Get task by ID.
+        
+        Parameters
+        ----------
+        id
+            Task ID.
+        
+        Returns
+        -------
+        Task | None
+            Task if found.
+        """
+        row = await self._db.fetchone(
+            "SELECT * FROM tasks WHERE id = ?",
+            (id,),
+        )
+        return self._row_to_task(row) if row else None
+    
+    async def get_all(
+        self,
+        status: str | None = None,
+        category: str | None = None,
+        priority: str | None = None,
+        sort_by: str = "created_at",
+        order: str = "asc",
+    ) -> list[Task]:
+        """
+        Get tasks with optional filters.
+        
+        Parameters
+        ----------
+        status
+            Filter by status.
+        category
+            Filter by category.
+        priority
+            Filter by priority.
+        sort_by
+            Sort field.
+        order
+            Sort order (asc/desc).
+        
+        Returns
+        -------
+        list[Task]
+            Matching tasks.
+        """
+        query = "SELECT * FROM tasks WHERE 1=1"
+        params = []
+        
+        if status:
+            query += " AND status = ?"
+            params.append(status)
+        if category:
+            query += " AND category = ?"
+            params.append(category)
+        if priority:
+            query += " AND priority = ?"
+            params.append(priority)
+        
+        # Validate sort field to prevent SQL injection
+        valid_sorts = {"created_at", "updated_at", "priority", "due_date", "title"}
+        if sort_by not in valid_sorts:
+            sort_by = "created_at"
+        
+        order = "DESC" if order.lower() == "desc" else "ASC"
+        query += f" ORDER BY {sort_by} {order}"
+        
+        rows = await self._db.fetchall(query, tuple(params))
+        return [self._row_to_task(row) for row in rows]
+    
+    async def create(self, task: Task) -> str:
+        """Create new task."""
+        await self._db.execute(
+            """
+            INSERT INTO tasks (
+                id, title, description, status, priority, category,
+                due_date, created_at, updated_at, completed_at, metadata
+            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
+            """,
+            (
+                task.id,
+                task.title,
+                task.description,
+                task.status,
+                task.priority,
+                task.category,
+                task.due_date.isoformat() if task.due_date else None,
+                task.created_at.isoformat(),
+                task.updated_at.isoformat(),
+                task.completed_at.isoformat() if task.completed_at else None,
+                json.dumps(task.metadata) if task.metadata else None,
+            ),
+        )
+        return task.id
+    
+    async def update(self, task: Task) -> None:
+        """Update existing task."""
+        task.updated_at = datetime.now()
+        await self._db.execute(
+            """
+            UPDATE tasks SET
+                title = ?, description = ?, status = ?, priority = ?,
+                category = ?, due_date = ?, updated_at = ?,
+                completed_at = ?, metadata = ?
+            WHERE id = ?
+            """,
+            (
+                task.title,
+                task.description,
+                task.status,
+                task.priority,
+                task.category,
+                task.due_date.isoformat() if task.due_date else None,
+                task.updated_at.isoformat(),
+                task.completed_at.isoformat() if task.completed_at else None,
+                json.dumps(task.metadata) if task.metadata else None,
+                task.id,
+            ),
+        )
+    
+    async def delete(self, id: str) -> None:
+        """Delete task by ID."""
+        await self._db.execute("DELETE FROM tasks WHERE id = ?", (id,))
+    
+    def _row_to_task(self, row: dict) -> Task:
+        """Convert database row to Task entity."""
+        return Task(
+            id=row["id"],
+            title=row["title"],
+            description=row["description"],
+            status=row["status"],
+            priority=row["priority"],
+            category=row["category"],
+            due_date=datetime.fromisoformat(row["due_date"]) if row["due_date"] else None,
+            created_at=datetime.fromisoformat(row["created_at"]),
+            updated_at=datetime.fromisoformat(row["updated_at"]),
+            completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
+            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
+        )
+```
+
+### Database Connection
+```python
+import aiosqlite
+from pathlib import Path
+
+class Database:
+    """Async SQLite database wrapper."""
+    
+    def __init__(self, path: Path) -> None:
+        self._path = path
+        self._conn: aiosqlite.Connection | None = None
+    
+    async def connect(self) -> None:
+        """Open database connection and initialise schema."""
+        # Ensure directory exists
+        self._path.parent.mkdir(parents=True, exist_ok=True)
+        
+        self._conn = await aiosqlite.connect(self._path)
+        self._conn.row_factory = aiosqlite.Row
+        
+        # Enable foreign keys
+        await self._conn.execute("PRAGMA foreign_keys = ON")
+        
+        # Run migrations
+        await self._run_migrations()
+    
+    async def close(self) -> None:
+        """Close database connection."""
+        if self._conn:
+            await self._conn.close()
+            self._conn = None
+    
+    async def execute(self, query: str, params: tuple = ()) -> None:
+        """Execute a write query."""
+        async with self._conn.execute(query, params):
+            await self._conn.commit()
+    
+    async def fetchone(self, query: str, params: tuple = ()) -> dict | None:
+        """Fetch single row."""
+        async with self._conn.execute(query, params) as cursor:
+            row = await cursor.fetchone()
+            return dict(row) if row else None
+    
+    async def fetchall(self, query: str, params: tuple = ()) -> list[dict]:
+        """Fetch all rows."""
+        async with self._conn.execute(query, params) as cursor:
+            rows = await cursor.fetchall()
+            return [dict(row) for row in rows]
+    
+    async def _run_migrations(self) -> None:
+        """Apply database migrations."""
+        # Create migrations table if not exists
+        await self._conn.execute("""
+            CREATE TABLE IF NOT EXISTS migrations (
+                id INTEGER PRIMARY KEY,
+                name TEXT NOT NULL UNIQUE,
+                applied_at TEXT NOT NULL
+            )
+        """)
+        await self._conn.commit()
+        
+        # Get applied migrations
+        cursor = await self._conn.execute("SELECT name FROM migrations")
+        applied = {row[0] for row in await cursor.fetchall()}
+        
+        # Apply pending migrations
+        for migration in MIGRATIONS:
+            if migration.name not in applied:
+                await migration.apply(self._conn)
+                await self._conn.execute(
+                    "INSERT INTO migrations (name, applied_at) VALUES (?, ?)",
+                    (migration.name, datetime.now().isoformat()),
+                )
+                await self._conn.commit()
+                logger.info(f"Applied migration: {migration.name}")
+```
+
+## Migrations
+
+### Migration Definition
+```python
+@dataclass
+class Migration:
+    """Database migration."""
+    name: str
+    sql: str
+    
+    async def apply(self, conn: aiosqlite.Connection) -> None:
+        """Apply migration."""
+        await conn.executescript(self.sql)
+
+
+# Ordered list of migrations
+MIGRATIONS = [
+    Migration(
+        name="001_initial_schema",
+        sql="""
+        CREATE TABLE IF NOT EXISTS tasks (
+            id TEXT PRIMARY KEY,
+            title TEXT NOT NULL,
+            description TEXT,
+            status TEXT NOT NULL DEFAULT 'active',
+            priority TEXT DEFAULT 'medium',
+            category TEXT,
+            due_date TEXT,
+            created_at TEXT NOT NULL,
+            updated_at TEXT NOT NULL,
+            completed_at TEXT,
+            metadata TEXT
+        );
+        
+        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
+        CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
+        
+        CREATE TABLE IF NOT EXISTS lists (
+            id TEXT PRIMARY KEY,
+            name TEXT NOT NULL UNIQUE,
+            description TEXT,
+            created_at TEXT NOT NULL,
+            updated_at TEXT NOT NULL,
+            metadata TEXT
+        );
+        
+        CREATE TABLE IF NOT EXISTS list_items (
+            id TEXT PRIMARY KEY,
+            list_id TEXT NOT NULL,
+            content TEXT NOT NULL,
+            checked INTEGER NOT NULL DEFAULT 0,
+            position INTEGER NOT NULL DEFAULT 0,
+            created_at TEXT NOT NULL,
+            updated_at TEXT NOT NULL,
+            metadata TEXT,
+            FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE
+        );
+        
+        CREATE INDEX IF NOT EXISTS idx_list_items_list_id ON list_items(list_id);
+        """,
+    ),
+    Migration(
+        name="002_time_logs",
+        sql="""
+        CREATE TABLE IF NOT EXISTS time_logs (
+            id TEXT PRIMARY KEY,
+            task_id TEXT,
+            description TEXT NOT NULL,
+            category TEXT,
+            start_time TEXT NOT NULL,
+            end_time TEXT,
+            duration_seconds INTEGER,
+            created_at TEXT NOT NULL,
+            metadata TEXT,
+            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL
+        );
+        
+        CREATE INDEX IF NOT EXISTS idx_time_logs_task_id ON time_logs(task_id);
+        CREATE INDEX IF NOT EXISTS idx_time_logs_start_time ON time_logs(start_time);
+        """,
+    ),
+    Migration(
+        name="003_memories",
+        sql="""
+        CREATE TABLE IF NOT EXISTS memories (
+            id TEXT PRIMARY KEY,
+            content TEXT NOT NULL,
+            category TEXT,
+            source TEXT,
+            importance INTEGER DEFAULT 1,
+            created_at TEXT NOT NULL,
+            last_accessed TEXT,
+            access_count INTEGER DEFAULT 0,
+            metadata TEXT
+        );
+        
+        CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
+        """,
+    ),
+    Migration(
+        name="004_sessions",
+        sql="""
+        CREATE TABLE IF NOT EXISTS sessions (
+            id TEXT PRIMARY KEY,
+            started_at TEXT NOT NULL,
+            ended_at TEXT,
+            message_count INTEGER DEFAULT 0,
+            metadata TEXT
+        );
+        
+        CREATE TABLE IF NOT EXISTS threads (
+            id TEXT PRIMARY KEY,
+            session_id TEXT NOT NULL,
+            name TEXT,
+            created_at TEXT NOT NULL,
+            metadata TEXT,
+            FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
+        );
+        """,
+    ),
+]
+```
+
+## Storage Service
+
+### Unified Access
+```python
+class Storage:
+    """
+    Unified storage service.
+    
+    Provides access to all repositories through a single interface.
+    """
+    
+    def __init__(self, db: Database) -> None:
+        self._db = db
+        self.tasks = TaskRepository(db)
+        self.lists = ListRepository(db)
+        self.time_logs = TimeLogRepository(db)
+        self.memories = MemoryRepository(db)
+        self.sessions = SessionRepository(db)
+    
+    async def connect(self) -> None:
+        """Connect to database."""
+        await self._db.connect()
+    
+    async def close(self) -> None:
+        """Close database connection."""
+        await self._db.close()
+
+
+# Usage in bootstrap
+async def create_storage(config: CatoConfig) -> Storage:
+    """
+    Create and connect storage service.
+    
+    Parameters
+    ----------
+    config
+        Application configuration.
+    
+    Returns
+    -------
+    Storage
+        Connected storage service.
+    """
+    db = Database(expand_path(config.storage.database_path))
+    storage = Storage(db)
+    await storage.connect()
+    return storage
+```
+
+## Backup
+
+### Automatic Backup
+```python
+import shutil
+from datetime import datetime
+
+class BackupManager:
+    """Manage database backups."""
+    
+    def __init__(self, config: StorageConfig) -> None:
+        self._config = config
+        self._db_path = expand_path(config.database_path)
+        self._backup_dir = self._db_path.parent / "backups"
+    
+    async def create_backup(self) -> Path:
+        """
+        Create database backup.
+        
+        Returns
+        -------
+        Path
+            Path to backup file.
+        """
+        self._backup_dir.mkdir(exist_ok=True)
+        
+        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
+        backup_path = self._backup_dir / f"cato_{timestamp}.db"
+        
+        # Copy database file
+        shutil.copy2(self._db_path, backup_path)
+        
+        # Clean old backups (keep last 7)
+        self._cleanup_old_backups(keep=7)
+        
+        logger.info(f"Database backed up to: {backup_path}")
+        return backup_path
+    
+    def _cleanup_old_backups(self, keep: int) -> None:
+        """Remove old backups, keeping the most recent."""
+        backups = sorted(
+            self._backup_dir.glob("cato_*.db"),
+            key=lambda p: p.stat().st_mtime,
+            reverse=True,
+        )
+        
+        for backup in backups[keep:]:
+            backup.unlink()
+            logger.debug(f"Removed old backup: {backup}")
+```
+
+## Configuration
+
+### Storage Config
+```yaml
+storage:
+  database_path: "~/.local/share/cato/cato.db"
+  backup_enabled: true
+  backup_frequency_hours: 24
+```
+
+## ID Generation
+```python
+import uuid
+from datetime import datetime
+
+def generate_id(prefix: str = "") -> str:
+    """
+    Generate unique ID.
+    
+    Parameters
+    ----------
+    prefix
+        Optional prefix for ID.
+    
+    Returns
+    -------
+    str
+        Unique ID string.
+    """
+    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
+    unique = uuid.uuid4().hex[:8]
+    
+    if prefix:
+        return f"{prefix}_{timestamp}_{unique}"
+    return f"{timestamp}_{unique}"
+```

```



MarkAsCompleted: 1 items
Final spec remaining - the display system.


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DISPLAY.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DISPLAY.md
@@ -0,0 +1,659 @@
+# Display Technical Specification
+
+## Overview
+Cato uses Rich for formatted output and prompt_toolkit for input handling. The display layer is abstracted through a protocol to enable alternative frontends while maintaining terminal-first design.
+
+## Display Protocol
+
+### Interface Definition
+```python
+from typing import Protocol
+from dataclasses import dataclass
+
+@dataclass
+class Message:
+    """Display message."""
+    role: Literal["user", "assistant", "system", "error", "info"]
+    content: str
+    timestamp: datetime | None = None
+
+
+class Display(Protocol):
+    """
+    Protocol for display implementations.
+    
+    Abstracts terminal output to enable pluggable frontends.
+    """
+    
+    def show_message(self, message: Message) -> None:
+        """
+        Display a message.
+        
+        Parameters
+        ----------
+        message
+            Message to display.
+        """
+        ...
+    
+    def show_error(self, error: str, details: str | None = None) -> None:
+        """
+        Display an error message.
+        
+        Parameters
+        ----------
+        error
+            Error message.
+        details
+            Optional additional details.
+        """
+        ...
+    
+    def show_warning(self, warning: str) -> None:
+        """Display a warning message."""
+        ...
+    
+    def show_info(self, info: str) -> None:
+        """Display an informational message."""
+        ...
+    
+    def show_markdown(self, content: str) -> None:
+        """
+        Display markdown-formatted content.
+        
+        Parameters
+        ----------
+        content
+            Markdown text.
+        """
+        ...
+    
+    def show_code(self, code: str, language: str | None = None) -> None:
+        """
+        Display syntax-highlighted code.
+        
+        Parameters
+        ----------
+        code
+            Code to display.
+        language
+            Language for syntax highlighting.
+        """
+        ...
+    
+    def show_table(
+        self,
+        headers: list[str],
+        rows: list[list[str]],
+        title: str | None = None,
+    ) -> None:
+        """
+        Display a table.
+        
+        Parameters
+        ----------
+        headers
+            Column headers.
+        rows
+            Table rows.
+        title
+            Optional table title.
+        """
+        ...
+    
+    def show_spinner(self, message: str) -> SpinnerContext:
+        """
+        Show a loading spinner.
+        
+        Parameters
+        ----------
+        message
+            Message to show while loading.
+        
+        Returns
+        -------
+        SpinnerContext
+            Context manager that stops spinner on exit.
+        """
+        ...
+    
+    def clear(self) -> None:
+        """Clear the terminal screen."""
+        ...
+    
+    def show_welcome(self) -> None:
+        """Display welcome message."""
+        ...
+```
+
+## Rich Implementation
+
+### Console Setup
+```python
+from rich.console import Console
+from rich.theme import Theme
+from rich.markdown import Markdown
+from rich.syntax import Syntax
+from rich.table import Table
+from rich.panel import Panel
+from rich.spinner import Spinner
+from rich.live import Live
+
+class RichDisplay:
+    """Rich-based terminal display implementation."""
+    
+    def __init__(self, config: DisplayConfig) -> None:
+        self._config = config
+        
+        # Load theme
+        theme = self._load_theme(config.theme)
+        
+        # Create console
+        self._console = Console(
+            theme=theme,
+            width=config.max_width,
+            force_terminal=True,
+        )
+    
+    def _load_theme(self, theme_name: str) -> Theme:
+        """Load theme from config or built-in."""
+        # Built-in themes
+        themes = {
+            "default": Theme({
+                "user": "bold cyan",
+                "assistant": "bold green",
+                "system": "dim",
+                "error": "bold red",
+                "warning": "bold yellow",
+                "info": "bold blue",
+                "code": "on grey23",
+            }),
+            "gruvbox-dark": Theme({
+                "user": "bold #83a598",      # Blue
+                "assistant": "bold #b8bb26", # Green
+                "system": "#928374",         # Grey
+                "error": "bold #fb4934",     # Red
+                "warning": "bold #fabd2f",   # Yellow
+                "info": "bold #8ec07c",      # Aqua
+                "code": "on #3c3836",        # Dark bg
+            }),
+        }
+        
+        if theme_name in themes:
+            return themes[theme_name]
+        
+        # Try to load custom theme from file
+        custom_path = Path(f"~/.config/cato/themes/{theme_name}.yaml").expanduser()
+        if custom_path.exists():
+            return self._load_custom_theme(custom_path)
+        
+        return themes["default"]
+    
+    def show_message(self, message: Message) -> None:
+        """Display a message with role-based styling."""
+        prefix = self._get_prefix(message.role)
+        style = message.role
+        
+        if self._config.timestamps and message.timestamp:
+            timestamp = message.timestamp.strftime("%H:%M")
+            prefix = f"[dim]{timestamp}[/dim] {prefix}"
+        
+        if message.role == "assistant" and self._config.markdown_enabled:
+            self._console.print(prefix, style=style)
+            self._console.print(Markdown(message.content))
+        else:
+            self._console.print(f"{prefix} {message.content}", style=style)
+    
+    def _get_prefix(self, role: str) -> str:
+        """Get display prefix for role."""
+        prefixes = {
+            "user": "You:",
+            "assistant": "Cato:",
+            "system": "System:",
+            "error": "❌",
+            "warning": "⚠️",
+            "info": "ℹ️",
+        }
+        return prefixes.get(role, "")
+    
+    def show_error(self, error: str, details: str | None = None) -> None:
+        """Display an error message."""
+        self._console.print(f"❌ {error}", style="error")
+        if details:
+            self._console.print(f"   {details}", style="dim")
+    
+    def show_warning(self, warning: str) -> None:
+        """Display a warning."""
+        self._console.print(f"⚠️  {warning}", style="warning")
+    
+    def show_info(self, info: str) -> None:
+        """Display info message."""
+        self._console.print(f"ℹ️  {info}", style="info")
+    
+    def show_markdown(self, content: str) -> None:
+        """Render and display markdown."""
+        md = Markdown(content, code_theme=self._config.code_theme)
+        self._console.print(md)
+    
+    def show_code(self, code: str, language: str | None = None) -> None:
+        """Display syntax-highlighted code."""
+        syntax = Syntax(
+            code,
+            language or "text",
+            theme=self._config.code_theme,
+            line_numbers=True,
+            word_wrap=True,
+        )
+        self._console.print(syntax)
+    
+    def show_table(
+        self,
+        headers: list[str],
+        rows: list[list[str]],
+        title: str | None = None,
+    ) -> None:
+        """Display a formatted table."""
+        table = Table(title=title, show_header=True, header_style="bold")
+        
+        for header in headers:
+            table.add_column(header)
+        
+        for row in rows:
+            table.add_row(*row)
+        
+        self._console.print(table)
+    
+    def show_spinner(self, message: str) -> "SpinnerContext":
+        """Create spinner context manager."""
+        return SpinnerContext(self._console, message, self._config.spinner_style)
+    
+    def clear(self) -> None:
+        """Clear terminal."""
+        self._console.clear()
+    
+    def show_welcome(self) -> None:
+        """Display welcome banner."""
+        panel = Panel(
+            "[bold]Cato[/bold] - Chat at the Terminal Orchestrator\n"
+            "Type [cyan]/help[/cyan] for commands, [cyan]/exit[/cyan] to quit",
+            title="Welcome",
+            border_style="dim",
+        )
+        self._console.print(panel)
+```
+
+### Spinner Context
+```python
+from contextlib import contextmanager
+
+class SpinnerContext:
+    """Context manager for loading spinner."""
+    
+    def __init__(self, console: Console, message: str, style: str) -> None:
+        self._console = console
+        self._message = message
+        self._style = style
+        self._live: Live | None = None
+    
+    def __enter__(self) -> "SpinnerContext":
+        spinner = Spinner(self._style, text=self._message)
+        self._live = Live(spinner, console=self._console, refresh_per_second=10)
+        self._live.__enter__()
+        return self
+    
+    def __exit__(self, *args) -> None:
+        if self._live:
+            self._live.__exit__(*args)
+    
+    def update(self, message: str) -> None:
+        """Update spinner message."""
+        if self._live:
+            self._live.update(Spinner(self._style, text=message))
+
+
+# Usage
+async def send_message(self, content: str) -> str:
+    with self._display.show_spinner("Thinking..."):
+        response = await self._llm.complete(messages)
+    return response.content
+```
+
+## Input Handling
+
+### Prompt Toolkit Setup
+```python
+from prompt_toolkit import PromptSession
+from prompt_toolkit.history import FileHistory
+from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
+from prompt_toolkit.styles import Style
+from prompt_toolkit.key_binding import KeyBindings
+
+class InputHandler:
+    """Handle user input with prompt_toolkit."""
+    
+    def __init__(self, config: DisplayConfig, history_path: Path) -> None:
+        self._config = config
+        
+        # Custom key bindings
+        bindings = KeyBindings()
+        
+        @bindings.add("c-c")
+        def _(event):
+            """Handle Ctrl+C gracefully."""
+            event.app.exit(result=None)
+        
+        @bindings.add("c-d")
+        def _(event):
+            """Handle Ctrl+D for exit."""
+            raise EOFError()
+        
+        # Create session
+        self._session = PromptSession(
+            history=FileHistory(str(history_path)),
+            auto_suggest=AutoSuggestFromHistory(),
+            key_bindings=bindings,
+            style=self._get_style(),
+            multiline=False,
+            enable_history_search=True,
+        )
+    
+    def _get_style(self) -> Style:
+        """Get prompt style based on theme."""
+        if self._config.theme == "gruvbox-dark":
+            return Style.from_dict({
+                "prompt": "#83a598 bold",
+                "": "#ebdbb2",
+            })
+        return Style.from_dict({
+            "prompt": "cyan bold",
+            "": "",
+        })
+    
+    async def get_input(self, prompt: str = "> ") -> str | None:
+        """
+        Get user input.
+        
+        Parameters
+        ----------
+        prompt
+            Prompt string.
+        
+        Returns
+        -------
+        str | None
+            User input or None if cancelled.
+        """
+        try:
+            return await self._session.prompt_async(prompt)
+        except (EOFError, KeyboardInterrupt):
+            return None
+    
+    async def get_multiline_input(self, prompt: str = ">>> ") -> str | None:
+        """
+        Get multiline input (ends with blank line).
+        
+        Parameters
+        ----------
+        prompt
+            Prompt string.
+        
+        Returns
+        -------
+        str | None
+            Combined input or None if cancelled.
+        """
+        lines = []
+        continuation = "... "
+        
+        try:
+            while True:
+                p = prompt if not lines else continuation
+                line = await self._session.prompt_async(p)
+                
+                if not line and lines:
+                    break
+                lines.append(line)
+            
+            return "\n".join(lines)
+        except (EOFError, KeyboardInterrupt):
+            return None
+```
+
+## Theming
+
+### Theme Configuration
+```yaml
+display:
+  theme: "gruvbox-dark"
+  markdown_enabled: true
+  code_theme: "monokai"
+  max_width: null       # null = terminal width
+  timestamps: false
+  spinner_style: "dots"
+```
+
+### Custom Theme File
+```yaml
+# ~/.config/cato/themes/custom.yaml
+colors:
+  user: "#61afef"
+  assistant: "#98c379"
+  system: "#5c6370"
+  error: "#e06c75"
+  warning: "#e5c07b"
+  info: "#56b6c2"
+  code_background: "#282c34"
+```
+
+### Theme Loading
+```python
+def _load_custom_theme(self, path: Path) -> Theme:
+    """Load theme from YAML file."""
+    with open(path) as f:
+        data = yaml.safe_load(f)
+    
+    colors = data.get("colors", {})
+    return Theme({
+        "user": f"bold {colors.get('user', 'cyan')}",
+        "assistant": f"bold {colors.get('assistant', 'green')}",
+        "system": colors.get("system", "dim"),
+        "error": f"bold {colors.get('error', 'red')}",
+        "warning": f"bold {colors.get('warning', 'yellow')}",
+        "info": f"bold {colors.get('info', 'blue')}",
+        "code": f"on {colors.get('code_background', 'grey23')}",
+    })
+```
+
+## Context Display
+
+### Retrieved Context
+```python
+class ContextDisplay:
+    """Display retrieved context from vector store."""
+    
+    def __init__(self, display: Display) -> None:
+        self._display = display
+    
+    def show_context(
+        self,
+        context_items: list[str],
+        scores: list[float] | None = None,
+    ) -> None:
+        """
+        Display context excerpts.
+        
+        Parameters
+        ----------
+        context_items
+            Retrieved context strings.
+        scores
+            Optional similarity scores.
+        """
+        self._display.show_info(f"Found {len(context_items)} relevant context items:")
+        
+        for i, item in enumerate(context_items):
+            score_str = f" (score: {scores[i]:.2f})" if scores else ""
+            
+            # Truncate long items
+            preview = item[:200] + "..." if len(item) > 200 else item
+            preview = preview.replace("\n", " ")
+            
+            self._display.show_info(f"  [{i+1}]{score_str} {preview}")
+```
+
+## Output Formatting
+
+### Response Formatter
+```python
+class ResponseFormatter:
+    """Format assistant responses for display."""
+    
+    def __init__(self, config: DisplayConfig) -> None:
+        self._config = config
+    
+    def format(self, content: str) -> str:
+        """
+        Format response content.
+        
+        Parameters
+        ----------
+        content
+            Raw response content.
+        
+        Returns
+        -------
+        str
+            Formatted content.
+        """
+        if not self._config.markdown_enabled:
+            return self._strip_markdown(content)
+        return content
+    
+    def _strip_markdown(self, content: str) -> str:
+        """Remove markdown formatting for plain text display."""
+        # Basic markdown stripping
+        import re
+        
+        # Remove code blocks (keep content)
+        content = re.sub(r"```\w*\n?", "", content)
+        
+        # Remove inline code backticks
+        content = re.sub(r"`([^`]+)`", r"\1", content)
+        
+        # Remove bold/italic
+        content = re.sub(r"\*\*([^*]+)\*\*", r"\1", content)
+        content = re.sub(r"\*([^*]+)\*", r"\1", content)
+        content = re.sub(r"__([^_]+)__", r"\1", content)
+        content = re.sub(r"_([^_]+)_", r"\1", content)
+        
+        # Remove headers
+        content = re.sub(r"^#+\s+", "", content, flags=re.MULTILINE)
+        
+        return content
+```
+
+## Progress Display
+
+### Progress Bar
+```python
+from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
+
+class ProgressDisplay:
+    """Display progress for long operations."""
+    
+    def __init__(self, console: Console) -> None:
+        self._console = console
+    
+    @contextmanager
+    def progress(self, description: str, total: int | None = None):
+        """
+        Create progress context.
+        
+        Parameters
+        ----------
+        description
+            Progress description.
+        total
+            Total items (None for indeterminate).
+        """
+        if total:
+            with Progress(
+                SpinnerColumn(),
+                TextColumn("[progress.description]{task.description}"),
+                BarColumn(),
+                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
+                console=self._console,
+            ) as progress:
+                task = progress.add_task(description, total=total)
+                yield lambda n=1: progress.update(task, advance=n)
+        else:
+            with Progress(
+                SpinnerColumn(),
+                TextColumn("[progress.description]{task.description}"),
+                console=self._console,
+            ) as progress:
+                progress.add_task(description, total=None)
+                yield lambda: None
+
+
+# Usage
+with display.progress("Processing documents", total=len(files)) as advance:
+    for file in files:
+        process(file)
+        advance()
+```
+
+## Configuration
+
+### Display Config
+```python
+class DisplayConfig(BaseModel):
+    """Display configuration."""
+    
+    theme: str = "default"
+    markdown_enabled: bool = True
+    code_theme: str = "monokai"
+    max_width: int | None = Field(ge=40, default=None)
+    timestamps: bool = False
+    spinner_style: str = "dots"  # dots, line, moon, etc.
+```
+
+## Integration
+
+### Bootstrap
+```python
+def create_display(config: CatoConfig) -> Display:
+    """
+    Create display instance.
+    
+    Parameters
+    ----------
+    config
+        Application configuration.
+    
+    Returns
+    -------
+    Display
+        Configured display instance.
+    """
+    return RichDisplay(config.display)
+
+
+def create_input_handler(config: CatoConfig) -> InputHandler:
+    """
+    Create input handler.
+    
+    Parameters
+    ----------
+    config
+        Application configuration.
+    
+    Returns
+    -------
+    InputHandler
+        Configured input handler.
+    """
+    history_path = expand_path(config.commands.history_file)
+    history_path.parent.mkdir(parents=True, exist_ok=True)
+    return InputHandler(config.display, history_path)
+```

```



MarkAsCompleted: 1 items
All technical specs complete. Here's a summary of what was created:

**Technical Specifications Created:**

1. **TECH_CONFIG_SYSTEM.md** - YAML configuration with overlay system, Pydantic validation, environment variable overrides, and CLI precedence

2. **TECH_ERROR_HANDLING.md** (expanded) - Complete exception hierarchy with `CatoError` base class, logging setup with rotating file handlers, debug/warn modes

3. **TECH_LLM_INTEGRATION.md** - Provider protocol with OpenAI, Anthropic, Google, and Ollama implementations, message normalisation, retry logic, provider factory

4. **TECH_COMMAND_FRAMEWORK.md** - Decorator-based command registration, `CommandRegistry`, argument parsing with shlex, auto-discovery pattern

5. **TECH_VECTOR_STORE.md** - ChromaDB integration, OpenAI embeddings, text chunking with overlap, exchange storage, context retrieval

6. **TECH_STORAGE.md** - SQLite schema for tasks/lists/time logs/memories, repository pattern, migration system, backup manager

7. **TECH_DISPLAY.md** - Rich console with theming (including gruvbox-dark), prompt_toolkit input handling, spinner contexts, progress bars

All specs follow consistent patterns: protocol-based abstractions, numpy-format docstrings, type hints, and clear extension points. The architecture is now fully documented and ready for implementation.

USER:
in terms of build, install and deploy. Ocat used poetry. Do you suggest poetry, or something else like uv

AGENT:
Given your preference for uv (from your rules) and the current Python packaging landscape, I'd recommend **uv** over Poetry for Cato.

**Why uv:**

1. **Speed** - Dramatically faster dependency resolution and installs (10-100x faster than pip/Poetry)
2. **Modern standards** - Uses `pyproject.toml` with standard PEP 621 metadata (not Poetry's custom format)
3. **Simpler** - Single tool for venv management, dependency resolution, and package installation
4. **Active development** - Rapid improvements from Astral (same team behind Ruff)
5. **Better lockfile** - `uv.lock` is cross-platform and deterministic

**Poetry downsides:**

- Custom `pyproject.toml` format (non-standard `[tool.poetry]` section)
- Slower dependency resolution
- Heavier toolchain
- Less momentum in 2025/2026

**Suggested setup:**

```toml
# pyproject.toml
[project]
name = "cato"
version = "0.1.0"
description = "Chat at the Terminal Orchestrator"
requires-python = ">=3.11"
dependencies = [
    "rich>=13.0",
    "prompt-toolkit>=3.0",
    "pyyaml>=6.0",
    "pydantic>=2.0",
    "chromadb>=0.4",
    "openai>=1.0",
    "anthropic>=0.18",
    "httpx>=0.27",
    "aiosqlite>=0.19",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "ruff>=0.3",
    "mypy>=1.8",
]

[project.scripts]
cato = "cato.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```
**Workflow:**
```bash
uv venv
uv pip install -e ".[dev]"
uv pip compile pyproject.toml -o requirements.lock  # optional lockfile
```
This aligns with your existing conda workflow (uv can work alongside conda) and follows the MVP principle—simpler tooling, fewer moving parts.

USER:
ok, we'll use uv. Please document in the appropriate places

AGENT:


**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md**
```
# Development, Testing and Release Technical Specification

## Overview
This document defines the development workflow, testing strategy, continuous integration, and release process for Cato.

## Development Philosophy

### Single User, Local First
- Cato is developed for a single user on a single machine
- No multi-user deployment considerations
- Local development and testing is the primary workflow
- CI exists to catch regressions, not for complex deployment pipelines

### Minimal Ceremony
- Lightweight processes that don't impede rapid iteration
- Testing focused on core functionality, not exhaustive coverage
- Releases when meaningful changes accumulate, not on fixed schedules

## Branch Strategy

### Main Branch
- `main` is the stable branch
- All development work happens on feature branches
- Direct commits to `main` are prohibited

### Feature Branches
- Create a new branch for each feature or bug fix
- Branch naming: `feature/<short-description>` or `fix/<short-description>`
- Keep branches short-lived where possible
- Merge to `main` via pull request (or direct merge for solo development)

```bash
# Starting new work
git checkout main
git pull
git checkout -b feature/add-anthropic-provider

# After completion
git checkout main
git merge feature/add-anthropic-provider
git branch -d feature/add-anthropic-provider
```

## Testing Strategy

### Test Pyramid
```
        /\
       /  \     E2E Tests (few)
      /----\    - Full REPL interactions
     /      \   - Critical user journeys
    /--------\  Integration Tests (moderate)
   /          \ - Service + storage
  /------------\- Command + service
 /              \
/----------------\  Unit Tests (many)
                    - Individual functions
                    - Config validation
                    - Protocol implementations
```

### Unit Tests
**Scope**: Individual functions, classes, and methods in isolation

**What to test**:
- Configuration loading and validation
- Command argument parsing
- Message formatting
- Utility functions
- Protocol implementations with mocked dependencies

**Tools**: pytest

```python
# Example: testing config validation
def test_temperature_must_be_in_range():
    with pytest.raises(ValidationError):
        LLMConfig(temperature=5.0)  # Invalid: must be 0-2

def test_valid_config_loads():
    config = LLMConfig(provider="openai", model="gpt-4o")
    assert config.provider == "openai"
```

### Integration Tests
**Scope**: Multiple components working together

**What to test**:
- Service layer with real storage (test database)
- Command execution with mocked services
- Provider implementations with mocked API responses

**Approach**:
- Use pytest fixtures for test database setup/teardown
- Mock external APIs (OpenAI, Anthropic, etc.) at HTTP level
- Test realistic workflows

```python
# Example: testing chat service with vector store
@pytest.fixture
def test_vector_store(tmp_path):
    """Create a temporary ChromaDB instance."""
    return ChromaDBStore(path=tmp_path / "test_vectors")

def test_context_retrieval(test_vector_store):
    # Store some content
    test_vector_store.store("Python is a programming language", {})
    
    # Query should find it
    results = test_vector_store.query("What is Python?", k=1)
    assert len(results) == 1
    assert "Python" in results[0].content
```

### End-to-End Tests
**Scope**: Full application behaviour from user perspective

**What to test**:
- Application startup and shutdown
- Critical command flows (/help, /exit, /clear)
- Basic chat interaction (with mocked LLM)
- Error handling and graceful degradation

**Approach**:
- Use subprocess or pexpect to drive the REPL
- Mock LLM responses at API level
- Keep E2E tests minimal—they're slow and brittle

```python
# Example: testing /help command
def test_help_command(cato_process):
    cato_process.sendline("/help")
    output = cato_process.expect_output(timeout=5)
    assert "Available commands" in output
```

### What NOT to Test
- Third-party library internals (Rich, ChromaDB, etc.)
- Exact output formatting (too brittle)
- Every error path (focus on critical ones)
- Performance benchmarks (not initially)

### Test Organisation
```
tests/
├── conftest.py           # Shared fixtures
├── unit/
│   ├── test_config.py
│   ├── test_commands.py
│   ├── test_message_parsing.py
│   └── ...
├── integration/
│   ├── test_chat_service.py
│   ├── test_vector_store.py
│   ├── test_productivity.py
│   └── ...
└── e2e/
    ├── test_startup.py
    ├── test_basic_chat.py
    └── test_commands.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run with coverage
pytest --cov=cato --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_config.py

# Run tests matching pattern
pytest -k "test_config"
```

## Continuous Integration

### CI Philosophy
- CI should be fast (< 5 minutes)
- Fail fast on obvious issues
- Don't block on non-critical checks

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e ".[dev]"
      
      - name: Run linting
        run: ruff check cato/
      
      - name: Run type checking
        run: mypy cato/
      
      - name: Run tests
        run: pytest tests/unit tests/integration --tb=short

  # E2E tests run separately, only on main
  e2e:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    needs: test
    
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e ".[dev]"
      - name: Run E2E tests
        run: pytest tests/e2e --tb=short
```

### CI Checks
1. **Linting** (ruff): Code style and common errors
2. **Type checking** (mypy): Static type verification
3. **Unit tests**: Fast, isolated tests
4. **Integration tests**: Component interaction tests
5. **E2E tests**: Full application tests (main branch only)

### Pre-commit Hooks (Optional)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Code Quality Tools

### Linting: Ruff
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
]
```

### Type Checking: Mypy
```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
```

### Test Coverage
- Aim for ~70-80% coverage on core modules
- Don't chase 100%—diminishing returns
- Focus coverage on business logic, not boilerplate

## Release Process

### Versioning
Semantic versioning: `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes to config or commands
- **MINOR**: New features, new commands
- **PATCH**: Bug fixes, minor improvements

Pre-1.0: `0.x.y` where breaking changes are expected

### Release Checklist
1. Ensure all tests pass on `main`
2. Update version in `pyproject.toml`
3. Update CHANGELOG.md with notable changes
4. Create git tag: `git tag -a v0.1.0 -m "Release 0.1.0"`
5. Push tag: `git push origin v0.1.0`

### Changelog Format
```markdown
# Changelog

## [0.2.0] - 2026-01-20
### Added
- Anthropic provider support
- /speaklike command for custom TTS instructions

### Changed
- Improved context retrieval performance

### Fixed
- Vector store connection error on startup

## [0.1.0] - 2026-01-14
- Initial release
```

### No PyPI Publishing (Initially)
- Cato is for personal use
- Install from git: `pip install git+https://github.com/user/cato.git`
- Or local editable install: `pip install -e .`

## Development Environment

### Setup
```bash
# Clone repository
git clone https://github.com/user/cato.git
cd cato

# Create conda environment (per user preference)
conda create -n cato python=3.12
conda activate cato

# Install in editable mode with dev dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

### Dev Dependencies
```toml
# pyproject.toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.23",
    "mypy>=1.8",
    "ruff>=0.1",
    "pre-commit>=3.0",
]
```

### Running Locally
```bash
# Run from source
python -m cato

# Run with specific config
python -m cato --config ~/.cato/dev.yaml

# Run with debug logging
python -m cato --log-level DEBUG
```

## Documentation

### Code Documentation
- Numpy-format docstrings on all public functions
- Type hints on all function signatures
- README.md in each module directory
- `agent.txt` at repo root for AI navigation

### User Documentation
- In-app help system (`/help`)
- Help files in `cato/resources/help/`
- Keep help in sync with implementation

### Specification Maintenance
- Update specs when implementation diverges
- Log significant decisions in specs
- Specs are living documents, not write-once

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md
@@ -340,49 +340,155 @@
 - Install from git: `pip install git+https://github.com/user/cato.git`
 - Or local editable install: `pip install -e .`
 
+## Package Management: uv
+
+Cato uses **uv** for package management. uv is a fast, modern Python package manager from Astral (the Ruff team).
+
+### Why uv
+- **Speed**: 10-100x faster than pip/Poetry for dependency resolution
+- **Standard format**: Uses PEP 621 compliant `pyproject.toml` (no custom sections)
+- **Deterministic**: Cross-platform lockfile support
+- **Simple**: Single tool for venv, install, and lock
+
+### pyproject.toml
+```toml
+[project]
+name = "cato"
+version = "0.1.0"
+description = "Chat at the Terminal Orchestrator"
+requires-python = ">=3.11"
+license = {text = "MIT"}
+authors = [
+    {name = "Alex Loveless", email = "alex@alexloveless.uk"}
+]
+
+dependencies = [
+    "rich>=13.0",
+    "prompt-toolkit>=3.0",
+    "pyyaml>=6.0",
+    "pydantic>=2.0",
+    "pydantic-ai>=0.1",
+    "chromadb>=0.4",
+    "openai>=1.0",
+    "anthropic>=0.18",
+    "google-generativeai>=0.4",
+    "httpx>=0.27",
+    "aiosqlite>=0.19",
+    "click>=8.0",
+]
+
+[project.optional-dependencies]
+dev = [
+    "pytest>=8.0",
+    "pytest-cov>=4.0",
+    "pytest-asyncio>=0.23",
+    "mypy>=1.8",
+    "ruff>=0.3",
+    "pre-commit>=3.0",
+]
+
+[project.scripts]
+cato = "cato.main:main"
+
+[build-system]
+requires = ["hatchling"]
+build-backend = "hatchling.build"
+
+[tool.ruff]
+line-length = 100
+target-version = "py311"
+
+[tool.ruff.lint]
+select = [
+    "E",    # pycodestyle errors
+    "W",    # pycodestyle warnings
+    "F",    # pyflakes
+    "I",    # isort
+    "B",    # flake8-bugbear
+    "UP",   # pyupgrade
+]
+
+[tool.mypy]
+python_version = "3.11"
+strict = true
+warn_return_any = true
+warn_unused_ignores = true
+
+[tool.pytest.ini_options]
+asyncio_mode = "auto"
+testpaths = ["tests"]
+```
+
 ## Development Environment
 
-### Setup
+### Initial Setup
 ```bash
 # Clone repository
 git clone https://github.com/user/cato.git
 cd cato
 
-# Create conda environment (per user preference)
+# Create conda environment
 conda create -n cato python=3.12
 conda activate cato
 
-# Install in editable mode with dev dependencies
+# Install uv (if not already installed)
+pip install uv
+
+# Install Cato in editable mode with dev dependencies
 uv pip install -e ".[dev]"
 
 # Install pre-commit hooks (optional)
 pre-commit install
 ```
 
-### Dev Dependencies
-```toml
-# pyproject.toml
-[project.optional-dependencies]
-dev = [
-    "pytest>=8.0",
-    "pytest-cov>=4.0",
-    "pytest-asyncio>=0.23",
-    "mypy>=1.8",
-    "ruff>=0.1",
-    "pre-commit>=3.0",
-]
+### Daily Workflow
+```bash
+# Activate environment
+conda activate cato
+
+# Sync dependencies (if pyproject.toml changed)
+uv pip install -e ".[dev]"
+
+# Run tests
+pytest
+
+# Run linting and type checking
+ruff check cato/
+mypy cato/
+```
+
+### Adding Dependencies
+```bash
+# Add to pyproject.toml manually, then:
+uv pip install -e ".[dev]"
+
+# Or install directly (for experimentation)
+uv pip install some-package
 ```
 
+### Lockfile (Optional)
+For reproducible builds, generate a lockfile:
+```bash
+# Generate lockfile from pyproject.toml
+uv pip compile pyproject.toml -o requirements.lock
+
+# Install from lockfile
+uv pip sync requirements.lock
+```
+
 ### Running Locally
 ```bash
-# Run from source
+# Run from source (after install)
+cato
+
+# Or run as module
 python -m cato
 
 # Run with specific config
-python -m cato --config ~/.cato/dev.yaml
+cato --config ~/.config/cato/dev.yaml
 
 # Run with debug logging
-python -m cato --log-level DEBUG
+cato --debug
 ```
 
 ## Documentation

```



Now I'll update the TECH_ARCHITECTURE.md to reference uv in the project structure section:


**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**
```
# Architecture Technical Specification

## Overview
This document defines Cato's core architectural patterns, component organisation, and the principles that enable modularity and flexibility.

## Design Goals
1. **Swappable components**: Any major component (LLM provider, storage backend, display) replaceable via configuration
2. **Easy extension**: Adding commands, providers, or features requires minimal changes to existing code
3. **Testability**: All components testable in isolation through dependency injection
4. **Configuration-driven**: Behaviour controlled by YAML, not code changes
5. **Clear boundaries**: Each module has a single responsibility with explicit interfaces

## Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Presentation                           │
│              (Rich console, prompt_toolkit)                 │
├─────────────────────────────────────────────────────────────┤
│                        Commands                             │
│           (Slash commands, input routing, REPL)             │
├─────────────────────────────────────────────────────────────┤
│                        Services                             │
│          (Chat, Productivity, TTS, Web Search)              │
├─────────────────────────────────────────────────────────────┤
│                        Providers                            │
│       (LLM backends, Search engines, TTS engines)           │
├─────────────────────────────────────────────────────────────┤
│                        Storage                              │
│              (ChromaDB, SQLite, File I/O)                   │
├─────────────────────────────────────────────────────────────┤
│                          Core                               │
│              (Config, Errors, Logging, Types)               │
└─────────────────────────────────────────────────────────────┘
```

### Layer Rules
- Each layer may only import from layers below it
- No circular dependencies between layers
- Cross-cutting concerns (logging, errors) live in Core and are available to all layers

### Layer Responsibilities

#### Core
- Configuration loading, validation, and access
- Custom exception hierarchy
- Logging setup and configuration
- Shared type definitions and data classes

#### Storage
- Vector store operations (ChromaDB)
- Productivity data persistence (SQLite)
- File operations for attachments and exports
- No business logic—pure data access

#### Providers
- LLM API integration (OpenAI, Anthropic, Google, Ollama)
- Search engine integration (DuckDuckGo, Google, Bing)
- TTS engine integration (OpenAI TTS)
- Each provider implements a common protocol

#### Services
- Business logic orchestration
- Chat service: message handling, context retrieval, response generation
- Productivity service: task/list/memory operations
- TTS service: text processing, audio generation
- Web service: search execution, URL fetching

#### Commands
- Slash command parsing and dispatch
- Command registration and discovery
- Input routing (commands vs chat vs productivity)
- REPL loop management

#### Presentation
- Console output formatting (Rich)
- User input handling (prompt_toolkit)
- Theming and styling
- Spinners and progress indicators

## Protocol-Based Abstractions

Key interfaces are defined as Python `Protocol` classes, enabling duck typing without inheritance.

### LLM Provider Protocol
```python
from typing import Protocol, AsyncIterator

class LLMProvider(Protocol):
    """Protocol for LLM backend implementations."""
    
    @property
    def model_name(self) -> str:
        """Return the current model identifier."""
        ...
    
    async def complete(
        self, 
        messages: list[Message], 
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> CompletionResponse:
        """Generate a completion for the given messages."""
        ...
    
    async def stream(
        self, 
        messages: list[Message],
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> AsyncIterator[str]:
        """Stream a completion token by token."""
        ...
```

### Vector Store Protocol
```python
class VectorStore(Protocol):
    """Protocol for vector storage backends."""
    
    def store(
        self, 
        content: str, 
        metadata: dict[str, Any],
        embedding: list[float] | None = None
    ) -> str:
        """Store content and return its ID."""
        ...
    
    def query(
        self, 
        text: str, 
        k: int = 5,
        filters: dict[str, Any] | None = None
    ) -> list[QueryResult]:
        """Query for similar content."""
        ...
    
    def delete(self, ids: list[str]) -> int:
        """Delete items by ID, return count deleted."""
        ...
```

### Benefits of Protocols
- No base class inheritance required
- Any class with matching methods satisfies the protocol
- Easy to create test mocks
- Swap implementations by changing config, not code

## Dependency Injection

Components receive their dependencies at construction time rather than creating them internally.

### Pattern
```python
# Services receive providers via constructor
class ChatService:
    def __init__(
        self,
        llm: LLMProvider,
        vector_store: VectorStore,
        config: ChatConfig
    ):
        self._llm = llm
        self._vector_store = vector_store
        self._config = config

# NOT this - creates tight coupling
class ChatService:
    def __init__(self):
        self._llm = OpenAIProvider()  # Locked to OpenAI
```

### Bootstrap Module
A dedicated `bootstrap.py` module handles component wiring:
1. Load configuration
2. Instantiate providers based on config
3. Instantiate services with their dependencies
4. Instantiate commands with service references
5. Return fully-wired application instance

```python
def create_application(config_path: Path | None = None) -> Application:
    """Wire up all components and return runnable application."""
    config = load_config(config_path)
    
    # Create providers based on config
    llm = create_llm_provider(config.llm)
    vector_store = create_vector_store(config.vector_store)
    productivity_db = create_productivity_db(config.storage)
    
    # Create services with dependencies
    chat_service = ChatService(llm, vector_store, config.chat)
    productivity_service = ProductivityService(productivity_db, config.productivity)
    
    # Create command registry with services
    commands = create_command_registry(
        chat=chat_service,
        productivity=productivity_service,
        config=config
    )
    
    # Create display layer
    display = create_display(config.display)
    
    return Application(
        commands=commands,
        display=display,
        config=config
    )
```

## Directory Structure

```
cato/
├── __init__.py
├── __main__.py              # Entry point: python -m cato
├── bootstrap.py             # Component wiring and initialisation
├── app.py                   # Application class, main run loop
│
├── core/
│   ├── __init__.py
│   ├── README.md            # Module documentation
│   ├── config.py            # Config loading, Pydantic models
│   ├── errors.py            # CatoError hierarchy
│   ├── logging.py           # Logging setup
│   └── types.py             # Shared data classes (Message, etc.)
│
├── providers/
│   ├── __init__.py
│   ├── README.md
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py          # LLMProvider protocol
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   ├── google.py
│   │   └── ollama.py
│   ├── search/
│   │   ├── __init__.py
│   │   ├── base.py          # SearchProvider protocol
│   │   ├── duckduckgo.py
│   │   └── google.py
│   └── tts/
│       ├── __init__.py
│       ├── base.py          # TTSProvider protocol
│       └── openai.py
│
├── storage/
│   ├── __init__.py
│   ├── README.md
│   ├── vector/
│   │   ├── __init__.py
│   │   ├── base.py          # VectorStore protocol
│   │   └── chromadb.py
│   └── productivity/
│       ├── __init__.py
│       ├── base.py          # ProductivityStore protocol
│       ├── sqlite.py
│       └── schema.sql       # Table definitions
│
├── services/
│   ├── __init__.py
│   ├── README.md
│   ├── chat.py              # Chat orchestration
│   ├── productivity.py      # Task/list/memory logic
│   ├── tts.py               # TTS orchestration
│   └── web.py               # Web search orchestration
│
├── commands/
│   ├── __init__.py
│   ├── README.md
│   ├── base.py              # BaseCommand, @command decorator, registry
│   ├── core.py              # /help, /exit, /clear, /config
│   ├── history.py           # /history, /delete, /model, /showsys
│   ├── context.py           # /showcontext, /continue, /casual
│   ├── files.py             # /attach, /cd, /ls, /cat, /pwd
│   ├── export.py            # /writemd, /writecode, /writejson, etc.
│   ├── vector.py            # /vadd, /vdoc, /vquery, /vstats, /vdelete
│   ├── productivity.py      # /st, /list, /timelog, /remember
│   ├── tts.py               # /speak, /speaklike
│   └── web.py               # /web, /url
│
├── display/
│   ├── __init__.py
│   ├── README.md
│   ├── console.py           # Rich console, output formatting
│   ├── input.py             # prompt_toolkit setup
│   ├── markdown.py          # Markdown rendering
│   └── themes.py            # Style definitions
│
└── resources/
    ├── defaults.yaml        # Default configuration
    └── help/                # Help text files
        ├── overview.md
        ├── commands.md
        └── ...
```

## Extension Points

### Adding a New LLM Provider
1. Create `cato/providers/llm/newprovider.py`
2. Implement the `LLMProvider` protocol
3. Register in provider factory (one line)
4. Add config schema for provider-specific options
5. User selects via `llm.provider: newprovider` in config

### Adding a New Command
1. Create or edit file in `cato/commands/`
2. Use `@command` decorator:
```python
@command(name="mycommand", aliases=["mc"])
async def my_command(ctx: CommandContext, args: list[str]) -> CommandResult:
    """Help text for the command."""
    # Implementation
    return CommandResult(success=True, message="Done")
```
3. No other registration needed—decorator handles it

### Adding a New Storage Backend
1. Create implementation in `cato/storage/`
2. Implement relevant protocol (VectorStore or ProductivityStore)
3. Register in storage factory
4. User selects via config

## Configuration Integration

All components receive configuration through typed Pydantic models:

```python
# Components don't read config files directly
# They receive pre-validated config objects

class ChatService:
    def __init__(self, config: ChatConfig):
        self._temperature = config.temperature  # Already validated
        self._max_tokens = config.max_tokens
```

This ensures:
- No hard-coded defaults in implementation code
- Type safety throughout
- Single source of truth (YAML files)
- Easy testing with custom config objects

## Error Propagation

Errors flow upward through layers:
1. **Storage/Provider layer**: Raise specific exceptions (e.g., `VectorStoreError`, `ProviderAPIError`)
2. **Service layer**: Catch, log, optionally wrap in service-specific exception or re-raise
3. **Command layer**: Catch service exceptions, convert to user-friendly `CommandResult`
4. **Presentation layer**: Display error to user appropriately

```python
# Storage layer
def query(self, text: str) -> list[Result]:
    try:
        return self._client.query(text)
    except chromadb.errors.InvalidCollectionException as e:
        raise VectorStoreError(f"Collection not found: {e}") from e

# Service layer
async def get_context(self, query: str) -> list[str]:
    try:
        results = self._vector_store.query(query)
        return [r.content for r in results]
    except VectorStoreError:
        logger.warning("Vector store unavailable, continuing without context")
        return []  # Graceful degradation

# Command layer
async def execute(self, args: list[str]) -> CommandResult:
    try:
        context = await self._chat.get_context(args[0])
        return CommandResult(success=True, data=context)
    except CatoError as e:
        return CommandResult(success=False, message=str(e))
```

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Use protocol-based mocks for dependencies
- Test config validation separately

### Integration Tests
- Test service + storage combinations
- Test command + service combinations
- Use test fixtures for database state

### End-to-End Tests
- Test full REPL interactions
- Use subprocess or pytest fixtures
- Verify user-visible behaviour

## Flexibility Summary

| Requirement | How Achieved |
|-------------|--------------|
| Swap LLM providers | Protocol abstraction + config selection |
| Add commands easily | Decorator-based registration |
| Customise appearance | Config-driven theming, separate display layer |
| Run multiple configs | CLI `--config` flag, isolated instances |
| Test components | Dependency injection, protocol mocks |
| Extend storage | Protocol abstraction + factory pattern |
| Modify without breaking | Layered architecture, explicit interfaces |

```





**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**
```
# Architecture Technical Specification

## Overview
This document defines Cato's core architectural patterns, component organisation, and the principles that enable modularity and flexibility.

## Design Goals
1. **Swappable components**: Any major component (LLM provider, storage backend, display) replaceable via configuration
2. **Easy extension**: Adding commands, providers, or features requires minimal changes to existing code
3. **Testability**: All components testable in isolation through dependency injection
4. **Configuration-driven**: Behaviour controlled by YAML, not code changes
5. **Clear boundaries**: Each module has a single responsibility with explicit interfaces

## Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Presentation                           │
│              (Rich console, prompt_toolkit)                 │
├─────────────────────────────────────────────────────────────┤
│                        Commands                             │
│           (Slash commands, input routing, REPL)             │
├─────────────────────────────────────────────────────────────┤
│                        Services                             │
│          (Chat, Productivity, TTS, Web Search)              │
├─────────────────────────────────────────────────────────────┤
│                        Providers                            │
│       (LLM backends, Search engines, TTS engines)           │
├─────────────────────────────────────────────────────────────┤
│                        Storage                              │
│              (ChromaDB, SQLite, File I/O)                   │
├─────────────────────────────────────────────────────────────┤
│                          Core                               │
│              (Config, Errors, Logging, Types)               │
└─────────────────────────────────────────────────────────────┘
```

### Layer Rules
- Each layer may only import from layers below it
- No circular dependencies between layers
- Cross-cutting concerns (logging, errors) live in Core and are available to all layers

### Layer Responsibilities

#### Core
- Configuration loading, validation, and access
- Custom exception hierarchy
- Logging setup and configuration
- Shared type definitions and data classes

#### Storage
- Vector store operations (ChromaDB)
- Productivity data persistence (SQLite)
- File operations for attachments and exports
- No business logic—pure data access

#### Providers
- LLM API integration (OpenAI, Anthropic, Google, Ollama)
- Search engine integration (DuckDuckGo, Google, Bing)
- TTS engine integration (OpenAI TTS)
- Each provider implements a common protocol

#### Services
- Business logic orchestration
- Chat service: message handling, context retrieval, response generation
- Productivity service: task/list/memory operations
- TTS service: text processing, audio generation
- Web service: search execution, URL fetching

#### Commands
- Slash command parsing and dispatch
- Command registration and discovery
- Input routing (commands vs chat vs productivity)
- REPL loop management

#### Presentation
- Console output formatting (Rich)
- User input handling (prompt_toolkit)
- Theming and styling
- Spinners and progress indicators

## Protocol-Based Abstractions

Key interfaces are defined as Python `Protocol` classes, enabling duck typing without inheritance.

### LLM Provider Protocol
```python
from typing import Protocol, AsyncIterator

class LLMProvider(Protocol):
    """Protocol for LLM backend implementations."""
    
    @property
    def model_name(self) -> str:
        """Return the current model identifier."""
        ...
    
    async def complete(
        self, 
        messages: list[Message], 
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> CompletionResponse:
        """Generate a completion for the given messages."""
        ...
    
    async def stream(
        self, 
        messages: list[Message],
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> AsyncIterator[str]:
        """Stream a completion token by token."""
        ...
```

### Vector Store Protocol
```python
class VectorStore(Protocol):
    """Protocol for vector storage backends."""
    
    def store(
        self, 
        content: str, 
        metadata: dict[str, Any],
        embedding: list[float] | None = None
    ) -> str:
        """Store content and return its ID."""
        ...
    
    def query(
        self, 
        text: str, 
        k: int = 5,
        filters: dict[str, Any] | None = None
    ) -> list[QueryResult]:
        """Query for similar content."""
        ...
    
    def delete(self, ids: list[str]) -> int:
        """Delete items by ID, return count deleted."""
        ...
```

### Benefits of Protocols
- No base class inheritance required
- Any class with matching methods satisfies the protocol
- Easy to create test mocks
- Swap implementations by changing config, not code

## Dependency Injection

Components receive their dependencies at construction time rather than creating them internally.

### Pattern
```python
# Services receive providers via constructor
class ChatService:
    def __init__(
        self,
        llm: LLMProvider,
        vector_store: VectorStore,
        config: ChatConfig
    ):
        self._llm = llm
        self._vector_store = vector_store
        self._config = config

# NOT this - creates tight coupling
class ChatService:
    def __init__(self):
        self._llm = OpenAIProvider()  # Locked to OpenAI
```

### Bootstrap Module
A dedicated `bootstrap.py` module handles component wiring:
1. Load configuration
2. Instantiate providers based on config
3. Instantiate services with their dependencies
4. Instantiate commands with service references
5. Return fully-wired application instance

```python
def create_application(config_path: Path | None = None) -> Application:
    """Wire up all components and return runnable application."""
    config = load_config(config_path)
    
    # Create providers based on config
    llm = create_llm_provider(config.llm)
    vector_store = create_vector_store(config.vector_store)
    productivity_db = create_productivity_db(config.storage)
    
    # Create services with dependencies
    chat_service = ChatService(llm, vector_store, config.chat)
    productivity_service = ProductivityService(productivity_db, config.productivity)
    
    # Create command registry with services
    commands = create_command_registry(
        chat=chat_service,
        productivity=productivity_service,
        config=config
    )
    
    # Create display layer
    display = create_display(config.display)
    
    return Application(
        commands=commands,
        display=display,
        config=config
    )
```

## Directory Structure

```
cato/
├── __init__.py
├── __main__.py              # Entry point: python -m cato
├── bootstrap.py             # Component wiring and initialisation
├── app.py                   # Application class, main run loop
│
├── core/
│   ├── __init__.py
│   ├── README.md            # Module documentation
│   ├── config.py            # Config loading, Pydantic models
│   ├── errors.py            # CatoError hierarchy
│   ├── logging.py           # Logging setup
│   └── types.py             # Shared data classes (Message, etc.)
│
├── providers/
│   ├── __init__.py
│   ├── README.md
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py          # LLMProvider protocol
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   ├── google.py
│   │   └── ollama.py
│   ├── search/
│   │   ├── __init__.py
│   │   ├── base.py          # SearchProvider protocol
│   │   ├── duckduckgo.py
│   │   └── google.py
│   └── tts/
│       ├── __init__.py
│       ├── base.py          # TTSProvider protocol
│       └── openai.py
│
├── storage/
│   ├── __init__.py
│   ├── README.md
│   ├── vector/
│   │   ├── __init__.py
│   │   ├── base.py          # VectorStore protocol
│   │   └── chromadb.py
│   └── productivity/
│       ├── __init__.py
│       ├── base.py          # ProductivityStore protocol
│       ├── sqlite.py
│       └── schema.sql       # Table definitions
│
├── services/
│   ├── __init__.py
│   ├── README.md
│   ├── chat.py              # Chat orchestration
│   ├── productivity.py      # Task/list/memory logic
│   ├── tts.py               # TTS orchestration
│   └── web.py               # Web search orchestration
│
├── commands/
│   ├── __init__.py
│   ├── README.md
│   ├── base.py              # BaseCommand, @command decorator, registry
│   ├── core.py              # /help, /exit, /clear, /config
│   ├── history.py           # /history, /delete, /model, /showsys
│   ├── context.py           # /showcontext, /continue, /casual
│   ├── files.py             # /attach, /cd, /ls, /cat, /pwd
│   ├── export.py            # /writemd, /writecode, /writejson, etc.
│   ├── vector.py            # /vadd, /vdoc, /vquery, /vstats, /vdelete
│   ├── productivity.py      # /st, /list, /timelog, /remember
│   ├── tts.py               # /speak, /speaklike
│   └── web.py               # /web, /url
│
├── display/
│   ├── __init__.py
│   ├── README.md
│   ├── console.py           # Rich console, output formatting
│   ├── input.py             # prompt_toolkit setup
│   ├── markdown.py          # Markdown rendering
│   └── themes.py            # Style definitions
│
└── resources/
    ├── defaults.yaml        # Default configuration
    └── help/                # Help text files
        ├── overview.md
        ├── commands.md
        └── ...
```

## Extension Points

### Adding a New LLM Provider
1. Create `cato/providers/llm/newprovider.py`
2. Implement the `LLMProvider` protocol
3. Register in provider factory (one line)
4. Add config schema for provider-specific options
5. User selects via `llm.provider: newprovider` in config

### Adding a New Command
1. Create or edit file in `cato/commands/`
2. Use `@command` decorator:
```python
@command(name="mycommand", aliases=["mc"])
async def my_command(ctx: CommandContext, args: list[str]) -> CommandResult:
    """Help text for the command."""
    # Implementation
    return CommandResult(success=True, message="Done")
```
3. No other registration needed—decorator handles it

### Adding a New Storage Backend
1. Create implementation in `cato/storage/`
2. Implement relevant protocol (VectorStore or ProductivityStore)
3. Register in storage factory
4. User selects via config

## Configuration Integration

All components receive configuration through typed Pydantic models:

```python
# Components don't read config files directly
# They receive pre-validated config objects

class ChatService:
    def __init__(self, config: ChatConfig):
        self._temperature = config.temperature  # Already validated
        self._max_tokens = config.max_tokens
```

This ensures:
- No hard-coded defaults in implementation code
- Type safety throughout
- Single source of truth (YAML files)
- Easy testing with custom config objects

## Error Propagation

Errors flow upward through layers:
1. **Storage/Provider layer**: Raise specific exceptions (e.g., `VectorStoreError`, `ProviderAPIError`)
2. **Service layer**: Catch, log, optionally wrap in service-specific exception or re-raise
3. **Command layer**: Catch service exceptions, convert to user-friendly `CommandResult`
4. **Presentation layer**: Display error to user appropriately

```python
# Storage layer
def query(self, text: str) -> list[Result]:
    try:
        return self._client.query(text)
    except chromadb.errors.InvalidCollectionException as e:
        raise VectorStoreError(f"Collection not found: {e}") from e

# Service layer
async def get_context(self, query: str) -> list[str]:
    try:
        results = self._vector_store.query(query)
        return [r.content for r in results]
    except VectorStoreError:
        logger.warning("Vector store unavailable, continuing without context")
        return []  # Graceful degradation

# Command layer
async def execute(self, args: list[str]) -> CommandResult:
    try:
        context = await self._chat.get_context(args[0])
        return CommandResult(success=True, data=context)
    except CatoError as e:
        return CommandResult(success=False, message=str(e))
```

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Use protocol-based mocks for dependencies
- Test config validation separately

### Integration Tests
- Test service + storage combinations
- Test command + service combinations
- Use test fixtures for database state

### End-to-End Tests
- Test full REPL interactions
- Use subprocess or pytest fixtures
- Verify user-visible behaviour

## Flexibility Summary

| Requirement | How Achieved |
|-------------|--------------|
| Swap LLM providers | Protocol abstraction + config selection |
| Add commands easily | Decorator-based registration |
| Customise appearance | Config-driven theming, separate display layer |
| Run multiple configs | CLI `--config` flag, isolated instances |
| Test components | Dependency injection, protocol mocks |
| Extend storage | Protocol abstraction + factory pattern |
| Modify without breaking | Layered architecture, explicit interfaces |

```





**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**
```
# Architecture Technical Specification

## Overview
This document defines Cato's core architectural patterns, component organisation, and the principles that enable modularity and flexibility.

## Design Goals
1. **Swappable components**: Any major component (LLM provider, storage backend, display) replaceable via configuration
2. **Easy extension**: Adding commands, providers, or features requires minimal changes to existing code
3. **Testability**: All components testable in isolation through dependency injection
4. **Configuration-driven**: Behaviour controlled by YAML, not code changes
5. **Clear boundaries**: Each module has a single responsibility with explicit interfaces

## Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Presentation                           │
│              (Rich console, prompt_toolkit)                 │
├─────────────────────────────────────────────────────────────┤
│                        Commands                             │
│           (Slash commands, input routing, REPL)             │
├─────────────────────────────────────────────────────────────┤
│                        Services                             │
│          (Chat, Productivity, TTS, Web Search)              │
├─────────────────────────────────────────────────────────────┤
│                        Providers                            │
│       (LLM backends, Search engines, TTS engines)           │
├─────────────────────────────────────────────────────────────┤
│                        Storage                              │
│              (ChromaDB, SQLite, File I/O)                   │
├─────────────────────────────────────────────────────────────┤
│                          Core                               │
│              (Config, Errors, Logging, Types)               │
└─────────────────────────────────────────────────────────────┘
```

### Layer Rules
- Each layer may only import from layers below it
- No circular dependencies between layers
- Cross-cutting concerns (logging, errors) live in Core and are available to all layers

### Layer Responsibilities

#### Core
- Configuration loading, validation, and access
- Custom exception hierarchy
- Logging setup and configuration
- Shared type definitions and data classes

#### Storage
- Vector store operations (ChromaDB)
- Productivity data persistence (SQLite)
- File operations for attachments and exports
- No business logic—pure data access

#### Providers
- LLM API integration (OpenAI, Anthropic, Google, Ollama)
- Search engine integration (DuckDuckGo, Google, Bing)
- TTS engine integration (OpenAI TTS)
- Each provider implements a common protocol

#### Services
- Business logic orchestration
- Chat service: message handling, context retrieval, response generation
- Productivity service: task/list/memory operations
- TTS service: text processing, audio generation
- Web service: search execution, URL fetching

#### Commands
- Slash command parsing and dispatch
- Command registration and discovery
- Input routing (commands vs chat vs productivity)
- REPL loop management

#### Presentation
- Console output formatting (Rich)
- User input handling (prompt_toolkit)
- Theming and styling
- Spinners and progress indicators

## Protocol-Based Abstractions

Key interfaces are defined as Python `Protocol` classes, enabling duck typing without inheritance.

### LLM Provider Protocol
```python
from typing import Protocol, AsyncIterator

class LLMProvider(Protocol):
    """Protocol for LLM backend implementations."""
    
    @property
    def model_name(self) -> str:
        """Return the current model identifier."""
        ...
    
    async def complete(
        self, 
        messages: list[Message], 
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> CompletionResponse:
        """Generate a completion for the given messages."""
        ...
    
    async def stream(
        self, 
        messages: list[Message],
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> AsyncIterator[str]:
        """Stream a completion token by token."""
        ...
```

### Vector Store Protocol
```python
class VectorStore(Protocol):
    """Protocol for vector storage backends."""
    
    def store(
        self, 
        content: str, 
        metadata: dict[str, Any],
        embedding: list[float] | None = None
    ) -> str:
        """Store content and return its ID."""
        ...
    
    def query(
        self, 
        text: str, 
        k: int = 5,
        filters: dict[str, Any] | None = None
    ) -> list[QueryResult]:
        """Query for similar content."""
        ...
    
    def delete(self, ids: list[str]) -> int:
        """Delete items by ID, return count deleted."""
        ...
```

### Benefits of Protocols
- No base class inheritance required
- Any class with matching methods satisfies the protocol
- Easy to create test mocks
- Swap implementations by changing config, not code

## Dependency Injection

Components receive their dependencies at construction time rather than creating them internally.

### Pattern
```python
# Services receive providers via constructor
class ChatService:
    def __init__(
        self,
        llm: LLMProvider,
        vector_store: VectorStore,
        config: ChatConfig
    ):
        self._llm = llm
        self._vector_store = vector_store
        self._config = config

# NOT this - creates tight coupling
class ChatService:
    def __init__(self):
        self._llm = OpenAIProvider()  # Locked to OpenAI
```

### Bootstrap Module
A dedicated `bootstrap.py` module handles component wiring:
1. Load configuration
2. Instantiate providers based on config
3. Instantiate services with their dependencies
4. Instantiate commands with service references
5. Return fully-wired application instance

```python
def create_application(config_path: Path | None = None) -> Application:
    """Wire up all components and return runnable application."""
    config = load_config(config_path)
    
    # Create providers based on config
    llm = create_llm_provider(config.llm)
    vector_store = create_vector_store(config.vector_store)
    productivity_db = create_productivity_db(config.storage)
    
    # Create services with dependencies
    chat_service = ChatService(llm, vector_store, config.chat)
    productivity_service = ProductivityService(productivity_db, config.productivity)
    
    # Create command registry with services
    commands = create_command_registry(
        chat=chat_service,
        productivity=productivity_service,
        config=config
    )
    
    # Create display layer
    display = create_display(config.display)
    
    return Application(
        commands=commands,
        display=display,
        config=config
    )
```

## Directory Structure

```
cato/
├── __init__.py
├── __main__.py              # Entry point: python -m cato
├── bootstrap.py             # Component wiring and initialisation
├── app.py                   # Application class, main run loop
│
├── core/
│   ├── __init__.py
│   ├── README.md            # Module documentation
│   ├── config.py            # Config loading, Pydantic models
│   ├── errors.py            # CatoError hierarchy
│   ├── logging.py           # Logging setup
│   └── types.py             # Shared data classes (Message, etc.)
│
├── providers/
│   ├── __init__.py
│   ├── README.md
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py          # LLMProvider protocol
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   ├── google.py
│   │   └── ollama.py
│   ├── search/
│   │   ├── __init__.py
│   │   ├── base.py          # SearchProvider protocol
│   │   ├── duckduckgo.py
│   │   └── google.py
│   └── tts/
│       ├── __init__.py
│       ├── base.py          # TTSProvider protocol
│       └── openai.py
│
├── storage/
│   ├── __init__.py
│   ├── README.md
│   ├── vector/
│   │   ├── __init__.py
│   │   ├── base.py          # VectorStore protocol
│   │   └── chromadb.py
│   └── productivity/
│       ├── __init__.py
│       ├── base.py          # ProductivityStore protocol
│       ├── sqlite.py
│       └── schema.sql       # Table definitions
│
├── services/
│   ├── __init__.py
│   ├── README.md
│   ├── chat.py              # Chat orchestration
│   ├── productivity.py      # Task/list/memory logic
│   ├── tts.py               # TTS orchestration
│   └── web.py               # Web search orchestration
│
├── commands/
│   ├── __init__.py
│   ├── README.md
│   ├── base.py              # BaseCommand, @command decorator, registry
│   ├── core.py              # /help, /exit, /clear, /config
│   ├── history.py           # /history, /delete, /model, /showsys
│   ├── context.py           # /showcontext, /continue, /casual
│   ├── files.py             # /attach, /cd, /ls, /cat, /pwd
│   ├── export.py            # /writemd, /writecode, /writejson, etc.
│   ├── vector.py            # /vadd, /vdoc, /vquery, /vstats, /vdelete
│   ├── productivity.py      # /st, /list, /timelog, /remember
│   ├── tts.py               # /speak, /speaklike
│   └── web.py               # /web, /url
│
├── display/
│   ├── __init__.py
│   ├── README.md
│   ├── console.py           # Rich console, output formatting
│   ├── input.py             # prompt_toolkit setup
│   ├── markdown.py          # Markdown rendering
│   └── themes.py            # Style definitions
│
└── resources/
    ├── defaults.yaml        # Default configuration
    └── help/                # Help text files
        ├── overview.md
        ├── commands.md
        └── ...
```

## Extension Points

### Adding a New LLM Provider
1. Create `cato/providers/llm/newprovider.py`
2. Implement the `LLMProvider` protocol
3. Register in provider factory (one line)
4. Add config schema for provider-specific options
5. User selects via `llm.provider: newprovider` in config

### Adding a New Command
1. Create or edit file in `cato/commands/`
2. Use `@command` decorator:
```python
@command(name="mycommand", aliases=["mc"])
async def my_command(ctx: CommandContext, args: list[str]) -> CommandResult:
    """Help text for the command."""
    # Implementation
    return CommandResult(success=True, message="Done")
```
3. No other registration needed—decorator handles it

### Adding a New Storage Backend
1. Create implementation in `cato/storage/`
2. Implement relevant protocol (VectorStore or ProductivityStore)
3. Register in storage factory
4. User selects via config

## Configuration Integration

All components receive configuration through typed Pydantic models:

```python
# Components don't read config files directly
# They receive pre-validated config objects

class ChatService:
    def __init__(self, config: ChatConfig):
        self._temperature = config.temperature  # Already validated
        self._max_tokens = config.max_tokens
```

This ensures:
- No hard-coded defaults in implementation code
- Type safety throughout
- Single source of truth (YAML files)
- Easy testing with custom config objects

## Error Propagation

Errors flow upward through layers:
1. **Storage/Provider layer**: Raise specific exceptions (e.g., `VectorStoreError`, `ProviderAPIError`)
2. **Service layer**: Catch, log, optionally wrap in service-specific exception or re-raise
3. **Command layer**: Catch service exceptions, convert to user-friendly `CommandResult`
4. **Presentation layer**: Display error to user appropriately

```python
# Storage layer
def query(self, text: str) -> list[Result]:
    try:
        return self._client.query(text)
    except chromadb.errors.InvalidCollectionException as e:
        raise VectorStoreError(f"Collection not found: {e}") from e

# Service layer
async def get_context(self, query: str) -> list[str]:
    try:
        results = self._vector_store.query(query)
        return [r.content for r in results]
    except VectorStoreError:
        logger.warning("Vector store unavailable, continuing without context")
        return []  # Graceful degradation

# Command layer
async def execute(self, args: list[str]) -> CommandResult:
    try:
        context = await self._chat.get_context(args[0])
        return CommandResult(success=True, data=context)
    except CatoError as e:
        return CommandResult(success=False, message=str(e))
```

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Use protocol-based mocks for dependencies
- Test config validation separately

### Integration Tests
- Test service + storage combinations
- Test command + service combinations
- Use test fixtures for database state

### End-to-End Tests
- Test full REPL interactions
- Use subprocess or pytest fixtures
- Verify user-visible behaviour

## Flexibility Summary

| Requirement | How Achieved |
|-------------|--------------|
| Swap LLM providers | Protocol abstraction + config selection |
| Add commands easily | Decorator-based registration |
| Customise appearance | Config-driven theming, separate display layer |
| Run multiple configs | CLI `--config` flag, isolated instances |
| Test components | Dependency injection, protocol mocks |
| Extend storage | Protocol abstraction + factory pattern |
| Modify without breaking | Layered architecture, explicit interfaces |

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md
@@ -213,13 +213,22 @@
 ## Directory Structure
 
 ```
-cato/
-├── __init__.py
-├── __main__.py              # Entry point: python -m cato
-├── bootstrap.py             # Component wiring and initialisation
-├── app.py                   # Application class, main run loop
+cato/                        # Repository root
+├── pyproject.toml           # Package metadata, dependencies (uv/PEP 621)
+├── README.md
+├── CHANGELOG.md
+├── LICENSE
+├── agent.txt                # AI codebase navigation
+├── .gitignore
 │
-├── core/
+├── cato/                    # Python package
+│   ├── __init__.py
+│   ├── __main__.py          # Entry point: python -m cato
+│   ├── main.py              # CLI entry point for `cato` command
+│   ├── bootstrap.py         # Component wiring and initialisation
+│   ├── app.py               # Application class, main run loop
+│   │
+│   ├── core/
 │   ├── __init__.py
 │   ├── README.md            # Module documentation
 │   ├── config.py            # Config loading, Pydantic models

```



Now I need to fix the rest of the directory structure to properly nest within the `cato/` package and add tests:


**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**
```
# Architecture Technical Specification

## Overview
This document defines Cato's core architectural patterns, component organisation, and the principles that enable modularity and flexibility.

## Design Goals
1. **Swappable components**: Any major component (LLM provider, storage backend, display) replaceable via configuration
2. **Easy extension**: Adding commands, providers, or features requires minimal changes to existing code
3. **Testability**: All components testable in isolation through dependency injection
4. **Configuration-driven**: Behaviour controlled by YAML, not code changes
5. **Clear boundaries**: Each module has a single responsibility with explicit interfaces

## Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Presentation                           │
│              (Rich console, prompt_toolkit)                 │
├─────────────────────────────────────────────────────────────┤
│                        Commands                             │
│           (Slash commands, input routing, REPL)             │
├─────────────────────────────────────────────────────────────┤
│                        Services                             │
│          (Chat, Productivity, TTS, Web Search)              │
├─────────────────────────────────────────────────────────────┤
│                        Providers                            │
│       (LLM backends, Search engines, TTS engines)           │
├─────────────────────────────────────────────────────────────┤
│                        Storage                              │
│              (ChromaDB, SQLite, File I/O)                   │
├─────────────────────────────────────────────────────────────┤
│                          Core                               │
│              (Config, Errors, Logging, Types)               │
└─────────────────────────────────────────────────────────────┘
```

### Layer Rules
- Each layer may only import from layers below it
- No circular dependencies between layers
- Cross-cutting concerns (logging, errors) live in Core and are available to all layers

### Layer Responsibilities

#### Core
- Configuration loading, validation, and access
- Custom exception hierarchy
- Logging setup and configuration
- Shared type definitions and data classes

#### Storage
- Vector store operations (ChromaDB)
- Productivity data persistence (SQLite)
- File operations for attachments and exports
- No business logic—pure data access

#### Providers
- LLM API integration (OpenAI, Anthropic, Google, Ollama)
- Search engine integration (DuckDuckGo, Google, Bing)
- TTS engine integration (OpenAI TTS)
- Each provider implements a common protocol

#### Services
- Business logic orchestration
- Chat service: message handling, context retrieval, response generation
- Productivity service: task/list/memory operations
- TTS service: text processing, audio generation
- Web service: search execution, URL fetching

#### Commands
- Slash command parsing and dispatch
- Command registration and discovery
- Input routing (commands vs chat vs productivity)
- REPL loop management

#### Presentation
- Console output formatting (Rich)
- User input handling (prompt_toolkit)
- Theming and styling
- Spinners and progress indicators

## Protocol-Based Abstractions

Key interfaces are defined as Python `Protocol` classes, enabling duck typing without inheritance.

### LLM Provider Protocol
```python
from typing import Protocol, AsyncIterator

class LLMProvider(Protocol):
    """Protocol for LLM backend implementations."""
    
    @property
    def model_name(self) -> str:
        """Return the current model identifier."""
        ...
    
    async def complete(
        self, 
        messages: list[Message], 
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> CompletionResponse:
        """Generate a completion for the given messages."""
        ...
    
    async def stream(
        self, 
        messages: list[Message],
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> AsyncIterator[str]:
        """Stream a completion token by token."""
        ...
```

### Vector Store Protocol
```python
class VectorStore(Protocol):
    """Protocol for vector storage backends."""
    
    def store(
        self, 
        content: str, 
        metadata: dict[str, Any],
        embedding: list[float] | None = None
    ) -> str:
        """Store content and return its ID."""
        ...
    
    def query(
        self, 
        text: str, 
        k: int = 5,
        filters: dict[str, Any] | None = None
    ) -> list[QueryResult]:
        """Query for similar content."""
        ...
    
    def delete(self, ids: list[str]) -> int:
        """Delete items by ID, return count deleted."""
        ...
```

### Benefits of Protocols
- No base class inheritance required
- Any class with matching methods satisfies the protocol
- Easy to create test mocks
- Swap implementations by changing config, not code

## Dependency Injection

Components receive their dependencies at construction time rather than creating them internally.

### Pattern
```python
# Services receive providers via constructor
class ChatService:
    def __init__(
        self,
        llm: LLMProvider,
        vector_store: VectorStore,
        config: ChatConfig
    ):
        self._llm = llm
        self._vector_store = vector_store
        self._config = config

# NOT this - creates tight coupling
class ChatService:
    def __init__(self):
        self._llm = OpenAIProvider()  # Locked to OpenAI
```

### Bootstrap Module
A dedicated `bootstrap.py` module handles component wiring:
1. Load configuration
2. Instantiate providers based on config
3. Instantiate services with their dependencies
4. Instantiate commands with service references
5. Return fully-wired application instance

```python
def create_application(config_path: Path | None = None) -> Application:
    """Wire up all components and return runnable application."""
    config = load_config(config_path)
    
    # Create providers based on config
    llm = create_llm_provider(config.llm)
    vector_store = create_vector_store(config.vector_store)
    productivity_db = create_productivity_db(config.storage)
    
    # Create services with dependencies
    chat_service = ChatService(llm, vector_store, config.chat)
    productivity_service = ProductivityService(productivity_db, config.productivity)
    
    # Create command registry with services
    commands = create_command_registry(
        chat=chat_service,
        productivity=productivity_service,
        config=config
    )
    
    # Create display layer
    display = create_display(config.display)
    
    return Application(
        commands=commands,
        display=display,
        config=config
    )
```

## Directory Structure

```
cato/                        # Repository root
├── pyproject.toml           # Package metadata, dependencies (uv/PEP 621)
├── README.md
├── CHANGELOG.md
├── LICENSE
├── agent.txt                # AI codebase navigation
├── .gitignore
│
├── cato/                    # Python package
│   ├── __init__.py
│   ├── __main__.py          # Entry point: python -m cato
│   ├── main.py              # CLI entry point for `cato` command
│   ├── bootstrap.py         # Component wiring and initialisation
│   ├── app.py               # Application class, main run loop
│   │
│   ├── core/
│   ├── __init__.py
│   ├── README.md            # Module documentation
│   ├── config.py            # Config loading, Pydantic models
│   ├── errors.py            # CatoError hierarchy
│   ├── logging.py           # Logging setup
│   └── types.py             # Shared data classes (Message, etc.)
│
├── providers/
│   ├── __init__.py
│   ├── README.md
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py          # LLMProvider protocol
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   ├── google.py
│   │   └── ollama.py
│   ├── search/
│   │   ├── __init__.py
│   │   ├── base.py          # SearchProvider protocol
│   │   ├── duckduckgo.py
│   │   └── google.py
│   └── tts/
│       ├── __init__.py
│       ├── base.py          # TTSProvider protocol
│       └── openai.py
│
├── storage/
│   ├── __init__.py
│   ├── README.md
│   ├── vector/
│   │   ├── __init__.py
│   │   ├── base.py          # VectorStore protocol
│   │   └── chromadb.py
│   └── productivity/
│       ├── __init__.py
│       ├── base.py          # ProductivityStore protocol
│       ├── sqlite.py
│       └── schema.sql       # Table definitions
│
├── services/
│   ├── __init__.py
│   ├── README.md
│   ├── chat.py              # Chat orchestration
│   ├── productivity.py      # Task/list/memory logic
│   ├── tts.py               # TTS orchestration
│   └── web.py               # Web search orchestration
│
├── commands/
│   ├── __init__.py
│   ├── README.md
│   ├── base.py              # BaseCommand, @command decorator, registry
│   ├── core.py              # /help, /exit, /clear, /config
│   ├── history.py           # /history, /delete, /model, /showsys
│   ├── context.py           # /showcontext, /continue, /casual
│   ├── files.py             # /attach, /cd, /ls, /cat, /pwd
│   ├── export.py            # /writemd, /writecode, /writejson, etc.
│   ├── vector.py            # /vadd, /vdoc, /vquery, /vstats, /vdelete
│   ├── productivity.py      # /st, /list, /timelog, /remember
│   ├── tts.py               # /speak, /speaklike
│   └── web.py               # /web, /url
│
├── display/
│   ├── __init__.py
│   ├── README.md
│   ├── console.py           # Rich console, output formatting
│   ├── input.py             # prompt_toolkit setup
│   ├── markdown.py          # Markdown rendering
│   └── themes.py            # Style definitions
│
└── resources/
    ├── defaults.yaml        # Default configuration
    └── help/                # Help text files
        ├── overview.md
        ├── commands.md
        └── ...
```

## Extension Points

### Adding a New LLM Provider
1. Create `cato/providers/llm/newprovider.py`
2. Implement the `LLMProvider` protocol
3. Register in provider factory (one line)
4. Add config schema for provider-specific options
5. User selects via `llm.provider: newprovider` in config

### Adding a New Command
1. Create or edit file in `cato/commands/`
2. Use `@command` decorator:
```python
@command(name="mycommand", aliases=["mc"])
async def my_command(ctx: CommandContext, args: list[str]) -> CommandResult:
    """Help text for the command."""
    # Implementation
    return CommandResult(success=True, message="Done")
```
3. No other registration needed—decorator handles it

### Adding a New Storage Backend
1. Create implementation in `cato/storage/`
2. Implement relevant protocol (VectorStore or ProductivityStore)
3. Register in storage factory
4. User selects via config

## Configuration Integration

All components receive configuration through typed Pydantic models:

```python
# Components don't read config files directly
# They receive pre-validated config objects

class ChatService:
    def __init__(self, config: ChatConfig):
        self._temperature = config.temperature  # Already validated
        self._max_tokens = config.max_tokens
```

This ensures:
- No hard-coded defaults in implementation code
- Type safety throughout
- Single source of truth (YAML files)
- Easy testing with custom config objects

## Error Propagation

Errors flow upward through layers:
1. **Storage/Provider layer**: Raise specific exceptions (e.g., `VectorStoreError`, `ProviderAPIError`)
2. **Service layer**: Catch, log, optionally wrap in service-specific exception or re-raise
3. **Command layer**: Catch service exceptions, convert to user-friendly `CommandResult`
4. **Presentation layer**: Display error to user appropriately

```python
# Storage layer
def query(self, text: str) -> list[Result]:
    try:
        return self._client.query(text)
    except chromadb.errors.InvalidCollectionException as e:
        raise VectorStoreError(f"Collection not found: {e}") from e

# Service layer
async def get_context(self, query: str) -> list[str]:
    try:
        results = self._vector_store.query(query)
        return [r.content for r in results]
    except VectorStoreError:
        logger.warning("Vector store unavailable, continuing without context")
        return []  # Graceful degradation

# Command layer
async def execute(self, args: list[str]) -> CommandResult:
    try:
        context = await self._chat.get_context(args[0])
        return CommandResult(success=True, data=context)
    except CatoError as e:
        return CommandResult(success=False, message=str(e))
```

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Use protocol-based mocks for dependencies
- Test config validation separately

### Integration Tests
- Test service + storage combinations
- Test command + service combinations
- Use test fixtures for database state

### End-to-End Tests
- Test full REPL interactions
- Use subprocess or pytest fixtures
- Verify user-visible behaviour

## Flexibility Summary

| Requirement | How Achieved |
|-------------|--------------|
| Swap LLM providers | Protocol abstraction + config selection |
| Add commands easily | Decorator-based registration |
| Customise appearance | Config-driven theming, separate display layer |
| Run multiple configs | CLI `--config` flag, isolated instances |
| Test components | Dependency injection, protocol mocks |
| Extend storage | Protocol abstraction + factory pattern |
| Modify without breaking | Layered architecture, explicit interfaces |

```





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md
@@ -229,82 +229,95 @@
 │   ├── app.py               # Application class, main run loop
 │   │
 │   ├── core/
-│   ├── __init__.py
-│   ├── README.md            # Module documentation
-│   ├── config.py            # Config loading, Pydantic models
-│   ├── errors.py            # CatoError hierarchy
-│   ├── logging.py           # Logging setup
-│   └── types.py             # Shared data classes (Message, etc.)
-│
-├── providers/
-│   ├── __init__.py
-│   ├── README.md
-│   ├── llm/
 │   │   ├── __init__.py
-│   │   ├── base.py          # LLMProvider protocol
-│   │   ├── openai.py
-│   │   ├── anthropic.py
-│   │   ├── google.py
-│   │   └── ollama.py
-│   ├── search/
+│   │   ├── README.md        # Module documentation
+│   │   ├── config.py        # Config loading, Pydantic models
+│   │   ├── exceptions.py    # CatoError hierarchy
+│   │   ├── logging.py       # Logging setup
+│   │   └── types.py         # Shared data classes (Message, etc.)
+│   │
+│   ├── providers/
 │   │   ├── __init__.py
-│   │   ├── base.py          # SearchProvider protocol
-│   │   ├── duckduckgo.py
-│   │   └── google.py
-│   └── tts/
-│       ├── __init__.py
-│       ├── base.py          # TTSProvider protocol
-│       └── openai.py
-│
-├── storage/
-│   ├── __init__.py
-│   ├── README.md
-│   ├── vector/
+│   │   ├── README.md
+│   │   ├── llm/
+│   │   │   ├── __init__.py
+│   │   │   ├── base.py      # LLMProvider protocol
+│   │   │   ├── openai.py
+│   │   │   ├── anthropic.py
+│   │   │   ├── google.py
+│   │   │   └── ollama.py
+│   │   ├── search/
+│   │   │   ├── __init__.py
+│   │   │   ├── base.py      # SearchProvider protocol
+│   │   │   ├── duckduckgo.py
+│   │   │   └── google.py
+│   │   └── tts/
+│   │       ├── __init__.py
+│   │       ├── base.py      # TTSProvider protocol
+│   │       └── openai.py
+│   │
+│   ├── storage/
 │   │   ├── __init__.py
-│   │   ├── base.py          # VectorStore protocol
-│   │   └── chromadb.py
-│   └── productivity/
-│       ├── __init__.py
-│       ├── base.py          # ProductivityStore protocol
-│       ├── sqlite.py
-│       └── schema.sql       # Table definitions
-│
-├── services/
-│   ├── __init__.py
-│   ├── README.md
-│   ├── chat.py              # Chat orchestration
-│   ├── productivity.py      # Task/list/memory logic
-│   ├── tts.py               # TTS orchestration
-│   └── web.py               # Web search orchestration
-│
-├── commands/
-│   ├── __init__.py
-│   ├── README.md
-│   ├── base.py              # BaseCommand, @command decorator, registry
-│   ├── core.py              # /help, /exit, /clear, /config
-│   ├── history.py           # /history, /delete, /model, /showsys
-│   ├── context.py           # /showcontext, /continue, /casual
-│   ├── files.py             # /attach, /cd, /ls, /cat, /pwd
-│   ├── export.py            # /writemd, /writecode, /writejson, etc.
-│   ├── vector.py            # /vadd, /vdoc, /vquery, /vstats, /vdelete
-│   ├── productivity.py      # /st, /list, /timelog, /remember
-│   ├── tts.py               # /speak, /speaklike
-│   └── web.py               # /web, /url
-│
-├── display/
-│   ├── __init__.py
-│   ├── README.md
-│   ├── console.py           # Rich console, output formatting
-│   ├── input.py             # prompt_toolkit setup
-│   ├── markdown.py          # Markdown rendering
-│   └── themes.py            # Style definitions
+│   │   ├── README.md
+│   │   ├── vector/
+│   │   │   ├── __init__.py
+│   │   │   ├── base.py      # VectorStore protocol
+│   │   │   └── chromadb.py
+│   │   └── productivity/
+│   │       ├── __init__.py
+│   │       ├── base.py      # ProductivityStore protocol
+│   │       └── sqlite.py
+│   │
+│   ├── services/
+│   │   ├── __init__.py
+│   │   ├── README.md
+│   │   ├── chat.py          # Chat orchestration
+│   │   ├── productivity.py  # Task/list/memory logic
+│   │   ├── tts.py           # TTS orchestration
+│   │   └── web.py           # Web search orchestration
+│   │
+│   ├── commands/
+│   │   ├── __init__.py
+│   │   ├── README.md
+│   │   ├── base.py          # @command decorator, registry
+│   │   ├── core.py          # /help, /exit, /clear, /config
+│   │   ├── history.py       # /history, /delete, /model, /showsys
+│   │   ├── context.py       # /showcontext, /continue, /casual
+│   │   ├── files.py         # /attach, /cd, /ls, /cat, /pwd
+│   │   ├── export.py        # /writemd, /writecode, /writejson, etc.
+│   │   ├── vector.py        # /vadd, /vdoc, /vquery, /vstats, /vdelete
+│   │   ├── productivity.py  # /st, /list, /timelog, /remember
+│   │   ├── tts.py           # /speak, /speaklike
+│   │   └── web.py           # /web, /url
+│   │
+│   ├── display/
+│   │   ├── __init__.py
+│   │   ├── README.md
+│   │   ├── console.py       # Rich console, output formatting
+│   │   ├── input.py         # prompt_toolkit setup
+│   │   ├── markdown.py      # Markdown rendering
+│   │   └── themes.py        # Style definitions
+│   │
+│   └── resources/
+│       ├── defaults.yaml    # Default configuration
+│       └── help/            # Help text files
+│           ├── overview.md
+│           ├── commands.md
+│           └── ...
 │
-└── resources/
-    ├── defaults.yaml        # Default configuration
-    └── help/                # Help text files
-        ├── overview.md
-        ├── commands.md
-        └── ...
+└── tests/                   # Test suite
+    ├── conftest.py          # Shared fixtures
+    ├── unit/
+    │   ├── test_config.py
+    │   ├── test_commands.py
+    │   └── ...
+    ├── integration/
+    │   ├── test_chat_service.py
+    │   ├── test_vector_store.py
+    │   └── ...
+    └── e2e/
+        ├── test_startup.py
+        └── test_commands.py
 ```
 
 ## Extension Points

```



Updated both specs. Here's a summary of the changes:

**TECH_DEVELOPMENT.md:**
- Added comprehensive "Package Management: uv" section explaining why uv was chosen
- Included complete `pyproject.toml` example with PEP 621 metadata, dependencies, and tool configs
- Updated setup instructions to use `uv pip install`
- Added daily workflow commands
- Added lockfile generation instructions (`uv pip compile`)

**TECH_ARCHITECTURE.md:**
- Updated directory structure to show repository root with `pyproject.toml`
- Fixed package nesting (all Python code under `cato/` subdirectory)
- Added `tests/` directory structure
- Renamed `errors.py` to `exceptions.py` for consistency with other specs

USER:
configuration validation validation should be handled by pydantic. This does not seem to be the case for config

AGENT:
You're right. Let me check the config spec to see what needs correction.


**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md**
```
# Configuration System Technical Specification

## Overview
Cato uses a layered YAML configuration system where user settings overlay defaults. All configurable values live in YAML files—no hard-coded defaults in code.

## Configuration Hierarchy
```
defaults.yaml          # Shipped with Cato, never modified by user
    ↓
user_config.yaml       # User overrides, sparse (only differences)
    ↓
environment vars       # CATO_* env vars for secrets/runtime overrides
    ↓
CLI arguments          # Highest precedence, session-specific
```

## File Locations
```
~/.config/cato/
├── config.yaml        # User configuration
├── prompts/           # Custom system prompts
└── themes/            # Custom display themes

$PACKAGE/
└── defaults/
    ├── defaults.yaml  # Default configuration
    ├── prompts/       # Default prompts
    └── themes/        # Default themes
```

## Configuration Loading

### Load Sequence
```python
def load_config(user_path: Path | None = None) -> CatoConfig:
    """
    Load configuration with overlay system.
    
    Parameters
    ----------
    user_path
        Optional custom path to user config. If None, uses default location.
    
    Returns
    -------
    CatoConfig
        Validated configuration object.
    """
    # 1. Load defaults (always present, shipped with package)
    defaults = load_yaml(get_default_config_path())
    
    # 2. Load user config if exists
    user_config = {}
    if user_path and user_path.exists():
        user_config = load_yaml(user_path)
    elif default_user_path().exists():
        user_config = load_yaml(default_user_path())
    
    # 3. Deep merge: user overlays defaults
    merged = deep_merge(defaults, user_config)
    
    # 4. Apply environment variable overrides
    merged = apply_env_overrides(merged)
    
    # 5. Validate with Pydantic
    return CatoConfig.model_validate(merged)
```

### Deep Merge Behaviour
```python
# defaults.yaml
llm:
  provider: "openai"
  model: "gpt-4"
  temperature: 1.0
  max_tokens: 4096

# user_config.yaml
llm:
  model: "gpt-4-turbo"

# Result after merge
llm:
  provider: "openai"        # from defaults
  model: "gpt-4-turbo"      # from user (override)
  temperature: 1.0          # from defaults
  max_tokens: 4096          # from defaults
```

## Pydantic Schema

### Root Configuration
```python
class CatoConfig(BaseModel):
    """Root configuration model."""
    
    model_config = ConfigDict(extra="forbid")  # Warn on unknown keys
    
    llm: LLMConfig
    vector_store: VectorStoreConfig
    storage: StorageConfig
    display: DisplayConfig
    commands: CommandConfig
    logging: LoggingConfig
    paths: PathConfig
```

### LLM Configuration
```python
class LLMConfig(BaseModel):
    """LLM provider configuration."""
    
    provider: Literal["openai", "anthropic", "google", "ollama"]
    model: str
    temperature: float = Field(ge=0.0, le=2.0)
    max_tokens: int = Field(ge=1, le=200000)
    timeout_seconds: int = Field(ge=1, le=300)
    
    # Provider-specific settings
    openai: OpenAIConfig | None = None
    anthropic: AnthropicConfig | None = None
    google: GoogleConfig | None = None
    ollama: OllamaConfig | None = None
```

### Vector Store Configuration
```python
class VectorStoreConfig(BaseModel):
    """Vector store configuration."""
    
    enabled: bool
    backend: Literal["chromadb"]
    path: Path
    collection_name: str
    embedding_model: str
    chunk_size: int = Field(ge=100, le=10000)
    chunk_overlap: int = Field(ge=0)
    
    @field_validator("chunk_overlap")
    @classmethod
    def overlap_less_than_size(cls, v: int, info: ValidationInfo) -> int:
        if "chunk_size" in info.data and v >= info.data["chunk_size"]:
            raise ValueError("chunk_overlap must be less than chunk_size")
        return v
```

### Storage Configuration
```python
class StorageConfig(BaseModel):
    """SQLite storage configuration."""
    
    database_path: Path
    backup_enabled: bool
    backup_frequency_hours: int = Field(ge=1)
```

### Display Configuration
```python
class DisplayConfig(BaseModel):
    """Display and UI configuration."""
    
    theme: str
    markdown_enabled: bool
    code_theme: str
    max_width: int | None = Field(ge=40, default=None)
    timestamps: bool
    spinner_style: str
```

### Logging Configuration
```python
class LoggingConfig(BaseModel):
    """Logging configuration."""
    
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]
    file_path: Path | None
    format: str
    max_file_size_mb: int = Field(ge=1)
    backup_count: int = Field(ge=0)
```

## Environment Variable Overrides

### Naming Convention
```
CATO_<SECTION>_<KEY>=value
CATO_<SECTION>_<SUBSECTION>_<KEY>=value
```

### Examples
```bash
# Override LLM model
CATO_LLM_MODEL="claude-3-opus"

# Override logging level
CATO_LOGGING_LEVEL="DEBUG"

# API keys (primary use case)
CATO_OPENAI_API_KEY="sk-..."
CATO_ANTHROPIC_API_KEY="sk-ant-..."
```

### Implementation
```python
def apply_env_overrides(config: dict) -> dict:
    """
    Apply CATO_* environment variables as config overrides.
    
    Parameters
    ----------
    config
        Configuration dict to modify.
    
    Returns
    -------
    dict
        Configuration with env overrides applied.
    """
    prefix = "CATO_"
    for key, value in os.environ.items():
        if not key.startswith(prefix):
            continue
        
        # Parse key path: CATO_LLM_MODEL -> ["llm", "model"]
        parts = key[len(prefix):].lower().split("_")
        
        # Navigate to nested location and set value
        set_nested(config, parts, parse_env_value(value))
    
    return config
```

## CLI Argument Overrides
```python
@click.command()
@click.option("--config", type=Path, help="Path to config file")
@click.option("--model", help="Override LLM model")
@click.option("--debug", is_flag=True, help="Enable debug logging")
def main(config: Path | None, model: str | None, debug: bool) -> None:
    """Cato entry point."""
    cfg = load_config(config)
    
    # CLI overrides (highest precedence)
    if model:
        cfg.llm.model = model
    if debug:
        cfg.logging.level = "DEBUG"
```

## Validation Behaviour

### Unknown Keys
```python
class CatoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

# During validation
try:
    config = CatoConfig.model_validate(data)
except ValidationError as e:
    for error in e.errors():
        if error["type"] == "extra_forbidden":
            key = ".".join(str(loc) for loc in error["loc"])
            logger.warning(f"Unknown config key '{key}', ignoring")
    # Re-validate with extra="ignore" to continue
    config = CatoConfig.model_validate(data, strict=False)
```

### Invalid Values
```python
def validate_with_fallback(data: dict, defaults: dict) -> CatoConfig:
    """
    Validate config, falling back to defaults for invalid values.
    
    Parameters
    ----------
    data
        User configuration data.
    defaults
        Default configuration data.
    
    Returns
    -------
    CatoConfig
        Validated configuration, with defaults substituted for invalid values.
    """
    try:
        return CatoConfig.model_validate(data)
    except ValidationError as e:
        for error in e.errors():
            path = list(error["loc"])
            logger.warning(
                f"Invalid config value at '{'.'.join(map(str, path))}': "
                f"{error['msg']}. Using default."
            )
            # Reset to default value
            set_nested(data, path, get_nested(defaults, path))
        
        return CatoConfig.model_validate(data)
```

## Default Configuration File
```yaml
# defaults.yaml - Shipped with Cato, do not modify

llm:
  provider: "openai"
  model: "gpt-4"
  temperature: 1.0
  max_tokens: 4096
  timeout_seconds: 60

vector_store:
  enabled: true
  backend: "chromadb"
  path: "~/.local/share/cato/vectordb"
  collection_name: "cato_memory"
  embedding_model: "text-embedding-3-small"
  chunk_size: 1000
  chunk_overlap: 200

storage:
  database_path: "~/.local/share/cato/cato.db"
  backup_enabled: true
  backup_frequency_hours: 24

display:
  theme: "default"
  markdown_enabled: true
  code_theme: "monokai"
  max_width: null
  timestamps: false
  spinner_style: "dots"

commands:
  prefix: "/"
  history_file: "~/.local/share/cato/command_history"

logging:
  level: "WARNING"
  file_path: "~/.local/share/cato/cato.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  max_file_size_mb: 10
  backup_count: 3

paths:
  data_dir: "~/.local/share/cato"
  config_dir: "~/.config/cato"
  cache_dir: "~/.cache/cato"
```

## User Configuration Example
```yaml
# ~/.config/cato/config.yaml
# Only specify values that differ from defaults

llm:
  model: "gpt-4-turbo"
  temperature: 0.7

display:
  theme: "gruvbox-dark"
  timestamps: true

logging:
  level: "DEBUG"
```

## Runtime Configuration Access
```python
# Configuration is loaded once at startup and passed via dependency injection
class ChatService:
    def __init__(self, config: CatoConfig, llm: LLMProvider) -> None:
        self._config = config
        self._llm = llm
    
    async def send_message(self, message: str) -> str:
        return await self._llm.complete(
            message,
            temperature=self._config.llm.temperature,
            max_tokens=self._config.llm.max_tokens,
        )
```

## Path Expansion
All paths in configuration support:
- `~` for home directory
- Environment variables via `${VAR}`

```python
def expand_path(path: str | Path) -> Path:
    """Expand ~ and environment variables in path."""
    return Path(os.path.expandvars(os.path.expanduser(str(path))))
```

```



I see the issue. The config spec does show Pydantic validation (line 65-66: `CatoConfig.model_validate(merged)` and the Pydantic models with `Field` constraints), but the validation error handling section uses manual fallback logic instead of leveraging Pydantic properly. Let me check that section:


**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md**
```
# Configuration System Technical Specification

## Overview
Cato uses a layered YAML configuration system where user settings overlay defaults. All configurable values live in YAML files—no hard-coded defaults in code.

## Configuration Hierarchy
```
defaults.yaml          # Shipped with Cato, never modified by user
    ↓
user_config.yaml       # User overrides, sparse (only differences)
    ↓
environment vars       # CATO_* env vars for secrets/runtime overrides
    ↓
CLI arguments          # Highest precedence, session-specific
```

## File Locations
```
~/.config/cato/
├── config.yaml        # User configuration
├── prompts/           # Custom system prompts
└── themes/            # Custom display themes

$PACKAGE/
└── defaults/
    ├── defaults.yaml  # Default configuration
    ├── prompts/       # Default prompts
    └── themes/        # Default themes
```

## Configuration Loading

### Load Sequence
```python
def load_config(user_path: Path | None = None) -> CatoConfig:
    """
    Load configuration with overlay system.
    
    Parameters
    ----------
    user_path
        Optional custom path to user config. If None, uses default location.
    
    Returns
    -------
    CatoConfig
        Validated configuration object.
    """
    # 1. Load defaults (always present, shipped with package)
    defaults = load_yaml(get_default_config_path())
    
    # 2. Load user config if exists
    user_config = {}
    if user_path and user_path.exists():
        user_config = load_yaml(user_path)
    elif default_user_path().exists():
        user_config = load_yaml(default_user_path())
    
    # 3. Deep merge: user overlays defaults
    merged = deep_merge(defaults, user_config)
    
    # 4. Apply environment variable overrides
    merged = apply_env_overrides(merged)
    
    # 5. Validate with Pydantic
    return CatoConfig.model_validate(merged)
```

### Deep Merge Behaviour
```python
# defaults.yaml
llm:
  provider: "openai"
  model: "gpt-4"
  temperature: 1.0
  max_tokens: 4096

# user_config.yaml
llm:
  model: "gpt-4-turbo"

# Result after merge
llm:
  provider: "openai"        # from defaults
  model: "gpt-4-turbo"      # from user (override)
  temperature: 1.0          # from defaults
  max_tokens: 4096          # from defaults
```

## Pydantic Schema

### Root Configuration
```python
class CatoConfig(BaseModel):
    """Root configuration model."""
    
    model_config = ConfigDict(extra="forbid")  # Warn on unknown keys
    
    llm: LLMConfig
    vector_store: VectorStoreConfig
    storage: StorageConfig
    display: DisplayConfig
    commands: CommandConfig
    logging: LoggingConfig
    paths: PathConfig
```

### LLM Configuration
```python
class LLMConfig(BaseModel):
    """LLM provider configuration."""
    
    provider: Literal["openai", "anthropic", "google", "ollama"]
    model: str
    temperature: float = Field(ge=0.0, le=2.0)
    max_tokens: int = Field(ge=1, le=200000)
    timeout_seconds: int = Field(ge=1, le=300)
    
    # Provider-specific settings
    openai: OpenAIConfig | None = None
    anthropic: AnthropicConfig | None = None
    google: GoogleConfig | None = None
    ollama: OllamaConfig | None = None
```

### Vector Store Configuration
```python
class VectorStoreConfig(BaseModel):
    """Vector store configuration."""
    
    enabled: bool
    backend: Literal["chromadb"]
    path: Path
    collection_name: str
    embedding_model: str
    chunk_size: int = Field(ge=100, le=10000)
    chunk_overlap: int = Field(ge=0)
    
    @field_validator("chunk_overlap")
    @classmethod
    def overlap_less_than_size(cls, v: int, info: ValidationInfo) -> int:
        if "chunk_size" in info.data and v >= info.data["chunk_size"]:
            raise ValueError("chunk_overlap must be less than chunk_size")
        return v
```

### Storage Configuration
```python
class StorageConfig(BaseModel):
    """SQLite storage configuration."""
    
    database_path: Path
    backup_enabled: bool
    backup_frequency_hours: int = Field(ge=1)
```

### Display Configuration
```python
class DisplayConfig(BaseModel):
    """Display and UI configuration."""
    
    theme: str
    markdown_enabled: bool
    code_theme: str
    max_width: int | None = Field(ge=40, default=None)
    timestamps: bool
    spinner_style: str
```

### Logging Configuration
```python
class LoggingConfig(BaseModel):
    """Logging configuration."""
    
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]
    file_path: Path | None
    format: str
    max_file_size_mb: int = Field(ge=1)
    backup_count: int = Field(ge=0)
```

## Environment Variable Overrides

### Naming Convention
```
CATO_<SECTION>_<KEY>=value
CATO_<SECTION>_<SUBSECTION>_<KEY>=value
```

### Examples
```bash
# Override LLM model
CATO_LLM_MODEL="claude-3-opus"

# Override logging level
CATO_LOGGING_LEVEL="DEBUG"

# API keys (primary use case)
CATO_OPENAI_API_KEY="sk-..."
CATO_ANTHROPIC_API_KEY="sk-ant-..."
```

### Implementation
```python
def apply_env_overrides(config: dict) -> dict:
    """
    Apply CATO_* environment variables as config overrides.
    
    Parameters
    ----------
    config
        Configuration dict to modify.
    
    Returns
    -------
    dict
        Configuration with env overrides applied.
    """
    prefix = "CATO_"
    for key, value in os.environ.items():
        if not key.startswith(prefix):
            continue
        
        # Parse key path: CATO_LLM_MODEL -> ["llm", "model"]
        parts = key[len(prefix):].lower().split("_")
        
        # Navigate to nested location and set value
        set_nested(config, parts, parse_env_value(value))
    
    return config
```

## CLI Argument Overrides
```python
@click.command()
@click.option("--config", type=Path, help="Path to config file")
@click.option("--model", help="Override LLM model")
@click.option("--debug", is_flag=True, help="Enable debug logging")
def main(config: Path | None, model: str | None, debug: bool) -> None:
    """Cato entry point."""
    cfg = load_config(config)
    
    # CLI overrides (highest precedence)
    if model:
        cfg.llm.model = model
    if debug:
        cfg.logging.level = "DEBUG"
```

## Validation Behaviour

### Unknown Keys
```python
class CatoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

# During validation
try:
    config = CatoConfig.model_validate(data)
except ValidationError as e:
    for error in e.errors():
        if error["type"] == "extra_forbidden":
            key = ".".join(str(loc) for loc in error["loc"])
            logger.warning(f"Unknown config key '{key}', ignoring")
    # Re-validate with extra="ignore" to continue
    config = CatoConfig.model_validate(data, strict=False)
```

### Invalid Values
```python
def validate_with_fallback(data: dict, defaults: dict) -> CatoConfig:
    """
    Validate config, falling back to defaults for invalid values.
    
    Parameters
    ----------
    data
        User configuration data.
    defaults
        Default configuration data.
    
    Returns
    -------
    CatoConfig
        Validated configuration, with defaults substituted for invalid values.
    """
    try:
        return CatoConfig.model_validate(data)
    except ValidationError as e:
        for error in e.errors():
            path = list(error["loc"])
            logger.warning(
                f"Invalid config value at '{'.'.join(map(str, path))}': "
                f"{error['msg']}. Using default."
            )
            # Reset to default value
            set_nested(data, path, get_nested(defaults, path))
        
        return CatoConfig.model_validate(data)
```

## Default Configuration File
```yaml
# defaults.yaml - Shipped with Cato, do not modify

llm:
  provider: "openai"
  model: "gpt-4"
  temperature: 1.0
  max_tokens: 4096
  timeout_seconds: 60

vector_store:
  enabled: true
  backend: "chromadb"
  path: "~/.local/share/cato/vectordb"
  collection_name: "cato_memory"
  embedding_model: "text-embedding-3-small"
  chunk_size: 1000
  chunk_overlap: 200

storage:
  database_path: "~/.local/share/cato/cato.db"
  backup_enabled: true
  backup_frequency_hours: 24

display:
  theme: "default"
  markdown_enabled: true
  code_theme: "monokai"
  max_width: null
  timestamps: false
  spinner_style: "dots"

commands:
  prefix: "/"
  history_file: "~/.local/share/cato/command_history"

logging:
  level: "WARNING"
  file_path: "~/.local/share/cato/cato.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  max_file_size_mb: 10
  backup_count: 3

paths:
  data_dir: "~/.local/share/cato"
  config_dir: "~/.config/cato"
  cache_dir: "~/.cache/cato"
```

## User Configuration Example
```yaml
# ~/.config/cato/config.yaml
# Only specify values that differ from defaults

llm:
  model: "gpt-4-turbo"
  temperature: 0.7

display:
  theme: "gruvbox-dark"
  timestamps: true

logging:
  level: "DEBUG"
```

## Runtime Configuration Access
```python
# Configuration is loaded once at startup and passed via dependency injection
class ChatService:
    def __init__(self, config: CatoConfig, llm: LLMProvider) -> None:
        self._config = config
        self._llm = llm
    
    async def send_message(self, message: str) -> str:
        return await self._llm.complete(
            message,
            temperature=self._config.llm.temperature,
            max_tokens=self._config.llm.max_tokens,
        )
```

## Path Expansion
All paths in configuration support:
- `~` for home directory
- Environment variables via `${VAR}`

```python
def expand_path(path: str | Path) -> Path:
    """Expand ~ and environment variables in path."""
    return Path(os.path.expandvars(os.path.expanduser(str(path))))
```

```



The spec does use Pydantic for validation - see lines 65-66, 288-289, and all the `BaseModel` classes with `Field` constraints. However, I see the confusion:

1. The `validate_with_fallback` function (lines 271-299) manually handles fallback logic outside Pydantic
2. The unknown keys handling re-validates with different settings

This is intentional to support the GENERAL_PRINCIPLES.md requirement: "Unrecognised config items should warn but not crash - continue with defaults." But the approach could be cleaner using Pydantic's built-in features.

Let me update the spec to use a more Pydantic-native approach:


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md
@@ -249,54 +249,138 @@
 
 ## Validation Behaviour
 
-### Unknown Keys
+All validation is handled by Pydantic. The config system uses Pydantic's features to enforce constraints and provide defaults.
+
+### Pydantic Model Configuration
 ```python
+from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo
+
 class CatoConfig(BaseModel):
-    model_config = ConfigDict(extra="forbid")
+    """Root configuration with validation."""
+    
+    model_config = ConfigDict(
+        extra="ignore",          # Ignore unknown keys (warn separately)
+        validate_default=True,   # Validate default values too
+        str_strip_whitespace=True,
+    )
+    
+    llm: LLMConfig
+    vector_store: VectorStoreConfig
+    storage: StorageConfig
+    display: DisplayConfig
+    commands: CommandConfig
+    logging: LoggingConfig
+    paths: PathConfig
+```
 
-# During validation
-try:
-    config = CatoConfig.model_validate(data)
-except ValidationError as e:
-    for error in e.errors():
-        if error["type"] == "extra_forbidden":
-            key = ".".join(str(loc) for loc in error["loc"])
-            logger.warning(f"Unknown config key '{key}', ignoring")
-    # Re-validate with extra="ignore" to continue
-    config = CatoConfig.model_validate(data, strict=False)
+### Field-Level Validation
+Pydantic handles all value constraints:
+```python
+class LLMConfig(BaseModel):
+    """LLM configuration with Pydantic validation."""
+    
+    provider: Literal["openai", "anthropic", "google", "ollama"]
+    model: str = Field(min_length=1)  # Non-empty string
+    temperature: float = Field(ge=0.0, le=2.0)
+    max_tokens: int = Field(ge=1, le=200000)
+    timeout_seconds: int = Field(ge=1, le=300)
 ```
 
-### Invalid Values
+### Cross-Field Validation
 ```python
-def validate_with_fallback(data: dict, defaults: dict) -> CatoConfig:
+class VectorStoreConfig(BaseModel):
+    """Vector store config with cross-field validation."""
+    
+    enabled: bool
+    chunk_size: int = Field(ge=100, le=10000)
+    chunk_overlap: int = Field(ge=0)
+    
+    @field_validator("chunk_overlap")
+    @classmethod
+    def overlap_less_than_size(cls, v: int, info: ValidationInfo) -> int:
+        """Ensure overlap is smaller than chunk size."""
+        if "chunk_size" in info.data and v >= info.data["chunk_size"]:
+            raise ValueError("chunk_overlap must be less than chunk_size")
+        return v
+```
+
+### Unknown Keys Warning
+```python
+def load_config_with_warnings(data: dict) -> CatoConfig:
     """
-    Validate config, falling back to defaults for invalid values.
+    Load config, warning about unknown keys.
     
     Parameters
     ----------
     data
-        User configuration data.
-    defaults
-        Default configuration data.
+        Raw config dict.
     
     Returns
     -------
     CatoConfig
-        Validated configuration, with defaults substituted for invalid values.
+        Validated config (unknown keys ignored).
+    """
+    # Check for unknown keys before Pydantic ignores them
+    warn_unknown_keys(data, CatoConfig)
+    
+    # Pydantic validates and ignores unknown keys
+    return CatoConfig.model_validate(data)
+
+
+def warn_unknown_keys(data: dict, model: type[BaseModel], path: str = "") -> None:
+    """Recursively warn about unknown keys in config."""
+    if not isinstance(data, dict):
+        return
+    
+    model_fields = set(model.model_fields.keys())
+    for key in data:
+        full_path = f"{path}.{key}" if path else key
+        if key not in model_fields:
+            logger.warning(f"Unknown config key '{full_path}', ignoring")
+        elif key in model_fields:
+            field_type = model.model_fields[key].annotation
+            # Recurse into nested models
+            if hasattr(field_type, "model_fields"):
+                warn_unknown_keys(data[key], field_type, full_path)
+```
+
+### Validation Error Handling
+```python
+def load_config(user_path: Path | None = None) -> CatoConfig:
+    """
+    Load and validate configuration.
+    
+    On validation error: log the error and exit (fail fast).
+    Invalid config should not silently use defaults—user must fix it.
     """
+    defaults = load_yaml(get_default_config_path())
+    user_config = load_yaml(user_path) if user_path else {}
+    merged = deep_merge(defaults, user_config)
+    merged = apply_env_overrides(merged)
+    
     try:
-        return CatoConfig.model_validate(data)
+        return load_config_with_warnings(merged)
     except ValidationError as e:
         for error in e.errors():
-            path = list(error["loc"])
-            logger.warning(
-                f"Invalid config value at '{'.'.join(map(str, path))}': "
-                f"{error['msg']}. Using default."
-            )
-            # Reset to default value
-            set_nested(data, path, get_nested(defaults, path))
-        
-        return CatoConfig.model_validate(data)
+            path = ".".join(str(loc) for loc in error["loc"])
+            logger.error(f"Config error at '{path}': {error['msg']}")
+        raise ConfigurationError("Invalid configuration. See errors above.")
+```
+
+### Default Values in Pydantic
+Defaults come from the YAML file, not from Pydantic `Field(default=...)`. This keeps all defaults in one place:
+```python
+# GOOD: Defaults in YAML, Pydantic validates
+class LLMConfig(BaseModel):
+    temperature: float = Field(ge=0.0, le=2.0)  # No default here
+
+# defaults.yaml provides the actual default:
+# llm:
+#   temperature: 1.0
+
+# BAD: Defaults scattered in code
+class LLMConfig(BaseModel):
+    temperature: float = Field(default=1.0, ge=0.0, le=2.0)  # Don't do this
 ```
 
 ## Default Configuration File

```



Updated `TECH_CONFIG_SYSTEM.md` to make Pydantic's role in validation explicit:

**Key changes:**
1. Added clear section header: "All validation is handled by Pydantic"
2. Updated `ConfigDict` to use `extra="ignore"` with a separate warning function
3. Added `warn_unknown_keys()` function that recursively checks for unknown keys before Pydantic ignores them
4. Changed error handling to fail fast on validation errors (invalid config = exit, not silent fallback)
5. Added section explaining that defaults live in YAML only, not in Pydantic `Field(default=...)` to keep the "no hard-coded defaults" principle
6. Showed examples of field-level validation with `Field(ge=..., le=...)` and cross-field validation with `@field_validator`