import asyncio
from typing import Union

from aiogram import F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _

from kami.backend.presentation.client import BackendClient
from kami.bot_client.common.utils import auth_user
from kami.bot_client.keyboards.main_menu import build_main_menu_markup
from kami.bot_client.keyboards.onboarding import (
    OnboardingCD,
    ShowWhereCD,
    build_onboarding_step_markup,
)

router = Router()


@router.message(Command(commands=["onboarding"]))
@router.callback_query(OnboardingCD.filter(F.step == 1))
async def handle_start_onboarding(
    mescall: Union[Message, CallbackQuery],
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for first step of onboarding.

    :param message: Message from telegram.
    """

    tg_id = str(mescall.from_user.id)

    user = await auth_user(
        message=mescall if isinstance(mescall, Message) else mescall.message,
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        if isinstance(mescall, CallbackQuery):
            await mescall.answer()

            message = mescall.message
        else:
            message = mescall

        await backend_client.update_user(
            tg_id=tg_id,  # type: ignore[union-attr]
            onboarded=True,
        )

        await message.answer(  # type: ignore[union-attr]
            text=_(
                "Now I'll tell you how to use all my features, "
                "and then we can test your English level.",
            ),
            reply_markup=build_onboarding_step_markup(text="Cool idea 😊", step=2),
        )


@router.callback_query(OnboardingCD.filter(F.step == 2))
async def handle_onboarding_first(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for second step of onboarding.

    :param message: Message from telegram.
    """

    await state.clear()

    user = await auth_user(
        message=callback_query.message,
        backend_client=backend_client,
        tg_id=str(callback_query.from_user.id),
        state=state,
    )

    if user:
        await callback_query.answer()

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "At the bottom there is a quick menu with basic functions: "
                "Dialogues, Language Level, Translator.\n",
            ),
            reply_markup=build_main_menu_markup(),
        )
        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "Click on these buttons to quickly select the desired function. "
                "And also the <b>Menu</b> button with additional functions: \n"
                "Answers to questions, Payment, Feedback, and so on.",
            ),
            reply_markup=build_onboarding_step_markup(text="Got it", step=3),
            parse_mode=ParseMode.HTML,
        )


@router.callback_query(OnboardingCD.filter(F.step == 3))
async def handle_onboarding_second(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for third step of onboarding.

    :param message: Message from telegram.
    """

    user = await auth_user(
        message=callback_query.message,
        backend_client=backend_client,
        tg_id=str(callback_query.from_user.id),
        state=state,
    )

    if user:
        await callback_query.answer()

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "Now I will show you how to use the basic functions. "
                "But you can always go through this training again.",
            ),
        )

        await asyncio.sleep(1)

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "This video shows how to work with “Dialogues”.\n"
                "Watch the video, then click the “Got it” button",
            ),
            reply_markup=build_onboarding_step_markup(text="Got it", step=4),
        )


@router.callback_query(OnboardingCD.filter(F.step == 4))
async def handle_onboarding_third(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for fourth step of onboarding.

    :param message: Message from telegram.
    """

    user = await auth_user(
        message=callback_query.message,
        backend_client=backend_client,
        tg_id=str(callback_query.from_user.id),
        state=state,
    )

    if user:
        await callback_query.answer()

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "This video shows how the “Translator” works.\n"
                "Watch the video, then click the “Got it” button",
            ),
            reply_markup=build_onboarding_step_markup(text="Got it", step=5),
        )


@router.callback_query(OnboardingCD.filter(F.step == 5))
async def handle_onboarding_fourth(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for fourth step of onboarding.

    :param message: Message from telegram.
    """

    user = await auth_user(
        message=callback_query.message,
        backend_client=backend_client,
        tg_id=str(callback_query.from_user.id),
        state=state,
    )

    if user:
        await callback_query.answer()

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "This video shows how the “Language Level” works.\n"
                "Watch the video, then click the “Got it” button",
            ),
            reply_markup=build_onboarding_step_markup(text="Got it", step=6),
        )


@router.callback_query(OnboardingCD.filter(F.step == 6))
async def handle_onboarding_fifth(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for fourth step of onboarding.

    :param message: Message from telegram.
    """

    user = await auth_user(
        message=callback_query.message,
        backend_client=backend_client,
        tg_id=str(callback_query.from_user.id),
        state=state,
    )

    if user:
        await callback_query.answer()

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "Great, it's time to determine your level of English.\n"
                "Click the button below and take the 6-question test.\n"
                "This will help me choose the style and phrases to "
                "communicate with you.",
            ),
            reply_markup=build_onboarding_step_markup(
                text="Language level test",
                step=7,
            ),
        )


@router.callback_query(ShowWhereCD.filter())
async def handle_show_where(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for fourth step of onboarding.

    :param message: Message from telegram.
    """

    user = await auth_user(
        message=callback_query.message,
        backend_client=backend_client,
        tg_id=str(callback_query.from_user.id),
        state=state,
    )

    if user:
        await callback_query.answer()

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "Watch the videonote and everything will become clear.",
            ),
            reply_markup=build_onboarding_step_markup(text="Got it"),
        )
