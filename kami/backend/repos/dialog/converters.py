from kami.backend.domain.dialog.models import Dialog
from kami.backend.infra.db.tables.dialog import DialogTable


def dialogue_db_to_entity(dialog: DialogTable) -> Dialog:
    """
    Convert dialogue from DB to entity.

    :param dialogue: dialogue table in DB.
    :return: dialogue entity
    """

    return Dialog(
        id=dialog.id,
        tg_id=dialog.tg_id,
        topic=dialog.topic,
        context=dialog.context,
        created_at=dialog.created_at,
        updated_at=dialog.updated_at,
    )
