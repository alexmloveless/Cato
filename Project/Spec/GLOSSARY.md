# Glossary (Canonical)

## Exchange
A single user message and its assistant response, stored together for retrieval.

## Session
A single application run. Identified by a unique UUID and used for grouping exchanges.

## Thread
A logical conversation chain. Multiple sessions may continue the same thread.

## Context (Retrieved Context)
Relevant past exchanges or documents retrieved from the vector store for a new turn.

## Context Injection
Including retrieved context in the LLM request so it can influence the response.

## Context Mode
Display-only debug setting controlling how retrieved context is shown to the user (`off | on | summary`). It does not affect whether context is injected.

## Vector Store
Persistent storage of embeddings for similarity search across exchanges and documents.

## Vector Document
A stored item in the vector store containing `id`, `content`, `metadata`, and optional `embedding`.

## Embedding
A numeric representation of text used for semantic similarity comparisons.

## Embedding Provider
The component that generates embeddings (e.g., OpenAI or Ollama).

## Retrieval Strategy
The algorithm used to select and rank context results (e.g., default, dynamic).

## Similarity Threshold
Minimum similarity score required for a context result to be considered.

## Chunking
Splitting long documents into smaller parts for embedding and retrieval.

## Provider
An LLM vendor/backend (OpenAI, Anthropic, Google, Ollama).

## Model Identifier
The exact model name required by a provider API (no auto-detection).

## Slash Command
An explicit command triggered by a leading `/`.
