from kami.backend.domain.dialog.models import Dialog
from kami.backend.presentation.ucf import UseCaseFactory


class BackendClient():
    """Base backend interface implementation"""

    def __init__(self, ucf: UseCaseFactory):
        self.ucf = ucf

    def get_example(self) -> str:
        return "Btw, hello from backend client!"

    async def create_dialog(
        self,
        topic: str,
    ) -> Dialog:
        async with self.ucf.create_dialog() as create_dialog:
            return await create_dialog(topic=topic)
