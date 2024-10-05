from typing import Optional

from kami.backend.domain.dialog.models import Dialog
from kami.backend.domain.dialog.services import DialogService
from kami.backend.repos.dialog.repo import DialogRepo


class CreateDialogUseCase():
    """Use case of dialog creation"""

    def __init__(
        self,
        dialog_service: DialogService,
        dialog_repo: DialogRepo,
    ) -> None:
        self.dialog_service = dialog_service
        self.dialog_repo = dialog_repo

    async def __call__(
        self,
        tg_id: str,
        topic: str,
    ) -> Dialog:
        """
        Create Dialog.

        :param id: Dialog id.
        :param topic: Dialog id.
        :return: Dialog.
        """

        dialog = self.dialog_service.create_dialog(
            tg_id=tg_id,
            topic=topic,
        )

        await self.dialog_repo.save_dialog(dialog)

        return dialog

class GetDialogUseCase():
    """Use case of geting dialogue"""

    def __init__(
        self,
        dialog_repo: DialogRepo,
    ) -> None:
        self.dialog_repo = dialog_repo

    async def __call__(
            self,
            tg_id: str,
    ) -> Dialog:
        """
        Get Dialog.

        :param id: Dialog id.
        :param topic: Dialog id.
        :return: Dialog.
        """

        return await self.dialog_repo.get_dialog(tg_id=tg_id)


class GetDialogOrNoneUseCase():
    """Use case of geting dialogue or None if not exists"""

    def __init__(
        self,
        dialog_repo: DialogRepo,
    ) -> None:
        self.dialog_repo = dialog_repo

    async def __call__(
        self,
        dialog_id: str,
    ) -> Optional[Dialog]:
        """
        Get Dialog.

        :param dialog_id: Dialog id.
        :return: Dialog or None.
        """

        return await self.dialog_repo.get_dialog_by_id_or_none(dialog_id=dialog_id)
