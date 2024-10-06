import asyncio
from typing import BinaryIO, Optional, Union

from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.inaccessible_message import InaccessibleMessage
from aiogram.utils.i18n import gettext as _

from kami.backend.domain.user.exceptions import UserNotFoundError
from kami.backend.domain.user.models import User
from kami.backend.presentation.client import BackendClient
from kami.bot_client.enums.stickers import StickersEnum
from kami.bot_client.keyboards.share_contact import build_share_contact_markup
from kami.bot_client.states.register import RegisterFSM


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
    dialog_id: str,
    awaiting_time: int,
    message: Message,
    state: FSMContext,
    backend_client: BackendClient,
) -> None:
    """
    Wait if user is not responsing.

    :param message: Message.
    :param await_for_answer: How much awaiting in sec.
    :param state: FSM context.
    """

    async def notify_if_no_response() -> None:
        """Notify user if he is not respoding"""

        await asyncio.sleep(10)

        dialog = await backend_client.get_dialog_or_none(dialog_id=dialog_id)

        if dialog:
            await message.answer(
                text=_("Awaiting time is up. Continue dialog here /dialog."),
            )
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

        await message.answer_sticker(StickersEnum.KAMILA_AUTH)  # type: ignore[arg-type, union-attr]
        await message.answer(  # type: ignore[union-attr]
            text=_("Hello. Please, share your contact 👇"),
            reply_markup=build_share_contact_markup(),
        )
        return None
    else:
        if not user.active:
            await message.answer_sticker(StickersEnum.KAMILA_START_IF_NOT_PAID)  # type: ignore[arg-type, union-attr]
            await message.answer(  # type: ignore[union-attr]
                text=_(
                    "The administrator will check your data.\n"
                    "If your subscription is paid, you will receive a "
                    "notification and all the functions of the bot will work",
                ),
                parse_mode=ParseMode.HTML,
            )
            return None
        return user
