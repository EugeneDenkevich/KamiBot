from typing import Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from kami.backend.domain.lang_test.exceptions import LangTestNotFound
from kami.backend.domain.lang_test.models import LangTest
from kami.backend.infra.db.tables.lang_test import LangTestTable
from kami.backend.repos.lang_test.converters import lang_test_db_to_entity


class LangTestRepo():
    """Repository for LangTest entity"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_lang_test(self, lang_test: LangTest) -> None:
        """
        Save language test in DB.

        :param lang_test: Language test.
        """

        query = (
            insert(LangTestTable)
            .values(
                id=lang_test.id,
                tg_id=lang_test.tg_id,
                questions=lang_test.questions,
                current_question=lang_test.current_question,
                replies=lang_test.replies,
                created_at=lang_test.created_at,
                updated_at=lang_test.updated_at,
            )
        )

        await self.session.execute(query)
        await self.session.commit()

    async def get_lang_test_or_none(self, tg_id: str) -> Optional[LangTest]:
        """
        Get language test from DB.

        :param tg_id: Telegram id.
        :return: Language test.
        """

        query = select(LangTestTable).where(LangTestTable.tg_id == tg_id)

        await self.session.execute(query)

        lang_test = await self.session.scalar(query)

        if not lang_test:
            return None

        return lang_test_db_to_entity(lang_test)

    async def get_lang_test(self, tg_id: str) -> LangTest:
        """
        Get language test from DB.

        :param tg_id: Telegram id.
        :return: Language test.
        """

        lang_test = await self.get_lang_test_or_none(tg_id=tg_id)

        if not lang_test:
            raise LangTestNotFound()

        return lang_test

    async def update_lang_test(self, lang_test: LangTest) -> None:
        """
        Update language test in DB.

        :param lang_test: Language test.
        """

        query = (
            update(LangTestTable)
            .where(LangTestTable.id == lang_test.id)
            .values(
                questions=lang_test.questions,
                current_question=lang_test.current_question,
                replies=lang_test.replies,
                updated_at=lang_test.updated_at,
            )
        )

        await self.session.execute(query)
        await self.session.commit()

    async def delete_lang_test(self, lang_test: LangTest) -> None:
        """
        Delete language test from DB.

        :param lang_test: Language test.
        """

        query = (
            delete(LangTestTable)
            .where(LangTestTable.tg_id == lang_test.tg_id)
        )

        await self.session.execute(query)
        await self.session.commit()
