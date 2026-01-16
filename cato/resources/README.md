# Resources Directory

Static resources bundled with the Cato package.

## Contents

```
resources/
├── defaults.yaml           # Default configuration values
├── system_prompt.txt       # Default system prompt for LLM
├── help/                  # Help system content
│   ├── index.yaml         # Help navigation structure
│   ├── topics/            # Help topic files
│   │   ├── overview.md
│   │   └── commands.md
│   └── commands/          # Per-command help files
│       ├── help.md
│       ├── exit.md
│       ├── continue.md
│       ├── speak.md
│       └── ...
└── themes/                # Built-in display themes
    ├── default.yaml
    └── gruvbox-dark.yaml
```

## Files

### defaults.yaml

Complete default configuration with inline documentation. This file contains:

- All configurable settings with safe defaults
- Inline comments explaining each option
- Environment variable placeholders (e.g., `${OPENAI_API_KEY}`)
- Value ranges and validation rules

**Important**: This file should NEVER be edited by users. User customizations go in `~/.config/cato/config.yaml`.

**Format**:
```yaml
# Section comment
section:
  # Setting comment
  setting: value
```

### system_prompt.txt

The default system prompt sent to the LLM. This prompt:

- Defines Cato's personality and behavior
- Sets interaction guidelines
- Provides context about capabilities

Users can:
- Override entirely with `llm.base_prompt_file` + `llm.override_base_prompt: true`
- Append additional prompts with `llm.system_prompt_files`

### help/

#### index.yaml

Navigation structure for the help system. Contains:

- **topics**: List of help topics with paths
- **categories**: Groupings of related commands
- **commands**: Command metadata with paths to help files

**Structure**:
```yaml
topics:
  - id: overview
    title: Help Overview
    path: topics/overview.md

categories:
  - id: core
    title: Core Commands
    commands: [help, exit, clear]

commands:
  - id: help
    title: /help
    aliases: [h, ?]
    summary: "Show help information"
    usage: "/help [topic|command]"
    category: core
    path: commands/help.md
```

**Validation**: The `HelpService` ensures:
- All referenced files exist
- All registered commands have help entries
- No orphaned help files

#### topics/

Help topic markdown files. Topics are high-level documentation pages:

- `overview.md` - Introduction to Cato
- `commands.md` - Command reference overview

**Format**: Standard markdown with support for:
- Headers (`#`, `##`, `###`)
- Code blocks (` ``` `)
- Lists
- Links

#### commands/

Per-command help files in markdown format. Each command should have:

1. **Title**: `# /command`
2. **Description**: Brief explanation
3. **Usage**: Code block with syntax
4. **Arguments**: Table of parameters
5. **Examples**: Practical usage examples
6. **See Also**: Related commands

**Template**:
```markdown
# /command

Brief description.

## Usage

\```
/command [arg1] [arg2]
\```

## Description

Detailed explanation of what the command does.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| arg1 | Yes | First argument |
| arg2 | No | Optional argument |

## Examples

\```
/command example
/command with "quoted arg"
\```

## See Also

- [/related](related.md) - Related command
```

### themes/

Display theme YAML files. Each theme defines Rich styles for different UI elements.

**Structure**:
```yaml
name: "Theme Name"
description: "Theme description"

styles:
  user: "bold cyan"
  assistant: "green"
  system: "dim yellow"
  error: "bold red"
  warning: "yellow"
  info: "blue"
  code: "magenta"
```

**Built-in themes**:
- `default.yaml` - Clean, minimal theme
- `gruvbox-dark.yaml` - Retro warm dark theme

**Custom themes**: Users can add themes to `~/.config/cato/themes/`

**Rich style syntax**: `[modifier] [color] [on background]`
- Modifiers: bold, dim, italic, underline, reverse
- Colors: Standard terminal colors + hex codes
- Background: `on <color>`

## Usage in Code

### Loading Defaults

```python
from cato.core.config import get_default_config_path, load_yaml

defaults_path = get_default_config_path()
defaults = load_yaml(defaults_path)
```

### Loading System Prompt

```python
from pathlib import Path

prompt_path = Path(__file__).parent / "resources" / "system_prompt.txt"
system_prompt = prompt_path.read_text()
```

### Loading Help Content

```python
from cato.services.help import HelpService

help_service = HelpService()
content = help_service.get_help_content("continue")
```

### Loading Themes

```python
from cato.display.themes import load_theme

theme = load_theme("gruvbox-dark")
```

## Maintenance

### Adding a New Command Help File

1. Create `commands/<command>.md`
2. Update `index.yaml`:
   - Add to appropriate category
   - Add command entry with metadata
3. Test with `/help <command>`

### Creating a Custom Theme

1. Create `~/.config/cato/themes/mytheme.yaml`
2. Define all required style keys
3. Set in config: `display.theme: mytheme`
4. Test with different message types

### Updating Defaults

When adding new configuration options:

1. Add to `defaults.yaml` with inline docs
2. Add Pydantic model in `core/config.py`
3. Update `CONFIG_REFERENCE.md`
4. Update affected code

## Validation

### Help System Consistency

Run validation tests:

```bash
pytest tests/integration/test_help_validation.py
```

Checks:
- All registered commands have help entries
- All help files referenced in index exist
- No orphaned help files
- Proper index structure

### Configuration Validation

Pydantic automatically validates:
- Required fields
- Type correctness
- Value ranges
- Field dependencies

Test with:
```bash
pytest tests/unit/test_config.py
```

## See Also

- [Configuration Reference](../../CONFIG_REFERENCE.md) - Complete config docs
- [Help System](services/help.py) - Help service implementation
- [Display System](display/) - Theme and display implementation
