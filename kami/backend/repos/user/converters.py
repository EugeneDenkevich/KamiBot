from kami.backend.domain.user.models import User
from kami.backend.infra.db.tables.user import UserTable


def user_db_to_entity(user: UserTable) -> User:
    return User(
        id=user.id,
        tg_id=user.tg_id,
        username=user.username,
        fio=user.fio,
        phone=user.phone,
        active=user.active,
        onboarded=user.onboarded,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
