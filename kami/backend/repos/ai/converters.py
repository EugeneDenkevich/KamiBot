from kami.backend.domain.ai.models import AI
from kami.backend.infra.db.tables.ai import AITable


def ai_db_to_entity(ai: AITable) -> AI:
    """
    Convert AI from DB to entity.

    :param ai: AI table in DB.
    :return: AI entity
    """

    return AI(
        id=ai.id,
        gpt_api_key=str(ai.gpt_api_key),
        elevenlabs_api_key=str(ai.elevenlabs_api_key),
    )
