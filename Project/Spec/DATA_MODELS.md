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

## Task

- `id` (string)
- `title` (string)
- `description` (string | null)
- `status` (`active | in_progress | completed | deleted`)
- `priority` (`low | medium | high | urgent`)
- `category` (string | null)
- `due_date` (ISO 8601 | null)
- `created_at` (ISO 8601)
- `updated_at` (ISO 8601)
- `completed_at` (ISO 8601 | null)
- `metadata` (dict)

## List

- `id` (string)
- `name` (string)
- `description` (string | null)
- `created_at` (ISO 8601)
- `updated_at` (ISO 8601)
- `metadata` (dict)

## List Item

- `id` (string)
- `list_id` (string)
- `content` (string)
- `checked` (bool)
- `position` (int)
- `created_at` (ISO 8601)
- `updated_at` (ISO 8601)
- `metadata` (dict)
