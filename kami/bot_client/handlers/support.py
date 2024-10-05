from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from kami.bot_client.enums.stickers import StickersEnum

router = Router()


@router.message(Command(commands=["support"]))
async def handle_support(message: Message) -> None:
    """
    Handler for /support command.

    :param message: Message from telegram.
    """

    await message.answer_sticker(StickersEnum.KAMILA_SUPPORT)
    await message.answer(
        text=_("If you have found errors in the work of AI Kami "
               "or do not understand how the functionality works, write here: \n"
               "@NikMer")
    )
