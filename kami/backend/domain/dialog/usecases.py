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

    async def __call__(self, topic: str) -> Dialog:
        """
        Create Dialog.

        :param id: Dialog id.
        :param topic: Dialog id.
        :return: Dialog.
        """

        dialog = self.dialog_service.create_dialog(topic=topic)

        await self.dialog_repo.save_dialog(dialog)

        return dialog
