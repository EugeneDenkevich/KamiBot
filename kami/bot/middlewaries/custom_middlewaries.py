from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from kami.backend.client import BackendClient


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

        data["backend_client"] = BackendClient()
        return await handler(event, data)
