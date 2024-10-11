"""Bot handlers"""

from aiogram import Dispatcher

from kami.bot_admin.handlers.add_user import router as add_user_router
from kami.bot_admin.handlers.getid import router as getid_router
from kami.bot_admin.handlers.sending import (
    photo_sending_router,
    sending_start_router,
    text_sending_router,
    video_note_sending_router,
    video_sending_router,
)
from kami.bot_admin.handlers.start import router as start_router


def setup_routers(dispatcher: Dispatcher) -> None:
    """
    Add routers in dispatcher.

    :param dispatcher: Main dispatcher of routers.
    """

    dispatcher.include_router(start_router)
    dispatcher.include_router(getid_router)
    dispatcher.include_router(add_user_router)
    dispatcher.include_router(sending_start_router)
    dispatcher.include_router(text_sending_router)
    dispatcher.include_router(photo_sending_router)
    dispatcher.include_router(video_sending_router)
    dispatcher.include_router(video_note_sending_router)
