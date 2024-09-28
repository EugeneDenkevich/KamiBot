from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


class StartTranslatorCD(  # type: ignore[call-arg]
    CallbackData,
    prefix="trans",
):
    """Callback data for "Start translation" button"""

    direction: str


def build_translator_markup(language: str) -> InlineKeyboardMarkup:
    """
    Builder for start translator markup.

    :return: Translator markup
    """
    builder = InlineKeyboardBuilder()

    builder.button(
        text=_("{language} → English").format(language=language),
        callback_data=StartTranslatorCD(
            direction=f"from {language} to English",
        ).pack(),
    )
    builder.button(
        text=_("English → {language}").format(language=language),
        callback_data=StartTranslatorCD(
            direction=f"from English to {language}",
        ).pack(),
    )
    builder.adjust(1)

    return builder.as_markup()
