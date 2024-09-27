from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


class StartLangTestCallback(  # type: ignore[call-arg]
    CallbackData,
    prefix="start_lang_test",
):
    """Callback data for "Start language test" button"""


def build_lang_test_markup() -> InlineKeyboardMarkup:
    """
    Builder for start language test markup.

    :return: Language test markup
    """

    builder = InlineKeyboardBuilder()

    builder.button(
        text=_("Start language test"),
        callback_data=StartLangTestCallback().pack(),
    )

    return builder.as_markup()
