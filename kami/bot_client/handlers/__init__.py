"""Bot handlers"""

from aiogram import Dispatcher

from kami.bot_client.handlers.dialog import router as dialogue_router
from kami.bot_client.handlers.lang_test import router as lang_test_router
from kami.bot_client.handlers.onboarding import router as onboarding_router
from kami.bot_client.handlers.register import router as register_router
from kami.bot_client.handlers.start import router as start_router
from kami.bot_client.handlers.translator import router as translator_router


def setup_routers(dispatcher: Dispatcher) -> None:
    """
    Add routers in dispatcher.

    :param dispatcher: Main dispatcher of routers.
    """
    dispatcher.include_router(start_router)
    dispatcher.include_router(lang_test_router)
    dispatcher.include_router(register_router)
    dispatcher.include_router(onboarding_router)
    dispatcher.include_router(dialogue_router)
    dispatcher.include_router(translator_router)
