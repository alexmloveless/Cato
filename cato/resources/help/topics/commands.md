# All Commands

This page lists all available commands organized by category.
For detailed help on any command, use `/help <command>`.

## Core Commands

Essential commands for basic operation.

- `/help` - Show help information
- `/exit`, `/quit`, `/q` - Exit the application
- `/clear` - Clear conversation history and screen
- `/config` - Show current configuration

## History & Context

Manage conversation history and context.

- `/history [n]` - Show conversation history
- `/delete [n]` - Delete recent exchanges
- `/model [name]` - Show or change LLM model
- `/showsys` - Display system prompt
- `/loglevel [level]` - Show or change logging level

## Vector Store

Semantic search and conversation memory.

- `/vadd <text>` - Add text to vector store
- `/vdoc <path>` - Add document file to vector store
- `/vquery <query>` - Query vector store for similar content
- `/vstats` - Display vector store statistics
- `/vdelete <id>` - Delete document from vector store
- `/vget <id>` - Retrieve document by ID

## Productivity

Task and list management.

- `/st [options]` - Show tasks with filtering and sorting
- `/list [name]` - Show lists and list items

## Web & Search

Search the web and fetch URL content.

- `/web "query" [engine]` - Search the web and add results to context
- `/url <url>` - Fetch URL content and add to conversation
- `/url_store` - Store previously fetched URL content in vector store

## Text-to-Speech

Convert responses to speech.

- `/speak [voice] [model]` - Speak the last assistant response
- `/speaklike "instructions" [voice] [model]` - Speak with custom instructions

---

Use `/help <command>` for detailed help on any command.
