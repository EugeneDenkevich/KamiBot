"""Bot handlers"""

from aiogram import Dispatcher

from kami.bot_admin.handlers.add_user import router as add_user_router
from kami.bot_admin.handlers.getid import router as getid_router
from kami.bot_admin.handlers.start import router as start_router


def setup_routers(dispatcher: Dispatcher) -> None:
    """
    Add routers in dispatcher.

    :param dispatcher: Main dispatcher of routers.
    """
    dispatcher.include_router(start_router)
    dispatcher.include_router(getid_router)
    dispatcher.include_router(add_user_router)
