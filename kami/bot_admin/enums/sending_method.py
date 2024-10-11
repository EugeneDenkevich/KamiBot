from enum import StrEnum
from typing import List


class SendingMetdhodEnum(StrEnum):
    """Enum for sending methods"""

    ALL = "Send all"
    CUSTOM = "Send by ids"

    @classmethod
    def get_values(cls) -> List[str]:
        return [sending_method.value for sending_method in cls]
