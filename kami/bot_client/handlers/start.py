from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from kami.bot_client.keyboards.start import build_start_keyboard

router = Router()


@router.message(Command(commands=["start"]))
async def handle_start(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Handler for /start command.

    :param message: Message from telegram.
    """

    await state.clear()

    await message.answer(
        text=_("Hello World!"),
        reply_markup=build_start_keyboard(bot_name="KamiBOT"),
    )
    await message.answer(
        text=_("And hello again!"),
        reply_markup=build_start_keyboard(bot_name="KamiBOT"),
    )
    await message.answer(
        text=_("Hello one more time!"),
        reply_markup=build_start_keyboard(bot_name="KamiBOT"),
    )
