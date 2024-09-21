import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from kami.backend.domain.ai.exceptions import AINotFoundError
from kami.backend.domain.ai.models import AI
from kami.backend.infra.db.tables.ai import AITable
from kami.backend.repos.ai.converters import ai_db_to_entity


class AIRepo():
    """Repository for AI entity"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_ai(self) -> AI:
        """
        Get AI from DB.

        :return: AI entity.
        """

        query = select(AITable)

        result = await self.session.execute(query)
        ai = result.scalar()

        if not ai:
            raise AINotFoundError()

        return ai_db_to_entity(ai)
        


