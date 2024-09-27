from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


class AddUserCallbackData(CallbackData, prefix="add_user"):  # type: ignore[call-arg]
    """Callback data for "Add user" button"""

    tg_id: str
    phone: str


def build_add_user_markup(
    tg_id: str,
    phone: str,
) -> InlineKeyboardMarkup:
    """
    Builder for add user keyboard.

    :param tg_id: User telegram id.
    :param fio: User fullname.
    """

    builder = InlineKeyboardBuilder()

    builder.button(
        text=_("Add user"),
        callback_data=AddUserCallbackData(
            tg_id=tg_id,
            phone=phone,
        ).pack(),
    )

    return builder.as_markup()
