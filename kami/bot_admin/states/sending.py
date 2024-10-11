from aiogram.fsm.state import State, StatesGroup


class SendTemplateFSM(StatesGroup):
    """Example form for stages in FSM"""

    template = State()
    """Wait for template from admin for sending"""

    users_ids = State()
    """Wait for users ids"""
