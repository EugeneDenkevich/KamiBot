from typing import Optional

from aiogram import F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.input_file import BufferedInputFile
from aiogram.utils.i18n import gettext as _

from kami.backend.presentation.client import BackendClient
from kami.bot_client.common.utils import get_voice_reply
from kami.bot_client.keyboards.dialogue import (
    MyTopicCallback,
    TopicSelectedCD,
    build_dialog_markup,
)
from kami.bot_client.states.dialogue import DialogFSM

router = Router()


@router.message(Command(commands=["dialog"]))
async def handle_dialog_command(
    message: Message,
    state: Optional[FSMContext],
) -> None:
    """
    Handler for /dialogue

    :param message: Message from telegram.
    """

    await state.clear()  # type: ignore[union-attr]

    await message.answer(
        text=_(
            "Let's practice English!\n"
            "Select any topic to begin the dialog and we'll "
            "be able to talk by voice messages on this topic:",
        ),
        reply_markup=build_dialog_markup(bot_name="KamiBOT"),
    )


@router.callback_query(MyTopicCallback.filter())
async def handle_my_topic(
    callback: CallbackQuery,
    state: Optional[FSMContext],
) -> None:
    """
    Handler for "Topic of dialogue" button's.

    :param mescall: Message or callback.
    :param state: User Status.
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
) -> None:
    """
    Handler for "Topic of dialogue" button's.

    :param mescall: Message or callback.
    :param state: User Status.
    """

    await callback.answer()

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


@router.message(DialogFSM.my_topic)
async def handle_my_topic_selected(
    message: Message,
    state: Optional[FSMContext],
    backend_client: BackendClient,
) -> None:
    """
    Handler for "Topic of dialogue" button's.

    :param mescall: Message or callback.
    :param state: User Status.
    """

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


@router.message(F.voice and DialogFSM.conversation)
async def handle_dialog_voice(
    message: Message,
    backend_client: BackendClient,
    state: Optional[FSMContext],
) -> None:

    voice_reply = await get_voice_reply(message)

    await message.bot.send_chat_action(  # type: ignore[union-attr]
        chat_id=message.chat.id,
        action=ChatAction.RECORD_VOICE,
    )

    try:
        voice = await backend_client.continue_dialogue(
            tg_id=str(message.from_user.id),  # type: ignore[union-attr]
            voice=voice_reply,
        )
    except:
        await state.clear()  # type: ignore[union-attr]
        raise
    else:
        await message.answer_audio(
            audio=BufferedInputFile(file=voice, filename="voice1.ogg"),
        )
