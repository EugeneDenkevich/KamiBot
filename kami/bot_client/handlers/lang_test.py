
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from kami.backend.domain.ai.exceptions import AINotFoundError
from kami.backend.domain.lang_test.exceptions import NoQuestionsError
from kami.backend.presentation.client import BackendClient
from kami.bot_client.common.utils import auth_user, get_voice_reply, parse_question
from kami.bot_client.keyboards.dialog_after_test import build_dialog_after_test_markup
from kami.bot_client.keyboards.lang_test import (
    StartLangTestCallback,
    build_lang_test_markup,
)
from kami.bot_client.keyboards.main_menu import build_main_menu_markup
from kami.bot_client.states.lang_test import LangTestFSM

router = Router()


@router.message(F.text == __("Language Level"))
@router.message(Command(commands=["lang_test"]))
async def handle_lang_test(
    message: Message,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for /lang_test command.

    :param message: Message from telegram.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    user = await auth_user(
        message=message,
        backend_client=backend_client,
        tg_id=str(message.from_user.id),  # type: ignore[union-attr]
        state=state,
    )

    if user:
        await state.clear()

        await message.answer(
            text=_("Start test?"),
            reply_markup=build_lang_test_markup(),
        )


@router.callback_query(StartLangTestCallback.filter())
async def handle_testing(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for "Start language test" button.

    :param mescall: Message or callback.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    await callback_query.answer()  # type: ignore[call-arg]

    tg_id = str(callback_query.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=callback_query.message,  # type: ignore[union-attr, arg-type]
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_("One moment..."),
            reply_markup=ReplyKeyboardRemove(),
        )

        await state.set_state(LangTestFSM.lang_testing)

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_("Test is creating..."),
        )

        try:
            await backend_client.start_test(tg_id=tg_id)
        except AINotFoundError:
            await state.clear()
            await callback_query.message.answer(  # type: ignore[union-attr]
                text=_(
                    "Error while test creating: NoAiError",
                ),
            )
        else:
            await callback_query.message.answer(  # type: ignore[union-attr]
                text=_("Test was created."),
            )

            current_question = await backend_client.ask_one(tg_id=tg_id)
            await callback_query.message.answer(  # type: ignore[union-attr]
                text=parse_question(current_question=current_question),
            )


@router.message(F.text, LangTestFSM.lang_testing)
async def handle_lang_test_text(
    message: Message,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for user language test text answer.

    :param message: Message from user.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    tg_id = str(message.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=message,
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await state.set_state(LangTestFSM.lang_testing)

        try:
            await backend_client.save_reply(
                tg_id=tg_id,
                reply=message.text,  # type: ignore[arg-type]
            )

            current_question = await backend_client.ask_one(tg_id=tg_id)
        except NoQuestionsError:
            await state.clear()

            rate = await backend_client.rate_lang_level(tg_id=tg_id)

            await message.answer(  # type: ignore[union-attr]
                text=_("Yor result is: {rate}.").format(rate=rate),
                reply_markup=build_main_menu_markup(),
            )
            await message.answer(  # type: ignore[union-attr]
                text=_(
                    "Now i recommend you to practise your speaking skills.",
                ).format(rate=rate),
                reply_markup=build_dialog_after_test_markup(),
            )

            return
        await message.answer(  # type: ignore[union-attr]
            text=parse_question(current_question),
        )


@router.message(F.voice, LangTestFSM.lang_testing)
async def handle_lang_test_voice(
    message: Message,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for user language test voice answer.

    :param message: Message from user.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    tg_id = str(message.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
            message=message,
            backend_client=backend_client,
            tg_id=tg_id,
            state=state,
    )

    if user:
        await state.set_state(LangTestFSM.lang_testing)

        voice_reply = await get_voice_reply(message)

        try:
            await backend_client.save_reply(tg_id=tg_id, reply=voice_reply)

            current_question = await backend_client.ask_one(tg_id=tg_id)
        except NoQuestionsError:
            await state.clear()

            rate = await backend_client.rate_lang_level(tg_id=tg_id)
            await message.answer(  # type: ignore[union-attr]
                text=_("Yor result is: {rate}.").format(rate=rate),
            )

            return
        await message.answer(  # type: ignore[union-attr]
            text=parse_question(current_question),
        )
