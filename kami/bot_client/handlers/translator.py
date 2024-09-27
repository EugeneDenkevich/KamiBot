from typing import Optional

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from kami.backend.presentation.client import BackendClient
from kami.bot_client.common.utils import auth_user

router = Router()


@router.message(Command(commands=["translator"]))
@router.message(F.text == "Translator")
async def handle_dialog_command(
    message: Message,
    backend_client: BackendClient,
    state: Optional[FSMContext],
) -> None:
    """
    Handler for /translator

    :param message: Message from telegram.
    """

    await state.clear()  # type: ignore[union-attr]

    user = await auth_user(
        message=message,
        backend_client=backend_client,
        tg_id=str(message.from_user.id),
        state=state,
    )

    if user:
        await message.answer(
            text=_(
                "Edit your text and I helped translate it!\n",
            ),
        )
