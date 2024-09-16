from aiogram import Bot, Dispatcher

from kami.bot_client.common.setup_bot import (
    set_commands,
    setup_dispatcher,
    setup_i18n,
)
from kami.bot_client.handlers import setup_routers
from kami.common import get_work_dir


async def run_bot(bot_token: str, language: str) -> None:
    """
    Run Bot.

    :param bot_token: Bot token.
    """

    bot = Bot(token=bot_token)
    dispatcher = Dispatcher()

    await set_commands(bot)

    setup_routers(dispatcher)

    setup_dispatcher(dispatcher)

    setup_i18n(
        dispatcher=dispatcher,
        work_dir=get_work_dir(),
        language=language,
    )

    await dispatcher.start_polling(bot)
