from uuid import UUID

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from kami.backend.infra.db.base import Base


class AITable(Base):
    """Table for AI entity."""

    __tablename__ = "ai"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    """ID."""

    gpt_api_key: Mapped[UUID] = mapped_column(String, nullable=False)
    """ChatGPT api key"""

    elevenlabs_api_key: Mapped[UUID] = mapped_column(String, nullable=False)
    """ElevenLabs api key"""
