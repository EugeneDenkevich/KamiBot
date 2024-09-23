from typing import Union

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _

from kami.backend.domain.lang_test.exceptions import NoQuestionsError
from kami.backend.presentation.client import BackendClient
from kami.backend.presentation.exceptions import StartTestError
from kami.bot_client.common.utils import get_voice_reply, parse_question
from kami.bot_client.keyboards.lang_test import (
    StartLangTestCallback,
    build_lang_test_keyboard,
)
from kami.bot_client.states.lang_test import LangTestFSM

router = Router()


@router.message(Command(commands=["lang_test"]))
async def handle_start(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Handler for /lang_test command.

    :param message: Message from telegram.
    """

    await state.clear()

    await message.answer(
        text=_("Start test?"),
        reply_markup=build_lang_test_keyboard(),
    )


@router.callback_query(StartLangTestCallback.filter())
async def handle_lang_test(
    callback: Union[Message, CallbackQuery],
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for "Start language test" button.

    :param callback: Callback query from button.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    tg_id = str(callback.from_user.id)  # type: ignore[union-attr]

    await state.set_state(LangTestFSM.lang_testing)
    await callback.answer()  # type: ignore[call-arg]

    await callback.message.answer(  # type: ignore[union-attr]
        text=_("Test is creating..."),
    )

    try:
        await backend_client.start_test(tg_id=tg_id)
    except StartTestError:
        await state.clear()
        await callback.message.answer(  # type: ignore[union-attr]
            text=_(
                "Error while test creating try again: {command}.",
            ).format(command="/lang_test"),
        )

    await callback.message.answer(  # type: ignore[union-attr]
        text=_("Test was created."),
    )

    current_question = await backend_client.ask_one(tg_id=tg_id)
    await callback.message.answer(  # type: ignore[union-attr]
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
