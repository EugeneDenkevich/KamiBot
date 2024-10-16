import datetime
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class AntiFloodMiddleware(BaseMiddleware):
    """Middleware for antiflood."""

    user_last_press_time: Dict[int, datetime.datetime] = {}  # type: ignore[union-attr]

    def __init__(self, cooldown: float = 2.0):
        super().__init__()
        self.cooldown = cooldown

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Create antiflood middleware.

        :param handler: Handler which handle event.
        :param event: Event with Telegram data.
        :param data: Additional data.
        :return: Result of the event handling or None.
        """
        if event.message:
            message = event.message
            tg_id = message.from_user.id

            current_time = datetime.datetime.now()

            last_press_time = self.user_last_press_time.get(
                tg_id,
                datetime.datetime.min,
            )
            time_since_last_press = current_time - last_press_time
            seconds_since_last_press = time_since_last_press.total_seconds()

            if seconds_since_last_press < self.cooldown:
                self.user_last_press_time[tg_id] = current_time

                return None

            self.user_last_press_time[tg_id] = current_time

            return await handler(event, data)

        return None
