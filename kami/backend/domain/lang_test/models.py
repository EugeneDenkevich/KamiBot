from datetime import datetime
from typing import Dict, List, Union
from uuid import UUID

from pydantic import BaseModel, Field

QuestT = Dict[str, Union[str, Dict[str, str]]]


class LangTest(BaseModel):
    """Model of LangTest entity"""

    id: UUID
    tg_id: str
    questions: List[QuestT]
    current_question: QuestT = Field(default_factory=dict)
    replies: List[QuestT] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
