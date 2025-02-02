from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


class TopicSelectedCD(
    CallbackData,
    prefix="topic_callback",  # type: ignore[call-arg]
):
    topic: str


class MyTopicCallback(
    CallbackData,
    prefix="my_callback",  # type: ignore[call-arg]
):
    pass


class ContinueDialogueCD(
    CallbackData,
    prefix="continue_callback",  # type: ignore[call-arg]
):
    pass


def build_dialog_markup(no_dialog: bool) -> InlineKeyboardMarkup:
    """
    Builder for dialogue message keyboard.

    :param no_dialog: If previous dialog is saved.
    """

    builder = InlineKeyboardBuilder()

    text = _("A trip to the airport ✈️")
    builder.button(
        text=text,
        callback_data=TopicSelectedCD(topic=text).pack(),
    ).adjust(1)

    text = _("Acquaintance 👫")
    builder.button(
        text=text,
        callback_data=TopicSelectedCD(topic=text).pack(),
    ).adjust(1)

    text = _("Ordering food at a restaurant 🍔")
    builder.button(
        text=text,
        callback_data=TopicSelectedCD(topic=text).pack(),
    ).adjust(1)

    text = _("Job interview 👩‍💼")
    builder.button(
        text=text,
        callback_data=TopicSelectedCD(topic=text).pack(),
    ).adjust(1)

    text = _("My topic 💃")
    builder.button(
        text=text,
        callback_data=MyTopicCallback().pack(),
    ).adjust(1)

    if not no_dialog:
        text = _("Continue dialogue")
        builder.button(
            text=text,
            callback_data=ContinueDialogueCD().pack(),
        ).adjust(1)

    return builder.as_markup()
