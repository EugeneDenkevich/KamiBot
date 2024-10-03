from datetime import datetime
from typing import List, Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from kami.backend.domain.audit.models import Audit
from kami.backend.infra.db.tables.audit import AuditTable
from kami.backend.repos.audit.converters import audit_db_to_entity


class AuditRepo():
    """Repository for ActionLog entity"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_log(self, audit: Audit) -> None:
        """
        Save audit in DB.

        :param audit: Audit.
        """

        query = (
            insert(AuditTable)
            .values(
                id=audit.id,
                tg_id=audit.tg_id,
                module=audit.module,
                action=audit.action,
                created_at=audit.created_at,
            )
        )

        await self.session.execute(query)
        await self.session.commit()

    async def get_logs(
        self,
        tg_id: Optional[str] = None,
        module: Optional[str] = None,
        action: Optional[str] = None,
        created_at: Optional[datetime] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Audit]:
        """
        Get audit logs with optional filters.

        :param telegram_id: User telegram ID.
        :param module: Module name.
        :param action: Action type.
        :param created_at: Date of creation.
        :param limit: Limit of records.
        :param offset: Offset of records.
        :return: List of Audits.
        """

        query = select(AuditTable)

        if tg_id:
            query = query.where(AuditTable.tg_id == tg_id)
        if module:
            query = query.where(AuditTable.module == module)
        if action:
            query = query.where(AuditTable.action == action)
        if created_at:
            query = query.where(AuditTable.created_at == created_at)

        if limit:
            query = query.limit(limit)
        if created_at:
            query = query.offset(offset)

        response = await self.session.execute(query)
        audits = response.scalars()

        return [audit_db_to_entity(audit=audit) for audit in audits]
