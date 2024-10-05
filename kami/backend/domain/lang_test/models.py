from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

QuestT = Dict[str, str]


class LangTest(BaseModel):
    """Model of LangTest entity"""

    id: UUID
    tg_id: str
    questions: List[str]
    current_question: Optional[str] = None
    replies: List[QuestT] = []
    created_at: datetime
    updated_at: datetime
