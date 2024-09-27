from typing import Optional

from aiogram import F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.input_file import BufferedInputFile
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _

from kami.backend.domain.dialog.exceptions import DialogueNotFoundError
from kami.backend.presentation.client import BackendClient
from kami.bot_client.common.utils import auth_user, get_voice_reply, wait_for_answer
from kami.bot_client.keyboards.dialogue import (
    ContinueDialogueCD,
    MyTopicCallback,
    TopicSelectedCD,
    build_dialog_markup,
)
from kami.bot_client.states.dialogue import DialogFSM
from kami.settings import Settings

router = Router()


@router.message(Command(commands=["dialog"]))
@router.message(F.text == "Dialogues")
async def handle_dialog_command(
    message: Message,
    state: Optional[FSMContext],
    backend_client: BackendClient,
) -> None:
    """
    Handler for /dialogue

    :param message: Message from telegram.
    :param state: FSM state.
    """

    await state.clear()  # type: ignore[union-attr]

    user = await auth_user(
        message=message,
        backend_client=backend_client,
        tg_id=str(message.from_user.id),
        state=state,
    )

    if user:
        no_dialog = False
        try:
            await backend_client.get_dialog(
                tg_id=str(message.from_user.id),  # type: ignore[union-attr]
            )
        except DialogueNotFoundError:
            no_dialog = True

        await message.answer(
            text=_(
                "Let's practice English!\n"
                "Select any topic to begin the dialog and we'll "
                "be able to talk by voice messages on this topic:",
            ),
            reply_markup=build_dialog_markup(no_dialog=no_dialog),
        )


@router.callback_query(MyTopicCallback.filter())
async def handle_my_topic(
    callback: CallbackQuery,
    state: Optional[FSMContext],
) -> None:
    """
    Handler for "Topic of dialogue" button's.

    :param mescall: Message or callback.
    :param state: FSM state.
    """

    await callback.answer()

    await state.set_state(DialogFSM.my_topic)  # type: ignore[union-attr]

    await callback.message.answer(   # type: ignore[union-attr]
        text="Input your topic, please",
    )


@router.callback_query(TopicSelectedCD.filter())
async def handle_topic_selected(
    callback: CallbackQuery,
    callback_data: TopicSelectedCD,
    state: Optional[FSMContext],
    backend_client: BackendClient,
    settings: Settings,
) -> None:
    """
    Handler for "Topic of dialogue" button's.

    :param mescall: Message or callback.
    :param state: FSM state.
    """

    await callback.answer()

    await callback.message.answer(  # type: ignore[union-attr]
        text=_("One moment..."),
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.set_state(DialogFSM.conversation)  # type: ignore[union-attr]

    await callback.bot.send_chat_action(  # type: ignore[union-attr]
        chat_id=callback.message.chat.id,  # type: ignore[union-attr]
        action=ChatAction.RECORD_VOICE,
    )

    try:
        voice_answer = await backend_client.start_dialog(
            tg_id=str(callback.from_user.id),
            topic=callback_data.topic,
        )
    except:
        await state.clear()  # type: ignore[union-attr]
        raise
    else:
        await callback.message.answer_audio(   # type: ignore[union-attr]
            audio=BufferedInputFile(file=voice_answer, filename="voice.ogg"),
        )

        await wait_for_answer(
            awaiting_time=settings.awaiting_time,
            message=callback.message,  # type: ignore[arg-type]
            state=state,  # type: ignore[arg-type]
            text=_("Awaiting time is up. Continue dialog here /dialog."),
        )


@router.message(DialogFSM.my_topic)
async def handle_my_topic_selected(
    message: Message,
    state: Optional[FSMContext],
    backend_client: BackendClient,
    settings: Settings,
) -> None:
    """
    Handler for "Topic of dialogue" button's.

    :param message: Message from telegram.
    :param state: FSM state.
    :param backend_client: Backend client.
    :param settings: Project settings.
    """

    await message.answer(
        text=_("One moment..."),
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.set_state(DialogFSM.conversation)  # type: ignore[union-attr]

    await message.bot.send_chat_action(  # type: ignore[union-attr]
        chat_id=message.chat.id,
        action=ChatAction.RECORD_VOICE,
    )

    try:
        voice_answer = await backend_client.start_dialog(
            tg_id=str(message.from_user.id),  # type: ignore[union-attr]
            topic=message.text,  # type: ignore[arg-type]
        )
    except:
        await state.clear()  # type: ignore[union-attr]
        raise
    else:
        await message.answer_audio(   # type: ignore[union-attr]
            audio=BufferedInputFile(file=voice_answer, filename="voice.ogg"),
        )

        await wait_for_answer(
            awaiting_time=settings.awaiting_time,
            message=message,
            state=state,  # type: ignore[arg-type]
            text=_("Awaiting time is up. Continue dialog here /dialog."),
        )


@router.message(F.voice and DialogFSM.conversation)
async def handle_dialog_voice(
    message: Message,
    backend_client: BackendClient,
    state: Optional[FSMContext],
    settings: Settings,
) -> None:
    """
    Hadle dialog voice.

    :param message: Message from telegram.
    :param state: FSM state.
    :param backend_client: Backend client.
    :param settings: Project settings.
    """

    voice_reply = await get_voice_reply(message)

    await message.bot.send_chat_action(  # type: ignore[union-attr]
        chat_id=message.chat.id,
        action=ChatAction.RECORD_VOICE,
    )

    try:
        voice, mistakes = await backend_client.continue_dialog(
            tg_id=str(message.from_user.id),  # type: ignore[union-attr]
            voice=voice_reply,
        )
    except:
        await state.clear()  # type: ignore[union-attr]
        raise
    else:
        if mistakes is not None:
            await message.answer(text=mistakes, parse_mode=ParseMode.HTML)

        await message.answer_audio(
            audio=BufferedInputFile(file=voice, filename="voice1.ogg"),
        )

        await wait_for_answer(
            awaiting_time=settings.awaiting_time,
            message=message,
            state=state,   # type: ignore[arg-type]
            text=_("Awaiting time is up. Continue dialog here /dialog."),
        )


@router.callback_query(ContinueDialogueCD.filter())
async def handle_continue_dialog(
    callback: CallbackQuery,
    backend_client: BackendClient,
    state: Optional[FSMContext],
) -> None:
    """
    Handler for continuing dialog button.

    :param callback: Callback.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    await callback.answer()

    await callback.message.answer(  # type: ignore[union-attr]
        text=_("One moment..."),
        reply_markup=ReplyKeyboardRemove(),
    )

    tg_id = str(callback.from_user.id)

    try:
        await backend_client.get_dialog(tg_id=tg_id)
    except DialogueNotFoundError:
        await callback.message.answer(   # type: ignore[union-attr]
            _(
                "You dont have a created dialog yet! "
                "Choose a topic for the dialogue and start your first dialogue.",
            ),
        )
    else:
        await callback.message.bot.send_chat_action(  # type: ignore[union-attr]
            chat_id=callback.message.chat.id,   # type: ignore[union-attr]
            action=ChatAction.RECORD_VOICE,
        )

        voice_answer = await backend_client.return_to_dialog(tg_id=tg_id)

        await callback.message.answer_audio(   # type: ignore[union-attr]
            audio=BufferedInputFile(file=voice_answer, filename="voice.ogg"),
        )

        await state.set_state(DialogFSM.conversation)   # type: ignore[union-attr]
