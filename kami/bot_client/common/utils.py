import asyncio
from typing import BinaryIO

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from kami.backend.domain.lang_test.models import QuestT
from kami.bot_client.states.dialogue import DialogFSM


def parse_question(
    current_question: QuestT,
) -> str:

    question = f"{current_question['question']}\n"
    options = current_question["options"]
    for leeter, option in options.items():  # type: ignore[union-attr]
        question += f"\n{leeter}). {option}"
    return question


async def get_voice_reply(message: Message) -> bytes:
    """
    Get voice reply from message.

    :param message: Message from telegram.
    """

    voice_file = await message.bot.get_file(  # type: ignore[union-attr]
        file_id=message.voice.file_id,  # type: ignore[union-attr]
    )
    voice_binary: BinaryIO = await message.bot.download(   # type: ignore[assignment, union-attr]
        file=voice_file,
    )

    return voice_binary.read()


async def wait_for_answer(
    awaiting_time: int,
    message: Message,
    state: FSMContext,
    text: str,
) -> None:
    """
    Wait if user is not responsing.

    :param message: Message.
    :param await_for_answer: How much awaiting in sec.
    :param state: FSM context.
    """

    async def notify_if_no_response() -> None:
        await asyncio.sleep(awaiting_time)

        if await state.get_state() == DialogFSM.conversation.state:
            await message.answer(text)
            await state.clear()

    asyncio.create_task(notify_if_no_response())
