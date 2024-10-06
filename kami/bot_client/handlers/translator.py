from aiogram import F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from kami.backend.domain.audit.enums import ActionEnum, ModuleEnum
from kami.backend.presentation.client import BackendClient
from kami.bot_client.common.utils import auth_user, get_voice_reply
from kami.bot_client.enums.stickers import StickersEnum
from kami.bot_client.keyboards.translator import (
    StartTranslatorCD,
    build_translator_markup,
)
from kami.bot_client.states.translator import TranslatorFSM
from kami.settings import Settings

router = Router()


@router.message(Command(commands=["translator"]))
@router.message(F.text == __("Translator"))
async def handle_translator_command(
    message: Message,
    backend_client: BackendClient,
    state: FSMContext,
    settings: Settings,
) -> None:
    """
    Handler for /translator command.

    :param message: Message from telegram.
    :param backend_client: Backend client.
    :param state: FSM state.
    :param settings: Get Settings.
    """

    await state.clear()

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
            module=ModuleEnum.TRANSLATE,
            action=ActionEnum.USER_PUSH,
        )

        await message.answer_sticker(StickersEnum.KAMILA_TRANSLATE)

        await message.answer(
            text=_("👇 Choose the language in which you want to translate."),
            reply_markup=build_translator_markup(language=settings.translation_language),
        )


@router.callback_query(StartTranslatorCD.filter())
async def handle_direction_choice(
    callback_query: CallbackQuery,
    backend_client: BackendClient,
    callback_data: StartTranslatorCD,
    state: FSMContext,
) -> None:
    """
    Handler for "Way of translate" button's.

    :param callback_query: Callback query from button.
    :param backend_client: Backend client.
    :param callback_data: Callback data.
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
            module=ModuleEnum.TRANSLATE,
            action=ActionEnum.BOT_SENT,
        )

        await state.update_data(direction=callback_data.direction)

        await callback_query.message.answer_sticker(
            StickersEnum.KAMILA_SECOND_TRANSLATE
        )
        await callback_query.message.answer(  # type: ignore[union-attr]
            text=_(
                "Now it is possible to send a message:\n"
                "🖋 as text\n"
                "🗣 or voice\n"
                "I will translate it and send a response via SMS.\n"
                "❕ If you wish to change the translation direction, press "
                "the Menu button and select the translation language again.",
            ),
        )

        await state.set_state(TranslatorFSM.translating)

        await callback_query.answer()


@router.message(F.text, TranslatorFSM.translating)
async def handle_translator_text(
    message: Message,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for text translation to text.

    :param message: Message from telegram.
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
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.TRANSLATE,
            action=ActionEnum.BOT_SENT,
        )

        user_data = await state.get_data()
        direction = user_data["direction"]

        await message.bot.send_chat_action(  # type: ignore[union-attr]
            chat_id=message.chat.id,
            action=ChatAction.TYPING,
        )

        translated_text = await backend_client.translate_text_to_text(
            direction=direction,
            text=message.text,  # type: ignore[arg-type]
        )

        await message.answer(translated_text)


@router.message(F.voice, TranslatorFSM.translating)
async def handle_translator_voice(
    message: Message,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for voice translation to text.

    :param message: Message from telegram.
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
        await backend_client.log_to_db(
            tg_id=tg_id,
            module=ModuleEnum.TRANSLATE,
            action=ActionEnum.BOT_SENT,
        )

        user_data = await state.get_data()
        direction = user_data["direction"]
        voice_reply = await get_voice_reply(message)

        await message.bot.send_chat_action(  # type: ignore[union-attr]
            chat_id=message.chat.id,
            action=ChatAction.TYPING,
        )

        translated_text = await backend_client.translate_voice_to_text(
            direction=direction,
            voice=voice_reply,
        )

        await message.answer(translated_text)
