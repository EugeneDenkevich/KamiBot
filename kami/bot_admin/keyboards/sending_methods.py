from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from kami.bot_admin.enums.sending_method import SendingMetdhodEnum


class SendingMethodCD(CallbackData, prefix="sending"):  # type: ignore[call-arg]
    """Callback data for selected senging method button"""

    sending_method: str
    """Sending method"""


def build_sending_methods_markup() -> InlineKeyboardMarkup:
    """Builder for start message keyboard"""

    builder = InlineKeyboardBuilder()

    for sending_method in SendingMetdhodEnum.get_values():
        builder.button(
            text=sending_method,
            callback_data=SendingMethodCD(sending_method=sending_method).pack(),
        )

    return builder.as_markup()
