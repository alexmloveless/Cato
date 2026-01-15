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
- `SPEC_VECTOR_STORE.md` references `similarity_threshold`
- `TECH_CONFIG_SYSTEM.md` uses different nested structures

The functional spec (SPEC_CONFIGURATION.md line 79) shows `context_similarity_threshold` while the vector store functional spec uses `similarity_threshold`.

**Proposal:** Create a canonical `defaults.yaml` reference document that all other specs must align with. Use consistent naming: `vector_store.context_similarity_threshold` everywhere.

---

### 3. ~~Memory System Specified But Not Defined~~ RESOLVED

**Resolution:** Memory system has been descoped from v1. All references to memories, memory storage, memory retrieval, and related configuration have been removed from the specifications.

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

**Proposal:** Create `GLOSSARY.md` defining terms like "exchange", "thread", "session", "context" which are used throughout but with subtly different meanings.

### 23. Add State Diagram

**Proposal:** Add a state diagram for conversation/session lifecycle to SPEC_CORE_CHAT.md showing how sessions, threads, and exchanges relate.

### 24. Consolidate Configuration Reference

**Proposal:** Create a single `CONFIG_REFERENCE.md` that is the authoritative source for all configuration keys. Other specs should reference this rather than re-documenting options.

---

## Summary of Priority Actions

**Must Fix Before Implementation:**
1. Resolve duplicate overview documents
2. ~~Define or descope memory system~~ ✅ RESOLVED - memory descoped
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
