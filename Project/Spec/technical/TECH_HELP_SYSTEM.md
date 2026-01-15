# Help System Technical Specification

## Overview
This document defines how help documentation is stored, indexed, and rendered in-app. It ensures a consistent approach to finding and presenting help content and enforces complete documentation coverage for commands.

## Source of Truth
Help content lives in the repository and is packaged with the app. The help system must not depend on external services or runtime discovery of documentation.

## File Layout
All help content lives under:
```
cato/resources/help/
```

### Required Files
```
cato/resources/help/
├── index.yaml              # Navigation + command index (single source of truth)
├── topics/
│   ├── overview.md         # /help
│   ├── commands.md         # /help commands
│   └── <category>.md       # /help <category>
└── commands/
    └── <command>.md        # /help <command>
```

## Index Schema (index.yaml)
`index.yaml` drives all navigation and lookup. It must contain:
- **topics**: named topic pages
- **categories**: command groups
- **commands**: authoritative list of commands, their aliases, and file paths

Example structure:
```
topics:
  - id: overview
    title: Help Overview
    path: topics/overview.md
  - id: commands
    title: All Commands
    path: topics/commands.md

categories:
  - id: core
    title: Core Commands
    commands: [help, exit, clear, config]
  - id: productivity
    title: Productivity Commands
    commands: [st, list]

commands:
  - id: help
    title: /help
    aliases: [h, "?"]
    summary: "Show help information."
    usage: "/help [topic]"
    category: core
    path: commands/help.md
```

## Lookup and Rendering

### Resolution Rules
- `/help` renders `topics/overview.md`.
- `/help commands` renders `topics/commands.md`.
- `/help <category>` renders the category page for `<category>`.
- `/help <command>` renders the command page by command ID or alias.
- Unknown identifiers return a suggestion list derived from `index.yaml`.

### Display
- Help pages are rendered as Markdown through the display layer.
- The command list in `/help commands` is generated from `index.yaml`, not from free-form text.
- Category listings are generated from `index.yaml` to guarantee completeness.

## /help model Integration
When `/help model "<question>"` is invoked:
1. Load **all** help markdown files and `index.yaml`.
2. Provide them to the model as context.
3. Instruct the model to answer strictly from help docs.
4. Do **not** write to conversation history or context stores.

## Consistency and Validation

### Required Consistency Checks
The following must be validated (unit test or CI check):
- Every command registered in the command registry has a matching `commands` entry in `index.yaml`.
- Every command entry in `index.yaml` has a corresponding markdown file.
- Every alias listed in `index.yaml` resolves to a command page.

### Update Workflow (Definition of Done)
When adding or changing a command:
1. Add or update `commands/<command>.md`.
2. Add or update the command entry in `index.yaml`.
3. Ensure the command is listed under exactly one category.
4. Update category or topic pages if new categories are introduced.
