from typing import Union

from aiogram import F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.input_file import BufferedInputFile
from aiogram.utils.i18n import gettext as _

from kami.backend.domain.audit.enums import ActionEnum, ModuleEnum
from kami.backend.domain.dialog.exceptions import DialogueNotFoundError
from kami.backend.presentation.client import BackendClient
from kami.bot_client.common.utils import auth_user, get_voice_reply, wait_for_answer
from kami.bot_client.enums.stickers import StickersEnum
from kami.bot_client.keyboards.dialog_after_test import DialogAfterTestCD
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
@router.callback_query(DialogAfterTestCD.filter())
async def handle_dialog_command(
    mescall: Union[Message, CallbackQuery],
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for /dialogue

    :param mescall: Message or callback.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    await state.clear()  # type: ignore[union-attr]

    tg_id = str(mescall.from_user.id)  # type: ignore[union-attr]

    if isinstance(mescall, CallbackQuery):
        await mescall.answer()

        message = mescall.message
    else:
        message = mescall

    user = await auth_user(
        message=message,  # type: ignore[arg-type]
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.DIALOGS,
            action=ActionEnum.BOT_SENT,
        )

        no_dialog = False
        try:
            await backend_client.get_dialog(tg_id=tg_id)
        except DialogueNotFoundError:
            no_dialog = True

        if no_dialog:
            # Multiline i18n work only in such format
            await message.answer_sticker(StickersEnum.KAMILA_FIRST_DIALOG)
            await message.answer(  # type: ignore[union-attr]
                text=_(
                    "Let's practice 🗣 English!\n"
                    "😎 Select any topic to begin the dialog and we'll "
                    "be able to talk by voice messages on this topic:",
                ),
                reply_markup=build_dialog_markup(no_dialog=no_dialog),
            )
        else:
            # Multiline i18n work only in such format
            await message.answer_sticker(
                StickersEnum.KAMILA_SECOND_DIALOGUE,  # type: ignore[arg-type]
            )
            await message.answer(  # type: ignore[union-attr]
                text=_(
                    "🥰 Welcome back, let's continue the practice of communication!"
                    "Let's practice 🗣 English!\n"
                    "😎 Select any topic to begin the dialog and we'll "
                    "be able to talk by voice messages on this topic:",
                ),
                reply_markup=build_dialog_markup(no_dialog=no_dialog),
            )


@router.callback_query(MyTopicCallback.filter())
async def handle_my_topic(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for "Topic of dialogue" button's.

    :param callback_query: CallbackQuery.
    :param backend_client: Backend client.
    :param state: FSM state.
    """

    await callback_query.answer()

    tg_id = str(callback_query.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=callback_query.message,  # type: ignore[union-attr]
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.DIALOGS,
            action=ActionEnum.BOT_SENT,
        )

        await state.set_state(DialogFSM.my_topic)  # type: ignore[union-attr]

        await callback_query.message.answer_sticker(  # type: ignore[union-attr]
            StickersEnum.KAMILA_MY_TOPIC,  # type: ignore[arg-type]
        )
        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_("Input your topic, please"),
        )


@router.callback_query(TopicSelectedCD.filter())
async def handle_topic_selected(
    callback_query: CallbackQuery,
    callback_data: TopicSelectedCD,
    state: FSMContext,
    backend_client: BackendClient,
    settings: Settings,
) -> None:
    """
    Handler for "Topic of dialogue" button's.

    :param settings: Get settings.
    :param callback_query: Callback query.
    :param callback_data: Callback data.
    :param backend_client: BackendClient.
    :param state: FSM state.
    """

    await callback_query.answer()

    tg_id = str(callback_query.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=callback_query.message,  # type: ignore[union-attr]
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.DIALOGS,
            action=ActionEnum.USER_PUSH,
        )

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_("One moment..."),
        )

        await state.set_state(DialogFSM.conversation)  # type: ignore[union-attr]

        await callback_query.bot.send_chat_action(  # type: ignore[union-attr]
            chat_id=callback_query.message.chat.id,  # type: ignore[union-attr]
            action=ChatAction.RECORD_VOICE,
        )

        try:
            voice_answer = await backend_client.start_dialog(
                tg_id=tg_id,
                topic=callback_data.topic,
            )
        except:
            await state.clear()  # type: ignore[union-attr]
            raise
        else:
            await callback_query.message.answer_audio(  # type: ignore[union-attr]
                audio=BufferedInputFile(file=voice_answer, filename="voice.ogg"),
            )

            await wait_for_answer(
                awaiting_time=settings.awaiting_time,
                message=callback_query.message,  # type: ignore[arg-type]
                state=state,  # type: ignore[arg-type]
                text=_("Awaiting time is up. Continue dialog here /dialog."),
            )


@router.message(DialogFSM.my_topic)
async def handle_my_topic_selected(
    message: Message,
    state: FSMContext,
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

    tg_id = str(message.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=message,
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.DIALOGS,
            action=ActionEnum.BOT_SENT,
        )

        await message.answer(text=_("One moment..."))

        await state.set_state(DialogFSM.conversation)  # type: ignore[union-attr]

        await message.bot.send_chat_action(  # type: ignore[union-attr]
            chat_id=message.chat.id,
            action=ChatAction.RECORD_VOICE,
        )

        try:
            if message.content_type == "voice":
                voice_replay = await get_voice_reply(message)
                topic = await backend_client.voice_to_text(voice_replay)

            else:
                topic = message.text  # type: ignore[assignment]

            voice_answer = await backend_client.start_dialog(
                tg_id=tg_id,  # type: ignore[union-attr]
                topic=topic,  # type: ignore[arg-type]
            )
        except:
            await state.clear()  # type: ignore[union-attr]
            raise
        else:
            await message.answer_audio(  # type: ignore[union-attr]
                audio=BufferedInputFile(file=voice_answer, filename="voice.ogg"),
            )

        await wait_for_answer(
            awaiting_time=settings.awaiting_time,
            message=message,
            state=state,  # type: ignore[arg-type]
            text=_("Awaiting time is up. Continue dialog here /dialog."),
        )


@router.message(F.voice, DialogFSM.conversation)
async def handle_dialog_voice(
    message: Message,
    backend_client: BackendClient,
    state: FSMContext,
    settings: Settings,
) -> None:
    """
    Hadle dialog voice.

    :param message: Message from telegram.
    :param state: FSM state.
    :param backend_client: Backend client.
    :param settings: Project settings.
    """
    tg_id = str(message.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=message,
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.DIALOGS,
            action=ActionEnum.BOT_SENT,
        )

        voice_reply = await get_voice_reply(message)

        await message.bot.send_chat_action(  # type: ignore[union-attr]
            chat_id=message.chat.id,
            action=ChatAction.RECORD_VOICE,
        )
        try:
            voice, mistakes = await backend_client.continue_dialog(
                tg_id=tg_id,  # type: ignore[union-attr]
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
            state=state,  # type: ignore[arg-type]
            text=_("Awaiting time is up. Continue dialog here /dialog."),
        )


@router.callback_query(ContinueDialogueCD.filter())
async def handle_continue_dialog(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for continuing dialog button.

    :param callback_query: Callback.
    :param backend_client: Get functions from BackendClient.
    :param state: FSM state.
    """

    await callback_query.answer()

    tg_id = str(callback_query.from_user.id)  # type: ignore[union-attr]

    user = await auth_user(
        message=callback_query.message,  # type: ignore[arg-type]
        backend_client=backend_client,
        tg_id=tg_id,
        state=state,
    )

    if user:
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.DIALOGS,
            action=ActionEnum.BOT_SENT,
        )

        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_("One moment..."),
        )

        try:
            await backend_client.get_dialog(tg_id=tg_id)
        except DialogueNotFoundError:
            await callback_query.message.answer(  # type: ignore[union-attr]
                _(
                    "You dont have a created dialog yet! "
                    "Choose a topic for the dialogue and start your first dialogue.",
                ),
            )
        else:
            await callback_query.message.bot.send_chat_action(  # type: ignore[union-attr]
                chat_id=callback_query.message.chat.id,  # type: ignore[union-attr]
                action=ChatAction.RECORD_VOICE,
            )

            voice_answer = await backend_client.return_to_dialog(tg_id=tg_id)

            await callback_query.message.answer_audio(  # type: ignore[union-attr]
                audio=BufferedInputFile(file=voice_answer, filename="voice.ogg"),
            )

            await state.set_state(DialogFSM.conversation)  # type: ignore[union-attr]
