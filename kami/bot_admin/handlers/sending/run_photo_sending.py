from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.input_file import BufferedInputFile

from kami.backend.domain.audit.enums import ActionEnum, ModuleEnum
from kami.backend.presentation.client import BackendClient
from kami.bot_admin.common.multiple_sending import send_photo
from kami.bot_admin.enums.template_type import TemplateTypeEnum
from kami.bot_admin.keyboards.sending_confirming import (
    TextSendindCD,
    build_sending_confirming_markup,
)
from kami.bot_admin.states.sending import SendTemplateFSM
from kami.common import get_bytes

router = Router()


@router.message(
    SendTemplateFSM.template,
    F.photo,
)
async def handle_photo_sending(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Handler for photo sending.

    :param message: Message from telegram.
    :param state: FSM state.
    """

    await message.answer(text="Check if everything is okay 👇")

    photo = await get_bytes(
        file_id=message.photo[-1].file_id,  # type: ignore[index]
        bot=message.bot,
    )
    await state.update_data(photo=photo)
    await state.update_data(caption=message.caption)

    await message.bot.send_photo(
        chat_id=message.from_user.id,
        photo=BufferedInputFile(file=photo, filename="image.jpg"),
        caption=message.caption,
        parse_mode="html",
    )

    await message.answer(
        text='If everything is okay, press "Send"',
        reply_markup=build_sending_confirming_markup(
            template_type=TemplateTypeEnum.PHOTO,
        ),
    )


@router.callback_query(
    SendTemplateFSM.template,
    TextSendindCD.filter(F.template_type == TemplateTypeEnum.PHOTO),
)
async def handle_run_photo_sending(
    callback_query: CallbackQuery,
    state: FSMContext,
    bot_client: Bot,
    backend_client: BackendClient,
) -> None:
    """
    Handler for photo sending running.

    :param message: Message from telegram.
    :param state: FSM state.
    """

    await callback_query.answer()

    data = await state.get_data()
    users_tg_ids = data.get("users_tg_ids")
    photo = data.get("photo")
    caption = data.get("caption")

    if not users_tg_ids or not photo:
        return

    await callback_query.message.answer(text="Sending was started...")

    for user_tg_id in users_tg_ids:
        await send_photo(
            bot=bot_client,
            chat_id=int(user_tg_id),
            photo=BufferedInputFile(file=photo, filename="image.jpg"),
            caption=caption,
        )

        await backend_client.log_to_db(
            tg_id=user_tg_id,
            module=ModuleEnum.SENDING,
            action=ActionEnum.BOT_SENT,
        )

    await callback_query.message.answer(
        text="Sending was finished\n/start\n/getid\n/sending\n",
    )

    await state.clear()
