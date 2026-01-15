"""Logging setup for Cato application."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cato.core.config import LoggingConfig


def setup_logging(config: "LoggingConfig") -> None:
    """
    Configure application-wide logging.
    
    Sets up console handler (always) and optional file handler with rotation.
    
    Parameters
    ----------
    config : LoggingConfig
        Logging configuration containing level, file path, and formatting options.
    
    Notes
    -----
    - Console handler uses the configured level
    - File handler (if enabled) always uses DEBUG level
    - File logs are rotated when they reach max size
    """
    root_logger = logging.getLogger("cato")
    root_logger.setLevel(config.level)
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Console handler (always present)
    console = logging.StreamHandler()
    console.setLevel(config.level)
    console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    root_logger.addHandler(console)
    
    # File handler (if configured)
    if config.file_path:
        file_path = Path(config.file_path).expanduser()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=config.max_file_size_mb * 1024 * 1024,
            backupCount=config.backup_count,
        )
        # File gets all DEBUG and above regardless of console level
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(config.format))
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given module.
    
    Parameters
    ----------
    name : str
        Logger name, typically __name__ of the calling module.
    
    Returns
    -------
    logging.Logger
        Logger instance under the 'cato' hierarchy.
    """
    return logging.getLogger(f"cato.{name}" if not name.startswith("cato") else name)
