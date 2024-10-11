from typing import Union

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from kami.backend.presentation.client import BackendClient
from kami.bot_admin.enums.sending_method import SendingMetdhodEnum
from kami.bot_admin.keyboards.sending_methods import (
    SendingMethodCD,
    build_sending_methods_markup,
)
from kami.bot_admin.states.sending import SendTemplateFSM

router = Router()


@router.message(Command(commands=["sending"]))
async def handle_sending(
    message: Message,
) -> None:
    """
    Handler for /sending command.

    :param message: Message from telegram.
    :param is_admin: Message from telegram.
    """

    await message.answer(
        text="Select the sending method",
        reply_markup=build_sending_methods_markup(),
    )


@router.callback_query(
    SendingMethodCD.filter(F.sending_method == SendingMetdhodEnum.CUSTOM),
)
async def handle_get_user_ids(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    """
    Handler for sending to all method.

    :param callback_query: Callback query from telegram.
    :param state: FSM state.
    """

    await callback_query.answer()
    await callback_query.message.answer(text="Send users ids")

    await state.set_state(SendTemplateFSM.users_ids)


@router.message(SendTemplateFSM.users_ids)
@router.callback_query(
    SendingMethodCD.filter(F.sending_method == SendingMetdhodEnum.ALL),
)
async def handle_get_template(
    mescall: Union[Message, CallbackQuery],
    state: FSMContext,
    backend_client: BackendClient,
) -> None:
    """
    Handler for sending to all method.

    :param callback_query: Callback query from telegram.
    :param state: FSM state.
    """

    if isinstance(mescall, CallbackQuery):
        await mescall.answer()

        message = mescall.message

        users = await backend_client.get_users()
        await state.update_data(users_tg_ids=[user.tg_id for user in users])
    else:
        message = mescall

        users_tg_ids = message.text.split("\n")
        await state.update_data(users_tg_ids=users_tg_ids)

    await message.answer(text="Send one of:\n- Text\n- Picture\n- Video\n- Video note")
    await state.set_state(SendTemplateFSM.template)
