from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from kami.bot_admin.common.multiple_sending import send_text
from kami.bot_admin.enums.template_type import TemplateTypeEnum
from kami.bot_admin.keyboards.sending_confirming import (
    TextSendindCD,
    build_sending_confirming_markup,
)
from kami.bot_admin.states.sending import SendTemplateFSM

router = Router()


@router.message(
    SendTemplateFSM.template,
    F.text,
)
async def handle_text_sending(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Handler for text sending.

    :param message: Message from telegram.
    :param state: FSM state.
    """

    await message.answer(text="Check if everything is okay 👇")

    await message.answer(text=message.text)
    await state.update_data({"text": message.text})

    await message.answer(
        text='If everything is okay, press "Send"',
        reply_markup=build_sending_confirming_markup(
            template_type=TemplateTypeEnum.TEXT,
        ),
    )


@router.callback_query(
    SendTemplateFSM.template,
    TextSendindCD.filter(F.template_type == TemplateTypeEnum.TEXT),
)
async def handle_run_text_sending(
    callback_query: CallbackQuery,
    state: FSMContext,
    bot_client: Bot,
) -> None:
    """
    Handler for text sending running.

    :param message: Message from telegram.
    :param state: FSM state.
    """

    await callback_query.answer()

    data = await state.get_data()
    users_tg_ids = data.get("users_tg_ids")
    text = data.get("text")

    if not users_tg_ids or not text:
        return

    await callback_query.message.answer(text="Sending was started...")

    for user_tg_id in users_tg_ids:
        await send_text(
            bot=bot_client,
            chat_id=int(user_tg_id),
            text=text,
        )

    await callback_query.message.answer(
        text="Sending was finished\n/start\n/getid\n/sending\n",
    )

    await state.clear()
