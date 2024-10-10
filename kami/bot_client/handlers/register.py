from aiogram import Bot, F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _

from kami.backend.domain.audit.enums import ActionEnum, ModuleEnum
from kami.backend.presentation.client import BackendClient
from kami.bot_client.enums.stickers import StickersEnum
from kami.bot_client.keyboards.add_user import build_add_user_markup
from kami.settings import Settings

router = Router()


@router.message(F.contact)
async def handle_register(
    message: Message,
    bot_admin: Bot,
    settings: Settings,
    state: FSMContext,
    backend_client: BackendClient,
) -> None:

    await state.clear()

    tg_id = str(message.from_user.id)  # type: ignore[union-attr]

    await backend_client.log_to_db(
        tg_id=tg_id,
        module=ModuleEnum.AUTH,
        action=ActionEnum.SHARE_CONTACT,
    )

    fio = (
        f"{message.from_user.first_name} "   # type: ignore[union-attr]
        f"{message.from_user.last_name}"   # type: ignore[union-attr]
    )
    username = message.from_user.username  # type: ignore[union-attr]

    await message.answer_sticker(StickersEnum.KAMILA_START_IF_NOT_PAID)
    await message.answer(
        text=_(
            "The administrator will\n"
            "check your data.\n"
            "If your subscription is paid, you will receive "
            "a notification and all the functions of the bot will work",
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove(),
    )

    await bot_admin.send_message(
        chat_id=settings.admin_id,
        text=(
            "User wanted to be added:\n"
            "Tg id: {tg_id}\n"
            "Username: {username}\n"
            "Fullname: {fio}"
        )
        .format(tg_id=tg_id, fio=fio, username=username),
        reply_markup=build_add_user_markup(
            tg_id=tg_id,
            phone=message.contact.phone_number,  # type: ignore[union-attr]
        ),
        parse_mode=ParseMode.HTML,
    )
