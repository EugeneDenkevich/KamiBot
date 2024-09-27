from aiogram import Bot, F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _

from kami.bot_client.keyboards.add_user import build_add_user_markup
from kami.settings import Settings

router = Router()


@router.message(F.contact)
async def handle_register(
    message: Message,
    bot_admin: Bot,
    settings: Settings,
    state: FSMContext,
) -> None:

    await state.clear()

    tg_id = str(message.from_user.id)   # type: ignore[union-attr]
    fio = (
        f"{message.from_user.first_name} "   # type: ignore[union-attr]
        f"{message.from_user.last_name}"   # type: ignore[union-attr]
    )
    username = message.from_user.username  # type: ignore[union-attr]

    await message.answer(
        text=_(
            "We notified admin and you will get "
            "the <b>registration form</b> soon.\n"
            "After this press /start again.",
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove(),
    )

    await bot_admin.send_message(
        chat_id=settings.admin_id,
        text=_(
                "User wanted to be added:\n"
                "<b>Tg id:</b> {tg_id}\n"
                "<b>Username:</b> {username}\n"
                "<b>Fullname:</b> {fio}",
        )
        .format(tg_id=tg_id, fio=fio, username=username),
        reply_markup=build_add_user_markup(
            tg_id=tg_id,
            phone=message.contact.phone_number,  # type: ignore[union-attr]
        ),
        parse_mode=ParseMode.HTML,
    )
