from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _

from kami.backend.presentation.client import BackendClient
from kami.bot_client.keyboards.start import StartCallback, build_start_keyboard

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


@router.callback_query(StartCallback.filter())
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
        text=_("Dialog was created!"),
    )

    await callback.message.answer(  # type: ignore[union-attr]
        text=_("Welcome to {bot_name}").format(bot_name=callback_data.bot_name),
    )
    await callback.message.answer(  # type: ignore[union-attr]
        text=backend_client.get_example(),
    )
    await callback.answer()
