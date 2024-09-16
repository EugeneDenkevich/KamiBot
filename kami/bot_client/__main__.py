import asyncio

from kami.logging_settings import setup_logging
from kami.run import run_bot
from kami.settings import get_settings


def main() -> None:
    """Entrypoint of the application"""

    setup_logging()
    settings = get_settings()

    asyncio.run(
        run_bot(
            bot_token=settings.bot_client_token,
            language=settings.language,
        ),
    )


if __name__ == "__main__":
    main()
