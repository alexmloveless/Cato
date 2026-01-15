# Vector Store Specification

## Overview

The vector store provides persistent conversation context using vector embeddings for semantic similarity search. It enables context retrieval from previous conversations and document storage for future reference.

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
- Provider: OpenAI or Ollama (configurable)
- Model and dimensions are configurable
- Provider API key required when applicable

See CONFIG_REFERENCE.md for canonical keys.

## Exchange Storage

### Exchange Data Model

Each conversation exchange stores:

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| thread_id | UUID | Conversation thread grouping |
| session_id | UUID | Application session identifier |
| user_message | string | User's input message |
| assistant_message | string | Assistant's response |
| timestamp | string | ISO 8601 timestamp |
| prior_exchange_ids | list | Context exchanges used |
| thread_session_id | string | Composite ID (thread_id_session_id) |
| thread_continuation_seq | int | Continuation sequence (0 for original) |

### Storage Flow

1. User sends message, assistant responds
2. Combined text created: `"User: {user_message}\nAssistant: {assistant_message}"`
3. Text embedded using the configured embedding provider
4. Exchange stored in ChromaDB with metadata

### Automatic Storage
All conversation exchanges are automatically stored (except in dummy mode) for:
- Future context retrieval
- Thread continuation
- Conversation history
- Productivity exchanges and outputs are **not** stored

## Similarity Search

### Query Process
1. Query text embedded using the configured embedding provider
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
- Can be disabled to use static `similarity_threshold`

### Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| similarity_threshold | 0.65 | Minimum similarity score (static, used when dynamic disabled) |
| dynamic_threshold | true | Enable dynamic threshold adjustment |
| retrieval_strategy | default | Which retrieval strategy to use |
| context_results | 5 | Maximum context exchanges returned |
| search_context_window | 3 | Recent exchanges used to build the search query |

### Context Retrieval

During response generation:

1. **Build query** from recent exchanges (excluding commands)
2. **Select strategy** based on configuration
3. **Search regular context** using configured retrieval strategy
4. **Filter and rank** by similarity score
5. **Inject into prompt** when enabled and above similarity threshold
6. **Display context** based on `context_mode` (display-only)

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
| chunking_strategy | semantic | Chunking strategy |
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
│ Store Path       │ ~/.local/share/cato/vectordb              │
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
  backend: chromadb
  path: ~/.local/share/cato/vectordb
  collection_name: cato_memory
  context_results: 5
  search_context_window: 3
  similarity_threshold: 0.65
  dynamic_threshold: true
  retrieval_strategy: default
  embedding_provider: openai
  embedding_model: text-embedding-3-small
  embedding_dimensions: 1536
  chunking_strategy: semantic
  chunk_size: 1000
  chunk_overlap: 100
  max_chunk_size: 1500
  preserve_sentence_boundaries: true
```

## Error Handling

### Graceful Degradation
If vector store fails to initialize:
- Log warning
- Continue without context retrieval
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
- No `/v*` commands available
- `/continue` unavailable
