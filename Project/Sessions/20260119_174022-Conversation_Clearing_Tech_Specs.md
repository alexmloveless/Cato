USER:
are there tech specs for conversation clearing and the /clear commannd?

AGENT:
I'll search for technical specifications related to conversation clearing and the `/clear` command in the Cato repository.


**Grep Results:**

- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_PERFORMANCE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_COMMAND_FRAMEWORK.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_LISTS.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**




**File Glob Results:**

- **/home/alex/Documents/repos/Cato/Project/Spec/CONFIG_REFERENCE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/DATA_MODELS.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/GENERAL_PRINCIPLES.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/GLOSSARY.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/agents.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_LINE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CONFIGURATION.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_FILE_OPERATIONS.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_HELP_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_LISTS.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_PRODUCTIVITY.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_TTS.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_VECTOR_STORE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_WEB_SEARCH.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CLI.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CODE_ORGANISATION.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_COMMAND_FRAMEWORK.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DEVELOPMENT.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_DISPLAY.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_HELP_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_LLM_INTEGRATION.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_PERFORMANCE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_SPEC_LISTS.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_STORAGE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_VECTOR_STORE.md**


Let me read the relevant files that mention `/clear`:


**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md**
```
# Core Chat Specification

## Overview

The core chat system provides the primary LLM interaction loop, managing conversation history, context retrieval, and response display.

## LLM Provider Support

### Supported Providers

| Provider | Model Examples | API Key Environment Variable |
|----------|---------------|------------------------------|
| OpenAI | gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo | OPENAI_API_KEY |
| Anthropic | claude-3-opus, claude-3-sonnet, claude-3-haiku | ANTHROPIC_API_KEY |
| Google | gemini-pro, gemini-1.5-pro | GOOGLE_API_KEY |
| Ollama | llama2, mistral, codellama (local) | N/A (local) |

### Provider Selection
Provider selection is explicit:
- `llm.provider` selects the provider
- `llm.model` must match the provider's exact API model identifier

See CONFIG_REFERENCE.md for canonical config keys.

### LLM Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| model | gpt-4o-mini | Provider-specific | LLM model identifier |
| temperature | 1.0 | 0.0-2.0 | Response randomness |
| max_tokens | 4000 | >0 | Maximum response tokens |

## Conversation Management

### Message Types

| Role | Purpose |
|------|---------|
| system | System prompts defining assistant behavior |
| user | User input messages |
| assistant | LLM responses |

### Message Processing Flow

```
User Input
    ↓
Check for slash command (/) → Route to CommandParser
    ↓
Regular message processing:
    1. Add user message to history
    2. Retrieve relevant context from vector store
    3. Prepare messages for LLM API
    4. Generate response with progress indicator
    5. Add assistant response to history
    6. Store exchange in vector store
    7. Display formatted response
```

### System Prompts

#### Master/Base Prompt
A master base prompt is loaded from the package's `prompts/base_prompt.md` file. This establishes core assistant behavior.

**The master prompt is sacrosanct:**
- Contains only the minimum necessary for the model to do its job
- Does not include UI mechanics or Cato-specific knowledge
- Changes to the master prompt should be treated as code changes
- Should only be updated when absolutely necessary

The base prompt is automatically enhanced with:
- Current session timestamp (local and UTC)

#### User System Prompts
Additional system prompts can be loaded from files specified in configuration:
```yaml
llm:
  system_prompt_files:
    - ~/prompts/my_custom_prompt.md
    - ~/prompts/domain_knowledge.md
```

User prompts are **appended** to the master prompt (unless `override_base_prompt: true`).

#### Final System Prompt Structure
The generated system prompt has clear sections:
1. Master prompt (core behaviour)
2. User system prompts (appended)
3. Session metadata (timestamp, etc.)

### Context Retrieval

Before generating a response, the system:

1. **Builds search query** from recent non-command exchanges
   - Excludes messages starting with `/`
   - Uses configurable `search_context_window`

2. **Retrieves similar exchanges** from vector store
   - Uses similarity threshold from config
   - Returns up to `context_results` exchanges

3. **Injects context** into the API request when vector store is enabled and results pass the similarity threshold
4. **Displays context** based on `context_mode` (display-only)

### Context Display Modes

Controlled via `/showcontext` command:

| Mode | Behavior |
|------|----------|
| off | No context shown |
| on | Context excerpts displayed |
| summary | Only a count displayed |

When context is used, indicators appear before the response:
```
💭 Using context from 3 previous exchange(s):
   1. User: How do I configure... 
      Assistant: You can modify the...
```

## Response Generation

### Progress Indicator
While waiting for LLM response:
```
⠋ Generating response... (Press Ctrl+C to cancel)
```

### Timeout Handling
- Timeout: `llm.timeout_seconds` (default 60 seconds)
- On timeout: Show error message, return to prompt
- On Ctrl+C: Cancel request, return to prompt

### Dummy Mode
When `--dummy-mode` flag is set:
- Uses MockLLMBackend instead of real API
- Returns placeholder responses for testing
- Skips vector store writes

### Debug Mode
When `--debug` flag is set:
- Detailed logging of message processing
- Token estimation and timing
- API request/response details
- Context retrieval details

## Response Display

### Display Philosophy
**Response text must be directly copy-pasteable.**

- Do NOT use boxed/bordered panels that interfere with text selection
- Clear visual separation between exchanges without disrupting copy/paste
- Use delimiter lines and labels for clarity, not enclosing boxes

### Response Formatting

```
─ 🤖 Assistant ──────────────────────────────────────────────

Response content with **markdown** rendering

```python
def example():
    return "syntax highlighted"
```

──────────────────────────────────────────────────────────────
```

**Key points:**
- Header line with label and delimiter
- Response text is NOT enclosed in a box
- Markdown rendering applied to text
- Code blocks with syntax highlighting
- Footer delimiter to separate from next exchange

### Display Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| line_width | 80 | Terminal width for formatting |
| exchange_delimiter | "─" | Character for visual separation |
| exchange_delimiter_length | 60 | Length of delimiter line |

### Code Highlighting
- Automatic language detection from markdown fence
- Monokai theme when high_contrast enabled
- Default theme otherwise

## Conversation History

### In-Session History
- All messages stored in memory during session
- System messages preserved on `/clear`
- Arrow key navigation through input history

### Clear Command
`/clear` performs:
1. Remove all user/assistant messages
2. Keep system messages
3. Clear console screen
4. Show welcome message

### History Command
`/history [n]` displays:
- Last n messages (default: all)
- Excludes system messages
- Truncates long messages for readability

### Delete Command
`/delete [n]` removes:
- Last n user/assistant exchange pairs (default: 1)
- Preserves system messages

## Thread Continuation

### Continue Command
`/continue <thread_id>` allows resuming a previous conversation:

1. Validates thread_id exists in vector store
2. Clears current conversation (like `/clear`)
3. Loads all exchanges from the thread
4. Displays thread history to user
5. Sets thread continuation sequence number
6. New exchanges stored with incremented sequence

### Thread Identification
- Thread ID: UUID assigned at session start
- Session ID: UUID assigned at session start
- Thread Session ID: `{thread_id}_{session_id}` composite
- Continuation Sequence: Increments each time thread is continued

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Submit input |
| Up/Down | Navigate input history |
| Ctrl+C | Cancel current operation |
| Ctrl+D | Exit application |

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
For full help system behavior, navigation rules, and documentation requirements, see `SPEC_HELP_SYSTEM.md`.

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
/loglevel WARNING   # Set to WARNING
/loglevel ERROR     # Set to ERROR
```

### Context Commands

#### /showcontext
Toggle context display mode for all future exchanges.
```
/showcontext        # Toggle on/off (shows new state)
/showcontext on     # Enable context display with excerpts
/showcontext off    # Disable context display
/showcontext summary # Show only a count of retrieved context
```

**Behavior:**
- Acts as a **toggle** - calling `/showcontext` without arguments flips the current state
- When **on**: Context excerpts displayed before each response
- When **summary**: Only a count is displayed
- When **off**: No context information displayed (default)
- Context injection is always on when vector store is enabled and results pass the similarity threshold
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

### List Commands

See SPEC_LISTS.md for detailed list system documentation.

#### /lists, /ll
Show overview of all lists with item counts.
```
/lists                      # Show all lists overview
/ll                         # Short alias
```

#### /list, /l
Display items in one or all lists.
```
/list todo                  # Show items in todo list
/list                       # Show items from ALL lists
/l todo -s status           # Sort by status
/l todo -c work             # Filter by category
/l todo -S done             # Show done items
/l -p urgent                # Show urgent items across all lists
```

**Options:**
- `-s`: Sort field (priority, status, category, created, id)
- `-o`: Sort order (asc, desc)
- `-S`: Status filter (pending, active, in_progress, done, all)
- `-p`: Priority filter (urgent, high, medium, low)
- `-c`: Category filter
- `-t`: Tag filter

#### /add, /a
Add item to a list.
```
/add todo "Fix the bug"     # Add item
/a todo "Call dentist" -p high -c health
/a shopping "Milk" -t groceries
```

**Options:**
- `-p`: Priority (urgent, high, medium, low)
- `-S`: Status (pending, active, in_progress)
- `-c`: Category
- `-t`: Tag (repeatable)

#### /update, /u
Update an existing item (no list name needed, IDs are global).
```
/update 042 -S done         # Mark item 042 as done
/u 042 -p urgent            # Change priority
/u 042 -d "New description" # Update description
/u 042 -c work -t bug       # Update category and tags
```

**Options:**
- `-d`: Description
- `-S`: Status
- `-p`: Priority
- `-c`: Category
- `-t`: Replace all tags
- `-T`: Add tag
- `-R`: Remove tag

#### /remove, /rm
Remove an item (no list name needed, IDs are global).
```
/remove 042                 # Remove item 042
/rm 035                     # Short alias
```

#### /move, /mv
Move an item to a different list.
```
/move 042 backlog           # Move item 042 to backlog
/mv 035 archive             # Short alias
```

#### /newlist, /nl
Create a new list.
```
/newlist todo               # Create todo list
/nl shopping "Weekly groceries"
```

#### /dellist, /dl
Delete a list and all its items.
```
/dellist old_todos          # Delete list
/dl old_todos -f            # Force delete without confirmation
```

#### /clear
Clear items from a list.
```
/clear todo -S done         # Remove all done items
/clear shopping -f          # Remove all items (force)
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
| /lists | /ll |
| /list | /l |
| /add | /a |
| /update | /u |
| /remove | /rm |
| /move | /mv |
| /newlist | /nl |
| /dellist | /dl |
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

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_COMMAND_FRAMEWORK.md**
```
# Command Framework Technical Specification

## Overview
Cato uses a decorator-based command registration system. Commands are self-contained modules that register themselves on import, enabling easy addition of new commands without modifying core code.

## Command Protocol

### Base Interface
```python
from typing import Protocol
from dataclasses import dataclass

@dataclass
class CommandResult:
    """
    Result from command execution.
    
    Note: Uses dataclass rather than Pydantic as it's internal return data,
    not data crossing system boundaries.
    """
    success: bool
    message: str
    data: dict | None = None


class Command(Protocol):
    """
    Protocol for command implementations.
    
    Commands are stateless—all state accessed via injected dependencies.
    """
    
    @property
    def name(self) -> str:
        """Primary command name (without slash)."""
        ...
    
    @property
    def aliases(self) -> list[str]:
        """Alternative names for the command."""
        ...
    
    @property
    def description(self) -> str:
        """Brief description for help text."""
        ...
    
    @property
    def usage(self) -> str:
        """Usage pattern string."""
        ...
    
    async def execute(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        """
        Execute the command.
        
        Parameters
        ----------
        args
            Parsed arguments (command name excluded).
        context
            Execution context with dependencies.
        
        Returns
        -------
        CommandResult
            Result with success status and message.
        """
        ...
```

### Command Context
```python
@dataclass
class CommandContext:
    """
    Execution context providing access to application services.
    
    Injected at runtime—commands should not instantiate dependencies.
    Uses dataclass as it's a dependency container, not external data.
    """
    
    config: CatoConfig
    conversation: Conversation
    llm: LLMProvider
    vector_store: VectorStore | None
    storage: Storage
    display: Display
    
    # Current state
    cwd: Path  # Current working directory
    session_id: str
    thread_id: str | None
```

## Command Registration

### Decorator Pattern
```python
from typing import Callable, Type

# Global command registry
_COMMANDS: dict[str, Type[Command]] = {}
_ALIASES: dict[str, str] = {}  # alias -> primary name


def command(
    name: str,
    aliases: list[str] | None = None,
    description: str = "",
    usage: str = "",
) -> Callable[[Type], Type]:
    """
    Decorator to register a command class.
    
    Parameters
    ----------
    name
        Primary command name (without slash).
    aliases
        Alternative names.
    description
        Brief description for help.
    usage
        Usage pattern string.
    
    Returns
    -------
    Callable
        Decorator that registers the class.
    
    Example
    -------
    @command("help", aliases=["h", "?"], description="Show help")
    class HelpCommand:
        async def execute(self, args, context):
            ...
    """
    def decorator(cls: Type) -> Type:
        # Attach metadata to class
        cls._cmd_name = name
        cls._cmd_aliases = aliases or []
        cls._cmd_description = description
        cls._cmd_usage = usage
        
        # Register
        _COMMANDS[name] = cls
        for alias in (aliases or []):
            _ALIASES[alias] = name
        
        return cls
    return decorator
```

### Registry Access
```python
class CommandRegistry:
    """
    Central registry for command lookup and execution.
    
    Commands are discovered automatically when their modules are imported.
    """
    
    def __init__(self) -> None:
        self._commands = _COMMANDS
        self._aliases = _ALIASES
    
    def get(self, name: str) -> Type[Command] | None:
        """
        Look up a command by name or alias.
        
        Parameters
        ----------
        name
            Command name (with or without slash).
        
        Returns
        -------
        Type[Command] | None
            Command class if found.
        """
        # Strip leading slash if present
        name = name.lstrip("/")
        
        # Check aliases first
        if name in self._aliases:
            name = self._aliases[name]
        
        return self._commands.get(name)
    
    def list_commands(self) -> list[tuple[str, str, list[str]]]:
        """
        List all registered commands.
        
        Returns
        -------
        list[tuple[str, str, list[str]]]
            List of (name, description, aliases) tuples.
        """
        return [
            (name, cls._cmd_description, cls._cmd_aliases)
            for name, cls in sorted(self._commands.items())
        ]
    
    def resolve_alias(self, name: str) -> str:
        """Resolve an alias to its primary command name."""
        return self._aliases.get(name.lstrip("/"), name.lstrip("/"))
```

## Command Parsing

### Input Tokenization
```python
import shlex

def parse_command_input(input_text: str) -> tuple[str, list[str]] | None:
    """
    Parse user input into command name and arguments.
    
    Parameters
    ----------
    input_text
        Raw user input.
    
    Returns
    -------
    tuple[str, list[str]] | None
        (command_name, args) if input is a command, None otherwise.
    
    Examples
    --------
    >>> parse_command_input("/help")
    ("help", [])
    >>> parse_command_input('/web "search query" google')
    ("web", ["search query", "google"])
    >>> parse_command_input("hello")
    None
    """
    text = input_text.strip()
    
    # Must start with /
    if not text.startswith("/"):
        return None
    
    # Remove leading slash
    text = text[1:]
    
    # Handle empty command
    if not text:
        return None
    
    try:
        # Use shlex for shell-like tokenization
        tokens = shlex.split(text)
    except ValueError:
        # Unbalanced quotes - treat rest as single argument
        parts = text.split(maxsplit=1)
        tokens = [parts[0], parts[1]] if len(parts) > 1 else [parts[0]]
    
    command_name = tokens[0].lower()
    args = tokens[1:] if len(tokens) > 1 else []
    
    return (command_name, args)
```

### Argument Parsing
Commands can use argument parsers for complex arguments:

```python
from argparse import ArgumentParser, Namespace

class ListCommand:
    """Display list items with filtering and sorting."""

    def __init__(self) -> None:
        self._parser = ArgumentParser(prog="/list", add_help=False)
        self._parser.add_argument("list_name", nargs="?", default=None)
        self._parser.add_argument("-p", "--priority", choices=["urgent", "high", "medium", "low"])
        self._parser.add_argument("-s", "--sort", default="priority")
        self._parser.add_argument("-o", "--order", choices=["asc", "desc"], default="asc")
        self._parser.add_argument("-S", "--status", default="pending")
    
    async def execute(self, args: list[str], context: CommandContext) -> CommandResult:
        try:
            parsed = self._parser.parse_args(args)
        except SystemExit:
            return CommandResult(
                success=False,
                message=f"Invalid arguments. Usage: {self._cmd_usage}",
            )
        
        # Use parsed.category, parsed.priority, etc.
        ...
```

## Command Execution

### Execution Flow
```python
class CommandExecutor:
    """
    Executes commands with proper context and error handling.
    """
    
    def __init__(
        self,
        registry: CommandRegistry,
        context_factory: Callable[[], CommandContext],
    ) -> None:
        self._registry = registry
        self._context_factory = context_factory
    
    async def execute(self, input_text: str) -> CommandResult | None:
        """
        Parse and execute a command from user input.
        
        Parameters
        ----------
        input_text
            Raw user input.
        
        Returns
        -------
        CommandResult | None
            Result if input was a command, None if not a command.
        
        Raises
        ------
        CommandNotFoundError
            Unknown command name.
        CommandExecutionError
            Command failed during execution.
        """
        parsed = parse_command_input(input_text)
        if parsed is None:
            return None  # Not a command
        
        command_name, args = parsed
        
        # Look up command
        command_cls = self._registry.get(command_name)
        if command_cls is None:
            raise CommandNotFoundError(
                f"Unknown command: /{command_name}",
                context={"available": [c[0] for c in self._registry.list_commands()]},
            )
        
        # Create instance and execute
        command = command_cls()
        context = self._context_factory()
        
        try:
            return await command.execute(args, context)
        except CatoError:
            raise  # Let Cato errors propagate
        except Exception as e:
            raise CommandExecutionError(
                f"Command /{command_name} failed: {e}",
                context={"command": command_name, "args": args},
            ) from e
```

## Command Implementation Examples

### Simple Command
```python
@command("clear", description="Clear conversation and screen")
class ClearCommand:
    """Clear conversation history and terminal screen."""
    
    @property
    def name(self) -> str:
        return "clear"
    
    @property
    def aliases(self) -> list[str]:
        return []
    
    @property
    def description(self) -> str:
        return "Clear conversation and screen"
    
    @property
    def usage(self) -> str:
        return "/clear"
    
    async def execute(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        # Clear conversation (keep system prompt)
        context.conversation.messages.clear()
        
        # Clear screen
        context.display.clear()
        context.display.show_welcome()
        
        return CommandResult(success=True, message="Conversation cleared")
```

### Command with Arguments
```python
@command(
    "history",
    aliases=["h"],
    description="Show conversation history",
    usage="/history [count]",
)
class HistoryCommand:
    """Display conversation history."""
    
    @property
    def name(self) -> str:
        return "history"
    
    @property
    def aliases(self) -> list[str]:
        return ["h"]
    
    @property
    def description(self) -> str:
        return "Show conversation history"
    
    @property
    def usage(self) -> str:
        return "/history [count]"
    
    async def execute(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        # Parse optional count argument
        count = None
        if args:
            try:
                count = int(args[0])
                if count < 1:
                    raise ValueError()
            except ValueError:
                return CommandResult(
                    success=False,
                    message=f"Invalid count: {args[0]}. Must be a positive integer.",
                )
        
        # Get messages
        messages = context.conversation.messages
        if count:
            messages = messages[-count:]
        
        # Format and display
        for msg in messages:
            context.display.show_message(msg.role, msg.content)
        
        return CommandResult(
            success=True,
            message=f"Showing {len(messages)} messages",
        )
```

### Command with Subcommands
```python
@command(
    "help",
    aliases=["h", "?"],
    description="Show help information",
    usage="/help [topic]",
)
class HelpCommand:
    """Display help information."""
    # Help content structure and lookup are defined in TECH_HELP_SYSTEM.md.
    
    # Subcommand handlers
    _TOPICS = {
        "commands": "_show_commands",
        "lists": "_show_lists",
        "files": "_show_files",
        "model": "_ask_model",
    }
    
    async def execute(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        if not args:
            return await self._show_overview(context)
        
        topic = args[0].lower()
        handler_name = self._TOPICS.get(topic)
        
        if handler_name:
            handler = getattr(self, handler_name)
            return await handler(args[1:], context)
        
        return CommandResult(
            success=False,
            message=f"Unknown help topic: {topic}",
            data={"available": list(self._TOPICS.keys())},
        )
    
    async def _show_overview(self, context: CommandContext) -> CommandResult:
        # Show general help
        ...
    
    async def _ask_model(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        # Special handling for /help model "question"
        if not args:
            return CommandResult(
                success=False,
                message='Usage: /help model "your question"',
            )
        
        question = " ".join(args)
        # Load help docs, query model, return response
        ...
```

## Command Discovery

### Auto-Import Pattern
Commands are discovered by importing all modules in `cato/commands/`:

```python
# cato/commands/__init__.py
import importlib
import pkgutil
from pathlib import Path

def discover_commands() -> None:
    """
    Import all command modules to trigger registration.
    
    Called once at startup after core is initialised.
    """
    package_dir = Path(__file__).parent
    
    for module_info in pkgutil.iter_modules([str(package_dir)]):
        if not module_info.name.startswith("_"):
            importlib.import_module(f"cato.commands.{module_info.name}")
```

### File Structure
```
cato/commands/
├── __init__.py          # discover_commands()
├── base.py              # Command protocol, decorator, registry
├── core.py              # /help, /exit, /clear, /config
├── history.py           # /history, /delete, /showsys
├── files.py             # /attach, /pwd, /cd, /ls, /cat
├── export.py            # /writecode, /writemd, /writejson
├── vector.py            # /vadd, /vdoc, /vquery, /vstats
├── lists.py             # /list, /add, /update, /remove, etc.
├── web.py               # /web, /url
└── tts.py               # /speak, /speaklike
```

## Adding New Commands

To add a new command:

1. Create file in `cato/commands/` (or add to existing related file)
2. Import decorator: `from cato.commands.base import command`
3. Implement class with `@command` decorator
4. Command is auto-discovered on next startup

```python
# cato/commands/mycommand.py
from cato.commands.base import command, CommandContext, CommandResult

@command(
    "mycommand",
    aliases=["mc"],
    description="Do something useful",
    usage="/mycommand <arg>",
)
class MyCommand:
    """Implementation of mycommand."""
    
    @property
    def name(self) -> str:
        return "mycommand"
    
    @property
    def aliases(self) -> list[str]:
        return ["mc"]
    
    @property
    def description(self) -> str:
        return "Do something useful"
    
    @property
    def usage(self) -> str:
        return "/mycommand <arg>"
    
    async def execute(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        if not args:
            return CommandResult(
                success=False,
                message="Missing required argument",
            )
        
        # Do the thing
        result = await self._do_something(args[0], context)
        
        return CommandResult(
            success=True,
            message=f"Done: {result}",
            data={"result": result},
        )
```

## Error Handling

Commands should:
- Validate arguments before execution
- Return `CommandResult(success=False, ...)` for user errors
- Raise `CommandArgumentError` for invalid argument types
- Let other exceptions propagate (caught by executor)

```python
async def execute(self, args: list[str], context: CommandContext) -> CommandResult:
    # Validate required args
    if len(args) < 1:
        return CommandResult(
            success=False,
            message=f"Missing required argument. Usage: {self.usage}",
        )
    
    # Validate argument types
    try:
        count = int(args[0])
    except ValueError:
        raise CommandArgumentError(
            f"Expected integer, got: {args[0]}",
            context={"argument": "count", "value": args[0]},
        )
    
    # Execute - let other errors propagate
    result = await context.storage.get_items(count)
    return CommandResult(success=True, message="OK", data={"items": result})
```

```



Yes, there are specs for the `/clear` command. Here's what I found:

## Functional Spec (SPEC_COMMAND_SYSTEM.md)
- Basic command definition at lines 73-82
- Behavior specified: removes all user/assistant messages, preserves system messages, clears terminal screen, displays welcome message

## Functional Spec (SPEC_CORE_CHAT.md)
- Conversation history clearing behavior at lines 200-205
- More detailed flow: performs 4 steps in order

## Technical Spec (TECH_COMMAND_FRAMEWORK.md)
- Implementation example at lines 371-404
- Shows the `ClearCommand` class structure with the `@command` decorator
- Demonstrates how to clear conversation messages and screen through the `CommandContext`

The specs cover both the user-facing behavior (functional) and implementation requirements (technical) for `/clear`. However, I didn't find a separate, dedicated technical specification document specifically for conversation clearing—it's integrated into the command system specs.

USER:
impement it

AGENT:
I'll implement the `/clear` command. Let me first check the current project state and structure.


**Files Read:**

**/home/alex/Documents/repos/Cato/Project/PROGRESS.md**
```
# Cato Implementation Progress

This file tracks implementation progress across agent sessions. **Agents MUST update this file** when completing tasks.

## How to Use This File

### For Agents Starting a Session
1. Read this entire file to understand current state
2. Check `git branch` to confirm you're on the correct branch
3. Pick up where the last session left off (see "Current Focus" below)
4. If starting a new phase, create the feature branch first

### For Agents Completing Work
1. Mark completed items with `[x]`
2. Update "Current Focus" section
3. Update "Last Updated" timestamp
4. Commit this file with your other changes

### Branch Strategy
- Each phase gets a feature branch: `feature/phase-NN-<name>`
- Work on the phase branch until all tasks complete
- Merge to `main` when phase is fully complete and tested
- Example: `feature/phase-01-core`, `feature/phase-02-storage`

---

## Current Focus

**Phase**: Phase 13 complete (✅ WEB & TTS)
**Branch**: `feature/phase-13-web-tts`
**Next Task**: Phase 14 - Thread Continuation or Phase 15 - Testing
**Status**: Web search and TTS features implemented with help docs
**Blockers**: None

**Last Updated**: 2026-01-16T12:00:00Z

---

## Phase Overview

| Phase | Name | Status | Branch |
|-------|------|--------|--------|
| 1 | Project Skeleton & Core | ✅ Complete | `feature/phase-01-core` |
| 2 | Storage Layer | ✅ Complete | `feature/phase-02-storage` |
| 3 | Provider Layer | ✅ Complete | `feature/phase-03-providers` |
| 4 | Display Layer | ✅ Complete | `feature/phase-04-display` |
| 5 | Command Framework | ✅ Complete | `feature/phase-05-commands` |
| 6 | Core Services | ⬜ Not Started | `feature/phase-08-core-commands` |
| 7 | Bootstrap & REPL | ⬜ Not Started | `feature/phase-08-core-commands` |
| 8 | Core Commands (MVP) | ⬜ Not Started | `feature/phase-08-core-commands` |
| 9 | Vector Store | ✅ Complete | `feature/phase-09-vector` |
| 10 | Productivity System | ✅ Complete | `feature/phase-10-productivity` |
| 11 | Help System | ✅ Complete | `feature/phase-11-help` |
| 12 | File Operations | ⬜ Not Started | `feature/phase-12-files` |
| 13 | Web & TTS | ✅ Complete | `feature/phase-13-web-tts` |
| 14 | Thread Continuation | ⬜ Not Started | `feature/phase-14-threads` |
| 15 | Testing & Validation | ⬜ Not Started | `feature/phase-15-testing` |
| 16 | Documentation & Polish | ⬜ Not Started | `feature/phase-16-docs` |

Status Legend: ⬜ Not Started | 🔄 In Progress | ✅ Complete | ⏸️ Blocked

---

## Detailed Task Tracking

### Phase 1: Project Skeleton & Core
**Goal**: Runnable entry point with config loading and error hierarchy.

#### 1.1 Project Setup
- [x] Create `pyproject.toml` with uv/PEP 621 metadata
- [x] Define all dependencies
- [x] Create directory structure per `TECH_ARCHITECTURE.md`
- [x] Create `cato/__init__.py`
- [x] Create `cato/__main__.py`
- [x] Create `cato/main.py`

#### 1.2.1 Exception Hierarchy
- [x] Create `cato/core/__init__.py`
- [x] Create `cato/core/exceptions.py` with full hierarchy
- [x] Create `cato/core/README.md`

#### 1.2.2 Logging Setup
- [x] Create `cato/core/logging.py`

#### 1.2.3 Shared Types
- [x] Create `cato/core/types.py`

#### 1.2.4 Configuration System
- [x] Create `cato/core/config.py` with Pydantic models
- [x] Create `cato/resources/defaults.yaml`

---

### Phase 2: Storage Layer
**Goal**: SQLite database operational for productivity data.

#### 2.1 Database Foundation
- [x] Create `cato/storage/__init__.py`
- [x] Create `cato/storage/README.md`
- [x] Create `cato/storage/database.py`
- [x] Create `cato/storage/migrations.py`

#### 2.2 Repository Protocol & Implementations
- [x] Create `cato/storage/repositories/__init__.py`
- [x] Create `cato/storage/repositories/base.py`
- [x] Create `cato/storage/repositories/tasks.py`
- [x] Create `cato/storage/repositories/lists.py`
- [x] Create `cato/storage/repositories/sessions.py`

#### 2.3 Storage Service
- [x] Create `cato/storage/service.py`

---

### Phase 3: Provider Layer
**Goal**: LLM providers abstracted and swappable.

#### 3.1 LLM Provider Protocol
- [x] Create `cato/providers/__init__.py`
- [x] Create `cato/providers/README.md`
- [x] Create `cato/providers/llm/__init__.py`
- [x] Create `cato/providers/llm/base.py`

#### 3.2 Provider Implementations
- [x] Create `cato/providers/llm/openai.py`
- [x] Create `cato/providers/llm/anthropic.py`
- [x] Create `cato/providers/llm/google.py`
- [x] Create `cato/providers/llm/ollama.py`

#### 3.3 Provider Factory
- [x] Create `cato/providers/llm/factory.py`

---

### Phase 4: Display Layer
**Goal**: Rich terminal output and prompt_toolkit input.

#### 4.1 Display Protocol
- [x] Create `cato/display/__init__.py`
- [x] Create `cato/display/README.md`
- [x] Create `cato/display/base.py`

#### 4.2 Rich Implementation
- [x] Create `cato/display/console.py`
- [x] Create `cato/display/themes.py`

#### 4.3 Input Handler
- [x] Create `cato/display/input.py`

#### 4.4 Response Formatting
- [x] Formatting integrated in console.py

---

### Phase 5: Command Framework
**Goal**: Slash command registration and execution infrastructure.

#### 5.1 Command Protocol & Registry
- [x] Create `cato/commands/__init__.py`
- [x] Create `cato/commands/README.md`
- [x] Create `cato/commands/base.py`
- [x] Create `cato/commands/registry.py`
- [x] Create `cato/commands/parser.py`

#### 5.2 Command Executor
- [x] Create `cato/commands/executor.py`

#### 5.3 Command Discovery
- [x] Command discovery via decorator registration

---

### Phase 6: Core Services
**Goal**: Chat service orchestrating LLM interactions.

#### 6.1 Conversation Management
- [x] Create `cato/services/__init__.py`
- [x] Create `cato/services/README.md`
- [x] Create `cato/services/conversation.py`
- [x] Create `cato/resources/system_prompt.txt`

#### 6.2 Chat Service
- [x] Create `cato/services/chat.py`

---

### Phase 7: Application Bootstrap & REPL
**Goal**: Runnable application with basic chat.

#### 7.1 Bootstrap Module
- [x] Create `cato/bootstrap.py`

#### 7.2 Application Class & REPL
- [x] Create `cato/app.py`

#### 7.3 CLI Entry Point
- [ ] Update `cato/main.py` with CLI arguments

---

### Phase 8: Core Commands (MVP)
**Goal**: Essential commands for usable chat client.

#### 8.1 Core Commands
- [x] Create `cato/commands/core.py` (/help, /exit, /clear, /config)

#### 8.2 History Commands
- [x] Create `cato/commands/history.py`

#### 8.3 Context Commands
- [ ] Create `cato/commands/context.py`

**🎯 MVP CHECKPOINT**: After Phase 8, basic chat should be functional.

---

### Phase 9: Vector Store Integration
**Goal**: Conversation memory with similarity search.

#### 9.1 Vector Store Protocol
- [x] Create `cato/storage/vector/__init__.py`
- [x] Create `cato/storage/vector/base.py`
- [x] Create `cato/storage/embedding/__init__.py`
- [x] Create `cato/storage/embedding/base.py`
- [x] Create `cato/storage/embedding/openai.py`
- [x] Create `cato/storage/embedding/ollama.py`

#### 9.2 ChromaDB Implementation
- [x] Create `cato/storage/vector/chromadb.py`
- [x] Create `cato/storage/vector/utils.py` (TextChunker, DocumentProcessor)

#### 9.3 Vector Commands
- [x] Create `cato/commands/vector.py`

#### 9.4 Chat Service Integration
- [x] Update `cato/services/chat.py` for context retrieval and exchange storage
- [x] Update `bootstrap.py` with vector store factory functions
- [x] Update `app.py` to inject vector_store into commands

---

### Phase 10: Productivity System
**Goal**: Task and list management.

#### 10.1 Productivity Service
- [x] Create `cato/services/productivity.py`

#### 10.2 Productivity Commands
- [x] Create `cato/commands/productivity.py` with /st and /list commands

#### 10.3 Productivity Agent (Optional)
- [ ] Deferred - MVP uses direct repository queries

---

### Phase 11: Help System
**Goal**: Comprehensive in-app help.

#### 11.1 Help Content Structure
- [x] Create `cato/resources/help/index.yaml`
- [x] Create `cato/resources/help/topics/overview.md`
- [x] Create `cato/resources/help/topics/commands.md`
- [x] Create command help files for all commands

#### 11.2 Help Service
- [x] Create `cato/services/help.py`

#### 11.3 Help Command Completion
- [x] Update `cato/commands/core.py` with full /help implementation
- [x] Implement /help model for LLM-powered help queries

---

### Phase 12: File Operations
**Goal**: File commands for context attachment and export.

#### 12.1 File Commands
- [ ] Create `cato/commands/files.py`

#### 12.2 Export Commands
- [ ] Create `cato/commands/export.py`

---

### Phase 13: Web & TTS Features (Optional)
**Goal**: Optional external integrations.

#### 13.1 Web Search
- [x] Create `cato/providers/search/__init__.py`
- [x] Create `cato/providers/search/base.py`
- [x] Create `cato/providers/search/duckduckgo.py`
- [x] Create `cato/services/web.py`
- [x] Create `cato/commands/web.py`

#### 13.2 TTS
- [x] Create `cato/providers/tts/__init__.py`
- [x] Create `cato/providers/tts/base.py`
- [x] Create `cato/providers/tts/openai.py`
- [x] Create `cato/services/tts.py`
- [x] Create `cato/commands/tts.py`

#### 13.3 Help Documentation
- [x] Create help docs for /web, /url, /url_store
- [x] Create help docs for /speak, /speaklike
- [x] Update help index.yaml with new categories and commands
- [x] Update commands.md topic with new command listings

---

### Phase 14: Thread Continuation & Sessions (Optional)
**Goal**: Resume previous conversations.

#### 14.1 Thread Commands
- [ ] Update `cato/commands/context.py` with /continue
- [ ] Update `cato/services/chat.py` for thread loading

---

### Phase 15: Testing & Validation
**Goal**: Test coverage for core functionality.

#### 15.1 Test Infrastructure
- [ ] Create `tests/__init__.py`
- [ ] Create `tests/conftest.py`

#### 15.2 Unit Tests
- [ ] Create `tests/unit/test_config.py`
- [ ] Create `tests/unit/test_exceptions.py`
- [ ] Create `tests/unit/test_commands.py`
- [ ] Create `tests/unit/test_repositories.py`

#### 15.3 Integration Tests
- [ ] Create `tests/integration/test_chat.py`
- [ ] Create `tests/integration/test_productivity.py`
- [ ] Create `tests/integration/test_vector.py`

#### 15.4 Validation
- [ ] Help system consistency checks pass
- [ ] All registered commands have help entries

---

### Phase 16: Documentation & Polish
**Goal**: Production-ready documentation.

#### 16.1 Code Documentation
- [ ] README.md for each module directory
- [ ] All public functions have NumPy docstrings

#### 16.2 User Documentation
- [ ] Update top-level README.md
- [ ] Create CHANGELOG.md
- [ ] Sync CONFIG_REFERENCE.md with implementation

#### 16.3 AI Navigation
- [ ] Update AGENTS.md/WARP.md with actual (not planned) structure
- [ ] Add agents.md to subdirectories

---

## Session Log

Record significant sessions here for continuity.

| Date | Agent/User | Summary |
|------|------------|---------|
| 2026-01-15 | Claude | Created implementation plan and progress tracking system |
| 2026-01-15 | Claude | Phase 1 complete: project skeleton, exceptions, logging, types, config |
| 2026-01-15 | Claude | Phase 2 complete: storage layer with SQLite, repositories, migrations |
| 2026-01-15 | Claude | Phase 3 complete: provider layer with OpenAI, Anthropic, Google, Ollama |
| 2026-01-15 | Claude | Phase 4 complete: display layer with Rich output and prompt_toolkit input |
| 2026-01-15 | Claude | Phase 5 complete: command framework with decorator registration |

| 2026-01-15 | Claude | Phase 8 complete: core services with Conversation and ChatService |
| 2026-01-15 | Claude | Phase 8 complete: bootstrap module, Application class, REPL loop |
| 2026-01-15 | Claude | Phase 8 complete: core commands (/help, /exit, /clear, /config, /info) |
| 2026-01-15 | Claude | Phase 9 complete: vector store with ChromaDB, embeddings, context retrieval |
| 2026-01-15 | Claude | Phase 10 complete: productivity service and commands (/st, /list) |
| 2026-01-15 | Claude | Phase 11 complete: comprehensive help system with markdown docs and /help model |
| 2026-01-16 | Claude | Phase 13 complete: web search (/web, /url, /url_store) and TTS (/speak, /speaklike) with DuckDuckGo and OpenAI providers |

```




```bash
git branch
```

**Current Output:**
```
  feature/cli-specs
  feature/codebase-review-2026-01-15
  feature/display-style-config
  feature/help-system-specs
  feature/phase-01-core
  feature/phase-02-storage
  feature/phase-03-providers
  feature/phase-04-display
  feature/phase-05-commands
  feature/phase-06-services
  feature/phase-07-bootstrap
  feature/phase-08-core-commands
  feature/phase-09-vector
  feature/phase-10-productivity
  feature/phase-11-help
  feature/phase-12-files
  feature/phase-13-web-tts
  feature/readme-intent
  feature/spec-consistency
  fix/spec-config-consistency
* main
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
(END)<|cursor|>
```

Subagent: 43233c49-3987-4ef9-98da-2b90259e346e

I can see the `git branch` command is running and showing output in a pager. The current branch is **main** (indicated by the asterisk). Let me exit this pager to complete the task.

```
%                                                                                          
```

Perfect. The command has exited. The current branch is **main**.

According to PROGRESS.md, the `/clear` command was already implemented in Phase 8 (line 205). Let me check if it actually exists:


**File Glob Results:**

- **/home/alex/Documents/repos/Cato/cato/commands/__init__.py**
- **/home/alex/Documents/repos/Cato/cato/commands/base.py**
- **/home/alex/Documents/repos/Cato/cato/commands/context.py**
- **/home/alex/Documents/repos/Cato/cato/commands/core.py**
- **/home/alex/Documents/repos/Cato/cato/commands/executor.py**
- **/home/alex/Documents/repos/Cato/cato/commands/files.py**
- **/home/alex/Documents/repos/Cato/cato/commands/lists.py**
- **/home/alex/Documents/repos/Cato/cato/commands/parser.py**
- **/home/alex/Documents/repos/Cato/cato/commands/productivity.py**
- **/home/alex/Documents/repos/Cato/cato/commands/registry.py**
- **/home/alex/Documents/repos/Cato/cato/commands/tts.py**
- **/home/alex/Documents/repos/Cato/cato/commands/vector.py**
- **/home/alex/Documents/repos/Cato/cato/commands/web.py**




**Grep Results:**

- **/home/alex/Documents/repos/Cato/cato/commands/core.py**


Let me check the existing implementation:


**Files Read:**

**/home/alex/Documents/repos/Cato/cato/commands/core.py**
```
"""
Core commands for essential application functionality.

This module implements the most basic commands needed for a functional
chat client: help, exit, clear, and config display.
"""

import logging

from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command
from cato.services.help import HelpService

logger = logging.getLogger(__name__)


@command(name="help", aliases=["h", "?"])
async def help_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Display help information about commands and topics.

    Usage: 
      /help                    # Show overview
      /help commands           # List all commands
      /help <topic>            # Show topic or category
      /help <command>          # Show command help
      /help model "question"   # Ask model about Cato

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Query (topic, category, or command) or 'model' with question.

    Returns
    -------
    CommandResult
        Help information to display.
    """
    # Initialize HelpService
    help_service = HelpService()
    
    # Handle /help model "question"
    if args and args[0] == "model":
        if len(args) < 2:
            return CommandResult(
                success=False,
                message="Usage: /help model \"your question\""
            )
        
        question = " ".join(args[1:])
        
        # Get all help files for context
        help_files = help_service.get_all_help_files()
        
        # Build context from help files
        context = "# Cato Help Documentation\n\n"
        for file_path, content in help_files:
            context += f"## {file_path}\n\n{content}\n\n---\n\n"
        
        # Create one-off LLM query
        try:
            from cato.core.types import Message
            
            messages = [
                Message(
                    role="system",
                    content="You are a helpful assistant for Cato, a terminal-first LLM chat client. "
                            "Answer questions strictly based on the help documentation provided. "
                            "If the answer is not in the documentation, say so."
                ),
                Message(
                    role="user",
                    content=f"{context}\n\nQuestion: {question}"
                )
            ]
            
            # Use LLM provider directly (don't add to conversation history)
            result = await ctx.llm.complete(messages=messages)
            
            return CommandResult(
                success=True,
                message=f"**Help Model Response:**\n\n{result.content}"
            )
        except Exception as e:
            logger.error(f"Failed to query help model: {e}")
            return CommandResult(
                success=False,
                message=f"Failed to query help model: {e}"
            )
    
    # Regular help query
    query = args[0] if args else None
    content = help_service.get_help_content(query)
    
    if content:
        return CommandResult(success=True, message=content)
    
    # Not found - provide suggestions
    suggestions = help_service.get_suggestions(query) if query else []
    
    error_msg = f"Help topic not found: {query}\n\n"
    if suggestions:
        error_msg += "Did you mean:\n"
        for suggestion in suggestions:
            error_msg += f"- /help {suggestion}\n"
    else:
        error_msg += "Try:\n- /help commands - List all commands\n- /help <category> - Show category commands"
    
    return CommandResult(success=False, message=error_msg.strip())


@command(name="exit", aliases=["quit", "q"])
async def exit_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Exit the application.

    Usage: /exit

    Cleanly shuts down Cato and returns to the terminal.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Command arguments (unused).

    Returns
    -------
    CommandResult
        Exit confirmation message.
    """
    return CommandResult(
        success=True,
        message="Exiting Cato...",
        data={"should_exit": True}
    )


@command(name="clear", aliases=["cls"])
async def clear_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Clear the conversation history.

    Usage: /clear

    Removes all messages from the current conversation, keeping only
    the system prompt. The next message will start a fresh conversation.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Command arguments (unused).

    Returns
    -------
    CommandResult
        Confirmation message.
    """
    # TODO: Implement conversation clearing when conversation service is ready
    return CommandResult(
        success=True,
        message="Conversation clearing not yet implemented."
    )


@command(name="config", aliases=["cfg"])
async def config_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Display current configuration.

    Usage: /config [section]

    Without arguments, shows key configuration values.
    With a section name (llm, display, storage), shows detailed config for that section.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Optional section name.

    Returns
    -------
    CommandResult
        Configuration information.
    """
    config = ctx.config

    # Show specific section
    if args:
        section = args[0].lower()
        
        if section == "llm":
            info = f"""# LLM Configuration

**Provider**: {config.llm.provider}
**Model**: {config.llm.model}
**Temperature**: {config.llm.temperature}
**Max Tokens**: {config.llm.max_tokens}
**Timeout**: {config.llm.timeout_seconds}s
"""
        elif section == "display":
            info = f"""# Display Configuration

**Theme**: {config.display.theme}
**Markdown**: {'enabled' if config.display.markdown_enabled else 'disabled'}
**Code Theme**: {config.display.code_theme}
**Prompt**: {config.display.prompt_symbol}
"""
        elif section == "storage":
            info = f"""# Storage Configuration

**Database**: {config.storage.database_path}
**Backup**: {'enabled' if config.storage.backup_enabled else 'disabled'}
"""
        elif section == "commands":
            info = f"""# Commands Configuration

**Prefix**: {config.commands.prefix}
**History File**: {config.commands.history_file}
"""
        else:
            return CommandResult(
                success=False,
                message=f"Unknown config section: {section}\\n"
                        "Available sections: llm, display, storage, commands"
            )
        
        return CommandResult(success=True, message=info.strip())
    
    # Show overview
    info = f"""# Cato Configuration

**LLM Provider**: {config.llm.provider} ({config.llm.model})
**Theme**: {config.display.theme}
**Database**: {config.storage.database_path}
**Debug Mode**: {'enabled' if config.debug else 'disabled'}

Use `/config <section>` for detailed configuration.
Available sections: llm, display, storage, commands
"""
    
    return CommandResult(success=True, message=info.strip())


@command(name="info", aliases=["about"])
async def info_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Display information about Cato.

    Usage: /info

    Shows version, current session stats, and system information.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Command arguments (unused).

    Returns
    -------
    CommandResult
        Application information.
    """
    message_count = ctx.chat_service.get_message_count()
    
    info = f"""# Cato - Terminal LLM Chat Client

**Version**: 0.1.0
**Provider**: {ctx.chat_service.provider.name}
**Model**: {ctx.chat_service.provider.model}

**Current Session**:
- Messages: {message_count}
- Storage: {ctx.config.storage.database_path}

Cato is a terminal-first LLM chat client with conversation memory,
productivity features, and extensible command system.
"""

    return CommandResult(success=True, message=info.strip())


@command(name="loglevel", aliases=["log"])
async def loglevel_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Show or change the logging level.

    Usage:
      /loglevel              # Show current level
      /loglevel <level>      # Set level (DEBUG, INFO, WARNING, ERROR)

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Optional log level to set.

    Returns
    -------
    CommandResult
        Current or updated log level.
    """
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]

    # Show current level
    if not args:
        current_level = logging.getLogger().level
        level_name = logging.getLevelName(current_level)

        return CommandResult(
            success=True,
            message=f"Current log level: **{level_name}**\n\n"
                   f"Available levels: {', '.join(valid_levels)}\n"
                   f"Usage: /loglevel <level>"
        )

    # Set new level
    new_level = args[0].upper()

    if new_level not in valid_levels:
        return CommandResult(
            success=False,
            message=f"Invalid log level: {new_level}\n"
                   f"Valid levels: {', '.join(valid_levels)}"
        )

    # Update logging level
    logging.getLogger().setLevel(getattr(logging, new_level))
    logger.info(f"Log level changed to {new_level}")

    return CommandResult(
        success=True,
        message=f"✓ Log level set to **{new_level}**"
    )

```



The command is registered but not implemented (lines 164-168 show a TODO). Let me check what the conversation service looks like and then implement it:


**Files Read:**

**/home/alex/Documents/repos/Cato/cato/services/conversation.py**
```
"""
Conversation management for chat sessions.

This module provides the Conversation class for managing message history,
system prompts, and token-aware truncation.
"""

from dataclasses import dataclass, field
from typing import Callable

from cato.core.types import Message


@dataclass
class Conversation:
    """
    Manages conversation state and history.

    This class tracks the system prompt and message history for a chat session,
    providing methods to add messages and truncate history to fit within token limits.

    Parameters
    ----------
    system_prompt : str
        System prompt to prepend to all LLM requests.
    messages : list[Message], optional
        Initial message history (default: empty list).

    Attributes
    ----------
    system_prompt : str
        Current system prompt.
    messages : list[Message]
        Conversation message history (user and assistant messages only).
    """

    system_prompt: str
    messages: list[Message] = field(default_factory=list)

    def add_user_message(self, content: str) -> None:
        """
        Add a user message to conversation history.

        Parameters
        ----------
        content : str
            User message content.
        """
        self.messages.append(Message(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        """
        Add an assistant response to conversation history.

        Parameters
        ----------
        content : str
            Assistant message content.
        """
        self.messages.append(Message(role="assistant", content=content))

    def to_messages(self) -> list[Message]:
        """
        Get full message list for LLM request.

        Returns the system prompt as the first message, followed by all
        conversation messages.

        Returns
        -------
        list[Message]
            Complete message list (system + history).
        """
        return [Message(role="system", content=self.system_prompt)] + self.messages

    def truncate_to_tokens(self, max_tokens: int, counter: Callable[[str], int]) -> None:
        """
        Truncate conversation history to fit within token limit.

        Removes oldest messages (after system prompt) until the total token count
        is within the specified limit. Always preserves the system prompt and the
        most recent exchange (last 2 messages).

        Parameters
        ----------
        max_tokens : int
            Maximum allowed token count.
        counter : Callable[[str], int]
            Function to count tokens in text (e.g., provider.count_tokens).

        Notes
        -----
        - System prompt is always kept
        - Last 2 messages are preserved when possible
        - Removes messages from oldest to newest
        """
        # Keep removing oldest messages until we're under the limit
        # Always keep at least the last 2 messages (most recent exchange)
        while self._count_tokens(counter) > max_tokens and len(self.messages) > 2:
            self.messages.pop(0)

    def _count_tokens(self, counter: Callable[[str], int]) -> int:
        """
        Count total tokens in conversation (system + all messages).

        Parameters
        ----------
        counter : Callable[[str], int]
            Token counting function.

        Returns
        -------
        int
            Total token count.
        """
        total = counter(self.system_prompt)
        for msg in self.messages:
            total += counter(msg.content)
        return total

    def clear(self) -> None:
        """
        Clear all messages from conversation history.

        The system prompt is preserved.
        """
        self.messages.clear()

    def message_count(self) -> int:
        """
        Get the number of messages in history (excluding system prompt).

        Returns
        -------
        int
            Message count.
        """
        return len(self.messages)

```

**/home/alex/Documents/repos/Cato/cato/commands/base.py**
```
"""Command base types and protocol."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from cato.core.config import CatoConfig


@dataclass
class CommandResult:
    """
    Result from command execution.
    
    Note: Uses dataclass as it's internal return data, not external.
    
    Parameters
    ----------
    success : bool
        Whether command succeeded.
    message : str
        Result message.
    data : dict[str, Any] | None, optional
        Optional result data.
    """
    
    success: bool
    message: str
    data: dict[str, Any] | None = None


@dataclass
class CommandContext:
    """
    Execution context providing access to application services.
    
    Injected at runtime—commands should not instantiate dependencies.
    Uses dataclass as it's a dependency container, not external data.
    
    Parameters
    ----------
    config : CatoConfig
        Application configuration.
    conversation : Conversation
        Current conversation state.
    llm : LLMProvider
        LLM provider instance.
    vector_store : VectorStore | None
        Vector store if enabled.
    storage : Storage
        Storage service.
    display : Display
        Display implementation.
    chat : ChatService
        Chat service for accessing context state.
    cwd : Path
        Current working directory.
    session_id : str
        Current session ID.
    thread_id : str | None
        Current thread ID if any.
    registry : CommandRegistry | None
        Command registry for command lookup.
    """
    
    config: "CatoConfig"
    conversation: Any  # Will be Conversation from services
    llm: Any  # Will be LLMProvider
    vector_store: Any | None  # Will be VectorStore
    storage: Any  # Will be Storage
    display: Any  # Will be Display
    chat: Any  # Will be ChatService
    cwd: Path = field(default_factory=lambda: Path.cwd())
    session_id: str = ""
    thread_id: str | None = None
    registry: Any | None = None  # Will be CommandRegistry


class Command(Protocol):
    """
    Protocol for command implementations.
    
    Commands are stateless—all state accessed via injected dependencies.
    """
    
    @property
    def name(self) -> str:
        """Primary command name (without slash)."""
        ...
    
    @property
    def aliases(self) -> list[str]:
        """Alternative names for the command."""
        ...
    
    @property
    def description(self) -> str:
        """Brief description for help text."""
        ...
    
    @property
    def usage(self) -> str:
        """Usage pattern string."""
        ...
    
    async def execute(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        """
        Execute the command.
        
        Parameters
        ----------
        args : list[str]
            Parsed arguments (command name excluded).
        context : CommandContext
            Execution context with dependencies.
        
        Returns
        -------
        CommandResult
            Result with success status and message.
        """
        ...

```

**/home/alex/Documents/repos/Cato/cato/display/console.py**
```
"""Rich-based terminal display implementation."""

import logging
from typing import Any

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.spinner import Spinner
from rich.syntax import Syntax
from rich.table import Table

from cato.core.config import DisplayConfig
from cato.display.base import DisplayMessage
from cato.display.themes import load_theme

logger = logging.getLogger(__name__)


class RichDisplay:
    """
    Rich-based terminal display implementation.
    
    Parameters
    ----------
    config : DisplayConfig
        Display configuration.
    """
    
    def __init__(self, config: DisplayConfig) -> None:
        self._config = config
        theme = load_theme(config.theme, config.style_overrides)
        self._console = Console(theme=theme, width=config.max_width, force_terminal=True)
    
    def show_message(self, message: DisplayMessage) -> None:
        """Display a message with role-based styling."""
        prefix = self._get_prefix(message.role)
        style = message.role

        if self._config.timestamps and message.timestamp:
            timestamp = message.timestamp.strftime("%H:%M")
            prefix = f"[dim]{timestamp}[/dim] {prefix}"

        # Add spacing before message
        self._console.print()

        if message.role == "assistant" and self._config.markdown_enabled:
            self._console.print(prefix, style=style)
            self._console.print(Markdown(message.content, code_theme=self._config.code_theme))
            # Add horizontal rule after assistant response
            self._console.print()
            self._console.print(Rule(style="dim"))
        else:
            self._console.print(f"{prefix} {message.content}", style=style)
            # Add spacing after user messages
            if message.role == "user":
                self._console.print()
    
    def _get_prefix(self, role: str) -> str:
        """Get display prefix for role."""
        prefixes = {
            "user": "You:",
            "assistant": "Cato:",
            "system": "System:",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
        }
        return prefixes.get(role, "")
    
    def show_error(self, error: str, details: str | None = None) -> None:
        """Display an error message."""
        self._console.print(f"❌ {error}", style="error")
        if details:
            self._console.print(f"   {details}", style="dim")
    
    def show_warning(self, warning: str) -> None:
        """Display a warning."""
        self._console.print(f"⚠️  {warning}", style="warning")
    
    def show_info(self, info: str) -> None:
        """Display info message."""
        self._console.print(f"ℹ️  {info}", style="info")
    
    def show_markdown(self, content: str) -> None:
        """Render and display markdown."""
        md = Markdown(content, code_theme=self._config.code_theme)
        self._console.print(md)
    
    def show_code(self, code: str, language: str | None = None) -> None:
        """Display syntax-highlighted code."""
        syntax = Syntax(
            code,
            language or "text",
            theme=self._config.code_theme,
            line_numbers=True,
            word_wrap=True,
        )
        self._console.print(syntax)
    
    def show_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        title: str | None = None,
    ) -> None:
        """Display a formatted table."""
        table = Table(title=title, show_header=True, header_style="bold")
        
        for header in headers:
            table.add_column(header)
        
        for row in rows:
            table.add_row(*row)
        
        self._console.print(table)
    
    def show_spinner(self, message: str) -> "RichSpinnerContext":
        """Create spinner context manager."""
        return RichSpinnerContext(self._console, message, self._config.spinner_style)
    
    def spinner(self, message: str) -> "RichSpinnerContext":
        """Create spinner context manager (alias for show_spinner)."""
        return self.show_spinner(message)
    
    def clear(self) -> None:
        """Clear terminal."""
        self._console.clear()
    
    def show_welcome(self) -> None:
        """Display welcome banner."""
        panel = Panel(
            "[bold]Cato[/bold] - Chat at the Terminal Orchestrator\n"
            "Type [cyan]/help[/cyan] for commands, [cyan]/exit[/cyan] to quit",
            title="Welcome",
            border_style="dim",
        )
        self._console.print(panel)
    
    def show_context_full(self, context_items: list[str]) -> None:
        """
        Display full context excerpts.
        
        Parameters
        ----------
        context_items : list[str]
            Context items to display.
        """
        if not context_items:
            return
        
        context_text = "\n\n[dim]---[/dim]\n\n".join([
            f"[cyan]Context {i+1}:[/cyan]\n{item}"
            for i, item in enumerate(context_items)
        ])
        
        panel = Panel(
            context_text,
            title="📚 Retrieved Context",
            border_style="cyan",
            padding=(1, 2),
        )
        self._console.print(panel)
        self._console.print()  # Add spacing
    
    def show_context_summary(self, count: int) -> None:
        """
        Display context count summary.
        
        Parameters
        ----------
        count : int
            Number of context items retrieved.
        """
        if count > 0:
            self._console.print(
                f"[dim cyan]📚 Retrieved {count} context item{'s' if count != 1 else ''}[/dim cyan]"
            )
            self._console.print()  # Add spacing


class RichSpinnerContext:
    """Context manager for loading spinner."""
    
    def __init__(self, console: Console, message: str, style: str) -> None:
        self._console = console
        self._message = message
        self._style = style
        self._live: Live | None = None
    
    def __enter__(self) -> "RichSpinnerContext":
        spinner = Spinner(self._style, text=self._message)
        self._live = Live(spinner, console=self._console, refresh_per_second=10)
        self._live.__enter__()
        return self
    
    def __exit__(self, *args: Any) -> None:
        if self._live:
            self._live.__exit__(*args)
    
    def update(self, message: str) -> None:
        """Update spinner message."""
        if self._live:
            self._live.update(Spinner(self._style, text=message))

```



Perfect! I can see that:
1. The `Conversation` class has a `clear()` method (line 121-127)
2. The `RichDisplay` class has `clear()` and `show_welcome()` methods (lines 128-140)
3. The command structure is function-based with decorators

Now I'll implement the `/clear` command:


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/cato/commands/core.py
+++ /home/alex/Documents/repos/Cato/cato/commands/core.py
@@ -161,10 +161,18 @@
     CommandResult
         Confirmation message.
     """
-    # TODO: Implement conversation clearing when conversation service is ready
+    # Clear conversation messages (preserves system prompt)
+    ctx.conversation.clear()
+    
+    # Clear terminal screen
+    ctx.display.clear()
+    
+    # Show welcome message
+    ctx.display.show_welcome()
+    
     return CommandResult(
         success=True,
-        message="Conversation clearing not yet implemented."
+        message="Conversation cleared"
     )
 
 

```



Now let me verify the implementation is correct and check if there are any tests I should run:


**Files Read:**

**/home/alex/Documents/repos/Cato/cato/commands/core.py**
```
"""
Core commands for essential application functionality.

This module implements the most basic commands needed for a functional
chat client: help, exit, clear, and config display.
"""

import logging

from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command
from cato.services.help import HelpService

logger = logging.getLogger(__name__)


@command(name="help", aliases=["h", "?"])
async def help_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Display help information about commands and topics.

    Usage: 
      /help                    # Show overview
      /help commands           # List all commands
      /help <topic>            # Show topic or category
      /help <command>          # Show command help
      /help model "question"   # Ask model about Cato

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Query (topic, category, or command) or 'model' with question.

    Returns
    -------
    CommandResult
        Help information to display.
    """
    # Initialize HelpService
    help_service = HelpService()
    
    # Handle /help model "question"
    if args and args[0] == "model":
        if len(args) < 2:
            return CommandResult(
                success=False,
                message="Usage: /help model \"your question\""
            )
        
        question = " ".join(args[1:])
        
        # Get all help files for context
        help_files = help_service.get_all_help_files()
        
        # Build context from help files
        context = "# Cato Help Documentation\n\n"
        for file_path, content in help_files:
            context += f"## {file_path}\n\n{content}\n\n---\n\n"
        
        # Create one-off LLM query
        try:
            from cato.core.types import Message
            
            messages = [
                Message(
                    role="system",
                    content="You are a helpful assistant for Cato, a terminal-first LLM chat client. "
                            "Answer questions strictly based on the help documentation provided. "
                            "If the answer is not in the documentation, say so."
                ),
                Message(
                    role="user",
                    content=f"{context}\n\nQuestion: {question}"
                )
            ]
            
            # Use LLM provider directly (don't add to conversation history)
            result = await ctx.llm.complete(messages=messages)
            
            return CommandResult(
                success=True,
                message=f"**Help Model Response:**\n\n{result.content}"
            )
        except Exception as e:
            logger.error(f"Failed to query help model: {e}")
            return CommandResult(
                success=False,
                message=f"Failed to query help model: {e}"
            )
    
    # Regular help query
    query = args[0] if args else None
    content = help_service.get_help_content(query)
    
    if content:
        return CommandResult(success=True, message=content)
    
    # Not found - provide suggestions
    suggestions = help_service.get_suggestions(query) if query else []
    
    error_msg = f"Help topic not found: {query}\n\n"
    if suggestions:
        error_msg += "Did you mean:\n"
        for suggestion in suggestions:
            error_msg += f"- /help {suggestion}\n"
    else:
        error_msg += "Try:\n- /help commands - List all commands\n- /help <category> - Show category commands"
    
    return CommandResult(success=False, message=error_msg.strip())


@command(name="exit", aliases=["quit", "q"])
async def exit_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Exit the application.

    Usage: /exit

    Cleanly shuts down Cato and returns to the terminal.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Command arguments (unused).

    Returns
    -------
    CommandResult
        Exit confirmation message.
    """
    return CommandResult(
        success=True,
        message="Exiting Cato...",
        data={"should_exit": True}
    )


@command(name="clear", aliases=["cls"])
async def clear_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Clear the conversation history.

    Usage: /clear

    Removes all messages from the current conversation, keeping only
    the system prompt. The next message will start a fresh conversation.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Command arguments (unused).

    Returns
    -------
    CommandResult
        Confirmation message.
    """
    # Clear conversation messages (preserves system prompt)
    ctx.conversation.clear()
    
    # Clear terminal screen
    ctx.display.clear()
    
    # Show welcome message
    ctx.display.show_welcome()
    
    return CommandResult(
        success=True,
        message="Conversation cleared"
    )


@command(name="config", aliases=["cfg"])
async def config_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Display current configuration.

    Usage: /config [section]

    Without arguments, shows key configuration values.
    With a section name (llm, display, storage), shows detailed config for that section.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Optional section name.

    Returns
    -------
    CommandResult
        Configuration information.
    """
    config = ctx.config

    # Show specific section
    if args:
        section = args[0].lower()
        
        if section == "llm":
            info = f"""# LLM Configuration

**Provider**: {config.llm.provider}
**Model**: {config.llm.model}
**Temperature**: {config.llm.temperature}
**Max Tokens**: {config.llm.max_tokens}
**Timeout**: {config.llm.timeout_seconds}s
"""
        elif section == "display":
            info = f"""# Display Configuration

**Theme**: {config.display.theme}
**Markdown**: {'enabled' if config.display.markdown_enabled else 'disabled'}
**Code Theme**: {config.display.code_theme}
**Prompt**: {config.display.prompt_symbol}
"""
        elif section == "storage":
            info = f"""# Storage Configuration

**Database**: {config.storage.database_path}
**Backup**: {'enabled' if config.storage.backup_enabled else 'disabled'}
"""
        elif section == "commands":
            info = f"""# Commands Configuration

**Prefix**: {config.commands.prefix}
**History File**: {config.commands.history_file}
"""
        else:
            return CommandResult(
                success=False,
                message=f"Unknown config section: {section}\\n"
                        "Available sections: llm, display, storage, commands"
            )
        
        return CommandResult(success=True, message=info.strip())
    
    # Show overview
    info = f"""# Cato Configuration

**LLM Provider**: {config.llm.provider} ({config.llm.model})
**Theme**: {config.display.theme}
**Database**: {config.storage.database_path}
**Debug Mode**: {'enabled' if config.debug else 'disabled'}

Use `/config <section>` for detailed configuration.
Available sections: llm, display, storage, commands
"""
    
    return CommandResult(success=True, message=info.strip())


@command(name="info", aliases=["about"])
async def info_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Display information about Cato.

    Usage: /info

    Shows version, current session stats, and system information.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Command arguments (unused).

    Returns
    -------
    CommandResult
        Application information.
    """
    message_count = ctx.chat_service.get_message_count()
    
    info = f"""# Cato - Terminal LLM Chat Client

**Version**: 0.1.0
**Provider**: {ctx.chat_service.provider.name}
**Model**: {ctx.chat_service.provider.model}

**Current Session**:
- Messages: {message_count}
- Storage: {ctx.config.storage.database_path}

Cato is a terminal-first LLM chat client with conversation memory,
productivity features, and extensible command system.
"""

    return CommandResult(success=True, message=info.strip())


@command(name="loglevel", aliases=["log"])
async def loglevel_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Show or change the logging level.

    Usage:
      /loglevel              # Show current level
      /loglevel <level>      # Set level (DEBUG, INFO, WARNING, ERROR)

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Optional log level to set.

    Returns
    -------
    CommandResult
        Current or updated log level.
    """
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]

    # Show current level
    if not args:
        current_level = logging.getLogger().level
        level_name = logging.getLevelName(current_level)

        return CommandResult(
            success=True,
            message=f"Current log level: **{level_name}**\n\n"
                   f"Available levels: {', '.join(valid_levels)}\n"
                   f"Usage: /loglevel <level>"
        )

    # Set new level
    new_level = args[0].upper()

    if new_level not in valid_levels:
        return CommandResult(
            success=False,
            message=f"Invalid log level: {new_level}\n"
                   f"Valid levels: {', '.join(valid_levels)}"
        )

    # Update logging level
    logging.getLogger().setLevel(getattr(logging, new_level))
    logger.info(f"Log level changed to {new_level}")

    return CommandResult(
        success=True,
        message=f"✓ Log level set to **{new_level}**"
    )

```




**Command Executed:**
```bash
cd /home/alex/Documents/repos/Cato && python -m py_compile cato/commands/core.py
```

**Output:**
```

```

Good! The syntax is valid. Now let me check if there's help documentation for `/clear` that might need updating:


**Grep Results:**

- **/home/alex/Documents/repos/Cato/cato/resources/help/index.yaml**
- **/home/alex/Documents/repos/Cato/cato/resources/help/commands/done.md**
- **/home/alex/Documents/repos/Cato/cato/resources/help/commands/remove.md**
- **/home/alex/Documents/repos/Cato/cato/resources/help/commands/clear.md**
- **/home/alex/Documents/repos/Cato/cato/resources/help/commands/continue.md**
- **/home/alex/Documents/repos/Cato/cato/resources/help/topics/commands.md**
- **/home/alex/Documents/repos/Cato/cato/resources/help/topics/overview.md**




**Files Read:**

**/home/alex/Documents/repos/Cato/cato/resources/help/commands/clear.md**
```
# /clear



## Usage

```

```

For detailed information, see command implementation.

```



The help documentation is a stub. Let me update it to match the spec and implementation:


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/cato/resources/help/commands/clear.md
+++ /home/alex/Documents/repos/Cato/cato/resources/help/commands/clear.md
@@ -1,11 +1,40 @@
 # /clear
 
-
+Clear the conversation history and terminal screen.
 
 ## Usage
 
 ```
+/clear
+```
+
+## Description
+
+Removes all user and assistant messages from the current conversation, keeping only the system prompt. The terminal screen is cleared and the welcome message is displayed.
+
+This is useful when you want to:
+- Start a fresh conversation on a new topic
+- Clear the context window to reduce token usage
+- Remove sensitive information from the conversation history
+
+## Aliases
+
+- `/cls`
 
+## Behavior
+
+1. Clears all messages from conversation history (system prompt is preserved)
+2. Clears the terminal screen
+3. Displays the welcome message
+4. The next message will start a fresh conversation
+
+## Examples
+
+```
+/clear
 ```
 
-For detailed information, see command implementation.
+## Related Commands
+
+- `/history` - View conversation history before clearing
+- `/delete` - Remove specific exchanges without clearing everything

```



Implemented! The `/clear` command now:
1. Clears conversation messages (preserving system prompt) via `ctx.conversation.clear()`
2. Clears the terminal screen via `ctx.display.clear()`
3. Shows the welcome message via `ctx.display.show_welcome()`
4. Returns a success message

I also updated the help documentation to describe the command's behavior, usage, aliases, and related commands per the specs.