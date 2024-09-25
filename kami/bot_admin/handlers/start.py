from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from kami.bot_admin.keyboards.start import build_start_keyboard

router = Router()


@router.message(Command(commands=["start"]))
async def handle_start(
    message: Message,
) -> None:
    """
    Handler for /start command.

    :param message: Message from telegram.
    """

    await message.answer(
        text="Hello World!",
        reply_markup=build_start_keyboard(bot_name="KamiBOT"),
    )
