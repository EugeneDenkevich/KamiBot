from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from kami.backend.domain.user.exceptions import UserNotFoundError
from kami.backend.presentation.client import BackendClient
from kami.bot_client.keyboards.main_menu import build_main_menu_markup
from kami.bot_client.keyboards.onboarding import build_onboarding_step_markup
from kami.bot_client.keyboards.share_contact import build_share_contact_markup
from kami.bot_client.states.register import RegisterFSM

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
    """

    await state.clear()

    tg_id = str(message.from_user.id)  # type: ignore[union-attr]

    try:
        user = await backend_client.get_user(tg_id=tg_id)
    except UserNotFoundError:
        await state.set_state(RegisterFSM.share_contact)

        await message.answer(
            text=_("Hello. Please, share your contact"),
            reply_markup=build_share_contact_markup(),
        )
    else:
        if not user.active:
            await message.answer(
                text=_(
                    "Hello. Unfortunately, your subscription is not activated.\n"
                    "To continue, go to the <b>Menu</b> and select <b>Payment</b> "
                    "or pay now by clicking <b>Activate subscribtion</b>.\n"
                    "After payment, the administrator will confirm your account "
                    "activation and you can press /start again",
                ),
                parse_mode=ParseMode.HTML,
            )
        else:
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
