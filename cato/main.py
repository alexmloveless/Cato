"""CLI entry point for the cato command."""

import argparse
import asyncio
import sys
from pathlib import Path

from cato.bootstrap import create_application
from cato.core.exceptions import CatoError
from cato.core.logging import setup_logging, get_logger


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="cato",
        description="Cato - Terminal-first LLM chat client with memory and productivity features",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-c", "--config",
        type=Path,
        metavar="PATH",
        help="Path to configuration file (default: ~/.config/cato/config.yaml)",
    )

    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="cato 0.1.0",
    )

    return parser.parse_args()


def main() -> None:
    """
    Main entry point for Cato CLI.

    Parses arguments, creates application, and starts REPL.
    """
    args = parse_args()

    # Setup basic logging first (will be reconfigured from config later)
    setup_logging()
    logger = get_logger(__name__)

    try:
        # Create application with dependency injection
        logger.info("Starting Cato")
        app = create_application(config_path=args.config)

        # Override debug mode if specified on CLI
        if args.debug:
            app.config.debug = True
            setup_logging()  # Reconfigure with debug

        # Run the application
        asyncio.run(app.run())

    except CatoError as e:
        logger.error(f"Cato error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        logger.exception("Unexpected error")
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
