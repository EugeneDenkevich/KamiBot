from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import JSON, DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from kami.backend.domain.lang_test.models import QuestT
from kami.backend.infra.db.base import Base


class LangTestTable(Base):
    """Table for LangTest entity."""

    __tablename__ = "lang_tests"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    """ID."""

    tg_id: Mapped[str] = mapped_column(String, nullable=False)
    """Telegram id"""

    questions: Mapped[List[QuestT]] = mapped_column(JSON, nullable=False)
    """Questions for user"""

    current_question: Mapped[QuestT] = mapped_column(JSON, nullable=True)
    """Current question"""

    replies: Mapped[List[QuestT]] = mapped_column(JSON, nullable=True)
    """User replies"""

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    """Date and time of creation"""

    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    """Date and time of updating"""
