from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from kami.settings import get_settings


class AdminMiddleware(BaseMiddleware):
    """Custom chat middlewaries class"""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,  # type: ignore[override]
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

        if int(settings.admin_id) == event.chat.id:
            return await handler(event, data)

        await event.answer("Operation forbidden")

        return None
