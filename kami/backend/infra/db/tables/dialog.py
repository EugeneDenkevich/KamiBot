from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from kami.backend.domain.dialog.models import ContextT
from kami.backend.infra.db.base import Base


class DialogTable(Base):
    """Table for Dialog entity."""

    __tablename__ = "dialogs"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    """ID."""

    tg_id: Mapped[str] = mapped_column(String, primary_key=True)
    """Telegram ID."""

    topic: Mapped[str] = mapped_column(String, nullable=False)
    """Topic of current dialog"""

    context: Mapped[ContextT] = mapped_column(JSON, nullable=False)
    """Context of current dialog"""

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    """Date and time of creation"""

    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    """Date and time of updating"""
