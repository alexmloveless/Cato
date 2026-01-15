USER:
remote all references to the memory creation and retrieval system as this is not required. 

AGENT:
I'll search for all references to memory creation and retrieval across the codebase and specification documents.


**Grep Results:**

- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_VECTOR_STORE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_PERFORMANCE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_VECTOR_STORE.md**
- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-14_spec_review.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ERROR_HANDLING.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_STORAGE.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/GENERAL_PRINCIPLES.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_PRODUCTIVITY.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**
- **/home/alex/Documents/repos/Cato/Project/Notes/Jan 14 at 11-01.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md**
- **/home/alex/Documents/repos/Cato/WARP.md**


Let me read the key files to understand the memory system references and what needs to be removed:


**Files Read:**

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

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_VECTOR_STORE.md**
```
# Vector Store Specification

## Overview

The vector store provides persistent conversation memory using vector embeddings for semantic similarity search. It enables context retrieval from previous conversations and document storage for future reference.

## Critical Performance Requirements

**NEVER load the entire vector store into memory.**

- All queries must be performed on-demand against the database
- No caching of vector store contents outside current conversation context
- Startup must not be delayed by vector store loading
- See TECH_PERFORMANCE.md for detailed performance requirements

## Storage Backend

### ChromaDB
- Persistent storage using DuckDB backend
- Cosine similarity for vector comparison
- Automatic persistence on write

### Embeddings
- Model: OpenAI text-embedding-3-small (default)
- Dimensions: 1536 (configurable)
- Requires OPENAI_API_KEY environment variable

The model should be configurable.

## Exchange Storage

### Exchange Data Model

Each conversation exchange stores:

| Field | Type | Description |
|-------|------|-------------|
| exchange_id | UUID | Unique identifier |
| thread_id | UUID | Conversation thread grouping |
| session_id | UUID | Application session identifier |
| user_prompt | string | User's input message |
| assistant_response | string | Assistant's response |
| timestamp | float | Unix timestamp |
| prior_exchange_ids | list | Context exchanges used |
| thread_session_id | string | Composite ID (thread_id_session_id) |
| thread_continuation_seq | int | Continuation sequence (0 for original) |

### Storage Flow

1. User sends message, assistant responds
2. Combined text created: `"User: {prompt}\nAssistant: {response}"`
3. Text embedded using OpenAI embeddings
4. Exchange stored in ChromaDB with metadata

### Automatic Storage
All conversation exchanges are automatically stored (except in dummy mode) for:
- Future context retrieval
- Thread continuation
- Conversation history
- Productivity exchanges and outputs are **not** stored

## Similarity Search

### Query Process
1. Query text embedded using same model
2. ChromaDB performs cosine similarity search
3. Results filtered by similarity threshold (static or dynamic)
4. Top-k results returned

### Retrieval Strategy Architecture

The retrieval system is designed to be **pluggable** to allow experimentation with different strategies and algorithms.

#### Strategy Interface
All retrieval strategies must implement a common interface:
- Accept query embedding and parameters
- Return ranked results with similarity scores
- Support configuration options

#### Built-in Strategies

| Strategy | Description |
|----------|-------------|
| default | Standard cosine similarity with static threshold |
| dynamic | Adjusts threshold based on context length |
| (extensible) | Additional strategies can be added |

#### Dynamic Thresholding
When `dynamic_threshold: true` in config:
- Threshold adjusts based on current conversation context length
- Shorter context → lower threshold (more permissive retrieval)
- Longer context → higher threshold (more selective)
- Algorithm: Simple linear adjustment based on context message count
- Can be disabled to use static `context_similarity_threshold`

### Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| context_similarity_threshold | 0.65 | Minimum similarity score (static, used when dynamic disabled) |
| dynamic_threshold | true | Enable dynamic threshold adjustment |
| retrieval_strategy | default | Which retrieval strategy to use |
| context_results | 5 | Maximum context exchanges returned |

### Context Retrieval

During response generation:

1. **Build query** from recent exchanges (excluding commands)
2. **Select strategy** based on configuration
3. **Search regular context** using configured retrieval strategy
4. **Filter and rank** by similarity score
5. **Inject into prompt** based on context mode

## Document Indexing

### Document Chunking

Long documents are split into chunks for better retrieval.

**Chunking Strategies:**

| Strategy | Description |
|----------|-------------|
| truncate | Simple truncation to chunk_size |
| fixed_size | Split into equal-sized chunks with overlap |
| semantic | Split at paragraph/sentence boundaries |
| hybrid | Combine semantic splitting with size limits |

**Configuration:**

| Setting | Default | Description |
|---------|---------|-------------|
| strategy | semantic | Chunking strategy |
| chunk_size | 1000 | Target chunk size (characters) |
| chunk_overlap | 100 | Overlap between chunks |
| max_chunk_size | 1500 | Maximum chunk size (hard limit) |
| preserve_sentence_boundaries | true | Avoid mid-sentence splits |

### /vadd Command
Add text directly to vector store.

```
/vadd This is important information to remember
```

**Behavior:**
- Short text: Stored as single exchange
- Long text: Automatically chunked using configured strategy
- Metadata: `source: vadd_command, manual_entry: true`

### /vdoc Command
Add a document file with chunking.

```
/vdoc /path/to/document.txt
/vdoc docs:readme.md
```

**Behavior:**
1. Read file content
2. Apply chunking strategy
3. Store each chunk as exchange
4. Link chunks via metadata

**Metadata:**
- `source: vdoc_command`
- `source_file: {filepath}`
- `chunk_index: n`
- `total_chunks: N`


## Vector Store Commands

### /vquery
Query for similar exchanges.

```
/vquery "search query"       # Default k results
/vquery "search query" 10    # Return 10 results
```

**Display:**
```
┌─ Vector Store Query Results ─────────────────────────────────┐
│ Result 1 (similarity: 0.89)                                  │
│ Thread: abc123... | Session: def456...                       │
│ User: How do I configure...                                  │
│ Assistant: You can modify the config file...                 │
├──────────────────────────────────────────────────────────────┤
│ Result 2 (similarity: 0.82)                                  │
│ ...                                                          │
└──────────────────────────────────────────────────────────────┘
```

### /vget
Retrieve specific exchanges.

```
/vget <exchange_id>      # Get by ID
/vget session            # Get current session's exchanges
/vget thread             # Get current thread's exchanges
```

### /vdelete
Delete an exchange by ID.

```
/vdelete <exchange_id>
```

**Behavior:**
- Removes from ChromaDB
- Cannot be undone
- Does not affect conversation history

### /vstats
Display vector store statistics.

```
/vstats
```

**Display:**
```
┌─ Vector Store Statistics ────────────────────────────────────┐
│ Metric           │ Value                                     │
├──────────────────┼───────────────────────────────────────────┤
│ Total Exchanges  │ 1,234                                     │
│ Store Path       │ ./vector_stores/default/                  │
│ Vector Dimension │ 1536                                      │
│ Embedding Model  │ text-embedding-3-small                    │
└──────────────────┴───────────────────────────────────────────┘
```

## Thread Management

### Thread Continuation
`/continue <thread_id>` loads a previous thread:

1. Fetch all exchanges with matching thread_id
2. Sort by timestamp
3. Calculate next continuation sequence
4. Clear current conversation
5. Load thread history as messages
6. Display history to user
7. Resume conversation with new session

### Thread Session Tracking
- Each exchange has `thread_id` and `session_id`
- Composite `thread_session_id` for unique identification
- `thread_continuation_seq` tracks which continuation (0 = original)

## Headless Operations

### CLI Arguments
For automation without interactive session:

```bash
# Add document to vector store
cato --add-to-vector-store /path/to/document.txt

# Query vector store
cato --query-vector-store "search query"

# Show statistics
cato --vector-store-stats
```

## Configuration

### Vector Store Config
```yaml
vector_store:
  enabled: true
  path: ./vector_stores/default/
  similarity_threshold: 0.65
  chat_window: 3
  context_results: 5
  search_context_window: 3
  memory_threshold: 0.7
  memory_results: 3
```

### Chunking Config
```yaml
chunking:
  strategy: semantic
  chunk_size: 1000
  chunk_overlap: 100
  max_chunk_size: 1500
  preserve_sentence_boundaries: true
```

### Embedding Config
```yaml
embedding:
  model: text-embedding-3-small
  dimensions: 1536
```

## Error Handling

### Graceful Degradation
If vector store fails to initialize:
- Log warning
- Continue without memory features
- Conversation still works

### Operation Failures
- Failed storage: Log warning, continue chat
- Failed retrieval: Use empty context
- Invalid queries: Show error message

## Disabling Vector Store

```yaml
vector_store:
  enabled: false
```

Or via CLI:
```bash
cato --no-vector-store
```

When disabled:
- No context retrieval
- No memory features
- No `/v*` commands available
- `/continue` unavailable

```

**/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_PRODUCTIVITY.md**
```
# Productivity System Specification

## Overview

The productivity system provides task management, list organization, time tracking, and memory storage through natural language interaction. It uses a dedicated AI agent to parse requests and manage productivity data stored in SQLite.


## Entity Types

### Tasks

Tasks represent actionable items with optional due dates, categories, and priorities.

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| content | string | Yes | Task description |
| status | enum | No | active, in_progress, completed, deleted |
| due_date | datetime | No | When task is due |
| category | string | No | Project or category name |
| priority | enum | No | urgent, high, medium, low |
| tags | list | No | Additional tags |
| pseudo_id | string | Auto | Human-readable ID (task001, task002) |
| created_at | datetime | Auto | Creation timestamp |
| updated_at | datetime | Auto | Last update timestamp |


**Status Transitions:**
- `active` → `in_progress` → `completed`
- `active` → `deleted`
- Any status → `deleted`

### Lists and List Items

Lists provide a way to organize items into named collections (shopping, projects, ideas, etc.).

**List Item Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| content | string | Yes | Item description |
| list_name | string | Yes | Name of the list |
| status | enum | No | active, completed, archived |
| category | string | No | Sub-category within list |
| pseudo_id | string | Auto | Human-readable ID (001) |
| created_at | datetime | Auto | Creation timestamp |


## Commands

### /st (Show Tasks)

Display open tasks with filtering and sorting options.

**Usage:**
```
/st                              # All open tasks
/st work                         # Filter by category
/st -p high                      # Filter by priority
/st -s priority -o asc           # Sort by priority ascending
/st --status=completed           # Show completed tasks
```

**Options:**
| Option | Values | Default |
|--------|--------|---------|
| -s, --sort | created, priority, category, due, id, status | created |
| -o, --order | asc, desc | desc (for created), asc (others) |
| -p, --priority | urgent, high, medium, low | none |
| -c, --category | any string | none |
| -S, --status | active, in_progress, completed | active + in_progress |

**Display:**
```
┌──────────────────────────────────────────────────────────┐
│ Open Tasks sorted by created ↓ (5)                       │
├─────┬──────────┬──────────┬───────┬─────────────┬────────┤
│ S   │ Priority │ Category │ ID    │ Task        │ Due    │
├─────┼──────────┼──────────┼───────┼─────────────┼────────┤
│ 🔵  │ 🔥 URGENT│ work     │ 005   │ Fix bug     │ Today  │
│ 🟡  │ ⚡ HIGH  │ personal │ 004   │ Call dentist│ 01/15  │
│ 🔵  │ ● MED    │ work     │ 003   │ Review doc  │        │
└─────┴──────────┴──────────┴───────┴─────────────┴────────┘
```

### /list (Show Lists)

Display lists and list items.

**Usage:**
```
/list                    # Show all lists with item counts
/list shopping           # Show items in shopping list
```

**List Overview Display:**
```
┌─────────────────────────────────────┐
│ Available Lists (3 lists)           │
├─────────────────┬───────────────────┤
│ List Name       │ Items             │
├─────────────────┼───────────────────┤
│ shopping        │ 12                │
│ ideas           │ 5                 │
│ books           │ 8                 │
└─────────────────┴───────────────────┘
```

**List Items Display:**
```
┌─────────────────────────────────────────────────────────┐
│ List: shopping (12 items)                               │
├───────┬─────┬──────────┬────────────────────┬───────────┤
│ ID    │ S   │ Category │ Item               │ Added     │
├───────┼─────┼──────────┼────────────────────┼───────────┤
│ 001   │ 🔵  │ dairy    │ Milk               │ 01/10     │
│ 002   │ 🔵  │ produce  │ Apples             │ 01/10     │
│ 003   │ ✅  │ bakery   │ Bread              │ 01/09     │
└───────┴─────┴──────────┴────────────────────┴───────────┘
```


## Storage

### SQLite Database
Productivity data is stored in SQLite for:
- Persistence across sessions
- Efficient querying and filtering
- Structured data with relationships

### Pseudo IDs
All entities receive human-readable IDs:
- Tasks: `001`, `002`, ...
- List items: `001`, `002`, ...

IDs are assigned sequentially and used for:
- Display in tables
- Reference in commands
- Updates and deletions

## Integration with Chat

### Productivity Agent
A dedicated AI agent processes productivity requests:
- Determines appropriate action
- Executes database operations
- Returns formatted response

### Response Format
Productivity responses are displayed in the assistant panel but not added to conversation history, keeping the main LLM context clean.

### Vector Store Integration
Productivity exchanges are stored in the vector store for:
- Future context retrieval
- Thread continuation support

```





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

The provider is automatically determined from the model name:
- `gpt-*`, `o1-*` → OpenAI
- `claude-*` → Anthropic
- `gemini-*` → Google
- Other models → Ollama (local)

### LLM Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| model | gpt-4o-mini | Provider-specific | LLM model identifier |
| temperature | 1.0 | 0.0-2.0 | Response randomness |
| max_tokens | 10000 | >0 | Maximum response tokens |

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
Check for productivity marker (%) → Route to ProductivityAgent
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
   - Uses configurable `search_context_window` (default: -1 = all exchanges)

2. **Retrieves similar exchanges** from vector store
   - Uses similarity threshold from config
   - Returns up to `context_results` exchanges

3. **Injects context** into API request
   - Memories always included if found
   - Regular context included based on `context_mode`:
     - `off`: No context injection (default)
     - `on`: Full context with excerpts shown
     - `summary`: Context injected but only count displayed

### Context Display Modes

Controlled via `/showcontext` command:

| Mode | Behavior |
|------|----------|
| off | No context shown or injected |
| on | Context injected, excerpts displayed |
| summary | Context injected, only count displayed |

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
- Default timeout: 120 seconds
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
| user_label | "User" | Label for user messages |
| assistant_label | "Assistant" | Label for assistant messages |
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

**/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_STORAGE.md**
```
# Storage Technical Specification

## Overview
Cato uses SQLite for structured data storage (tasks, lists, time logs, memories). The database provides persistent storage for productivity features with a simple data access layer.

## Database Location
```
~/.local/share/cato/cato.db
```

Configurable via `storage.database_path` in config.

## Schema

### Tasks Table
```sql
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'active',  -- active, in_progress, completed
    priority TEXT DEFAULT 'medium',          -- low, medium, high
    category TEXT,
    due_date TEXT,                           -- ISO 8601 format
    created_at TEXT NOT NULL,                -- ISO 8601 format
    updated_at TEXT NOT NULL,                -- ISO 8601 format
    completed_at TEXT,                       -- ISO 8601 format
    metadata TEXT                            -- JSON for extensibility
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
```

### Lists Table
```sql
CREATE TABLE IF NOT EXISTS lists (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS list_items (
    id TEXT PRIMARY KEY,
    list_id TEXT NOT NULL,
    content TEXT NOT NULL,
    checked INTEGER NOT NULL DEFAULT 0,
    position INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metadata TEXT,
    FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_list_items_list_id ON list_items(list_id);
```

### Time Logs Table
```sql
CREATE TABLE IF NOT EXISTS time_logs (
    id TEXT PRIMARY KEY,
    task_id TEXT,                            -- Optional link to task
    description TEXT NOT NULL,
    category TEXT,
    start_time TEXT NOT NULL,                -- ISO 8601 format
    end_time TEXT,                           -- ISO 8601 format (NULL if running)
    duration_seconds INTEGER,                -- Computed on stop
    created_at TEXT NOT NULL,
    metadata TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_time_logs_task_id ON time_logs(task_id);
CREATE INDEX IF NOT EXISTS idx_time_logs_start_time ON time_logs(start_time);
CREATE INDEX IF NOT EXISTS idx_time_logs_category ON time_logs(category);
```

### Memories Table
```sql
CREATE TABLE IF NOT EXISTS memories (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    category TEXT,
    source TEXT,                             -- 'user', 'conversation', 'import'
    importance INTEGER DEFAULT 1,            -- 1-5 scale
    created_at TEXT NOT NULL,
    last_accessed TEXT,
    access_count INTEGER DEFAULT 0,
    metadata TEXT
);

CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance);
```

### Sessions Table
```sql
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    message_count INTEGER DEFAULT 0,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS threads (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    name TEXT,
    created_at TEXT NOT NULL,
    metadata TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);
```

## Data Access Layer

### Repository Protocol
```python
from typing import Protocol, TypeVar, Generic

T = TypeVar("T")

class Repository(Protocol[T]):
    """Generic repository protocol for CRUD operations."""
    
    async def get(self, id: str) -> T | None:
        """Get entity by ID."""
        ...
    
    async def get_all(self, **filters) -> list[T]:
        """Get all entities, optionally filtered."""
        ...
    
    async def create(self, entity: T) -> str:
        """Create entity, return ID."""
        ...
    
    async def update(self, entity: T) -> None:
        """Update existing entity."""
        ...
    
    async def delete(self, id: str) -> None:
        """Delete entity by ID."""
        ...
```

### Task Repository
```python
from pydantic import BaseModel

class Task(BaseModel):
    """
    Task entity.
    
    Uses Pydantic for validation as data crosses SQLite boundary.
    """
    id: str
    title: str
    description: str | None
    status: Literal["active", "in_progress", "completed"]
    priority: Literal["low", "medium", "high"]
    category: str | None
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
    metadata: dict


class TaskRepository:
    """SQLite-backed task repository."""
    
    def __init__(self, db: Database) -> None:
        self._db = db
    
    async def get(self, id: str) -> Task | None:
        """
        Get task by ID.
        
        Parameters
        ----------
        id
            Task ID.
        
        Returns
        -------
        Task | None
            Task if found.
        """
        row = await self._db.fetchone(
            "SELECT * FROM tasks WHERE id = ?",
            (id,),
        )
        return self._row_to_task(row) if row else None
    
    async def get_all(
        self,
        status: str | None = None,
        category: str | None = None,
        priority: str | None = None,
        sort_by: str = "created_at",
        order: str = "asc",
    ) -> list[Task]:
        """
        Get tasks with optional filters.
        
        Parameters
        ----------
        status
            Filter by status.
        category
            Filter by category.
        priority
            Filter by priority.
        sort_by
            Sort field.
        order
            Sort order (asc/desc).
        
        Returns
        -------
        list[Task]
            Matching tasks.
        """
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        if category:
            query += " AND category = ?"
            params.append(category)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        
        # Validate sort field to prevent SQL injection
        valid_sorts = {"created_at", "updated_at", "priority", "due_date", "title"}
        if sort_by not in valid_sorts:
            sort_by = "created_at"
        
        order = "DESC" if order.lower() == "desc" else "ASC"
        query += f" ORDER BY {sort_by} {order}"
        
        rows = await self._db.fetchall(query, tuple(params))
        return [self._row_to_task(row) for row in rows]
    
    async def create(self, task: Task) -> str:
        """Create new task."""
        await self._db.execute(
            """
            INSERT INTO tasks (
                id, title, description, status, priority, category,
                due_date, created_at, updated_at, completed_at, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task.id,
                task.title,
                task.description,
                task.status,
                task.priority,
                task.category,
                task.due_date.isoformat() if task.due_date else None,
                task.created_at.isoformat(),
                task.updated_at.isoformat(),
                task.completed_at.isoformat() if task.completed_at else None,
                json.dumps(task.metadata) if task.metadata else None,
            ),
        )
        return task.id
    
    async def update(self, task: Task) -> None:
        """Update existing task."""
        task.updated_at = datetime.now()
        await self._db.execute(
            """
            UPDATE tasks SET
                title = ?, description = ?, status = ?, priority = ?,
                category = ?, due_date = ?, updated_at = ?,
                completed_at = ?, metadata = ?
            WHERE id = ?
            """,
            (
                task.title,
                task.description,
                task.status,
                task.priority,
                task.category,
                task.due_date.isoformat() if task.due_date else None,
                task.updated_at.isoformat(),
                task.completed_at.isoformat() if task.completed_at else None,
                json.dumps(task.metadata) if task.metadata else None,
                task.id,
            ),
        )
    
    async def delete(self, id: str) -> None:
        """Delete task by ID."""
        await self._db.execute("DELETE FROM tasks WHERE id = ?", (id,))
    
    def _row_to_task(self, row: dict) -> Task:
        """Convert database row to Task entity."""
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=row["status"],
            priority=row["priority"],
            category=row["category"],
            due_date=datetime.fromisoformat(row["due_date"]) if row["due_date"] else None,
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
        )
```

### Database Connection
```python
import aiosqlite
from pathlib import Path

class Database:
    """Async SQLite database wrapper."""
    
    def __init__(self, path: Path) -> None:
        self._path = path
        self._conn: aiosqlite.Connection | None = None
    
    async def connect(self) -> None:
        """Open database connection and initialise schema."""
        # Ensure directory exists
        self._path.parent.mkdir(parents=True, exist_ok=True)
        
        self._conn = await aiosqlite.connect(self._path)
        self._conn.row_factory = aiosqlite.Row
        
        # Enable foreign keys
        await self._conn.execute("PRAGMA foreign_keys = ON")
        
        # Run migrations
        await self._run_migrations()
    
    async def close(self) -> None:
        """Close database connection."""
        if self._conn:
            await self._conn.close()
            self._conn = None
    
    async def execute(self, query: str, params: tuple = ()) -> None:
        """Execute a write query."""
        async with self._conn.execute(query, params):
            await self._conn.commit()
    
    async def fetchone(self, query: str, params: tuple = ()) -> dict | None:
        """Fetch single row."""
        async with self._conn.execute(query, params) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def fetchall(self, query: str, params: tuple = ()) -> list[dict]:
        """Fetch all rows."""
        async with self._conn.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def _run_migrations(self) -> None:
        """Apply database migrations."""
        # Create migrations table if not exists
        await self._conn.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                applied_at TEXT NOT NULL
            )
        """)
        await self._conn.commit()
        
        # Get applied migrations
        cursor = await self._conn.execute("SELECT name FROM migrations")
        applied = {row[0] for row in await cursor.fetchall()}
        
        # Apply pending migrations
        for migration in MIGRATIONS:
            if migration.name not in applied:
                await migration.apply(self._conn)
                await self._conn.execute(
                    "INSERT INTO migrations (name, applied_at) VALUES (?, ?)",
                    (migration.name, datetime.now().isoformat()),
                )
                await self._conn.commit()
                logger.info(f"Applied migration: {migration.name}")
```

## Migrations

### Migration Definition
```python
from dataclasses import dataclass

@dataclass
class Migration:
    """
    Database migration.
    
    Note: Uses dataclass as it's internal configuration, not external data.
    """
    name: str
    sql: str
    
    async def apply(self, conn: aiosqlite.Connection) -> None:
        """Apply migration."""
        await conn.executescript(self.sql)


# Ordered list of migrations
MIGRATIONS = [
    Migration(
        name="001_initial_schema",
        sql="""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            priority TEXT DEFAULT 'medium',
            category TEXT,
            due_date TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            completed_at TEXT,
            metadata TEXT
        );
        
        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
        
        CREATE TABLE IF NOT EXISTS lists (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            metadata TEXT
        );
        
        CREATE TABLE IF NOT EXISTS list_items (
            id TEXT PRIMARY KEY,
            list_id TEXT NOT NULL,
            content TEXT NOT NULL,
            checked INTEGER NOT NULL DEFAULT 0,
            position INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            metadata TEXT,
            FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE
        );
        
        CREATE INDEX IF NOT EXISTS idx_list_items_list_id ON list_items(list_id);
        """,
    ),
    Migration(
        name="002_time_logs",
        sql="""
        CREATE TABLE IF NOT EXISTS time_logs (
            id TEXT PRIMARY KEY,
            task_id TEXT,
            description TEXT NOT NULL,
            category TEXT,
            start_time TEXT NOT NULL,
            end_time TEXT,
            duration_seconds INTEGER,
            created_at TEXT NOT NULL,
            metadata TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL
        );
        
        CREATE INDEX IF NOT EXISTS idx_time_logs_task_id ON time_logs(task_id);
        CREATE INDEX IF NOT EXISTS idx_time_logs_start_time ON time_logs(start_time);
        """,
    ),
    Migration(
        name="003_memories",
        sql="""
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            category TEXT,
            source TEXT,
            importance INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            last_accessed TEXT,
            access_count INTEGER DEFAULT 0,
            metadata TEXT
        );
        
        CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
        """,
    ),
    Migration(
        name="004_sessions",
        sql="""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            message_count INTEGER DEFAULT 0,
            metadata TEXT
        );
        
        CREATE TABLE IF NOT EXISTS threads (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            name TEXT,
            created_at TEXT NOT NULL,
            metadata TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
        );
        """,
    ),
]
```

## Storage Service

### Unified Access
```python
class Storage:
    """
    Unified storage service.
    
    Provides access to all repositories through a single interface.
    """
    
    def __init__(self, db: Database) -> None:
        self._db = db
        self.tasks = TaskRepository(db)
        self.lists = ListRepository(db)
        self.time_logs = TimeLogRepository(db)
        self.memories = MemoryRepository(db)
        self.sessions = SessionRepository(db)
    
    async def connect(self) -> None:
        """Connect to database."""
        await self._db.connect()
    
    async def close(self) -> None:
        """Close database connection."""
        await self._db.close()


# Usage in bootstrap
async def create_storage(config: CatoConfig) -> Storage:
    """
    Create and connect storage service.
    
    Parameters
    ----------
    config
        Application configuration.
    
    Returns
    -------
    Storage
        Connected storage service.
    """
    db = Database(expand_path(config.storage.database_path))
    storage = Storage(db)
    await storage.connect()
    return storage
```

## Backup

### Automatic Backup
```python
import shutil
from datetime import datetime

class BackupManager:
    """Manage database backups."""
    
    def __init__(self, config: StorageConfig) -> None:
        self._config = config
        self._db_path = expand_path(config.database_path)
        self._backup_dir = self._db_path.parent / "backups"
    
    async def create_backup(self) -> Path:
        """
        Create database backup.
        
        Returns
        -------
        Path
            Path to backup file.
        """
        self._backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self._backup_dir / f"cato_{timestamp}.db"
        
        # Copy database file
        shutil.copy2(self._db_path, backup_path)
        
        # Clean old backups (keep last 7)
        self._cleanup_old_backups(keep=7)
        
        logger.info(f"Database backed up to: {backup_path}")
        return backup_path
    
    def _cleanup_old_backups(self, keep: int) -> None:
        """Remove old backups, keeping the most recent."""
        backups = sorted(
            self._backup_dir.glob("cato_*.db"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        
        for backup in backups[keep:]:
            backup.unlink()
            logger.debug(f"Removed old backup: {backup}")
```

## Configuration

### Storage Config
```yaml
storage:
  database_path: "~/.local/share/cato/cato.db"
  backup_enabled: true
  backup_frequency_hours: 24
```

## ID Generation
```python
import uuid
from datetime import datetime

def generate_id(prefix: str = "") -> str:
    """
    Generate unique ID.
    
    Parameters
    ----------
    prefix
        Optional prefix for ID.
    
    Returns
    -------
    str
        Unique ID string.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique = uuid.uuid4().hex[:8]
    
    if prefix:
        return f"{prefix}_{timestamp}_{unique}"
    return f"{timestamp}_{unique}"
```

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



Let me continue reading the remaining files with memory references:


**Files Read:**

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
│   │   ├── __init__.py
│   │   ├── README.md        # Module documentation
│   │   ├── config.py        # Config loading, Pydantic models
│   │   ├── exceptions.py    # CatoError hierarchy
│   │   ├── logging.py       # Logging setup
│   │   └── types.py         # Shared data classes (Message, etc.)
│   │
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # LLMProvider protocol
│   │   │   ├── openai.py
│   │   │   ├── anthropic.py
│   │   │   ├── google.py
│   │   │   └── ollama.py
│   │   ├── search/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # SearchProvider protocol
│   │   │   ├── duckduckgo.py
│   │   │   └── google.py
│   │   └── tts/
│   │       ├── __init__.py
│   │       ├── base.py      # TTSProvider protocol
│   │       └── openai.py
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── vector/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # VectorStore protocol
│   │   │   └── chromadb.py
│   │   └── productivity/
│   │       ├── __init__.py
│   │       ├── base.py      # ProductivityStore protocol
│   │       └── sqlite.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── chat.py          # Chat orchestration
│   │   ├── productivity.py  # Task/list/memory logic
│   │   ├── tts.py           # TTS orchestration
│   │   └── web.py           # Web search orchestration
│   │
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── base.py          # @command decorator, registry
│   │   ├── core.py          # /help, /exit, /clear, /config
│   │   ├── history.py       # /history, /delete, /model, /showsys
│   │   ├── context.py       # /showcontext, /continue, /casual
│   │   ├── files.py         # /attach, /cd, /ls, /cat, /pwd
│   │   ├── export.py        # /writemd, /writecode, /writejson, etc.
│   │   ├── vector.py        # /vadd, /vdoc, /vquery, /vstats, /vdelete
│   │   ├── productivity.py  # /st, /list, /timelog, /remember
│   │   ├── tts.py           # /speak, /speaklike
│   │   └── web.py           # /web, /url
│   │
│   ├── display/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── console.py       # Rich console, output formatting
│   │   ├── input.py         # prompt_toolkit setup
│   │   ├── markdown.py      # Markdown rendering
│   │   └── themes.py        # Style definitions
│   │
│   └── resources/
│       ├── defaults.yaml    # Default configuration
│       └── help/            # Help text files
│           ├── overview.md
│           ├── commands.md
│           └── ...
│
└── tests/                   # Test suite
    ├── conftest.py          # Shared fixtures
    ├── unit/
    │   ├── test_config.py
    │   ├── test_commands.py
    │   └── ...
    ├── integration/
    │   ├── test_chat_service.py
    │   ├── test_vector_store.py
    │   └── ...
    └── e2e/
        ├── test_startup.py
        └── test_commands.py
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

All validation is handled by Pydantic. The config system uses Pydantic's features to enforce constraints and provide defaults.

### Pydantic Model Configuration
```python
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo

class CatoConfig(BaseModel):
    """Root configuration with validation."""
    
    model_config = ConfigDict(
        extra="ignore",          # Ignore unknown keys (warn separately)
        validate_default=True,   # Validate default values too
        str_strip_whitespace=True,
    )
    
    llm: LLMConfig
    vector_store: VectorStoreConfig
    storage: StorageConfig
    display: DisplayConfig
    commands: CommandConfig
    logging: LoggingConfig
    paths: PathConfig
```

### Field-Level Validation
Pydantic handles all value constraints:
```python
class LLMConfig(BaseModel):
    """LLM configuration with Pydantic validation."""
    
    provider: Literal["openai", "anthropic", "google", "ollama"]
    model: str = Field(min_length=1)  # Non-empty string
    temperature: float = Field(ge=0.0, le=2.0)
    max_tokens: int = Field(ge=1, le=200000)
    timeout_seconds: int = Field(ge=1, le=300)
```

### Cross-Field Validation
```python
class VectorStoreConfig(BaseModel):
    """Vector store config with cross-field validation."""
    
    enabled: bool
    chunk_size: int = Field(ge=100, le=10000)
    chunk_overlap: int = Field(ge=0)
    
    @field_validator("chunk_overlap")
    @classmethod
    def overlap_less_than_size(cls, v: int, info: ValidationInfo) -> int:
        """Ensure overlap is smaller than chunk size."""
        if "chunk_size" in info.data and v >= info.data["chunk_size"]:
            raise ValueError("chunk_overlap must be less than chunk_size")
        return v
```

### Unknown Keys Warning
```python
def load_config_with_warnings(data: dict) -> CatoConfig:
    """
    Load config, warning about unknown keys.
    
    Parameters
    ----------
    data
        Raw config dict.
    
    Returns
    -------
    CatoConfig
        Validated config (unknown keys ignored).
    """
    # Check for unknown keys before Pydantic ignores them
    warn_unknown_keys(data, CatoConfig)
    
    # Pydantic validates and ignores unknown keys
    return CatoConfig.model_validate(data)


def warn_unknown_keys(data: dict, model: type[BaseModel], path: str = "") -> None:
    """Recursively warn about unknown keys in config."""
    if not isinstance(data, dict):
        return
    
    model_fields = set(model.model_fields.keys())
    for key in data:
        full_path = f"{path}.{key}" if path else key
        if key not in model_fields:
            logger.warning(f"Unknown config key '{full_path}', ignoring")
        elif key in model_fields:
            field_type = model.model_fields[key].annotation
            # Recurse into nested models
            if hasattr(field_type, "model_fields"):
                warn_unknown_keys(data[key], field_type, full_path)
```

### Validation Error Handling
```python
def load_config(user_path: Path | None = None) -> CatoConfig:
    """
    Load and validate configuration.
    
    On validation error: log the error and exit (fail fast).
    Invalid config should not silently use defaults—user must fix it.
    """
    defaults = load_yaml(get_default_config_path())
    user_config = load_yaml(user_path) if user_path else {}
    merged = deep_merge(defaults, user_config)
    merged = apply_env_overrides(merged)
    
    try:
        return load_config_with_warnings(merged)
    except ValidationError as e:
        for error in e.errors():
            path = ".".join(str(loc) for loc in error["loc"])
            logger.error(f"Config error at '{path}': {error['msg']}")
        raise ConfigurationError("Invalid configuration. See errors above.")
```

### Default Values in Pydantic
Defaults come from the YAML file, not from Pydantic `Field(default=...)`. This keeps all defaults in one place:
```python
# GOOD: Defaults in YAML, Pydantic validates
class LLMConfig(BaseModel):
    temperature: float = Field(ge=0.0, le=2.0)  # No default here

# defaults.yaml provides the actual default:
# llm:
#   temperature: 1.0

# BAD: Defaults scattered in code
class LLMConfig(BaseModel):
    temperature: float = Field(default=1.0, ge=0.0, le=2.0)  # Don't do this
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

**/home/alex/Documents/repos/Cato/WARP.md**
```
# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management, conversational memory via vector storage, TTS, and web search.

**Status**: Pre-implementation - specification documents exist in `Project/Spec/`

### Purpose
Cato exists to provide maximum control over LLM interactions, tailored to specific user needs and idiosyncrasies. It is a chat client first, productivity client second.

### Intent
Cato provides a unified terminal interface for:
- Conversational AI interactions with multiple LLM providers
- Personal productivity management (tasks, lists, time tracking, memories)
- File operations and code management
- Persistent conversational memory with context retrieval
- Text-to-speech synthesis and web search integration

### Target User
- Single user on a single machine
- Users who are highly changeable, like to tinker and experiment
- Users who want flexible, modular architecture they can customise
- Multiple instances may run with different configurations simultaneously

## Before Starting Development

Read the specification documents in order:
1. `Project/Spec/GENERAL_PRINCIPLES.md` - Core philosophy and constraints
2. `Project/Spec/functional/SPEC_OVERVIEW.md` - Application flow and UI
3. Relevant functional specs in `Project/Spec/functional/`
4. Technical specs in `Project/Spec/technical/` (start with TECH_ARCHITECTURE.md)

## Architecture Overview

### Layered Architecture
```
Presentation → Commands → Services → Providers → Storage → Core
```
- Each layer may only import from layers below it
- No circular dependencies between layers
- Cross-cutting concerns (logging, errors) live in Core

### Protocol-Based Abstractions
- Key interfaces defined as Python `Protocol` classes
- Enables duck typing without inheritance
- Easy to create test mocks and swap implementations via config

### Dependency Injection
- Components receive dependencies at construction time
- `bootstrap.py` handles all component wiring
- No hard-coded provider instantiation in services

## Key Architectural Decisions

### Configuration
- YAML-driven configuration with overlay system (user config overlays defaults)
- **No hard-coded defaults in code** - all defaults in `cato/resources/defaults.yaml`
- Pydantic for all validation
- Unrecognised config keys warn but don't crash

### Multi-Provider LLM
- Must support OpenAI, Anthropic, Google, Ollama
- Use pydantic-ai over LangChain for agent/API interactions
- Each provider implements `LLMProvider` protocol

### Storage
- ChromaDB for vector store (embeddings, similarity search)
- SQLite for productivity data (tasks, lists, memories)
- **Never load entire vector store into memory**
- Storage layer contains no business logic—pure data access

### Command System
- Slash commands (`/help`, `/speak`, `/web`, etc.) for explicit actions
- Decorator-based registration - adding a command requires only one file
- **No natural language command interface** - commands use explicit syntax

### Error Handling
- Atomic exception handling (specific exceptions, not broad catches)
- Custom exception hierarchy (`CatoError` base class in `cato/core/exceptions.py`)
- Graceful degradation for non-critical failures
- Never silent failures
- Errors flow upward: Storage → Service → Command → Presentation

## Directory Structure

```
cato/                        # Repository root
├── pyproject.toml           # Package metadata (uv/PEP 621)
├── agent.txt                # AI codebase navigation
├── cato/                    # Python package
│   ├── __main__.py          # Entry point: python -m cato
│   ├── bootstrap.py         # Component wiring
│   ├── app.py               # Main run loop
│   ├── core/                # Config, exceptions, logging, types
│   ├── providers/           # LLM, search, TTS backends
│   │   ├── llm/             # OpenAI, Anthropic, Google, Ollama
│   │   ├── search/          # DuckDuckGo, Google
│   │   └── tts/             # OpenAI TTS
│   ├── storage/             # ChromaDB, SQLite
│   ├── services/            # Business logic orchestration
│   ├── commands/            # Slash command implementations
│   ├── display/             # Rich console, prompt_toolkit
│   └── resources/           # defaults.yaml, help files
└── tests/                   # Unit, integration, e2e
```

## Code Organisation Requirements

- Create `agent.txt` at root for AI navigation
- Each module directory must have a README explaining purpose and extension
- Numpy-format docstrings, type hints on all functions
- Relative imports within package
- Single responsibility per file

## Testing Strategy

- **Unit tests**: Individual functions/classes in isolation with mocked dependencies
- **Integration tests**: Service + storage, command + service combinations
- **E2E tests**: Critical user journeys only (minimal—they're slow and brittle)
- Use pytest with fixtures for test database setup/teardown
- Mock external APIs at HTTP level
- Focus on core functionality, not exhaustive coverage

## Technology Stack

### Required
- Rich (formatting), prompt_toolkit (input)
- ChromaDB, OpenAI Embeddings API
- PyYAML, Pydantic
- pydantic-ai (productivity agent)
- LLM provider SDKs (OpenAI, Anthropic, Google)

### Optional
- OpenAI TTS API
- DuckDuckGo/Google/Bing search
- Ollama (local LLM)

## Development Workflow

- `main` is the stable branch; all work on feature branches
- Branch naming: `feature/<description>` or `fix/<description>`
- CI should be fast (< 5 minutes)
- Releases when meaningful changes accumulate

```



Now I have a complete picture. Let me create a todo list to track the removal of memory references across all files:
UpdateTodos: 11 items


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_OVERVIEW.md
@@ -2,15 +2,15 @@
 
 ## Application Summary
 
-**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management capabilities, and conversational memory through vector storage.
+**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management capabilities, and conversational context through vector storage.
 
 ## Purpose
 
 Cato provides a unified terminal interface for:
 - Conversational AI interactions with multiple LLM providers
-- Personal productivity management (tasks, lists, time tracking, memories)
+- Personal productivity management (tasks, lists, time tracking)
 - File operations and code management
-- Persistent conversational memory with context retrieval
+- Persistent conversational context with retrieval
 - Text-to-speech synthesis
 - Web search integration
 
@@ -19,7 +19,7 @@
 1. **Terminal-First**: All functionality accessible via keyboard in a command-line interface
 2. **Rich Output**: Markdown rendering, syntax highlighting, and formatted tables
 3. **Unified Experience**: Single interface for chat, productivity, and file operations
-4. **Persistent Memory**: Conversation and productivity data persisted across sessions
+4. **Persistent Storage**: Conversation and productivity data persisted across sessions
 5. **Extensible Commands**: Slash command system for explicit actions
 6. **Graceful Degradation**: Continue operation when individual components fail
 
@@ -39,11 +39,10 @@
 ### Input Processing Order
 User input is processed in the following priority order:
 
-1. **Memory prompts**: If awaiting yes/no response for memory storage suggestion
-2. **Slash commands**: Input starting with `/` routes to command parser
-3. **Productivity routing**: Input starting with `%` routes to productivity agent
-4. **File routing**: Input starting with `@` routes to file tools agent
-5. **Regular chat**: All other input sent to LLM with context retrieval
+1. **Slash commands**: Input starting with `/` routes to command parser
+2. **Productivity routing**: Input starting with `%` routes to productivity agent
+3. **File routing**: Input starting with `@` routes to file tools agent
+4. **Regular chat**: All other input sent to LLM with context retrieval
 
 ### Session State
 - **Session ID**: Unique UUID generated per application launch
@@ -60,7 +59,7 @@
 |----------|-------------|
 | SPEC_CORE_CHAT.md | LLM integration, message processing, display |
 | SPEC_COMMAND_SYSTEM.md | Slash command framework and all commands |
-| SPEC_PRODUCTIVITY.md | Tasks, lists, timelog, memories |
+|| SPEC_PRODUCTIVITY.md | Tasks, lists, timelog |
 | SPEC_FILE_OPERATIONS.md | File commands, attach, export, aliases |
 | SPEC_VECTOR_STORE.md | Conversation storage, similarity search |
 | SPEC_TTS.md | Text-to-speech functionality |
@@ -109,7 +108,6 @@
 - 🟡 In Progress  
 - ✅ Completed
 - 🗑️ Deleted
-- 🧠 Memory recall indicator
 - 💭 Context indicator
 - 🔊 TTS indicator
 
@@ -133,7 +131,7 @@
 ## Error Handling Philosophy
 
 1. **Non-critical failures**: Log warning, continue with reduced functionality
-   - Vector store unavailable → chat continues without memory
+   - Vector store unavailable → chat continues without context retrieval
    - TTS playback fails → show error, continue chat
    - Web search fails → show error, allow retry
 

```



MarkAsCompleted: 1 items


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_VECTOR_STORE.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_VECTOR_STORE.md
@@ -2,7 +2,7 @@
 
 ## Overview
 
-The vector store provides persistent conversation memory using vector embeddings for semantic similarity search. It enables context retrieval from previous conversations and document storage for future reference.
+The vector store provides persistent conversation context using vector embeddings for semantic similarity search. It enables context retrieval from previous conversations and document storage for future reference.
 
 ## Critical Performance Requirements
 
@@ -278,8 +278,6 @@
   chat_window: 3
   context_results: 5
   search_context_window: 3
-  memory_threshold: 0.7
-  memory_results: 3
 ```
 
 ### Chunking Config
@@ -304,7 +302,7 @@
 ### Graceful Degradation
 If vector store fails to initialize:
 - Log warning
-- Continue without memory features
+- Continue without context retrieval
 - Conversation still works
 
 ### Operation Failures
@@ -326,6 +324,5 @@
 
 When disabled:
 - No context retrieval
-- No memory features
 - No `/v*` commands available
 - `/continue` unavailable

```



MarkAsCompleted: 1 items


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_PRODUCTIVITY.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_PRODUCTIVITY.md
@@ -2,7 +2,7 @@
 
 ## Overview
 
-The productivity system provides task management, list organization, time tracking, and memory storage through natural language interaction. It uses a dedicated AI agent to parse requests and manage productivity data stored in SQLite.
+The productivity system provides task management, list organization, and time tracking through natural language interaction. It uses a dedicated AI agent to parse requests and manage productivity data stored in SQLite.
 
 
 ## Entity Types
@@ -147,8 +147,3 @@
 
 ### Response Format
 Productivity responses are displayed in the assistant panel but not added to conversation history, keeping the main LLM context clean.
-
-### Vector Store Integration
-Productivity exchanges are stored in the vector store for:
-- Future context retrieval
-- Thread continuation support

```



MarkAsCompleted: 1 items


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md
@@ -303,8 +303,6 @@
 /vstats
 ```
 
-### Memory Commands
-
 ### Productivity Commands
 
 See SPEC_PRODUCTIVITY.md for detailed productivity documentation.

```



MarkAsCompleted: 1 items


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

The provider is automatically determined from the model name:
- `gpt-*`, `o1-*` → OpenAI
- `claude-*` → Anthropic
- `gemini-*` → Google
- Other models → Ollama (local)

### LLM Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| model | gpt-4o-mini | Provider-specific | LLM model identifier |
| temperature | 1.0 | 0.0-2.0 | Response randomness |
| max_tokens | 10000 | >0 | Maximum response tokens |

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
Check for productivity marker (%) → Route to ProductivityAgent
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
   - Uses configurable `search_context_window` (default: -1 = all exchanges)

2. **Retrieves similar exchanges** from vector store
   - Uses similarity threshold from config
   - Returns up to `context_results` exchanges

3. **Injects context** into API request
   - Memories always included if found
   - Regular context included based on `context_mode`:
     - `off`: No context injection (default)
     - `on`: Full context with excerpts shown
     - `summary`: Context injected but only count displayed

### Context Display Modes

Controlled via `/showcontext` command:

| Mode | Behavior |
|------|----------|
| off | No context shown or injected |
| on | Context injected, excerpts displayed |
| summary | Context injected, only count displayed |

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
- Default timeout: 120 seconds
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
| user_label | "User" | Label for user messages |
| assistant_label | "Assistant" | Label for assistant messages |
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





**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_CORE_CHAT.md
@@ -103,12 +103,10 @@
    - Uses similarity threshold from config
    - Returns up to `context_results` exchanges
 
-3. **Injects context** into API request
-   - Memories always included if found
-   - Regular context included based on `context_mode`:
-     - `off`: No context injection (default)
-     - `on`: Full context with excerpts shown
-     - `summary`: Context injected but only count displayed
+3. **Injects context** into API request based on `context_mode`:
+   - `off`: No context injection (default)
+   - `on`: Full context with excerpts shown
+   - `summary`: Context injected but only count displayed
 
 ### Context Display Modes
 

```



MarkAsCompleted: 1 items
Now let me handle the technical specs:


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_STORAGE.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_STORAGE.md
@@ -1,7 +1,7 @@
 # Storage Technical Specification
 
 ## Overview
-Cato uses SQLite for structured data storage (tasks, lists, time logs, memories). The database provides persistent storage for productivity features with a simple data access layer.
+Cato uses SQLite for structured data storage (tasks, lists, time logs). The database provides persistent storage for productivity features with a simple data access layer.
 
 ## Database Location
 ```
@@ -80,24 +80,6 @@
 CREATE INDEX IF NOT EXISTS idx_time_logs_category ON time_logs(category);
 ```
 
-### Memories Table
-```sql
-CREATE TABLE IF NOT EXISTS memories (
-    id TEXT PRIMARY KEY,
-    content TEXT NOT NULL,
-    category TEXT,
-    source TEXT,                             -- 'user', 'conversation', 'import'
-    importance INTEGER DEFAULT 1,            -- 1-5 scale
-    created_at TEXT NOT NULL,
-    last_accessed TEXT,
-    access_count INTEGER DEFAULT 0,
-    metadata TEXT
-);
-
-CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
-CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance);
-```
-
 ### Sessions Table
 ```sql
 CREATE TABLE IF NOT EXISTS sessions (
@@ -488,25 +470,7 @@
         """,
     ),
     Migration(
-        name="003_memories",
-        sql="""
-        CREATE TABLE IF NOT EXISTS memories (
-            id TEXT PRIMARY KEY,
-            content TEXT NOT NULL,
-            category TEXT,
-            source TEXT,
-            importance INTEGER DEFAULT 1,
-            created_at TEXT NOT NULL,
-            last_accessed TEXT,
-            access_count INTEGER DEFAULT 0,
-            metadata TEXT
-        );
-        
-        CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
-        """,
-    ),
-    Migration(
-        name="004_sessions",
+        name="003_sessions",
         sql="""
         CREATE TABLE IF NOT EXISTS sessions (
             id TEXT PRIMARY KEY,
@@ -545,7 +509,6 @@
         self.tasks = TaskRepository(db)
         self.lists = ListRepository(db)
         self.time_logs = TimeLogRepository(db)
-        self.memories = MemoryRepository(db)
         self.sessions = SessionRepository(db)
     
     async def connect(self) -> None:

```



MarkAsCompleted: 1 items


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md
@@ -62,7 +62,7 @@
 #### Services
 - Business logic orchestration
 - Chat service: message handling, context retrieval, response generation
-- Productivity service: task/list/memory operations
+- Productivity service: task/list operations
 - TTS service: text processing, audio generation
 - Web service: search execution, URL fetching
 
@@ -272,7 +272,7 @@
 │   │   ├── __init__.py
 │   │   ├── README.md
 │   │   ├── chat.py          # Chat orchestration
-│   │   ├── productivity.py  # Task/list/memory logic
+│   │   ├── productivity.py  # Task/list logic
 │   │   ├── tts.py           # TTS orchestration
 │   │   └── web.py           # Web search orchestration
 │   │

```



MarkAsCompleted: 1 items


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_CONFIG_SYSTEM.md
@@ -398,7 +398,7 @@
   enabled: true
   backend: "chromadb"
   path: "~/.local/share/cato/vectordb"
-  collection_name: "cato_memory"
+  collection_name: "cato_context"
   embedding_model: "text-embedding-3-small"
   chunk_size: 1000
   chunk_overlap: 200

```



MarkAsCompleted: 1 items
The TECH_PERFORMANCE.md references to "memory" are about RAM/system memory (e.g., "don't load into memory"), not the memory feature. Let me verify:


**Files Read:**

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



Good - all the "memory" references in TECH_PERFORMANCE.md are about system RAM, not the memory feature. Same for GENERAL_PRINCIPLES.md line 89. I'll mark those as done and handle WARP.md.
MarkAsCompleted: 2 items


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/WARP.md
+++ /home/alex/Documents/repos/Cato/WARP.md
@@ -4,7 +4,7 @@
 
 ## Project Overview
 
-**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management, conversational memory via vector storage, TTS, and web search.
+**Cato** (Chat at the Terminal Orchestrator) is an interactive command-line LLM chat application with integrated productivity features, file management, conversational context via vector storage, TTS, and web search.
 
 **Status**: Pre-implementation - specification documents exist in `Project/Spec/`
 
@@ -14,9 +14,9 @@
 ### Intent
 Cato provides a unified terminal interface for:
 - Conversational AI interactions with multiple LLM providers
-- Personal productivity management (tasks, lists, time tracking, memories)
+- Personal productivity management (tasks, lists, time tracking)
 - File operations and code management
-- Persistent conversational memory with context retrieval
+- Persistent conversational context with retrieval
 - Text-to-speech synthesis and web search integration
 
 ### Target User
@@ -68,7 +68,7 @@
 
 ### Storage
 - ChromaDB for vector store (embeddings, similarity search)
-- SQLite for productivity data (tasks, lists, memories)
+- SQLite for productivity data (tasks, lists)
 - **Never load entire vector store into memory**
 - Storage layer contains no business logic—pure data access
 

```



MarkAsCompleted: 1 items
Let me also check the spec review report and notes files for any memory references that should be updated:


**Files Read:**

**/home/alex/Documents/repos/Cato/Project/Reports/2026-01-14_spec_review.md**
```
# Cato Specification Critical Review
**Date:** 2026-01-14
**Reviewer:** Warp Agent

## Executive Summary

The Cato specification is comprehensive and well-structured for a pre-implementation project. However, several critical issues, inconsistencies, and areas of under-specification were identified that should be addressed before implementation begins.

---

## Critical Issues

### 1. Duplicate Overview Documents
**Location:** `functional/SPEC_OVERVIEW.md` and `functional/FUNCTIONAL_SPECIFICATION_OVERVIEW.md`

**Criticism:** Two documents serve essentially the same purpose, creating maintenance burden and potential for divergence. The content overlaps significantly but isn't identical—for example, FUNCTIONAL_SPECIFICATION_OVERVIEW.md mentions "async operations" and "timeout handling" as features but SPEC_OVERVIEW.md doesn't.

**Proposal:** Merge into a single `FUNCTIONAL_SPECIFICATION_OVERVIEW.md` that serves as the canonical overview. The shorter `SPEC_OVERVIEW.md` can be deleted or converted to a brief index/TOC document.

---

### 2. Inconsistent Configuration Key Naming

**Location:** Multiple specs reference configuration differently.

**Criticism:** Configuration keys are inconsistent across documents:
- `SPEC_CONFIGURATION.md` uses `vector_store.context_similarity_threshold`
- `SPEC_VECTOR_STORE.md` references `similarity_threshold` and `memory_threshold`
- `TECH_CONFIG_SYSTEM.md` uses different nested structures

The functional spec (SPEC_CONFIGURATION.md line 79) shows `context_similarity_threshold` while the vector store functional spec (SPEC_VECTOR_STORE.md line 280) shows `similarity_threshold` and `memory_threshold` with different defaults (0.65 vs 0.7).

**Proposal:** Create a canonical `defaults.yaml` reference document that all other specs must align with. Use consistent naming: `vector_store.context_similarity_threshold` everywhere.

---

### 3. Memory System Specified But Not Defined

**Location:** Multiple references throughout specs

**Criticism:** The specs repeatedly reference "memories" as a productivity feature (SPEC_PRODUCTIVITY.md, TECH_STORAGE.md memories table), but there is no `SPEC_MEMORY.md` or dedicated functional specification for this feature. The command reference in SPEC_COMMAND_SYSTEM.md lists `/remember` with aliases `/rem, /r` but never defines what these commands do.

Similarly, SPEC_VECTOR_STORE.md mentions `memory_threshold` and `memory_results` config options (line 281-282) without explaining the memory retrieval flow.

**Proposal:** Either:
- Create a dedicated `SPEC_MEMORY.md` explaining the memory system, its integration with both SQLite (structured memories) and vector store (semantic memory retrieval)
- OR explicitly descope memories from v1 and remove all references

---

### 4. Timelog Feature Referenced But Not Specified

**Location:** SPEC_COMMAND_SYSTEM.md line 389, TECH_STORAGE.md

**Criticism:** The command alias table references `/timelog` with aliases `/tl, /time`, and TECH_STORAGE.md defines a `time_logs` table schema. However, there is no functional specification for time tracking. The productivity spec (SPEC_PRODUCTIVITY.md) only covers tasks and lists.

**Proposal:** Add a time tracking section to SPEC_PRODUCTIVITY.md or descope from v1.

---

### 5. Provider Auto-Detection vs Explicit Configuration Conflict

**Location:** SPEC_CORE_CHAT.md vs TECH_CONFIG_SYSTEM.md

**Criticism:** SPEC_CORE_CHAT.md (lines 20-25) states the provider is "automatically determined from the model name" (e.g., `gpt-*` → OpenAI). However, TECH_CONFIG_SYSTEM.md (line 113) specifies an explicit `provider: "openai"` configuration key with `Literal["openai", "anthropic", "google", "ollama"]` validation.

Which is canonical? If auto-detection, the explicit provider config is redundant. If explicit, the auto-detection description is misleading.

**Proposal:** Clarify the intended behaviour:
- **Recommended:** Use explicit `provider` config as primary. Model auto-detection can be a fallback when provider is `null` or "auto".

---

### 6. Context Mode vs Context Display Inconsistency

**Location:** SPEC_CORE_CHAT.md, SPEC_CONFIGURATION.md

**Criticism:** SPEC_CORE_CHAT.md (lines 107-121) defines three context modes: `off`, `on`, `summary`. The `off` mode description says "No context shown or injected" but this contradicts GENERAL_PRINCIPLES.md which emphasizes always using vector store for context retrieval.

If `off` means no context injection, the vector store becomes useless. If it only means "don't display", that should be clearer.

**Proposal:** Rename to `context_display_mode` and clarify:
- `off`: Context is retrieved and injected, but not displayed to user
- `on`: Context is retrieved, injected, and displayed with excerpts
- `summary`: Context is retrieved, injected, and count is displayed

---

### 7. Missing Embedding Provider Abstraction

**Location:** TECH_VECTOR_STORE.md, TECH_ARCHITECTURE.md

**Criticism:** The vector store spec hard-codes OpenAI embeddings (`OpenAIEmbeddingProvider`). This contradicts the general architecture principle of swappable components. Users wanting local-only operation (Ollama) cannot use embeddings without OpenAI API key.

**Proposal:** Define an `EmbeddingProvider` protocol similar to `LLMProvider`. Add:
- `OpenAIEmbeddingProvider`
- `OllamaEmbeddingProvider` (Ollama supports embeddings)
- Configuration option: `embedding.provider`

---

## Moderate Issues

### 8. Productivity Agent Undefined

**Location:** SPEC_PRODUCTIVITY.md line 143-148, SPEC_OVERVIEW.md line 44

**Criticism:** Multiple specs reference a "productivity agent" powered by pydantic-ai for natural language processing of productivity commands. However:
- The agent's capabilities are not specified
- Input/output format is not defined
- How it differs from the main LLM is unclear
- GENERAL_PRINCIPLES.md line 49 explicitly states "Natural language interface to productivity/commands is explicitly NOT wanted"

This is a significant contradiction.

**Proposal:** Clarify the productivity agent's role:
- If commands like `/st` use the agent to parse arguments, document this
- If the `%` prefix is meant for free-form natural language, this contradicts GENERAL_PRINCIPLES
- Consider removing the productivity agent and using structured command parsing only (simpler, more predictable)

---

### 9. File Routing Marker Undocumented

**Location:** SPEC_OVERVIEW.md line 46

**Criticism:** The input processing order mentions "File routing: Input starting with `@` routes to file tools agent" but:
- No functional spec documents this `@` prefix
- SPEC_FILE_OPERATIONS.md only covers `/file` commands
- The "file tools agent" is never defined

**Proposal:** Either:
- Add documentation for the `@` prefix and file tools agent
- OR remove this from input processing order if not in v1 scope

---

### 10. Pydantic vs Dataclass Usage Inconsistent

**Location:** TECH_COMMAND_FRAMEWORK.md, TECH_DISPLAY.md, TECH_LLM_INTEGRATION.md

**Criticism:** The specs attempt to distinguish when to use Pydantic vs dataclasses but apply it inconsistently:
- `CommandResult` is a dataclass (TECH_COMMAND_FRAMEWORK.md line 14) because it's "internal return data"
- `Message` is a Pydantic BaseModel (TECH_LLM_INTEGRATION.md line 13) for "normalised message format"
- `DisplayMessage` is a dataclass (TECH_DISPLAY.md line 14) because it's "internal display data"

But `Message` and `DisplayMessage` serve similar purposes. The rule "Pydantic for data crossing system boundaries" is subjective.

**Proposal:** Establish clearer guidelines:
- Pydantic: All models used in configuration, storage, or API responses (validates external data)
- Dataclass: Internal state containers that are never serialized or validated
- Document the reasoning in TECH_ARCHITECTURE.md

---

### 11. Dynamic Threshold Algorithm Unspecified

**Location:** SPEC_VECTOR_STORE.md lines 89-94

**Criticism:** Dynamic thresholding is documented as "adjusts threshold based on context length" with "Simple linear adjustment based on context message count" but no formula or parameters are provided. This makes implementation ambiguous.

**Proposal:** Specify the algorithm:
```
threshold = base_threshold - (adjustment_factor * message_count)
threshold = max(threshold, min_threshold)
```
With configurable `adjustment_factor` and `min_threshold`.

---

### 12. Casual Mode Undefined

**Location:** SPEC_COMMAND_SYSTEM.md lines 157-162

**Criticism:** `/casual on|off` is listed as a command to "Toggle casual conversation mode" but:
- What casual mode does is never defined
- No configuration options for it exist
- It's referenced in CLI arguments (SPEC_CONFIGURATION.md line 172: "casual mode")

**Proposal:** Define casual mode behaviour or remove if not in v1 scope. Possible interpretation: disables vector store context retrieval for lighter conversations.

---

### 13. Missing Error Messages for Commands

**Location:** SPEC_COMMAND_SYSTEM.md

**Criticism:** While error handling is documented at a high level, specific error messages for each command are not specified. For example:
- What happens if `/speak` is called but there's no previous response?
- What if `/continue` is given an invalid thread ID?
- What if `/model` is given an unsupported model name?

TECH_ERROR_HANDLING.md provides patterns but command-specific errors should be in the command spec.

**Proposal:** Add an "Error States" section to each command specification in SPEC_COMMAND_SYSTEM.md.

---

## Minor Issues

### 14. Inconsistent Status Indicators

**Location:** SPEC_OVERVIEW.md lines 108-115, SPEC_PRODUCTIVITY.md

**Criticism:** Status indicators use different emoji:
- SPEC_OVERVIEW.md: 🔵 Active, 🟡 In Progress, ✅ Completed
- SPEC_PRODUCTIVITY.md: No indicators defined, relies on overview

Should be consolidated in a single location (likely display/themes config).

**Proposal:** Move status indicator definitions to SPEC_CONFIGURATION.md under display settings, making them configurable.

---

### 15. /delete Command Semantics Unclear

**Location:** SPEC_COMMAND_SYSTEM.md lines 103-108, SPEC_CORE_CHAT.md lines 222-226

**Criticism:** `/delete [n]` removes "last n user/assistant exchange pairs" from history. But:
- Does it also delete from vector store?
- If not, deleted exchanges still appear in context retrieval
- If yes, this isn't documented

**Proposal:** Clarify: `/delete` removes from session history only. Add `/vdelete` for vector store deletion (already exists). Document that deleted messages may still appear in context retrieval.

---

### 16. Chat Window vs Search Context Window Confusion

**Location:** SPEC_CONFIGURATION.md lines 77-82

**Criticism:** Two similar-sounding config options:
- `chat_window`: "number of recent exchanges to maintain in current chat"
- `search_context_window`: "number of recent exchanges to use in vector for similarity search"

The distinction is subtle. One limits what goes to the LLM, the other limits what's used to build the search query.

**Proposal:** Rename for clarity:
- `chat_history_limit`: Max messages sent to LLM
- `context_query_depth`: Messages used to build vector search query

---

### 17. Bootstrap Module Over-specified

**Location:** TECH_ARCHITECTURE.md lines 175-211

**Criticism:** The bootstrap code example shows specific implementation details that may not survive contact with reality. For example, it assumes synchronous provider creation, but TECH_VECTOR_STORE.md shows async initialisation.

**Proposal:** Keep bootstrap documentation conceptual. The code examples should demonstrate patterns, not prescribe implementation.

---

### 18. Missing Conversation Export Format

**Location:** SPEC_FILE_OPERATIONS.md

**Criticism:** `/writejson` exports conversation with a specific JSON structure (lines 238-262), but the schema isn't formally defined. Similarly for `/writemd`. This makes it hard to write tests or create importers.

**Proposal:** Add JSON Schema definitions for export formats, or reference a schema file.

---

### 19. Audio Player Detection Not Portable

**Location:** SPEC_TTS.md lines 172-183

**Criticism:** Platform-specific audio player detection is documented (mpg123, ffplay, afplay) but:
- No fallback behaviour if none found
- Windows uses `start` which is unreliable
- No configuration option to specify preferred player

**Proposal:** Add `tts.audio_player` config option to specify player explicitly. Detection becomes fallback.

---

### 20. Web Search Rate Limiting Unspecified

**Location:** SPEC_WEB_SEARCH.md lines 217-227

**Criticism:** Rate limiting is mentioned as a "consideration" with vague guidance. For a spec-driven project, this should be concrete:
- How long between requests?
- Are concurrent requests allowed?
- What happens when rate limited by search engine?

**Proposal:** Specify defaults:
- `web_search.request_delay_ms: 500`
- `web_search.max_concurrent: 1`
- Document exponential backoff on 429 responses

---

## Structural Recommendations

### 21. Add Version Number to Specs

**Proposal:** Each spec document should have a version header and change log. This helps track when specs diverge from implementation.

### 22. Create Glossary

**Proposal:** Create `GLOSSARY.md` defining terms like "exchange", "thread", "session", "context", "memory" which are used throughout but with subtly different meanings.

### 23. Add State Diagram

**Proposal:** Add a state diagram for conversation/session lifecycle to SPEC_CORE_CHAT.md showing how sessions, threads, and exchanges relate.

### 24. Consolidate Configuration Reference

**Proposal:** Create a single `CONFIG_REFERENCE.md` that is the authoritative source for all configuration keys. Other specs should reference this rather than re-documenting options.

---

## Summary of Priority Actions

**Must Fix Before Implementation:**
1. Resolve duplicate overview documents
2. Define or descope memory system
3. Define or descope timelog system
4. Clarify provider auto-detection vs explicit configuration
5. Fix context mode semantics

**Should Fix:**
6. Standardise configuration key naming
7. Add embedding provider abstraction
8. Clarify productivity agent role
9. Document file routing marker
10. Specify dynamic threshold algorithm

**Nice to Have:**
11. Add version numbers to specs
12. Create glossary
13. Add state diagrams
14. Consolidate configuration reference

---

*Report generated by Warp Agent*

```



The spec review report discusses the memory system issue and suggests descoping it. I should update the relevant parts of this report to reflect that memory has been removed:


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Reports/2026-01-14_spec_review.md
+++ /home/alex/Documents/repos/Cato/Project/Reports/2026-01-14_spec_review.md
@@ -25,27 +25,19 @@
 
 **Criticism:** Configuration keys are inconsistent across documents:
 - `SPEC_CONFIGURATION.md` uses `vector_store.context_similarity_threshold`
-- `SPEC_VECTOR_STORE.md` references `similarity_threshold` and `memory_threshold`
+- `SPEC_VECTOR_STORE.md` references `similarity_threshold`
 - `TECH_CONFIG_SYSTEM.md` uses different nested structures
 
-The functional spec (SPEC_CONFIGURATION.md line 79) shows `context_similarity_threshold` while the vector store functional spec (SPEC_VECTOR_STORE.md line 280) shows `similarity_threshold` and `memory_threshold` with different defaults (0.65 vs 0.7).
+The functional spec (SPEC_CONFIGURATION.md line 79) shows `context_similarity_threshold` while the vector store functional spec uses `similarity_threshold`.
 
 **Proposal:** Create a canonical `defaults.yaml` reference document that all other specs must align with. Use consistent naming: `vector_store.context_similarity_threshold` everywhere.
 
 ---
 
-### 3. Memory System Specified But Not Defined
-
-**Location:** Multiple references throughout specs
+### 3. ~~Memory System Specified But Not Defined~~ RESOLVED
 
-**Criticism:** The specs repeatedly reference "memories" as a productivity feature (SPEC_PRODUCTIVITY.md, TECH_STORAGE.md memories table), but there is no `SPEC_MEMORY.md` or dedicated functional specification for this feature. The command reference in SPEC_COMMAND_SYSTEM.md lists `/remember` with aliases `/rem, /r` but never defines what these commands do.
+**Resolution:** Memory system has been descoped from v1. All references to memories, memory storage, memory retrieval, and related configuration have been removed from the specifications.
 
-Similarly, SPEC_VECTOR_STORE.md mentions `memory_threshold` and `memory_results` config options (line 281-282) without explaining the memory retrieval flow.
-
-**Proposal:** Either:
-- Create a dedicated `SPEC_MEMORY.md` explaining the memory system, its integration with both SQLite (structured memories) and vector store (semantic memory retrieval)
-- OR explicitly descope memories from v1 and remove all references
-
 ---
 
 ### 4. Timelog Feature Referenced But Not Specified
@@ -298,7 +290,7 @@
 
 ### 22. Create Glossary
 
-**Proposal:** Create `GLOSSARY.md` defining terms like "exchange", "thread", "session", "context", "memory" which are used throughout but with subtly different meanings.
+**Proposal:** Create `GLOSSARY.md` defining terms like "exchange", "thread", "session", "context" which are used throughout but with subtly different meanings.
 
 ### 23. Add State Diagram
 
@@ -314,7 +306,7 @@
 
 **Must Fix Before Implementation:**
 1. Resolve duplicate overview documents
-2. Define or descope memory system
+2. ~~Define or descope memory system~~ ✅ RESOLVED - memory descoped
 3. Define or descope timelog system
 4. Clarify provider auto-detection vs explicit configuration
 5. Fix context mode semantics

```



Now let me check if there are any remaining memory references I might have missed, particularly the `/remember` command alias:


**Grep Results:**

- **/home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md**
- **/home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md**




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
- Productivity service: task/list operations
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
│   │   ├── __init__.py
│   │   ├── README.md        # Module documentation
│   │   ├── config.py        # Config loading, Pydantic models
│   │   ├── exceptions.py    # CatoError hierarchy
│   │   ├── logging.py       # Logging setup
│   │   └── types.py         # Shared data classes (Message, etc.)
│   │
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # LLMProvider protocol
│   │   │   ├── openai.py
│   │   │   ├── anthropic.py
│   │   │   ├── google.py
│   │   │   └── ollama.py
│   │   ├── search/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # SearchProvider protocol
│   │   │   ├── duckduckgo.py
│   │   │   └── google.py
│   │   └── tts/
│   │       ├── __init__.py
│   │       ├── base.py      # TTSProvider protocol
│   │       └── openai.py
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── vector/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # VectorStore protocol
│   │   │   └── chromadb.py
│   │   └── productivity/
│   │       ├── __init__.py
│   │       ├── base.py      # ProductivityStore protocol
│   │       └── sqlite.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── chat.py          # Chat orchestration
│   │   ├── productivity.py  # Task/list logic
│   │   ├── tts.py           # TTS orchestration
│   │   └── web.py           # Web search orchestration
│   │
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── base.py          # @command decorator, registry
│   │   ├── core.py          # /help, /exit, /clear, /config
│   │   ├── history.py       # /history, /delete, /model, /showsys
│   │   ├── context.py       # /showcontext, /continue, /casual
│   │   ├── files.py         # /attach, /cd, /ls, /cat, /pwd
│   │   ├── export.py        # /writemd, /writecode, /writejson, etc.
│   │   ├── vector.py        # /vadd, /vdoc, /vquery, /vstats, /vdelete
│   │   ├── productivity.py  # /st, /list, /timelog, /remember
│   │   ├── tts.py           # /speak, /speaklike
│   │   └── web.py           # /web, /url
│   │
│   ├── display/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── console.py       # Rich console, output formatting
│   │   ├── input.py         # prompt_toolkit setup
│   │   ├── markdown.py      # Markdown rendering
│   │   └── themes.py        # Style definitions
│   │
│   └── resources/
│       ├── defaults.yaml    # Default configuration
│       └── help/            # Help text files
│           ├── overview.md
│           ├── commands.md
│           └── ...
│
└── tests/                   # Test suite
    ├── conftest.py          # Shared fixtures
    ├── unit/
    │   ├── test_config.py
    │   ├── test_commands.py
    │   └── ...
    ├── integration/
    │   ├── test_chat_service.py
    │   ├── test_vector_store.py
    │   └── ...
    └── e2e/
        ├── test_startup.py
        └── test_commands.py
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



I need to remove the `/remember` command alias and update the productivity.py file reference:

_File edits failed: Could not apply all diffs to /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md. _



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
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md
@@ -286,7 +286,7 @@
 │   │   ├── files.py         # /attach, /cd, /ls, /cat, /pwd
 │   │   ├── export.py        # /writemd, /writecode, /writejson, etc.
 │   │   ├── vector.py        # /vadd, /vdoc, /vquery, /vstats, /vdelete
-│   │   ├── productivity.py  # /st, /list, /timelog, /remember
+│   ├── productivity.py  # /st, /list, /timelog
 │   │   ├── tts.py           # /speak, /speaklike
 │   │   └── web.py           # /web, /url
 │   │

--- /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/functional/SPEC_COMMAND_SYSTEM.md
@@ -381,7 +381,6 @@
 | /continue | /cont |
 | /speak | /s |
 | /speaklike | /sl |
-| /remember | /rem, /r |
 | /st | /show-tasks, /tasks |
 | /list | /lists, /show-lists |
 | /timelog | /tl, /time |

```



Let me verify the edit was applied correctly by checking the file:


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



Now let me fix the TECH_ARCHITECTURE.md file - there seems to be a formatting issue:


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
- Productivity service: task/list operations
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
│   │   ├── __init__.py
│   │   ├── README.md        # Module documentation
│   │   ├── config.py        # Config loading, Pydantic models
│   │   ├── exceptions.py    # CatoError hierarchy
│   │   ├── logging.py       # Logging setup
│   │   └── types.py         # Shared data classes (Message, etc.)
│   │
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # LLMProvider protocol
│   │   │   ├── openai.py
│   │   │   ├── anthropic.py
│   │   │   ├── google.py
│   │   │   └── ollama.py
│   │   ├── search/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # SearchProvider protocol
│   │   │   ├── duckduckgo.py
│   │   │   └── google.py
│   │   └── tts/
│   │       ├── __init__.py
│   │       ├── base.py      # TTSProvider protocol
│   │       └── openai.py
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── vector/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # VectorStore protocol
│   │   │   └── chromadb.py
│   │   └── productivity/
│   │       ├── __init__.py
│   │       ├── base.py      # ProductivityStore protocol
│   │       └── sqlite.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── chat.py          # Chat orchestration
│   │   ├── productivity.py  # Task/list logic
│   │   ├── tts.py           # TTS orchestration
│   │   └── web.py           # Web search orchestration
│   │
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── base.py          # @command decorator, registry
│   │   ├── core.py          # /help, /exit, /clear, /config
│   │   ├── history.py       # /history, /delete, /model, /showsys
│   │   ├── context.py       # /showcontext, /continue, /casual
│   │   ├── files.py         # /attach, /cd, /ls, /cat, /pwd
│   │   ├── export.py        # /writemd, /writecode, /writejson, etc.
│   │   ├── vector.py        # /vadd, /vdoc, /vquery, /vstats, /vdelete
│   ├── productivity.py  # /st, /list, /timelog
│   │   ├── tts.py           # /speak, /speaklike
│   │   └── web.py           # /web, /url
│   │
│   ├── display/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── console.py       # Rich console, output formatting
│   │   ├── input.py         # prompt_toolkit setup
│   │   ├── markdown.py      # Markdown rendering
│   │   └── themes.py        # Style definitions
│   │
│   └── resources/
│       ├── defaults.yaml    # Default configuration
│       └── help/            # Help text files
│           ├── overview.md
│           ├── commands.md
│           └── ...
│
└── tests/                   # Test suite
    ├── conftest.py          # Shared fixtures
    ├── unit/
    │   ├── test_config.py
    │   ├── test_commands.py
    │   └── ...
    ├── integration/
    │   ├── test_chat_service.py
    │   ├── test_vector_store.py
    │   └── ...
    └── e2e/
        ├── test_startup.py
        └── test_commands.py
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



The edit seems to have broken the tree formatting. Let me fix that:


**Diff:**
```diff
--- /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md
+++ /home/alex/Documents/repos/Cato/Project/Spec/technical/TECH_ARCHITECTURE.md
@@ -286,7 +286,7 @@
 │   │   ├── files.py         # /attach, /cd, /ls, /cat, /pwd
 │   │   ├── export.py        # /writemd, /writecode, /writejson, etc.
 │   │   ├── vector.py        # /vadd, /vdoc, /vquery, /vstats, /vdelete
-│   ├── productivity.py  # /st, /list, /timelog
+│   │   ├── productivity.py  # /st, /list, /timelog
 │   │   ├── tts.py           # /speak, /speaklike
 │   │   └── web.py           # /web, /url
 │   │

```



Let me do one final grep to ensure all memory-related references have been removed:


**Grep Results:**

- **/home/alex/Documents/repos/Cato/Project/Reports/2026-01-14_spec_review.md**


Only the spec review report mentions it, and that's appropriate since it documents the decision to descope the feature.

Removed all references to the memory creation and retrieval system from the Cato specification documents:

**Files modified:**
- `SPEC_OVERVIEW.md` - Removed memories from purpose, input processing, status indicators
- `SPEC_VECTOR_STORE.md` - Removed memory config options and memory feature references  
- `SPEC_PRODUCTIVITY.md` - Removed memory storage from overview and vector store integration
- `SPEC_COMMAND_SYSTEM.md` - Removed Memory Commands section and `/remember` alias
- `SPEC_CORE_CHAT.md` - Removed "memories always included" from context injection
- `TECH_STORAGE.md` - Removed memories table schema, migration, and repository
- `TECH_ARCHITECTURE.md` - Removed memory from service descriptions and directory tree
- `TECH_CONFIG_SYSTEM.md` - Renamed `cato_memory` to `cato_context`
- `WARP.md` - Updated overview and storage descriptions
- `2026-01-14_spec_review.md` - Marked memory issue as resolved/descoped