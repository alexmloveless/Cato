
# Cato Specification Critical Review (Functional + Technical)
**Date:** 2026-01-15  
**Reviewer:** Warp Agent (gpt-5.2 high reasoning)  
**Scope reviewed:**  
- `Project/Spec/GENERAL_PRINCIPLES.md`  
- `Project/Spec/functional/*.md`  
- `Project/Spec/technical/*.md`

## Executive summary (blunt)
The specs are ambitious and *feel* cohesive at a philosophy level, but they are not yet implementation-grade because the documents disagree on core truths (config locations, provider selection, vector-store interfaces, data models, defaults). If you implement “to spec” today, you’ll be forced to either (a) pick a canon ad hoc (breaking “spec is the bible”), or (b) build an over-abstracted system that still won’t satisfy the conflicting requirements.

The highest-value fix is not “more detail”; it’s **spec consolidation + a single canonical glossary/config/data-model reference** that every other document links to instead of re-stating.

Also: there is already a prior report in `Project/Reports/2026-01-14_spec_review_claude_opus_4_5.md`. Some earlier issues appear partially resolved (e.g., I don’t see the duplicate overview doc it mentions), but the deeper inconsistencies remain and are more severe than stylistic issues.

---

## Must-fix contradictions (implementation blockers)

### 1) Config file locations and naming are inconsistent (will break UX + docs + tests)
**Evidence**
- `SPEC_CONFIGURATION.md` lists `~/.cato/config.yaml` and `./cato.yaml` style fallbacks (lines ~29–34).
- `TECH_CONFIG_SYSTEM.md` uses XDG-style `~/.config/cato/` and package defaults under `$PACKAGE/defaults/` (lines ~17–29).
- `SPEC_OVERVIEW.md` welcome example shows `~/.cato/margaret.yaml` (line ~82).

**Criticism**
This is not a “minor doc mismatch”; it defines the *primary user workflow*. If you ship with one path but docs show another, you’ll create instant confusion and degrade trust in every other spec.

**Proposal**
Pick one canonical scheme and delete the others:
- **Recommended (Linux-friendly, portable):**  
  - Config: `~/.config/cato/config.yaml` and optional `~/.config/cato/profiles/<name>.yaml`  
  - Data: `~/.local/share/cato/`  
  - Cache: `~/.cache/cato/`  
- Update `SPEC_CONFIGURATION.md` + `SPEC_OVERVIEW.md` examples to match `TECH_CONFIG_SYSTEM.md`.
- Explicitly state whether `./cato.yaml` is supported (personally: I’d drop it for MVP to reduce surprise/collision).

---

### 2) Provider selection: “auto-detect from model name” vs “explicit provider” (core architecture conflict)
**Evidence**
- `SPEC_CORE_CHAT.md` says provider is determined from model prefix (gpt-* → OpenAI, etc.) (lines ~20–24).
- `TECH_CONFIG_SYSTEM.md` and `TECH_LLM_INTEGRATION.md` assume an explicit `llm.provider` (e.g., `Literal["openai","anthropic","google","ollama"]`) and a provider factory (TECH_LLM_INTEGRATION around “Provider Factory”).

**Criticism**
This is a fundamental contract: do users configure *provider* or just *model*? Your config schema, validation, CLI overrides, help text, error messages, and tests all depend on this decision.

**Proposal**
- Make `llm.provider` the canonical selection.
- If you want convenience, add **optional** `provider: "auto"` or `provider: null` meaning “infer from model”, but do **not** document inference as the primary path.
- Update `SPEC_CORE_CHAT.md` to: “If provider is `auto`, infer from model name; otherwise explicit provider wins.”

---

### 3) “No hard-coded defaults in code” is contradicted repeatedly by the technical specs
**Evidence**
- `GENERAL_PRINCIPLES.md`: “No hard-coded inline values” (line ~34).
- `TECH_CONFIG_SYSTEM.md` shows Pydantic fields with defaults (e.g., `theme: str = "default"` etc.) and code examples that mutate config (`cfg.llm.model = model`) (around lines ~157+ and ~233+).
- `TECH_LLM_INTEGRATION.md` and `TECH_VECTOR_STORE.md` contain multiple baked-in defaults in examples (e.g., `base_url or "http://localhost:11434"`, token estimation fallback, etc.).

**Criticism**
The principle is written absolutistically, but the docs you wrote demonstrate you *can’t* actually follow it literally in Python without either:
- violating Pydantic idioms,
- making config models unusably strict,
- or making the project far more complex than needed.

**Proposal**
Rewrite the principle to something implementable:
- “No **user-visible behavioral defaults** hard-coded in code; put them in `defaults.yaml`.”  
- Allow internal safety constants (timeouts, fallbacks) *only* when they’re not user-facing or when required for safe failure modes.
- In technical docs, stop showing code that sets Pydantic model fields after validation unless you explicitly choose a mutable config strategy. Prefer immutable config + `model_copy(update=...)`.

---

### 4) Vector store interfaces disagree (sync vs async, method names, data model)
**Evidence**
- `TECH_ARCHITECTURE.md` shows a `VectorStore` protocol with `store/query/delete` sync methods (lines ~116–141).
- `TECH_VECTOR_STORE.md` defines an async protocol with `add/search/get/delete/count` (lines ~40+).
- `SPEC_VECTOR_STORE.md` describes `store/query/delete` semantics and exchange fields that don’t appear in technical models (thread_session_id, continuation seq, etc.).

**Criticism**
You can’t implement three different vector-store APIs simultaneously without a pointless adapter layer and confusion across services/commands.

**Proposal**
Pick one canonical protocol and align every doc:
- **Recommended:** async protocol (`add/search/get/delete/count`) because embeddings + chromadb + providers may become remote.
- Update `TECH_ARCHITECTURE.md` to match `TECH_VECTOR_STORE.md` (or vice versa), and update functional specs to reference the canonical method names rather than inventing their own.
- Create a single “Vector store data model” section (Exchange, DocumentChunk, Metadata keys) and have both functional + technical specs reference it.

---

### 5) “Unknown config keys warn but don’t crash” conflicts with `extra="forbid"` / “ignore”
**Evidence**
- `GENERAL_PRINCIPLES.md`: unrecognised config items should warn but not crash (line ~38).
- `TECH_CONFIG_SYSTEM.md` alternates between `extra="forbid"` (line ~97) and later `extra="ignore"` with separate warnings (line ~261+).

**Criticism**
This matters because it determines whether users can safely “tinker” (one of the project’s stated goals) without hard failures.

**Proposal**
- Canon: **ignore unknown keys but warn** (your stated philosophy).
- Enforce via a consistent implementation strategy (pre-walk keys + warn, then Pydantic `extra="ignore"`).
- Remove contradictory examples.

---

## Major functional gaps / under-specification (will produce churn)

### 6) `%` productivity routing contradicts “no natural language command interface”
**Evidence**
- `SPEC_OVERVIEW.md` routes `%` input to “ProductivityAgent” (line ~43–44).
- `GENERAL_PRINCIPLES.md` explicitly says no natural language interface to productivity/commands (line ~49).
- `SPEC_PRODUCTIVITY.md` says productivity is “through natural language interaction” (line ~5) and “dedicated AI agent” (lines ~142+).

**Criticism**
This is not a small mismatch; it’s a product decision. If you keep `%` natural language, you *are* building an agent-like subsystem, with all the testing, determinism, cost, and failure-mode implications.

**Proposal (choose one)**
- **Option A (recommended MVP):** Remove `%` routing entirely; productivity is **only** via explicit slash commands with deterministic parsing. Keep pydantic-ai out of v1.
- **Option B:** Keep `%` but explicitly scope it: “only runs when user opts in with `%`”, and document it as an exception to the “no natural language commands” rule.

---

### 7) `@` file routing is referenced but not specified anywhere else
**Evidence**
- `SPEC_OVERVIEW.md` routes `@` input to “file tools agent” (line ~44).
- `SPEC_FILE_OPERATIONS.md` does not define `@` or any file agent behavior.

**Criticism**
Either the file agent exists (and needs a real spec), or it’s vapor and should be removed from the overview to avoid false promises.

**Proposal**
- MVP: delete `@` routing from `SPEC_OVERVIEW.md` unless you write a real spec for it (capabilities, safety boundaries, history interaction, etc.).
- If you keep it, define: what can it do that `/file ...` cannot? Why is it an “agent” at all?

---

### 8) Productivity data model is inconsistent with storage schema (guaranteed rework)
**Evidence**
- `SPEC_PRODUCTIVITY.md` task fields include `content`, `tags`, `pseudo_id`, statuses including `deleted` (lines ~14–31).
- `TECH_STORAGE.md` schema uses `title/description`, priorities only low/medium/high, status excludes deleted, no tags, no pseudo_id, plus additional tables (sessions/threads) that aren’t functionally specified.

**Criticism**
This will cause churn in the first week of implementation. The task/list/time-log model must be consistent across functional + technical. Right now it isn’t.

**Proposal**
- Decide the canonical domain model first (fields + allowed status values).
- Then derive the SQLite schema from it.
- If you want pseudo IDs, model them explicitly (and document uniqueness/scoping: per-user, per-category, per-list?).
- If you want “deleted”, decide whether it is:
  - a soft-delete state (recommended), or
  - a hard delete.

---

## Risky / brittle areas (spec encourages fragile implementation)

### 9) Web search spec assumes scraping Google/Bing HTML (likely to fail)
**Evidence**
- `SPEC_WEB_SEARCH.md` defines URL patterns like `https://www.google.com/search?q={query}` and parsing HTML (lines ~44–49, ~66+).

**Criticism**
HTML scraping of major search engines is brittle and often blocked/captcha’d. If you implement “as spec”, you’ll spend disproportionate time fighting anti-bot behavior rather than building Cato.

**Proposal (MVP-safe)**
- MVP: support **DuckDuckGo only** and document it as such, or use an API-backed provider only when configured.
- Make `SPEC_WEB_SEARCH.md` explicitly describe reliability constraints and failure modes.
- Add explicit config for rate limiting / concurrency (your prior report already suggested concrete defaults; I agree).

---

### 10) `/file write` + command tokenization is not viable for real content
**Evidence**
- `SPEC_COMMAND_SYSTEM.md` uses shlex-like parsing (lines ~12–23).
- `SPEC_FILE_OPERATIONS.md` documents `/file write <path> <content>` and implies quoted content (lines ~82–96).

**Criticism**
This is fine for tiny strings; it’s unusable for multi-paragraph content or code. You’ll either (a) implement a half-broken quoting system, or (b) users will hate it.

**Proposal**
Add an explicit editor-based workflow (and since your preference is Neovim, specify that in docs as the default example):
- `/edit <path>` opens `$EDITOR` (example: `nvim`) on the file.
- `/writemd <path>` continues to export conversation, but for arbitrary content creation/editing, prefer `/edit`.

---

## Internal consistency issues (death by a thousand cuts)

### 11) Defaults disagree across documents (max_tokens is a prime offender)
**Evidence**
- `SPEC_CORE_CHAT.md` max_tokens default 10000 (line ~32).
- `SPEC_CONFIGURATION.md` max_tokens default 4000 (line ~66).
- `TECH_CONFIG_SYSTEM.md` examples use 4096.

**Criticism**
Defaults *are user-facing behavior*. If they disagree, users cannot trust the docs, and tests won’t know what to assert.

**Proposal**
- Single source of truth: `cato/resources/defaults.yaml` (as already intended).
- Every spec that mentions a default should either:
  - quote the value *and* assert it must match defaults.yaml, or
  - stop listing numeric defaults and instead say “see defaults.yaml”.

---

### 12) “Context mode off” semantics are confused (display vs injection)
**Evidence**
- `SPEC_CORE_CHAT.md` says `off`: “No context shown or injected” (lines ~106–120).
- But the overall product positioning heavily implies “memory/context” is a core value proposition.

**Criticism**
If `off` disables injection, then a major subsystem becomes inert without the user realizing (and “vector store enabled” becomes misleading). If it only hides display, the wording is wrong.

**Proposal**
Rename and separate concerns:
- `context_injection: on|off`
- `context_display: off|summary|full`
…and document which commands affect which.

---

### 13) Error-handling rules are contradicted by examples
**Evidence**
- `GENERAL_PRINCIPLES.md` and `TECH_ERROR_HANDLING.md` say avoid broad exception catching.
- `TECH_VECTOR_STORE.md` bootstrap example uses `except Exception as e: ... return None` (lines ~673–675).

**Criticism**
You *will* end up broad-catching at integration boundaries (startup/bootstrap) if you want graceful degradation. The spec needs to admit that and define where broad catches are allowed, otherwise engineers will “technically violate spec” constantly.

**Proposal**
Define explicit “boundary exception policy”:
- Inside modules: atomic/specific exceptions only.
- At top-level boundaries (bootstrap, REPL loop): broad catch is allowed **only** to translate into a typed `CatoError` + user-visible message + structured log context.

---

## Concrete proposals (minimal set that unlocks implementation)

1) **Create a canonical “truth set” and make everything else reference it**
   - `Project/Spec/CONFIG_REFERENCE.md` (all keys + meanings + types; defaults live in defaults.yaml but names live here)
   - `Project/Spec/GLOSSARY.md` (exchange/thread/session/context/document chunk)
   - `Project/Spec/DATA_MODELS.md` (task/list/time-log + vector-store metadata keys)

2) **Pick an MVP scope and delete/mark out-of-scope features**
   - Either remove `%` and `@` routing from v1, or fully specify them.
   - Either ship `/web` with reliable provider constraints, or make it `/url` only in v1.

3) **Normalize config + storage paths to XDG and update all examples**
   - Remove `~/.cato` references unless you intentionally want a non-XDG scheme.

4) **Unify LLM provider selection semantics**
   - Explicit provider (with optional `auto` fallback), not implicit model-prefix heuristics as the main path.

5) **Unify vector-store API + metadata schema**
   - One protocol, one set of method names, one set of metadata keys.

---

## “If you do nothing else” priority list
- Fix config path/location inconsistency.
- Resolve provider selection contradiction.
- Resolve vector-store protocol contradiction.
- Make productivity model match storage schema (or de-scope productivity agent and define deterministic commands only).
- Decide whether `%` and `@` exist in v1 and update the overview accordingly.

---

*End of report*
