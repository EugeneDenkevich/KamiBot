from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from kami.backend.domain.audit.enums import ActionEnum, ModuleEnum
from kami.backend.presentation.client import BackendClient
from kami.bot_client.common.utils import auth_user
from kami.bot_client.keyboards.main_menu import build_main_menu_markup
from kami.bot_client.keyboards.onboarding import build_onboarding_step_markup

router = Router()


@router.message(Command(commands=["start"]))
async def handle_start(
    message: Message,
    backend_client: BackendClient,
    state: FSMContext,
) -> None:
    """
    Handler for /start command.

    :param message: Message from telegram.
    :param backend_client: Get functions from BackendClient.
    :param state: FSM state.
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
            module=ModuleEnum.START,
            action=ActionEnum.USER_PUSH,
        )

        await message.answer(
            text=_(
                "Hello, I'm Kami, your online English teacher!",
            ),
            reply_markup=(
                build_main_menu_markup()
                if user.onboarded
                else
                build_onboarding_step_markup(
                    text=_("Hello, Kami 👋"),
                    step=1,
                )
            ),
        )
