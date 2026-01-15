# Cato

## Intent
Cato is a terminal-first chat client with productivity features. It is designed for maximum control over LLM interactions, tailored to a single, highly configurable user, while maintaining a clean and dependable interface.

## Core Principles
- **Chat client first, productivity second** — commands are explicit; no natural-language command layer.
- **Modular and flexible architecture** — components can be swapped or removed without rewrites.
- **Spec-driven development** — the functional and technical specs are the source of truth.
- **Configuration-driven** — YAML defaults with overlays; avoid hard-coded values.
- **Robust, navigable help** — documentation must be comprehensive and kept up to date.

## Scope
Cato is built as a single-user, single-machine application with strong focus on clear UX, fast startup, and reliable context retrieval through a vector store.
