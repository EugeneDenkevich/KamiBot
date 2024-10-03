import uvicorn

from kami.bot_admin.web.app import (
    get_app,
    get_bot,
    get_dispatcher,
    lifespan,
)
from kami.bot_admin.web.router import setup_fastapi_routers
from kami.logging_settings import setup_logging
from kami.settings import get_settings


def main() -> None:
    """Entrypoint of the application"""

    setup_logging()
    settings = get_settings()

    bot = get_bot(token=settings.bot_admin_token)
    dp = get_dispatcher()
    app = get_app(
        lifespan=lifespan, # type: ignore[arg-type]
        bot=bot,
        dp=dp,
        url=settings.server_domain,
        language=settings.admin_language,
        token=settings.bot_admin_token,
    )

    setup_fastapi_routers(app=app)

    uvicorn.run(app, host=settings.server_host, port=settings.server_port_admin)


if __name__ == "__main__":
    main()
