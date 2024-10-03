from typing import Annotated

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import APIRouter, Depends, FastAPI
from fastapi.requests import Request

from kami.settings import get_settings

fastapi_router = APIRouter()
settings = get_settings()


def get_current_bot(request: Request) -> Bot:
    """
    Retrieves the current Bot instance from the FastAPI request.

    :param request: The FastAPI Request object.
    """

    return request.app.state.bot


def get_current_dp(request: Request) -> Dispatcher:
    """
    Retrieves the current Dispatcher instance from the FastAPI request.

    :param request: The FastAPI Request object.
    """

    return request.app.state.dp


BotD = Annotated[Bot, Depends(get_current_bot)]
DispatcherD = Annotated[Dispatcher, Depends(get_current_dp)]


@fastapi_router.post(path=f"/{settings.bot_admin_token}", response_model=None)
async def webhook(
    request: Request,
    bot: BotD,
    dp: DispatcherD,
) -> None:
    """
    Processes incoming webhook updates from Telegram.

    :param request: Webhook payload.
    :param bot: Bot instance.
    :param dp: Dispatcher instance for handling updates.
    """

    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)


def setup_fastapi_routers(app: FastAPI) -> None:
    """
    Add FastAPI routers to the app.

    :param app: FastAPI application instance.
    """

    app.include_router(router=fastapi_router)
