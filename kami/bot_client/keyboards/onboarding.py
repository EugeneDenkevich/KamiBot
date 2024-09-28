from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from kami.bot_client.keyboards.lang_test import StartLangTestCallback


class OnboardingCD(
    CallbackData,
    prefix="onboarding",  # type: ignore[call-arg]
):
    """Callback data for onboarding's button"""

    step: int


class ShowWhereCD(
    CallbackData,
    prefix="onboarding",  # type: ignore[call-arg]
):
    """Callback data for "Show where" button"""


def build_onboarding_step_markup(
    text: str,
    step: Optional[int] = None,
) -> InlineKeyboardMarkup:
    """Builder for first step of onboarding."""

    builder = InlineKeyboardBuilder()

    if step != 7:
        builder.button(
            text=text,
            callback_data=OnboardingCD(step=step if step else 3).pack(),
        )
    else:
        builder.button(
            text=text,
            callback_data=StartLangTestCallback().pack(),
        )

    if step == 3:
        builder.button(
            text=_("Show where it is"),
            callback_data=ShowWhereCD().pack(),
        )

    return builder.as_markup()
