from enum import StrEnum


class ModuleEnum(StrEnum):
    START = "Start"
    AUTH = "Authorisation"
    ONBOARDING = "Onboarding"
    MENU = "Menu"
    TRANSLATE = "Translator"
    DIALOGS = "Dialog"
    LANG_TEST = "Language test"
    SENDING = "Sending"


class ActionEnum(StrEnum):
    BOT_SENT = "Bot sent message"
    USER_SENT = "User sent message"
    USER_PUSH = "User push button"
    SHARE_CONTACT = "User sharing his contact"
