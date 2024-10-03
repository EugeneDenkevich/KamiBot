from typing import Optional

from kami.backend.domain.user.exceptions import UserAlreadyExistsError
from kami.backend.domain.user.models import User
from kami.backend.domain.user.services import UserService
from kami.backend.repos.user.repo import UserRepo


class CreateUserUseCase():
    """Use case of user creation"""

    def __init__(
            self,
            user_service: UserService,
            user_repo: UserRepo,
    ) -> None:
        self.user_service = user_service
        self.user_repo = user_repo

    async def __call__(
        self,
        tg_id: str,
        fio: str,
        phone: str,
        username: Optional[str] = None,
    ) -> User:
        """
        Create User.

        :param tg_id: User telegram ID.
        :param fio: User fio.
        :param phone: User phone number.
        :param username: User username.
        :return: User.
        """

        user = await self.user_repo.get_user_or_none(tg_id=tg_id)

        if user:
            raise UserAlreadyExistsError()

        user = self.user_service.create_user(
            tg_id=tg_id,
            fio=fio,
            phone=phone,
            username=username,
        )

        await self.user_repo.save_user(user)

        return user


class GetUserUseCase:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def __call__(self, tg_id: str) -> User:
        """
        Get user by telegram id.

        :param tg_id: User telegram id.
        :return: User.
        """

        return await self.user_repo.get_user(tg_id=tg_id)


class UpdateUserUseCase():
    """Use case for updation user"""

    def __init__(
            self,
            user_service: UserService,
            user_repo: UserRepo,
    ) -> None:
        self.user_service = user_service
        self.user_repo = user_repo

    async def __call__(
        self,
        tg_id: str,
        fio: Optional[str] = None,
        phone: Optional[str] = None,
        username: Optional[str] = None,
        active: Optional[bool] = None,
        onboarded: Optional[bool] = None,
    ) -> User:
        """
        Update User.

        :param tg_id: User telegram ID.
        :param fio: User fio.
        :param phone: User phone number.
        :param username: User username.
        :param active: User active status.
        :param onboarded: User onboarded status.
        :return: User.
        """

        user = await self.user_repo.get_user(tg_id=tg_id)

        self.user_service.update_user(
            user=user,
            username=username,
            fio=fio,
            phone=phone,
            active=active,
            onboarded=onboarded,
        )

        await self.user_repo.update_user(user)

        return user
