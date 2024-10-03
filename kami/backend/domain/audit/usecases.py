from kami.backend.domain.audit.services import AuditService
from kami.backend.repos.audit.repo import AuditRepo
from kami.backend.repos.user.repo import UserRepo


class LogToDBUseCase():
    """Use case for save log in database"""

    def __init__(
        self,
        audit_service: AuditService,
        audit_repo: AuditRepo,
        user_repo: UserRepo,
        admin_id: str,
    ) -> None:
        self.audit_service = audit_service
        self.audit_repo = audit_repo
        self.user_repo = user_repo
        self.admin_id = admin_id

    async def __call__(
        self,
        tg_id: str,
        module: str,
        action: str,
    ) -> None:
        """
        Create Audit.

        :param telegram_id: User telegram ID.
        :param module: Module name.
        :param action: User action.
        :return: Audit.
        """

        user = await self.user_repo.get_user_or_none(tg_id=tg_id)

        if user and user.tg_id == self.admin_id:

            # Pass if user is admin
            pass

        audit = self.audit_service.create_audit(
            tg_id=tg_id,
            module=module,
            action=action,
        )

        await self.audit_repo.save_log(audit)
