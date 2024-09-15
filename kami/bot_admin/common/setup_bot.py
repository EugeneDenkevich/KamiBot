from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from kami.bot_admin.handlers.start import register_start
from kami.bot_admin.middlewaries.custom_middlewaries import CustomMiddleware


async def set_commands(bot: Bot) -> None:
    """
    Set commands for bot.

    :param bot: Bot.
    """

    await bot.set_my_commands([
        BotCommand(command="start", description="Start from this"),
    ])


def setup_dispatcher(dispatcher: Dispatcher) -> None:
    """
    Setup dispatcher.

    :param bot: Dispatcher.
    """

    dispatcher.update.middleware(CustomMiddleware())


def register_handlers() -> None:
    """Register all handlers"""

    register_start()
