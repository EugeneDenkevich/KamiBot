from typing import Union
from uuid import UUID

from pydantic import BaseModel


class AI(BaseModel):
    """AI"""

    id: UUID
    gpt_api_key: str
    elevenlabs_api_key: str


class Answer(BaseModel):
    """Answer from AI"""

    content: Union[str, bytes]
    gpt_chat_id: str
