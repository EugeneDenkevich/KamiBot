from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from kami.backend.presentation.dependencies import get_backend_client


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

        data["backend_client"] = await get_backend_client()
        return await handler(event, data)
