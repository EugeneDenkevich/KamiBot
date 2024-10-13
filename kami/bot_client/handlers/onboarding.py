import asyncio
import logging
from typing import Union

from aiogram import F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramNetworkError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.i18n import gettext as _

from kami.backend.domain.audit.enums import ActionEnum, ModuleEnum
from kami.backend.presentation.client import BackendClient
from kami.bot_client.common.utils import auth_user
from kami.bot_client.enums.stickers import StickersEnum
from kami.bot_client.enums.video_notes import VideoNotesEnum
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

    :param mescall: Message or callback.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    tg_id = str(mescall.from_user.id)  # type: ignore[union-attr]

    if isinstance(mescall, CallbackQuery):
        await mescall.answer()

        message = mescall.message
    else:
        message = mescall

    user = await auth_user(
        message=message,
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.ONBOARDING,
            action=ActionEnum.USER_PUSH,
        )

        await backend_client.update_user(
            tg_id=tg_id,
            onboarded=True,
        )
        await message.answer_sticker(StickersEnum.KAMILA_ONBOARDING_START)
        await message.answer(  # type: ignore[union-attr]
            text=_(
                "Now I'll tell you how to use all my features, "
                "and then we can test your English level.",
            ),
            reply_markup=build_onboarding_step_markup(
                text=_("Cool idea 😊"),
                step=2,
            ),
        )


@router.callback_query(OnboardingCD.filter(F.step == 2))
async def handle_onboarding_first(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for second step of onboarding.

    :param callback_query: CallbackQuery.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    await state.clear()

    tg_id = str(callback_query.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=callback_query.message,
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.ONBOARDING,
            action=ActionEnum.BOT_SENT,
        )

        await callback_query.answer()

        await callback_query.message.answer_sticker(StickersEnum.KAMILA_BASE_FUNC)
        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "👇At the bottom there is a quick menu with basic functions:\n"
                "📍Dialogues\n"
                "📍Language Level\n"
                "📍Translator\n",
            ),
            reply_markup=build_main_menu_markup(),
        )

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "🔴<b>Click</b> on these buttons to quickly "
                "select the desired function.\n"
                "And also the <b>Menu</b> button with additional functions: \n"
                "📍Onboarding \n",
            ),
            reply_markup=build_onboarding_step_markup(
                text=_("Got it"),
                step=3,
            ),
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

    :param callback_query: CallbackQuery.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    tg_id = str(callback_query.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=callback_query.message,
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.ONBOARDING,
            action=ActionEnum.BOT_SENT,
        )

        await callback_query.answer()

        await callback_query.message.answer_sticker(StickersEnum.KAMILA_ONBOARDING_START)
        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "Now I will show you how to use the basic functions. "
                "But you can always go through this training again.",
            ),
        )

        await asyncio.sleep(1)

        await callback_query.message.bot.send_chat_action(  # type: ignore[union-attr]
            chat_id=callback_query.message.chat.id,
            action=ChatAction.RECORD_VIDEO_NOTE,
        )

        video_file = FSInputFile(VideoNotesEnum.KAMILA_DIALOG)

        try:
            await callback_query.message.answer_video_note(video_file)
        except TelegramNetworkError:
            logging.error(f"No file {VideoNotesEnum.KAMILA_DIALOG}")
            pass

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "📹 This video shows how to work with “Dialogues”.\n"
                "👀 Watch the video, then click the “Got it” button",
            ),
            reply_markup=build_onboarding_step_markup(
                text=_("Got it 😉"),
                step=4,
            ),
        )


@router.callback_query(OnboardingCD.filter(F.step == 4))
async def handle_onboarding_third(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for fourth step of onboarding.

    :param callback_query: CallbackQuery.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    tg_id = str(callback_query.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=callback_query.message,
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.ONBOARDING,
            action=ActionEnum.BOT_SENT,
        )

        await callback_query.answer()

        await callback_query.message.bot.send_chat_action(  # type: ignore[union-attr]
            chat_id=callback_query.message.chat.id,
            action=ChatAction.RECORD_VIDEO_NOTE,
        )

        video_file = FSInputFile(VideoNotesEnum.KAMILA_TRANSLATE)

        try:
            await callback_query.message.answer_video_note(video_file)
        except TelegramNetworkError:
            logging.error(f"No file {VideoNotesEnum.KAMILA_TRANSLATE}")
            pass

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "This video shows how the “Translator” works.\n"
                "Watch the video, then click the “Got it” button",
            ),
            reply_markup=build_onboarding_step_markup(
                text=_("Got it 😊"),
                step=5,
            ),
        )


@router.callback_query(OnboardingCD.filter(F.step == 5))
async def handle_onboarding_fourth(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for fourth step of onboarding.

    :param callback_query: CallbackQuery.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    tg_id = str(callback_query.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=callback_query.message,
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.ONBOARDING,
            action=ActionEnum.BOT_SENT,
        )

        await callback_query.answer()

        await callback_query.message.bot.send_chat_action(  # type: ignore[union-attr]
            chat_id=callback_query.message.chat.id,
            action=ChatAction.RECORD_VIDEO_NOTE,
        )

        video_file = FSInputFile(VideoNotesEnum.KAMILA_LANGUAGE_TEST)

        try:
            await callback_query.message.answer_video_note(video_file)
        except TelegramNetworkError:
            logging.error(f"No file {VideoNotesEnum.KAMILA_LANGUAGE_TEST}")
            pass

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "This video shows how the “Language Level” works.\n"
                "Watch the video, then click the “Got it” button",
            ),
            reply_markup=build_onboarding_step_markup(
                text=_("Got it"),
                step=6,
            ),
        )


@router.callback_query(OnboardingCD.filter(F.step == 6))
async def handle_onboarding_fifth(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for fourth step of onboarding.

    :param callback_query: CallbackQuery.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    tg_id = str(callback_query.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=callback_query.message,
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.ONBOARDING,
            action=ActionEnum.BOT_SENT,
        )

        await callback_query.answer()

        await callback_query.message.answer_sticker(StickersEnum.KAMILA_LANGUAGE_TEST)
        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "😉 Great, it's time to determine your <b>level</b> of English. 🧐\n"
                "Click the <b>button below</b> 🖲 and take the 6-question test.\n"
                "📝 This will help me choose the style and phrases to "
                "communicate with you.",
            ),
            reply_markup=build_onboarding_step_markup(
                text=_("Language level test start 😉"),
                step=7,
            ),
            parse_mode=ParseMode.HTML,
        )


@router.callback_query(ShowWhereCD.filter())
async def handle_show_where(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for fourth step of onboarding.

    :param callback_query: CallbackQuery.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    tg_id = str(callback_query.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=callback_query.message,
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.ONBOARDING,
            action=ActionEnum.BOT_SENT,
        )

        await callback_query.answer()

        await callback_query.message.bot.send_chat_action(  # type: ignore[union-attr]
            chat_id=callback_query.message.chat.id,
            action=ChatAction.RECORD_VIDEO_NOTE,
        )

        video_file = FSInputFile(VideoNotesEnum.KAMILA_MENU)

        try:
            await callback_query.message.answer_video_note(video_file)
        except TelegramNetworkError:
            logging.error(f"No file {VideoNotesEnum.KAMILA_MENU}")
            pass

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "👀 Watch the videonote and everything will become clear.",
            ),
            reply_markup=build_onboarding_step_markup(text=_("Got it")),
        )
