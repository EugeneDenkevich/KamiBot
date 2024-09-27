from datetime import datetime
from typing import Optional
from uuid import uuid4

from kami.backend.domain.user.models import User


class UserService():
    """Service for User entity"""

    def create_user(
        self,
        tg_id: str,
        fio: str,
        phone: str,
        username: Optional[str] = None,
    ) -> User:
        return User(
            id=uuid4(),
            tg_id=tg_id,
            username=username,
            fio=fio,
            phone=phone,
            active=True,
            onboarded=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def update_user(
        self,
        user: User,
        fio: Optional[str] = None,
        phone: Optional[str] = None,
        username: Optional[str] = None,
        active: Optional[bool] = None,
        onboarded: Optional[bool] = None,
    ) -> None:
        """
        Update user.

        :param user: User.
        :param fio: User fio.
        :param phone: User phone number.
        :param username: User username.
        :param active: User active status.
        :param blocked: User block status.
        """

        if username is not None:
            user.username = username
        if fio is not None:
            user.fio = fio
        if phone is not None:
            user.phone = phone
        if active is not None:
            user.active = active
        if onboarded is not None:
            user.onboarded = onboarded
        user.updated_at = datetime.now()


def build_user_service() -> UserService:
    return UserService()
