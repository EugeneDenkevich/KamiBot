from aiogram import Bot, Router
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from kami.backend.domain.user.exceptions import UserAlreadyExistsError
from kami.backend.presentation.client import BackendClient
from kami.bot_admin.keyboards.add_user import AddUserCallbackData
from kami.bot_client.enums.stickers import StickersEnum

router = Router()


@router.callback_query(AddUserCallbackData.filter())
async def handle_add_user(
    callback_query: CallbackQuery,
    callback_data: AddUserCallbackData,
    backend_client: BackendClient,
    bot_client: Bot,
) -> None:
    """
    Handler for add user callback.

    :param callback_query: Callbacke query for user add.
    """

    await callback_query.answer()

    fio = (
        callback_query.message.text  # type: ignore[union-attr]
        .split("\n")[3]
        .strip("Fullname: ")
    )

    username = (
        callback_query.message.text  # type: ignore[union-attr]
        .split("\n")[2]
        .strip("Username: ")
    )

    try:
        await backend_client.create_user(
            tg_id=callback_data.tg_id,
            fio=fio,
            phone=callback_data.phone,
            username=username,
        )

        await bot_client.send_sticker(
            chat_id=callback_data.tg_id,
            sticker=StickersEnum.KAMILA_REGISTER_COMPLETE,
        )
        await bot_client.send_message(  # type: ignore[union-attr]
            chat_id=callback_data.tg_id,
            text=_(
                "Hello, beautiful soul! \n"
                "Your account is activated. Thank you very much for your trust."
                "Click here to start learning 👉🏻  /start",
            ),
        )
    except UserAlreadyExistsError:
        await callback_query.message.answer(  # type: ignore[union-attr]
            text="User already added.",
        )
    else:
        await callback_query.message.answer(  # type: ignore[union-attr]
            text="User was added.",
        )
