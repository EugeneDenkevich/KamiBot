from aiogram.fsm.state import State, StatesGroup


class LangTestFSM(StatesGroup):
    """FSM for language test"""

    lang_testing = State()
    """State when user answering the question on test"""
