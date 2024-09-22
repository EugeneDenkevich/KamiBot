from enum import StrEnum
from typing import List


class RateEnum(StrEnum):
    """User rates"""

    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"

    @classmethod
    def get_values(cls) -> List[str]:
        return [rate.value for rate in cls]


class LangTestPromtEnum(StrEnum):
    """Language test prompts"""

    LANG_TEST = "lang_test"
    LANG_TEST_RESULT = "lang_test_result"
