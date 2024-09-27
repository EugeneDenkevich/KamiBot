from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class StartCallbackData(CallbackData, prefix="any"):  # type: ignore[call-arg]
    """Callback data for "Find more" button"""

    bot_name: str


def build_start_keyboard(bot_name: str) -> InlineKeyboardMarkup:
    """
    Builder for start message keyboard.

    :paran bot_name: Name of current bot
    """

    builder = InlineKeyboardBuilder()

    builder.button(
        text="Find more!",
        callback_data=StartCallbackData(bot_name=bot_name).pack(),
    )

    return builder.as_markup()
