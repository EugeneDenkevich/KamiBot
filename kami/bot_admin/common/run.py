import asyncio

from aiogram import Bot, Dispatcher

from kami.bot_admin.common.setup_bot import setup_bot


def run_in_pooling(bot: Bot, dp: Dispatcher, language: str) -> None:
    """
    Run bot in pooling mode

    :param bot: Bot.
    :param dp: Dispatcher.
    :param language: Bot language.
    """

    try:
        loop = asyncio.get_event_loop()

        loop.run_until_complete(
            bot.delete_webhook(),
        )

        loop.run_until_complete(
            setup_bot(
                bot=bot,
                language=language,
                dispatcher=dp,
            ),
        )

        loop.run_until_complete(dp.start_polling(bot))
    finally:
        loop.close()
