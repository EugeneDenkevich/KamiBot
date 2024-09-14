from uuid import UUID

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from kami.backend.infra.db.base import Base


class DialogTable(Base):
    """Table for Dialog entity."""

    __tablename__ = "dialogs"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    """ID."""

    topic: Mapped[UUID] = mapped_column(String, nullable=False)
    """Topic of current dialog"""
