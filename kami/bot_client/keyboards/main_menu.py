from typing import List

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import KeyboardButton

from aiogram.utils.i18n import gettext as _


def get_main_reply_buttons() -> List[str]:
    return [
        "Dialoghi",
        "Livello linguistico",
        "Traduttore"
    ]


def build_main_menu_markup() -> ReplyKeyboardMarkup:
    """Builder for main menu."""

    keyboard = []
    main_reply_buttons = get_main_reply_buttons()

    for button in main_reply_buttons:
        keyboard.append(KeyboardButton(text=button))

    return ReplyKeyboardMarkup(
        keyboard=[keyboard],
        resize_keyboard=True,
    )
