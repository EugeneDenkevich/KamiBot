from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


class DialogAfterTestCD(
    CallbackData,
    prefix="dialog_button",  # type: ignore[call-arg]
):
    pass


def build_dialog_after_test_markup() -> InlineKeyboardMarkup:
    """
    Builder for dialogue button after language test.

    """

    builder = InlineKeyboardBuilder()

    builder.button(
        text=_("Now let's start a dialogue practice"),
        callback_data=DialogAfterTestCD().pack(),
    )
    return builder.as_markup()
