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
