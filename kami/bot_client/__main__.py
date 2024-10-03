import uvicorn

from kami.bot_client.common.run import run_in_pooling
from kami.bot_client.web.app import (
    get_app,
    get_bot,
    get_dispatcher,
    lifespan,
)
from kami.bot_client.web.router import setup_fastapi_routers
from kami.logging_settings import setup_logging
from kami.settings import get_settings


def main() -> None:
    """Entrypoint of the application"""

    setup_logging()
    settings = get_settings()

    bot = get_bot(token=settings.bot_client_token)
    dp = get_dispatcher()

    if settings.debug_mode:
        run_in_pooling(
            bot=bot,
            dp=dp,
            language=settings.client_language,
        )
    else:
        app = get_app(
            lifespan=lifespan, # type: ignore[arg-type]
            bot=bot,
            dp=dp,
            url=settings.server_domain,
            language=settings.client_language,
            token=settings.bot_client_token,
        )

        setup_fastapi_routers(app=app)

        uvicorn.run(app, host=settings.server_host, port=settings.server_port_client)


if __name__ == "__main__":
    main()
