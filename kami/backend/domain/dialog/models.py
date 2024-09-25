from datetime import datetime
from typing import Dict, List
from uuid import UUID

from pydantic import BaseModel

ContextT = List[Dict[str, str]]
class Dialog(BaseModel):
    """Modle of dialog entity"""

    id: UUID
    tg_id: str
    topic: str
    context: ContextT
    created_at: datetime
    updated_at: datetime
