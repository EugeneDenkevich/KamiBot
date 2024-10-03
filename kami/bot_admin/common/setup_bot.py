from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.utils.i18n import ConstI18nMiddleware, I18n

from kami.bot_admin.handlers import setup_routers
from kami.bot_admin.middlewaries.custom_middlewaries import CustomMiddleware
from kami.common import get_work_dir


async def set_commands(bot: Bot) -> None:
    """
    Set commands for bot.

    :param bot: Bot.
    """

    await bot.set_my_commands([
        BotCommand(command="start", description="Start from this"),
        BotCommand(command="getid", description="Get telegram id"),
    ])


def setup_dispatcher(dispatcher: Dispatcher) -> None:
    """
    Setup dispatcher.

    :param bot: Dispatcher.
    """

    dispatcher.update.middleware(CustomMiddleware())


def setup_i18n(
    dispatcher: Dispatcher,
    work_dir: Path,
    language: str,
) -> None:
    """
    Setup language.

    :param bot: Dispatcher.
    """

    i18n = I18n(path=work_dir / "locales", domain="kami")
    i18n_middlewarie = ConstI18nMiddleware(i18n=i18n, locale=language)

    dispatcher.update.middleware(i18n_middlewarie)


async def setup_bot(bot: Bot, language: str, dispatcher: Dispatcher) -> None:
    """
    Setup Bot.

    :param bot: Bot.
    :param language: Language for the bot.
    :param dispatcher: Dispatcher.
    """

    await set_commands(bot)
    setup_routers(dispatcher)
    setup_dispatcher(dispatcher)
    setup_i18n(
        dispatcher=dispatcher,
        work_dir=get_work_dir(),
        language=language,
    )
