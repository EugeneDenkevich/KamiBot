from aiogram.fsm.state import State, StatesGroup


class DialogFSM(StatesGroup):
    """FSM for Dialogue"""

    conversation = State()
    """State when user has conversation"""

    my_topic = State()
    """State when user select individual topic"""
