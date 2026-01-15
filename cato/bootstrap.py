"""
Bootstrap module for component initialization and dependency wiring.

This module provides factory functions to create and wire up all application
components based on configuration, implementing dependency injection throughout.
"""

import asyncio
from pathlib import Path

import cato.commands  # Import to register commands
from cato.commands.registry import CommandRegistry
from cato.core.config import CatoConfig, load_config
from cato.core.exceptions import ConfigurationError
from cato.core.logging import setup_logging, get_logger
from cato.display.console import RichDisplay
from cato.display.input import InputHandler
from cato.providers.llm.factory import create_provider
from cato.services.chat import ChatService
from cato.storage.service import create_storage

logger = get_logger(__name__)


def create_application(config_path: Path | None = None) -> "Application":
    """
    Wire up all application components and return configured instance.

    This is the main factory function that:
    1. Loads and validates configuration
    2. Sets up logging
    3. Creates providers based on config
    4. Creates services with dependencies
    5. Initializes display and input handlers
    6. Sets up command system
    7. Returns fully-wired Application

    Parameters
    ----------
    config_path : Path, optional
        Path to user configuration file. If None, uses default locations.

    Returns
    -------
    Application
        Fully initialized application instance ready to run.

    Raises
    ------
    ConfigurationError
        If configuration is invalid or cannot be loaded.
    """
    # Import here to avoid circular dependency
    from cato.app import Application

    logger.info("Bootstrapping Cato application")

    # Load configuration
    try:
        config = load_config(config_path)
        logger.info(f"Configuration loaded from {config_path or 'defaults'}")
    except Exception as e:
        raise ConfigurationError(
            f"Failed to load configuration: {e}",
            context={"config_path": str(config_path) if config_path else None}
        ) from e

    # Setup logging (already done but respect config overrides)
    setup_logging(config.logging)

    # Create components bottom-up through layers
    app = _create_application_with_config(config)
    
    logger.info("Application bootstrap complete")
    return app


def _create_application_with_config(config: CatoConfig) -> "Application":
    """
    Create application instance from validated config.

    Parameters
    ----------
    config : CatoConfig
        Validated configuration object.

    Returns
    -------
    Application
        Fully wired application instance.
    """
    from cato.app import Application

    # Create LLM provider
    logger.debug(f"Creating LLM provider: {config.llm.provider}")
    llm_provider = create_provider(config)

    # Create storage service
    logger.debug(f"Creating storage service at {config.storage.database_path}")
    storage = asyncio.run(create_storage(config))

    # Create chat service
    logger.debug("Creating chat service")
    chat_service = ChatService(
        provider=llm_provider,
        config=config,
    )

    # Create display components
    logger.debug(f"Creating display with theme: {config.display.theme}")
    display = RichDisplay(config=config.display)
    
    logger.debug("Creating input handler")
    input_handler = InputHandler(config=config.display, history_path=config.commands.history_file)

    # Create command system
    logger.debug("Creating command registry")
    registry = CommandRegistry()

    # Create application (executor will be created by Application)
    app = Application(
        config=config,
        chat_service=chat_service,
        storage=storage,
        display=display,
        input_handler=input_handler,
        registry=registry,
    )

    return app


def create_application_for_testing(
    config: CatoConfig | None = None,
    **overrides,
) -> "Application":
    """
    Create application instance for testing with optional overrides.

    This factory allows tests to provide mock components or custom config
    without needing to manipulate the filesystem or environment.

    Parameters
    ----------
    config : CatoConfig, optional
        Custom configuration. If None, uses defaults.
    **overrides
        Component overrides (e.g., llm_provider=MockProvider()).

    Returns
    -------
    Application
        Application instance for testing.

    Examples
    --------
    >>> app = create_application_for_testing(
    ...     config=test_config,
    ...     llm_provider=MockLLMProvider()
    ... )
    """
    from cato.app import Application

    # Use provided config or load defaults
    if config is None:
        config = load_config(config_path=None)

    # Create app normally if no overrides
    if not overrides:
        return _create_application_with_config(config)

    # Create with overrides (for testing)
    # Components will be created unless overridden
    components = {}
    
    if "llm_provider" not in overrides:
        components["llm_provider"] = create_provider(config)
    
    if "storage" not in overrides:
        components["storage"] = asyncio.run(create_storage(config))
    
    if "chat_service" not in overrides:
        components["chat_service"] = ChatService(
            provider=components.get("llm_provider") or overrides.get("llm_provider"),
            config=config,
        )
    
    if "display" not in overrides:
        components["display"] = RichDisplay(config=config.display)
    
    if "input_handler" not in overrides:
        components["input_handler"] = InputHandler(config=config.display, history_path=config.commands.history_file)
    
    if "registry" not in overrides:
        components["registry"] = CommandRegistry()

    # Merge overrides
    components.update(overrides)

    return Application(
        config=config,
        chat_service=components.get("chat_service"),
        storage=components.get("storage"),
        display=components.get("display"),
        input_handler=components.get("input_handler"),
        registry=components.get("registry"),
    )
