from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from kami.backend.presentation.client import BackendClient
from kami.bot.keyboards.start import StartCallback, build_start_keyboard

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


@router.message(Command(commands=["start"]))
async def handle_find_more(
    callback: CallbackQuery,
    callback_data: StartCallback,
    backend_client: BackendClient,
) -> None:
    """
    Handler for "Find more" button.

    :param callback: Callback query from button.
    :param callback_data: Callback data object.
    """

    await backend_client.create_dialog(topic="Super Topic")
    await callback.message.answer(  # type: ignore[union-attr]
        text="Dialog was created!",
    )

    await callback.message.answer(  # type: ignore[union-attr]
        text=f"Welcome to {callback_data.bot_name}",
    )
    await callback.message.answer(  # type: ignore[union-attr]
        text=backend_client.get_example(),
    )
    await callback.answer()


def register_start() -> None:
    """Register start handlers"""

    router.callback_query.register(handle_find_more, StartCallback.filter())
