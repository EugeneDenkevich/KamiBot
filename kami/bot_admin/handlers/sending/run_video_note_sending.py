from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.input_file import BufferedInputFile

from kami.bot_admin.common.multiple_sending import send_video_note
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
    F.video_note,
)
async def handle_video_note_sending(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Handler for video_note sending.

    :param message: Message from telegram.
    :param state: FSM state.
    """

    await message.answer(text="Check if everything is okay 👇")

    video_note = await get_bytes(file_id=message.video_note.file_id, bot=message.bot)
    await state.update_data(video_note=video_note)

    await message.bot.send_video_note(
        chat_id=message.from_user.id,
        video_note=BufferedInputFile(file=video_note, filename="video.mp4"),
    )

    await message.answer(
        text='If everything is okay, press "Send"',
        reply_markup=build_sending_confirming_markup(
            template_type=TemplateTypeEnum.VIDEO_NOTE,
        ),
    )


@router.callback_query(
    SendTemplateFSM.template,
    TextSendindCD.filter(F.template_type == TemplateTypeEnum.VIDEO_NOTE),
)
async def handle_run_video_note_sending(
    callback_query: CallbackQuery,
    state: FSMContext,
    bot_client: Bot,
) -> None:
    """
    Handler for video_note sending running.

    :param message: Message from telegram.
    :param state: FSM state.
    """

    await callback_query.answer()

    data = await state.get_data()
    users_tg_ids = data.get("users_tg_ids")
    video_note = data.get("video_note")

    if not users_tg_ids or not video_note:
        return

    await callback_query.message.answer(text="Sending was started...")

    for user_tg_id in users_tg_ids:
        await send_video_note(
            bot=bot_client,
            chat_id=int(user_tg_id),
            video_note=BufferedInputFile(file=video_note, filename="video.mp4"),
        )

    await callback_query.message.answer(
        text="Sending was finished\n/start\n/getid\n/sending\n",
    )

    await state.clear()
