from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Audit(BaseModel):
    """Model of Audit entity"""

    id: UUID
    tg_id: str
    action: str
    module: str
    created_at: datetime
