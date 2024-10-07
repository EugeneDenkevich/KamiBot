from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable

from aiogram import Bot, Dispatcher
from fastapi import FastAPI

from kami.bot_admin.common.setup_bot import setup_bot


def get_bot(token: str) -> Bot:
    """
    Initializes and returns a Bot instance with the given token.

    :param token: API token for the bot.
    """

    return Bot(token=token)


def get_dispatcher() -> Dispatcher:
    """
    Initializes and returns a Dispatcher instance.

    """

    return Dispatcher()


@asynccontextmanager
async def lifespan(
    app: FastAPI,
    bot: Bot,
    dp: Dispatcher,
    url: str,
    language: str,
    token: str,
) -> AsyncGenerator[Any, Any]:
    """
    Manages the lifespan of the FastAPI application.

    :param app: FastAPI application instance.
    :param bot: Bot instance.
    :param dp: Dispatcher instance.
    :param url: Webhook URL for the bot.
    :param language: Language settings for the bot.
    :param token: Bot admin token.
    """

    url_webhook = f"{url}/webhook-admin/{token}"

    await bot.delete_webhook()

    await bot.set_webhook(
        url=url_webhook,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )

    app.state.bot = bot
    app.state.dp = dp

    await setup_bot(
        bot=bot,
        language=language,
        dispatcher=dp,
    )

    yield

    await bot.delete_webhook()


def get_app(
    lifespan: Callable[[FastAPI], AsyncGenerator[Any, Any]],
    bot: Bot,
    dp: Dispatcher,
    url: str,
    language: str,
    token: str,
) -> FastAPI:
    """
    Creates and returns a FastAPI app configured by lifespan.

    :param lifespan: A callable that manages the lifecycle of the FastAPI app.
    :param bot: Bot instance.
    :param dp: Dispatcher instance.
    :param url: Webhook URL for the bot.
    :param language: Language settings for the bot.
    :param token: Bot admin token.
    """

    return FastAPI(
        lifespan=lambda app: lifespan( # type: ignore[call-arg, arg-type]
            app=app,
            bot=bot,
            dp=dp,
            url=url,
            language=language,
            token=token,
        ),
    )
