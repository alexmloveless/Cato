# Command System Specification

## Overview

Ocat uses a slash command system for explicit actions. Commands start with `/` and are parsed before any other input processing.

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
```

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
Change or display the current LLM model.
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
Control context display mode.
```
/showcontext        # Show current mode
/showcontext on     # Show full context with excerpts
/showcontext off    # Disable context display
/showcontext summary # Show context counts only
```

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

See SPEC_FILE_OPERATIONS.md for detailed file command documentation.

#### /file
Multi-purpose file operations command.
```
/file read <path>              # Read and display file
/file write <path> <content>   # Write content to file
/file append <path> <content>  # Append to file
/file list [path]              # List directory contents
/file search <pattern> [path]  # Search files
/file tree [path] [depth]      # Show directory tree
```

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

#### /mkdir
Create a new directory.
```
/mkdir new_directory
/mkdir path/to/new/directory
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

#### /remember, /rem, /r
Store information in vector store for future retrieval.
```
/remember fact I have a brother called Bob
/remember preference I prefer dark mode
/remember critical This is very important
/rem like I enjoy hiking
/r dislike I don't like spicy food
```

**Valid Types:**
| Type | Description |
|------|-------------|
| fact | General information |
| preference | User preferences |
| critical | High-priority information |
| nudge | Gentle reminders |
| like | Positive preferences |
| opinion | Personal views |
| dislike | Negative preferences |

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

#### /timelog, /tl, /time
Show and export timelog entries.
```
/timelog                            # Show all entries
/tl -p project_name                 # Filter by project
/tl --start=2024-01-01              # Filter by start date
/tl --end=2024-12-31                # Filter by end date
/tl -g project                      # Group by project
/tl -g week                         # Group by week
/tl -o csv -f output.csv            # Export to CSV
/tl --output=json --file=data.json  # Export to JSON
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
