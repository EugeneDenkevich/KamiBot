from datetime import datetime
from typing import Optional
from uuid import uuid4

from kami.backend.domain.dialog.models import ContextT, Dialog


class DialogService():
    """Service for Dialog entity"""

    def create_dialog(
            self,
            tg_id: str,
            topic: str,
    ) -> Dialog:

        return Dialog(
            id=uuid4(),
            tg_id=tg_id,
            topic=topic,
            context=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def update_dialog(
        self,
        dialog: Dialog,
        topic: Optional[str] = None,
        context: Optional[ContextT] = None,
    ) -> None:
        if topic is not None:
            dialog.topic = topic
        if context is not None:
            dialog.context = context
        dialog.updated_at=datetime.now()


def build_dialog_service() -> DialogService:
    return DialogService()
