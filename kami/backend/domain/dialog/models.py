from uuid import UUID

from pydantic import BaseModel


class Dialog(BaseModel):
    """Modle of dialog entity"""

    id: UUID
    topic: str
