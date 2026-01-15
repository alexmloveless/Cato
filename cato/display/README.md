# Display Module

This module handles terminal output and input using Rich and prompt_toolkit.

## Components

### `base.py`
Display protocol and base types.

**Key classes:**
- `Display`: Protocol defining display interface
- `DisplayMessage`: Message data for display (role, content, timestamp)

### `console.py`
Rich-based terminal output implementation.

**Key classes:**
- `RichDisplay`: Main display implementation using Rich console
- `SpinnerContext`: Context manager for loading spinners
- Theme support (default, gruvbox-dark, custom)
- Markdown rendering for assistant responses
- Syntax highlighting for code blocks
- Table display for structured data

### `input.py`
prompt_toolkit-based input handling.

**Key classes:**
- `InputHandler`: User input with history, auto-suggest, key bindings
- Single-line and multiline input support
- Ctrl+C and Ctrl+D handling
- Style customization

### `themes.py`
Theme definitions and loading.

**Built-in themes:**
- `default`: Standard terminal colors
- `gruvbox-dark`: Gruvbox dark color scheme

## Usage

```python
from cato.display import RichDisplay, InputHandler
from cato.core.config import load_config

config = load_config()
display = RichDisplay(config.display)
input_handler = InputHandler(config.display, config.commands.history_file)

# Display messages
display.show_message(DisplayMessage("user", "Hello!", datetime.now()))
display.show_markdown("**Bold** and *italic*")

# Get input
user_input = await input_handler.get_input()
```

## Design Principles

- **Protocol-based**: Display abstracted through protocol
- **Rich text**: Full markdown and syntax highlighting support
- **Themeable**: Multiple themes with override support
- **User-friendly**: History, auto-suggest, graceful interrupt handling
