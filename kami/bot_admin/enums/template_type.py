from enum import StrEnum
from typing import List


class TemplateTypeEnum(StrEnum):
    """Enum for template type"""

    TEXT = "text"
    PHOTO = "photo"
    VIDEO = "video"
    VIDEO_NOTE = "video_note"

    @classmethod
    def get_values(cls) -> List[str]:
        return [sending_method.value for sending_method in cls]
