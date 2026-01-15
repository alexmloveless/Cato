# Configuration Reference (Canonical)

This document is the single source of truth for configuration keys, file locations, and context handling semantics. Other specs should reference this document rather than restating config details.

## Canonical Paths (XDG)

```
~/.config/cato/         # Config directory
~/.local/share/cato/    # Data directory
~/.cache/cato/          # Cache directory
```

## Config File Resolution Order

1. `--config <path>` CLI argument  
2. `CATO_CONFIG_FILE` environment variable  
3. `~/.config/cato/config.yaml`

## Core Configuration Keys

### Root
- `profile_name` (string, optional)
- `debug` (bool)

### LLM (`llm`)
- `provider` (required): `openai | anthropic | google | ollama`
- `model` (required): exact provider model identifier (no auto-detection)
- `temperature`
- `max_tokens`
- `timeout_seconds`
- `system_prompt_files`
- `base_prompt_file`
- `override_base_prompt`
- Provider-specific sections: `llm.openai`, `llm.anthropic`, `llm.google`, `llm.ollama`

### Vector Store (`vector_store`)
- `enabled`
- `backend` (currently `chromadb`)
- `path`
- `collection_name`
- `context_results`
- `search_context_window`
- `similarity_threshold`
- `dynamic_threshold`
- `retrieval_strategy`
- `chat_window`
- Embedding:
  - `embedding_provider` (`openai | ollama`)
  - `embedding_model`
  - `embedding_dimensions`
- Chunking:
  - `chunking_strategy`
  - `chunk_size`
  - `chunk_overlap`
  - `max_chunk_size`
  - `preserve_sentence_boundaries`

### Storage (`storage`)
- `database_path`
- `backup_enabled`
- `backup_frequency_hours`

### Display (`display`)
- `theme`
- `markdown_enabled`
- `code_theme`
- `max_width`
- `timestamps`
- `spinner_style`
- `prompt_symbol`
- `line_width`
- `exchange_delimiter`
- `exchange_delimiter_length`

### Logging (`logging`)
- `level` (`DEBUG | INFO | WARNING | ERROR`)
- `file_path`
- `format`
- `max_file_size_mb`
- `backup_count`
### Commands (`commands`)
- `prefix`
- `history_file`

### Paths (`paths`)
- `data_dir`
- `config_dir`
- `cache_dir`

### TTS (`tts`)
- `enabled`
- `voice`
- `model`
- `audio_dir`

### Web Search (`web_search`)
- `enabled`
- `default_engine`
- `content_threshold`
- `max_results`
- `timeout`
- `engines`

### Locations (`locations`)
Alias map of name → path.

## Context Handling Semantics

- Context retrieval occurs on every chat turn when the vector store is enabled.
- Retrieved context **is always injected** into the LLM request if it passes the similarity threshold.
- `context_mode` (toggled via `/showcontext`) is **display-only**:
  - `off`: show nothing
  - `on`: show excerpts
  - `summary`: show count only

## Defaults

All defaults live in `cato/resources/defaults.yaml`. No defaults are hard-coded in Python.
