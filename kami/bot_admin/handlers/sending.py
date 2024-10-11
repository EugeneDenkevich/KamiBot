from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from kami.bot_admin.enums.sending_method import SendingMetdhodEnum
from kami.bot_admin.keyboards.sending_confirming import build_sending_confirming_markup
from kami.bot_admin.keyboards.sending_methods import (
    SendingMethodCD,
    build_sending_methods_markup,
)
from kami.bot_admin.states.sending import SendTemplateFSM

router = Router()


@router.message(Command(commands=["sending"]))
async def handle_start(
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
    SendingMethodCD.filter(F.sending_method == SendingMetdhodEnum.ALL),
)
async def handle_get_template(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    """
    Handler for sending to all method.

    :param callback_query: Callback query from telegram.
    :param state: FSM state.
    """

    await callback_query.answer()
    await callback_query.message.answer(text="Send text or picture with caption")

    await state.set_state(SendTemplateFSM.template)


@router.message(
    SendTemplateFSM.template,
    F.text,
)
async def handle_check_sending(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Handler for check sending.

    :param message: Message from telegram.
    :param state: FSM state.
    """

    await message.answer(text="Check if everything is okay 👇")

    await message.answer(text=message)

    await message.answer(
        text='If everything is okay, press "Send"',
        reply_markup=build_sending_confirming_markup(),
    )

    await state.clear()
