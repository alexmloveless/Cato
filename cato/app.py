"""
Application class and main REPL loop.

This module provides the Application class which orchestrates the main
event loop, handling user input, command execution, and chat interactions.
"""

import asyncio
from typing import TYPE_CHECKING

from cato.commands.base import CommandContext
from cato.commands.executor import CommandExecutor
from cato.commands.parser import parse_command_input
from cato.commands.registry import CommandRegistry
from cato.core.config import CatoConfig
from cato.core.exceptions import CatoError, CommandError
from cato.core.logging import get_logger
from cato.display.base import DisplayMessage
from cato.display.console import RichDisplay
from cato.display.input import InputHandler
from cato.services.chat import ChatService
from cato.storage.service import Storage
from cato.storage.vector.base import VectorStore

if TYPE_CHECKING:
    from cato.providers.llm.base import LLMProvider

logger = get_logger(__name__)


class Application:
    """
    Main Cato application class.

    Orchestrates the REPL loop, command execution, and chat interactions.
    All components are injected via constructor (dependency injection pattern).

    Parameters
    ----------
    config : CatoConfig
        Application configuration.
    chat_service : ChatService
        Chat service for LLM interactions.
    storage : Storage
        Storage service for productivity data.
    vector_store : VectorStore | None
        Vector store for conversation memory (optional).
    display : RichDisplay
        Display handler for output.
    input_handler : InputHandler
        Input handler for user input.
    registry : CommandRegistry
        Command registry for slash commands.

    Attributes
    ----------
    config : CatoConfig
        Application configuration.
    chat_service : ChatService
        Chat service instance.
    storage : Storage
        Storage service instance.
    vector_store : VectorStore | None
        Vector store instance (optional).
    display : RichDisplay
        Display handler instance.
    input_handler : InputHandler
        Input handler instance.
    executor : CommandExecutor
        Command executor instance.
    running : bool
        Whether the application is running.
    """

    def __init__(
        self,
        config: CatoConfig,
        chat_service: ChatService,
        storage: Storage,
        vector_store: VectorStore | None,
        display: RichDisplay,
        input_handler: InputHandler,
        registry: CommandRegistry,
        config_path: str | None = None,
    ) -> None:
        """
        Initialize application with injected dependencies.

        Parameters
        ----------
        config : CatoConfig
            Application configuration.
        chat_service : ChatService
            Chat service for LLM interactions.
        storage : Storage
            Storage service for productivity data.
        vector_store : VectorStore | None
            Vector store for conversation memory (optional).
        display : RichDisplay
            Display handler for output.
        input_handler : InputHandler
            Input handler for user input.
        registry : CommandRegistry
            Command registry for slash commands.
        config_path : str | None
            Path to config file that was loaded (optional).
        """
        self.config = config
        self.chat_service = chat_service
        self.storage = storage
        self.vector_store = vector_store
        self.display = display
        self.input_handler = input_handler
        self.registry = registry
        self.config_path = config_path
        self.running = False

        # Create executor with context factory
        self.executor = CommandExecutor(
            registry=registry,
            context_factory=self._create_command_context,
        )

        logger.info("Application initialized")

    async def run(self) -> None:
        """
        Start the main REPL loop.

        This is the primary entry point for the application. It:
        1. Shows welcome message
        2. Enters REPL loop
        3. Processes user input (commands or chat)
        4. Handles errors gracefully
        5. Exits cleanly on /exit or Ctrl+C/Ctrl+D

        The loop continues until the user exits or an unrecoverable error occurs.
        """
        logger.info("Starting application REPL")
        self.running = True

        # Show welcome message
        self._show_welcome()

        try:
            await self._repl_loop()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            self.display.show_info("Interrupted by user")
        except Exception as e:
            logger.exception("Unhandled exception in REPL")
            self.display.show_error(f"Fatal error: {e}")
        finally:
            await self._shutdown()

    async def _repl_loop(self) -> None:
        """
        Main read-eval-print loop.

        Continuously reads user input, processes it (either as a command or
        chat message), and displays the result.
        """
        while self.running:
            try:
                # Get user input
                user_input = await self.input_handler.get_input()
                
                # Handle empty input
                if not user_input or not user_input.strip():
                    continue

                # Check if it's a command or chat message
                if user_input.startswith(self.config.commands.prefix):
                    await self._handle_command(user_input)
                else:
                    await self._handle_chat(user_input)

            except EOFError:
                # Ctrl+D pressed
                logger.info("Received EOF")
                break
            except KeyboardInterrupt:
                # Ctrl+C pressed
                logger.info("Received keyboard interrupt in REPL loop")
                continue
            except Exception as e:
                logger.exception("Error in REPL loop")
                self.display.show_error(f"Error: {e}")

    def _create_command_context(self) -> CommandContext:
        """
        Create command context with current application state.
        
        Returns
        -------
        CommandContext
            Command execution context.
        """
        return CommandContext(
            config=self.config,
            conversation=None,  # TODO: Implement conversation tracking
            llm=self.chat_service.provider if hasattr(self.chat_service, 'provider') else None,
            vector_store=self.vector_store,
            storage=self.storage,
            display=self.display,
            registry=self.registry,
        )
    
    async def _handle_command(self, user_input: str) -> None:
        """
        Handle slash command execution.

        Parameters
        ----------
        user_input : str
            Raw user input starting with command prefix.
        """
        try:
            logger.debug(f"Executing command: {user_input}")

            # Execute command (executor will parse and create context)
            result = await self.executor.execute(user_input)

            # Display result
            if not result.success:
                self.display.show_error(result.message)
            elif result.message:
                self.display.show_info(result.message)

            # Handle special exit command result (check result data)
            if result and result.data and result.data.get("should_exit"):
                self.running = False

        except CommandError as e:
            logger.warning(f"Command error: {e}")
            self.display.show_error(str(e))
        except Exception as e:
            logger.exception("Unexpected error executing command")
            self.display.show_error(f"Command failed: {e}")

    async def _handle_chat(self, user_input: str) -> None:
        """
        Handle chat message with LLM.

        Parameters
        ----------
        user_input : str
            User's chat message.
        """
        try:
            # Show user message
            self.display.show_message(
                DisplayMessage(role="user", content=user_input)
            )

            # Show loading indicator while waiting for response
            with self.display.spinner("Thinking..."):
                # Get response from LLM
                result = await self.chat_service.send_message(user_input)

            # Show assistant response
            self.display.show_message(
                DisplayMessage(role="assistant", content=result.content)
            )

            logger.info(
                f"Chat exchange completed "
                f"(tokens: {result.usage.total_tokens if result.usage else 'unknown'})"
            )

        except CatoError as e:
            logger.warning(f"Chat error: {e}")
            self.display.show_error(f"Chat error: {e}")
        except Exception as e:
            logger.exception("Unexpected error in chat")
            self.display.show_error(f"Unexpected error: {e}")

    def _show_welcome(self) -> None:
        """
        Display welcome message and basic usage info.
        """
        from pathlib import Path

        # Get profile name
        profile_name = self.config.profile_name or "Default"

        # Get provider info
        provider = self.chat_service.provider.name.capitalize()
        model = self.chat_service.provider.model
        temp = self.config.llm.temperature
        max_tokens = self.config.llm.max_tokens

        # Get feature status
        vector_enabled = "✓" if self.vector_store else "✗"
        tts_enabled = "✓" if self.config.tts.enabled else "✗"
        web_enabled = "✓" if self.config.web_search.enabled else "✗"

        # Get absolute paths
        db_path = Path(self.storage._db._path).resolve()
        config_path = Path(self.config_path).resolve() if self.config_path else Path("~/.config/cato/config.yaml").expanduser()

        welcome_text = f"""[bold cyan]╔══════════════════════════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║[/bold cyan]                                                                      [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]     [bold white]██████╗ █████╗ ████████╗ ██████╗[/bold white]                                [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]    [bold white]██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗[/bold white]                               [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]    [bold white]██║     ███████║   ██║   ██║   ██║[/bold white]                               [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]    [bold white]██║     ██╔══██║   ██║   ██║   ██║[/bold white]                               [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]    [bold white]╚██████╗██║  ██║   ██║   ╚██████╔╝[/bold white]                               [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]     [bold white]╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝[/bold white]                                [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                      [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]    [dim]Terminal-first LLM chat with memory & productivity features[/dim]      [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                      [bold cyan]║[/bold cyan]
[bold cyan]╠══════════════════════════════════════════════════════════════════════╣[/bold cyan]
[bold cyan]║[/bold cyan]  [bold yellow]Profile:[/bold yellow] {profile_name:<27} [bold yellow]Provider:[/bold yellow] {provider:<20} [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [bold yellow]Model:[/bold yellow] {model:<29} [bold yellow]Temperature:[/bold yellow] {temp:<16} [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                      [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [bold green]Vector Store:[/bold green] [{vector_enabled}] Enabled          [bold green]TTS:[/bold green] [{tts_enabled}] Enabled                    [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [bold green]Web Search:[/bold green] [{web_enabled}] Enabled                                              [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                      [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [bold magenta]Config:[/bold magenta] {str(config_path):<58} [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [bold magenta]Database:[/bold magenta] {str(db_path):<56} [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                      [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [dim]Type messages to chat • /help for commands • /exit to quit[/dim]         [bold cyan]║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════════════════════════════════╝[/bold cyan]"""

        self.display.show_message(DisplayMessage(
            role="info",
            content=welcome_text
        ))
        logger.info(f"Welcome message displayed (profile={profile_name}, provider={provider})")

    async def _shutdown(self) -> None:
        """
        Clean up resources before exit.

        Closes database connections, saves any pending data, and performs
        graceful shutdown of all components.
        """
        logger.info("Shutting down application")
        self.running = False

        try:
            # Close storage connections
            if self.storage:
                await self.storage.close()
                logger.debug("Storage service closed")

            self.display.show_info("Goodbye!")
            
        except Exception as e:
            logger.exception("Error during shutdown")
            self.display.show_error(f"Shutdown error: {e}")

        logger.info("Application shutdown complete")

    def stop(self) -> None:
        """
        Signal the application to stop.

        Can be called from commands (e.g., /exit) or signal handlers.
        The REPL loop will exit gracefully on the next iteration.
        """
        logger.info("Stop requested")
        self.running = False
