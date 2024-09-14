from uuid import uuid4

from kami.backend.domain.dialog.models import Dialog


class DialogService():
    """Service for Dialog entity"""

    def create_dialog(self, topic: str) -> Dialog:
        return Dialog(
            id=uuid4(),
            topic=topic,
        )


def build_dialog_service() -> DialogService:
    return DialogService()
