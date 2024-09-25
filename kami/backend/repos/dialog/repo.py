from typing import Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from kami.backend.domain.dialog.exceptions import DialogueNotFoundError
from kami.backend.domain.dialog.models import Dialog
from kami.backend.infra.db import DialogTable
from kami.backend.repos.dialog.converters import dialogue_db_to_entity


class DialogRepo():
    """Repository for Dialog entity"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_dialog(self, dialog: Dialog) -> None:
        """
        Save dialog in DB.

        :param dialog: Dialogue.
        """

        query = (
            insert(DialogTable)
            .values(
                id=dialog.id,
                tg_id=dialog.tg_id,
                topic=dialog.topic,
                context=dialog.context,
                created_at=dialog.created_at,
                updated_at=dialog.updated_at,
            )
        )
        await self.session.execute(query)
        await self.session.commit()

    async def get_dialogue_or_none(self, tg_id: str) -> Optional[Dialog]:
        """
        Get dialog from DB.

        :param tg_id: Client's telegram ID.
        """

        query = select(DialogTable).where(DialogTable.tg_id == tg_id)

        result = await self.session.execute(query)
        dialogue = result.scalar()

        if not dialogue:
            return None

        return dialogue_db_to_entity(dialog=dialogue)

    async def get_dialog(self, tg_id: str) -> Dialog:
        """
        Get dialog from DB.

        :param tg_id: Client's telegram ID.
        """

        dialogue = await self.get_dialogue_or_none(tg_id=tg_id)

        if not dialogue:
            raise DialogueNotFoundError()

        return dialogue

    async def update_dialog(self, dialogue: Dialog) -> None:
        """
        Update dialog in DB.

        :param tg_id: Client's telegram ID.
        """

        query = (
            update(DialogTable)
            .where(DialogTable.tg_id == dialogue.tg_id)
            .values(
                topic=dialogue.topic,
                context=dialogue.context,
                updated_at=dialogue.updated_at,
            )
        )

        await self.session.execute(query)
        await self.session.commit()

    async def delete_dialogs(self, tg_id: str) -> None:
        """
        Update dialogs of the user from DB.

        :param tg_id: Client's telegram ID.
        """

        query = (
            delete(DialogTable)
            .where(DialogTable.tg_id == tg_id)
        )

        await self.session.execute(query)
        await self.session.commit()
