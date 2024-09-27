from typing import Optional

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

router = Router()


@router.message(Command(commands=["translator"]))
@router.message(F.text == "Translator")
async def handle_dialog_command(
    message: Message,
    state: Optional[FSMContext],
) -> None:
    """
    Handler for /translator

    :param message: Message from telegram.
    """

    await state.clear()  # type: ignore[union-attr]

    await message.answer(
        text=_(
            "Edit your text and I helped translate it!\n",
        ),
    )
