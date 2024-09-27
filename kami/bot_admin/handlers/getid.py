from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

router = Router()


@router.message(Command(commands=["getid"]))
async def handle_start(message: Message) -> None:
    """
    Handler for /getid command.

    :param message: Message from telegram.
    """

    await message.answer(
        text=_(
            "Your telegram id: "
            f"<b>{message.from_user.id}</b>",   # type: ignore[union-attr]
        ),
        parse_mode=ParseMode.HTML,
    )
