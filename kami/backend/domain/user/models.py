from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    """Model of User entity"""

    id: UUID
    tg_id: str
    fio: str
    phone: str
    active: bool
    username: Optional[str] = None
    onboarded: Optional[bool] = False
    created_at: datetime
    updated_at: datetime
