# File Operations Specification

## Overview

File operations provide comprehensive file system interaction including reading, writing, directory navigation, and conversation export capabilities.

## Routing

### Slash Commands
Direct file operations use slash commands without the routing marker.

## Location Aliases

### Purpose
Location aliases provide shortcuts to frequently accessed paths, simplifying file operations.

### Configuration
Aliases are defined in the YAML configuration:
```yaml
locations:
  docs: ~/Documents
  projects: ~/Code/projects
  config: ~/.config
  downloads: ~/Downloads
```

### Usage Syntax
Use `alias:filename` to reference files via aliases:
```
/file read docs:notes.txt       # Reads ~/Documents/notes.txt
/attach config:ocat.yaml        # Attaches ~/.config/ocat.yaml
/vdoc projects:readme.md        # Adds ~/Code/projects/readme.md to vector store
```

### Viewing Aliases
```
/locations
```
Displays configured aliases and their resolved paths.

### Validation
- Aliases must be unique
- Paths are expanded (~ resolved to home directory)
- Invalid paths logged as warnings during startup

## File Command (/file)

### Read Subcommand
Read and display file contents with syntax highlighting.

```
/file read <path>
/file read docs:config.yaml
```

**Behavior:**
- Detects file type by extension
- Applies syntax highlighting (Python, JavaScript, YAML, etc.)
- Displays in bordered panel with filename
- Error on binary files or permission denied

**Supported Syntax Highlighting:**
| Extension | Language |
|-----------|----------|
| .py | Python |
| .js | JavaScript |
| .ts | TypeScript |
| .html | HTML |
| .css | CSS |
| .json | JSON |
| .yaml, .yml | YAML |
| .xml | XML |
| .sql | SQL |
| .sh | Bash |
| .md | Markdown |
| .rs | Rust |
| .go | Go |
| .java | Java |
| .c, .cpp | C/C++ |
| .php | PHP |

### Write Subcommand
Create or overwrite a file.

```
/file write <path> <content>
/file write notes.txt "New content here"
/file write config:settings.yaml "key: value"
```

**Behavior:**
- Creates parent directories if needed
- Overwrites existing files
- Strips surrounding quotes from content
- UTF-8 encoding

### Append Subcommand
Add content to an existing file.

```
/file append <path> <content>
/file append notes.txt "Additional line"
```

**Behavior:**
- Creates file if it doesn't exist
- Adds newline before content if file doesn't end with one
- Preserves existing content

### List Subcommand (list/ls)
List directory contents. 

```
/file list                    # Current directory
/file ls                      # Current directory
/file list /path/to/dir       # Specific directory
/file ls docs:                # Via alias
```

**Display:**
```
┌─ 📁 Documents ───────────────────────────────────────────────┐
│ Type   │ Name              │ Size     │ Modified            │
├────────┼───────────────────┼──────────┼─────────────────────┤
│ 📁     │ projects/         │ -        │ 2024-01-15 10:30   │
│ 📄     │ notes.txt         │ 2.5 KB   │ 2024-01-14 15:45   │
│ 📄     │ config.yaml       │ 1.2 KB   │ 2024-01-10 09:00   │
└────────┴───────────────────┴──────────┴─────────────────────┘
```

## Directory Navigation

### /pwd
Show current working directory.
```
/pwd
```
Output: `/home/user/projects`

### /cd
Change current directory.
```
/cd /absolute/path
/cd relative/path
/cd ..
/cd ~
/cd docs:           # Via alias
```

**Behavior:**
- Updates session's current directory
- File operations use current directory for relative paths
- Validated before changing

### /ls
Alias for `/file list`.
```
/ls
/ls /path
```

### /cat
Alias for `/file read`.
```
/cat filename.txt
/cat alias:file.md
```

### /mkdir
Create a new directory.
```
/mkdir new_directory
/mkdir path/to/nested/directory
```
Creates parent directories as needed.

## File Attachment

### /attach Command
Attach file contents as conversation context.

```
/attach file.txt                          # Single file
/attach file1.py file2.py file3.md        # Multiple files (max 5)
/attach docs:notes.txt config:settings.yaml
```

**Behavior:**
1. Read each file's content
2. Add to conversation as user message with headers:
   ```
   [Attached Files]
   
   --- File: notes.txt ---
   File content here...
   
   --- File: settings.yaml ---
   Another file content...
   ```
3. Offer to add to vector store (y/n prompt)

**Limits:**
- Maximum 5 files per command
- Must be text files (binary files rejected)
- Files must be readable (permission check)

### Vector Store Integration
After attachment, user is prompted:
```
Would you like to also add these files to the vector store for future reference? (y/n)
```

If yes: Files are chunked and added to vector store with metadata.

## Export Commands

### /writecode
Extract code blocks from last assistant response.

```
/writecode output.py
/writecode docs:extracted_code.js
```

**Behavior:**
1. Find all markdown code blocks (```) in last response
2. Combine all code blocks
3. Write to specified file

### /writejson
Export conversation to JSON.

```
/writejson conversation.json
```

**Output Format:**
```json
{
  "conversation": [
    {
      "role": "system",
      "content": "System prompt...",
      "timestamp": null
    },
    {
      "role": "user",
      "content": "Hello",
      "timestamp": null
    },
    {
      "role": "assistant",
      "content": "Hi there!",
      "timestamp": null
    }
  ],
  "config": {
    "model": "gpt-4o-mini",
    "temperature": 1.0,
    "max_tokens": 4000
  }
}
```

### /writemd
Export thread to Markdown (excludes system prompts).

```
/writemd output.md
/w output.md          # Alias
```

**Output Format:**
```markdown
# Thread Export

**Model:** gpt-4o-mini
**Temperature:** 1.0

---

## User

Hello, how are you?

---

## Assistant

I'm doing well, thank you for asking!

---
```

### /writemdall
Export full conversation including system prompts.

```
/writemdall full_conversation.md
```

Same format as `/writemd` but includes system prompt section.

### /writeresp
Export last exchange only.

```
/writeresp output.txt           # Plain text
/writeresp output.json json     # JSON format
/writeresp output.md md         # Markdown format
```

### /append (Export)
Append last exchange or custom text to file.

```
/append notes.txt                  # Append last exchange
/append notes.txt "Custom text"    # Append specific text
```

## Clipboard

### /copy
Copy last assistant response to system clipboard.

```
/copy
```

**Behavior:**
- Extracts text from last assistant message
- Copies to system clipboard
- Works on macOS, Linux, Windows

## File Tools Agent

### Response Format
File agent responses are displayed but not added to main conversation history, keeping context clean.

## Path Resolution

### Resolution Order
1. Check for location alias prefix (alias:filename)
2. If relative path, combine with current directory
3. Expand ~ to home directory
4. Resolve to absolute path

### Error Handling
- File not found: Show error with path
- Permission denied: Show error
- Binary file: Show error (text operations only)
- Invalid alias: Show error with available aliases
