from enum import StrEnum


class DialoguePromtEnum(StrEnum):
    """Language test prompts"""

    START_DIALOG = "start_dialog"
    CONTINUE_DIALOG = "continue_dialog"
    EXCEPTIONS_DIALOG = "exceptions_dialog"
