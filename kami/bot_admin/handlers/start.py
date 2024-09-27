from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=["start"]))
async def handle_start(
    message: Message,
) -> None:
    """
    Handler for /start command.

    :param message: Message from telegram.
    """

    await message.answer(text="This is the Kami admin bot.")
