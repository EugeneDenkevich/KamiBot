from aiogram.fsm.state import State, StatesGroup


class TranslatorFSM(StatesGroup):
    """FSM for translator"""

    direction = State()
    """State when user chooses the translation direction"""

    translating = State()
    """State when user provides text or voice for translation"""
