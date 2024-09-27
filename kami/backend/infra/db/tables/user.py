from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from kami.backend.infra.db.base import Base


class UserTable(Base):
    """Table for User entity."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    """ID."""

    tg_id: Mapped[str] = mapped_column(String, nullable=False)
    """Telegram ID of current user"""

    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    """Name of current user"""

    fio: Mapped[str] = mapped_column(String, nullable=False)
    """Name of current user"""

    phone: Mapped[str] = mapped_column(String, nullable=False)
    """Phone number of current user"""

    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    """Subscribe activity of current user"""

    onboarded: Mapped[bool] = mapped_column(Boolean, nullable=False)
    """Onboarded status of current user"""

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    """Date and time of creation"""

    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    """Date and time of updating"""
