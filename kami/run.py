from aiogram import Bot, Dispatcher

from kami.bot_client.common.setup_bot import (
    register_handlers,
    set_commands,
    setup_dispatcher,
)
from kami.bot_client.handlers import setup_routers


async def run_bot(bot_token: str) -> None:
    """
    Run Bot.

    :param bot_token: Bot token.
    """

    bot = Bot(token=bot_token)
    dispatcher = Dispatcher()

    await set_commands(bot)
    setup_routers(dispatcher)
    setup_dispatcher(dispatcher)
    register_handlers()

    await dispatcher.start_polling(bot)
