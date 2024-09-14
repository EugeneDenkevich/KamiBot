from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from kami.backend.domain.dialog.models import Dialog
from kami.backend.infra.db import DialogTable


class DialogRepo():
    """Repository for Dialog entity"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_dialog(self, dialog: Dialog) -> None:
        """
        Save dialog in DB.

        :param id: Dialog id.
        :param topic: Dialog id.
        """

        query = (
            insert(DialogTable)
            .values(
                id=dialog.id,
                topic=dialog.topic,
            )
        )
        await self.session.execute(query)
        await self.session.commit()
