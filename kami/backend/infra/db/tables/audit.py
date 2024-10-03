from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Enum, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from kami.backend.domain.audit.enums import ActionEnum, ModuleEnum
from kami.backend.infra.db.base import Base


class AuditTable(Base):
    """Table for Audit entity."""

    __tablename__ = "audit"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    """ID."""

    tg_id: Mapped[str] = mapped_column(String, nullable=False)
    """User telegram ID of current user"""

    module: Mapped[ModuleEnum] = mapped_column(
        Enum(ModuleEnum, name="module_enum"),
        nullable=False,
    )
    """Module"""

    action: Mapped[ActionEnum] = mapped_column(
        Enum(ActionEnum, name="action_enum"),
        nullable=False,
    )
    """User action"""

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    """Creation date"""
