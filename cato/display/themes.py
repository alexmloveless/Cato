"""Theme definitions and loading for display."""

import logging
from pathlib import Path

import yaml
from rich.theme import Theme

logger = logging.getLogger(__name__)


# Built-in themes
BUILTIN_THEMES = {
    "default": Theme({
        "user": "bold cyan",
        "assistant": "bold green",
        "system": "dim",
        "error": "bold red",
        "warning": "bold yellow",
        "info": "bold blue",
        "code": "on grey23",
    }),
    "gruvbox-dark": Theme({
        "user": "bold #83a598",      # Blue
        "assistant": "bold #b8bb26",  # Green
        "system": "#928374",          # Grey
        "error": "bold #fb4934",      # Red
        "warning": "bold #fabd2f",    # Yellow
        "info": "bold #8ec07c",       # Aqua
        "code": "on #3c3836",         # Dark bg
    }),
}


def load_theme(theme_name: str, style_overrides: dict[str, str] | None = None) -> Theme:
    """
    Load theme by name.
    
    Tries built-in themes first, then custom theme files in ~/.config/cato/themes/.
    
    Parameters
    ----------
    theme_name : str
        Theme name to load.
    style_overrides : dict[str, str] | None, optional
        Style overrides to apply on top of theme.
    
    Returns
    -------
    Theme
        Loaded Rich theme.
    """
    # Try built-in theme
    theme = BUILTIN_THEMES.get(theme_name)
    
    if not theme:
        # Try custom theme file
        custom_path = Path(f"~/.config/cato/themes/{theme_name}.yaml").expanduser()
        if custom_path.exists():
            theme = load_custom_theme(custom_path)
            logger.info(f"Loaded custom theme from: {custom_path}")
        else:
            logger.warning(f"Theme '{theme_name}' not found, using default")
            theme = BUILTIN_THEMES["default"]
    
    # Apply style overrides
    if style_overrides:
        theme = apply_style_overrides(theme, style_overrides)
    
    return theme


def load_custom_theme(path: Path) -> Theme:
    """
    Load theme from YAML file.
    
    Expected format:
    ```yaml
    colors:
      user: "#61afef"
      assistant: "#98c379"
      system: "#5c6370"
      error: "#e06c75"
      warning: "#e5c07b"
      info: "#56b6c2"
      code_background: "#282c34"
    ```
    
    Parameters
    ----------
    path : Path
        Path to theme YAML file.
    
    Returns
    -------
    Theme
        Loaded theme.
    """
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        
        colors = data.get("colors", {})
        return Theme({
            "user": f"bold {colors.get('user', 'cyan')}",
            "assistant": f"bold {colors.get('assistant', 'green')}",
            "system": colors.get("system", "dim"),
            "error": f"bold {colors.get('error', 'red')}",
            "warning": f"bold {colors.get('warning', 'yellow')}",
            "info": f"bold {colors.get('info', 'blue')}",
            "code": f"on {colors.get('code_background', 'grey23')}",
        })
    except Exception as e:
        logger.error(f"Failed to load custom theme from {path}: {e}")
        return BUILTIN_THEMES["default"]


def apply_style_overrides(theme: Theme, overrides: dict[str, str]) -> Theme:
    """
    Apply style overrides to a theme.
    
    Parameters
    ----------
    theme : Theme
        Base theme.
    overrides : dict[str, str]
        Style overrides to apply.
    
    Returns
    -------
    Theme
        Theme with overrides applied.
    """
    merged = dict(theme.styles)
    merged.update(overrides)
    return Theme(merged)
