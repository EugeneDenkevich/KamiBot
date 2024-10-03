from kami.backend.domain.audit.models import Audit
from kami.backend.infra.db.tables.audit import AuditTable


def audit_db_to_entity(audit: AuditTable) -> Audit:
    """
    Convert audit from DB to entity.

    :param audit: Audit table in DB.
    :return: Audit entity
    """

    return Audit(
        id=audit.id,
        tg_id=audit.tg_id,
        action=audit.action,
        module=audit.module,
        created_at=audit.created_at,
    )
