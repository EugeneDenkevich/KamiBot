from kami.backend.domain.lang_test.models import LangTest
from kami.backend.infra.db.tables.lang_test import LangTestTable


def lang_test_db_to_entity(lang_test: LangTestTable) -> LangTest:
    """
    Convert language test from DB to entity,

    :param lang_test: DB model of language test.
    :return: Language test entity.
    """

    return LangTest(
        id=lang_test.id,
        tg_id=lang_test.tg_id,
        questions=lang_test.questions,
        current_question=lang_test.current_question,
        replies=lang_test.replies,
        created_at=lang_test.created_at,
        updated_at=lang_test.updated_at,
    )
