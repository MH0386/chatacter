"""A module that handles the configuration of logging for the application."""

from logging import WARNING, Formatter, Logger, getLogger
from typing import TYPE_CHECKING

from rich.console import Console
from rich.logging import RichHandler

if TYPE_CHECKING:
    from chatacter.settings import LoggerSettings

getLogger("httpx").setLevel(WARNING)


def get_logger() -> Logger:
    """Return the application logger.

    Returns:
        The ``chatacter`` logger, configured after ``setup_logger`` runs.

    """
    return getLogger("chatacter")


def setup_logger(log: LoggerSettings) -> Logger:
    """Initialize the logger for the application."""
    logger: Logger = getLogger(log.name)
    console: Console = Console()
    handler: RichHandler = RichHandler(level=log.level.value, console=console, rich_tracebacks=True)
    formatter: Formatter = Formatter(log.format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log.level.value)
    logger.propagate = log.propagate
    return logger
