# Project Reports Summary
**Date:** 2026-01-15

## Reports found
- `2026-01-14_spec_review_claude_opus_4_5.md`
- `2026-01-15_084913-Review_Repo_Specs_with_Critique_Report_GPT-5_2-high.md`
- `agents.md` (directory note)

Note: `2026-01-14_spec_review.md` appears in directory listing results but could not be read (missing at time of summarisation).

---

## 2026-01-14_spec_review_claude_opus_4_5.md (Warp Agent)
### Core message
The specs are broadly strong but contain multiple inconsistencies and under-specified areas that should be resolved before implementation.

### Main criticisms
- Duplicate/overlapping overview docs were claimed (risk: divergence + maintenance burden).
> Alex: remedied
- Configuration key naming is inconsistent across specs (risk: implementation ambiguity and broken docs).
> Alex: Please extract a list of examples for review
- Timelog feature is referenced (commands + storage) but not specified functionally.
> Alex: Remove all references to timelogging
- Provider selection is contradictory: auto-detection by model prefix vs explicit `provider` config.
> Alex: Use the providor paradigm. Model name should exactly match the value required by the api for that model. I.e. this function should be explicit and transparent.
- “Context mode” semantics are unclear (display vs injection; off/on/summary).
> Alex: provide examples of where this is unclear
- Vector store hard-codes OpenAI embeddings, undermining “swappable components”.
> Alex: good point. go with the suggestion below
- Productivity agent and `@` file-routing are referenced but not defined.
> Alex: @ based routings are deprecated and should be removed everywhere

### Concrete proposals
- Establish a canonical config reference (likely anchored on `defaults.yaml`).
> Alex: agreed
- Decide on explicit provider config as canonical, with optional auto-detect fallback.
- Clarify context mode (suggested rename to `context_display_mode`).
- Define or descope timelog.
- Add an EmbeddingProvider abstraction (OpenAI + Ollama embeddings).
- Add glossary/versioning/state diagrams for long-lived spec hygiene.

---

## 2026-01-15_084913-Review_Repo_Specs_with_Critique_Report_GPT-5_2-high.md (Warp Agent)
### Core message
The specs are not yet implementation-grade because they disagree on “core truths” (config locations, provider selection, vector-store API, data models, and defaults). The highest leverage fix is spec consolidation around a single canonical glossary/config/data-model set.

### Main criticisms (framed as implementation blockers)
- Config file location scheme is inconsistent across docs (XDG-style vs `~/.cato` examples vs local-file fallbacks).
- Provider selection contract is inconsistent (model-prefix inference vs explicit `llm.provider`).
- “No hard-coded defaults in code” is too absolute and contradicts the technical approach shown (Pydantic defaults, fallbacks, mutations).
- Vector store interfaces disagree (sync vs async; method names; data model).
- Unknown-config-key handling differs (`extra="forbid"` vs `ignore`).

### Additional “high churn” gaps
- `%` productivity routing conflicts with “no natural language command interface”.
- `@` file routing exists in overview but not in file ops spec.
- Productivity functional model diverges from SQLite schema in `TECH_STORAGE.md`.

### Fragility warnings
- Web search spec implies scraping Google/Bing HTML (brittle).
- `/file write` via shell tokenization is unsuitable for real content.

### Concrete proposals
- Create a canonical “truth set”:
  - `Project/Spec/CONFIG_REFERENCE.md`
  - `Project/Spec/GLOSSARY.md`
  - `Project/Spec/DATA_MODELS.md`
> Alex: Agreed
- Pick an MVP scope and delete/mark out-of-scope features (notably `%` and `@`).
> Alex: agreed
- Normalize on an XDG config/data layout and update all examples.
> Alex: agreed
- Make provider explicit with optional `auto`.
> Alex: agreed
- Unify vector store protocol + metadata schema.
> Alex: agreed

---

## Cross-report synthesis (what both reports agree on)
### Highest-confidence problems
1. **Specs disagree on core behavior** (config keys/paths, provider selection, context semantics, vector store API).
2. **Productivity and file “agent routing” are not coherently specified** (`%` and `@` are referenced but not pinned down).
> Alex: agreed. Remove these paradigms
3. **Vector store + embeddings are not consistently abstracted** and the interface differs across documents.
> Alex: agreed
4. **Defaults and naming drift** is already happening; without a single canonical reference it will worsen.
> Alex: agreed

### Highest-leverage corrective action
Create a small set of canonical reference docs (config key reference, glossary, data models) and modify all other specs to *reference* them rather than re-stating details.

---

## Suggested next steps (minimal, ordered)
1. Decide and document the canonical config location scheme (recommend XDG) and update examples across specs.
2. Decide provider selection semantics (recommend explicit `llm.provider` + optional `auto`).
3. Choose a single vector store protocol (recommend async `add/search/get/delete/count`) and align all docs.
4. Decide whether `%` and `@` exist in v1; if not, remove them from `SPEC_OVERVIEW.md` and related references.
5. Reconcile productivity functional fields with `TECH_STORAGE.md` schema (or descope pieces like timelog).
