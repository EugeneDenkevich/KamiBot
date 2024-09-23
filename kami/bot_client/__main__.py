import asyncio

from kami.bot_client.run import run_bot
from kami.logging_settings import setup_logging
from kami.settings import get_settings


def main() -> None:
    """Entrypoint of the application"""

    setup_logging()
    settings = get_settings()

    asyncio.run(
        run_bot(
            bot_token=settings.bot_client_token,
            language=settings.client_language,
        ),
    )


if __name__ == "__main__":
    main()
