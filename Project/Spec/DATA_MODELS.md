# Data Models (Canonical)

This document defines canonical data models. Functional and technical specs should align to these fields.

## Conversation Exchange

Stored in the vector store as a single document per exchange.

- `id` (UUID)
- `session_id` (UUID)
- `thread_id` (UUID | null)
- `user_message` (string)
- `assistant_message` (string)
- `timestamp` (ISO 8601)
- `prior_exchange_ids` (list[UUID])
- `thread_session_id` (string)
- `thread_continuation_seq` (int)
- `metadata` (dict)

## Vector Document

- `id` (string)
- `content` (string)
- `metadata` (dict)
- `embedding` (list[float] | null)

## Search Result

- `document` (VectorDocument)
- `score` (float)

## List

Metadata for a named list.

- `name` (string, unique) - List name (e.g., "todo", "shopping")
- `description` (string | null) - Optional description
- `created_at` (ISO 8601)
- `updated_at` (ISO 8601)
- `metadata` (dict) - Extensible metadata

## List Item

Unified item model for all list types (todo, shopping, etc.).

- `id` (integer, auto-increment) - Globally unique ID across all lists
- `list_name` (string) - Name of parent list
- `description` (string) - Item content
- `status` (`pending | active | in_progress | done`)
- `priority` (`urgent | high | medium | low`)
- `category` (string | null) - Optional grouping category
- `tags` (string[]) - Array of tags for flexible categorization
- `created_at` (ISO 8601)
- `updated_at` (ISO 8601)
- `metadata` (dict) - Extensible metadata (for future additions like due_date)
