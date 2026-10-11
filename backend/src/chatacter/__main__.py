from typing import TYPE_CHECKING

from livekit.agents import AgentServer, cli

from chatacter.core import setup_logger
from chatacter.service import setup_service
from chatacter.settings import Settings

if TYPE_CHECKING:
    from logging import Logger

settings: Settings = Settings()
logger: Logger = setup_logger(settings.log)
server: AgentServer = setup_service(settings)


def main() -> None:
    """Launch the LiveKit agent worker.

    Pass a LiveKit CLI mode as the first argument, for example `chatacter dev`, `chatacter start`, or `chatacter console`.
    """
    logger.info("Starting %s", settings.log.name)
    cli.run_app(server)


if __name__ == "__main__":
    main()
