from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import KeyboardButton


def build_main_menu_markup() -> ReplyKeyboardMarkup:
    """Builder for main menu."""

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Dialogues")),
                KeyboardButton(text=_("Language Level")),
                KeyboardButton(text=_("Translator")),
            ],
        ],
        resize_keyboard=True,
    )
