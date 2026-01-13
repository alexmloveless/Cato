# Ocat Functional Specification

## Overview

**Ocat** (Otherworldly Chats at the Terminal) is an interactive command-line LLM chat application with integrated productivity features, file management capabilities, and conversational memory through vector storage.

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
- **YAML Format**: Comprehensive configuration in `ocat.yaml`
- **Environment Variables**: Support for API keys and overrides
- **Profile System**: Multiple configuration profiles
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

