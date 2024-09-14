from aiogram.fsm.state import State, StatesGroup


class FSMForm(StatesGroup):
    """Example form for stages in FSM"""

    first_stage = State()  # First stage description
    second_stage = State()  # Second stage description
