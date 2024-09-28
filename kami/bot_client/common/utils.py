import asyncio
from typing import BinaryIO, Optional, Union

from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.inaccessible_message import InaccessibleMessage
from aiogram.utils.i18n import gettext as _

from kami.backend.domain.lang_test.models import QuestT
from kami.backend.domain.user.exceptions import UserNotFoundError
from kami.backend.domain.user.models import User
from kami.backend.presentation.client import BackendClient
from kami.bot_client.keyboards.share_contact import build_share_contact_markup
from kami.bot_client.states.dialogue import DialogFSM
from kami.bot_client.states.register import RegisterFSM


def parse_question(
    current_question: QuestT,
) -> str:

    question = f"{current_question['question']}\n"
    options = current_question["options"]
    for leeter, option in options.items():  # type: ignore[union-attr]
        question += f"\n{leeter}). {option}"
    return question


async def get_voice_reply(message: Message) -> bytes:
    """
    Get voice reply from message.

    :param message: Message from telegram.
    """

    voice_file = await message.bot.get_file(  # type: ignore[union-attr]
        file_id=message.voice.file_id,  # type: ignore[union-attr]
    )
    voice_binary: BinaryIO = await message.bot.download(   # type: ignore[assignment, union-attr]
        file=voice_file,
    )

    return voice_binary.read()


async def wait_for_answer(
    awaiting_time: int,
    message: Message,
    state: FSMContext,
    text: str,
) -> None:
    """
    Wait if user is not responsing.

    :param message: Message.
    :param await_for_answer: How much awaiting in sec.
    :param state: FSM context.
    """

    async def notify_if_no_response() -> None:
        await asyncio.sleep(awaiting_time)

        if await state.get_state() == DialogFSM.conversation.state:
            await message.answer(text)
            await state.clear()

    asyncio.create_task(notify_if_no_response())


async def auth_user(
    message: Union[Message, InaccessibleMessage, None],
    backend_client: BackendClient,
    tg_id: str,
    state: FSMContext,
) -> Optional[User]:
    """
    Try authorize in bot.

    :param message: Message from user.
    :param backend_client: Backend client.
    :param tg_id: Telegram user id.
    :param state: FSM state.
    """

    try:
        user = await backend_client.get_user(tg_id=tg_id)
    except UserNotFoundError:
        await state.set_state(RegisterFSM.share_contact)

        await message.answer(  # type: ignore[union-attr]
            text=_("Hello. Please, share your contact"),
            reply_markup=build_share_contact_markup(),
        )
        return None
    else:
        if not user.active:
            await message.answer(  # type: ignore[union-attr]
                text=_(
                    "Hello. Unfortunately, your subscription is not activated.\n"
                    "To continue, go to the <b>Menu</b> and select <b>Payment</b> "
                    "or pay now by clicking <b>Activate subscribtion</b>.\n"
                    "After payment, the administrator will confirm your account "
                    "activation and you can press /start again",
                ),
                parse_mode=ParseMode.HTML,
            )
            return None
        return user
