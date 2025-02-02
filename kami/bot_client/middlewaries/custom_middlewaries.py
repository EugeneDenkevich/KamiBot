from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from kami.backend.presentation.dependencies import get_backend_client
from kami.common import get_bot_admin
from kami.settings import get_settings


class CustomMiddleware(BaseMiddleware):
    """Custom middlewaries class"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Create custom middleware.

        :param handler: Handler which hadle event.
        :param event: Event with Telegram data.
        :param data: Additional data.
        :return: Result of the event handling.
        """

        settings = get_settings()

        data["settings"] = settings
        data["bot_admin"] = get_bot_admin(bot_admin_token=settings.bot_admin_token)
        data["backend_client"] = await get_backend_client()

        return await handler(event, data)
