from aiogram import Router
from aiogram.types import CallbackQuery

from kami.backend.domain.user.exceptions import UserAlreadyExestsError
from kami.backend.presentation.client import BackendClient
from kami.bot_admin.keyboards.add_user import AddUserCallbackData

router = Router()


@router.callback_query(AddUserCallbackData.filter())
async def handle_add_user(
    callback_query: CallbackQuery,
    callback_data: AddUserCallbackData,
    backend_client: BackendClient,
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
    except UserAlreadyExestsError:
        await callback_query.message.answer(  # type: ignore[union-attr]
            text="User already added.",
        )
    else:
        await callback_query.message.answer(  # type: ignore[union-attr]
            text="User was added.",
        )
