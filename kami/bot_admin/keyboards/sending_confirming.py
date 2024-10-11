from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from kami.bot_admin.enums.template_type import TemplateTypeEnum


class TextSendindCD(CallbackData, prefix="text_sending"):  # type: ignore[call-arg]
    """Callback data for text sending button"""

    template_type: str
    """Template type"""


def build_sending_confirming_markup(
    template_type: TemplateTypeEnum,
) -> InlineKeyboardMarkup:
    """
    Builder for sending confirmig markup.

    :paran template_type: Type of template.
    """

    builder = InlineKeyboardBuilder()

    builder.button(
        text="Send",
        callback_data=TextSendindCD(template_type=template_type).pack(),
    )

    return builder.as_markup()
