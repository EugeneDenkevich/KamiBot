from typing import List, Optional

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from kami.backend.domain.user.exceptions import UserNotFoundError
from kami.backend.domain.user.models import User
from kami.backend.infra.db.tables.user import UserTable
from kami.backend.repos.user.converters import user_db_to_entity


class UserRepo():
    """Repository for User entity"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_user(self, user: User) -> None:
        """
        Save user in DB.

        :param user: User.
        """

        query = (
            insert(UserTable)
            .values(
                id=user.id,
                tg_id=user.tg_id,
                username=user.username,
                fio=user.fio,
                phone=user.phone,
                active=user.active,
                onboarded=user.onboarded,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
        )

        await self.session.execute(query)
        await self.session.commit()

    async def get_user_or_none(self, tg_id: str) -> Optional[User]:
        """
        Get User from DB or None.

        :param tg_id: User telegram ID.
        """

        query = select(UserTable).where(UserTable.tg_id == tg_id)

        result = await self.session.execute(query)
        user = result.scalar()

        if not user:
            return None

        return user_db_to_entity(user=user)

    async def get_user(self, tg_id: str) -> User:
        """
        Get User from DB.

        :param tg_id: User telegram ID.
        """

        user = await self.get_user_or_none(tg_id)

        if not user:
            raise UserNotFoundError()

        return user

    async def update_user(self, user: User) -> None:
        """
        Update user in DB.

        :param user: User.
        """

        query = (
            update(UserTable)
            .where(UserTable.tg_id == user.tg_id)
            .values(
                id=user.id,
                tg_id=user.tg_id,
                username=user.username,
                fio=user.fio,
                phone=user.phone,
                active=user.active,
                onboarded=user.onboarded,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
        )

        await self.session.execute(query)
        await self.session.commit()

    async def get_users(self, tg_ids: List[str]) -> List[User]:
        """
        Get Users from DB
        
        :param tg_ids: Users telegram ids list.
        """

        query = select(UserTable)

        if tg_ids:
            query = query.where(UserTable.tg_id.in_(tg_ids))

        result = await self.session.execute(query)
        users = result.scalars()

        return [user_db_to_entity(user=user) for user in users]
