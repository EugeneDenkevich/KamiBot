from datetime import datetime
from uuid import uuid4

from kami.backend.domain.audit.models import Audit


class AuditService():
    """Service for ActionLog entity"""

    def create_audit(
        self,
        tg_id: str,
        module: str,
        action: str,
    ) -> Audit:
        """
        Create audit.

        :param telegram_id: User telegram id.
        :param module: Module.
        :param action: User action.
        :return: AuditService.
        """

        return Audit(
            id=uuid4(),
            tg_id=tg_id,
            module=module,
            action=action,
            created_at=datetime.now(),
        )


def build_audit_service() -> AuditService:
    return AuditService()
