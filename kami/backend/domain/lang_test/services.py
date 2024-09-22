import json
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from kami.backend.domain.lang_test.models import LangTest, QuestT


class LangTestService():
    """Service for LangTest entity"""

    def create_lang_test(self, tg_id: str, row_questions: str) -> LangTest:
        """
        Create language test

        :param tg_id: Telegram id.
        :param row_questions: Row questions string.
        :return: Language test.
        """

        return LangTest(
            id=uuid4(),
            tg_id=tg_id,
            questions=json.loads(row_questions),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def update_lang_test(
        self,
        lang_test: LangTest,
        questions: Optional[List[QuestT]] = None,
        current_question: Optional[QuestT] = None,
        replies: Optional[List[QuestT]] = None,
    ) -> None:
        """
        Update lananguage test

        :param lang_test: Language test.
        :param questions: Test questions.
        :param current_question: Current question.
        :param replies: Replies from user.
        """

        if questions is not None:
            lang_test.questions = questions
        if current_question is not None:
            lang_test.current_question = current_question
        if replies is not None:
            lang_test.replies = replies

        lang_test.updated_at = datetime.now()

    def set_current_question(
        self,
        lang_test: LangTest,
    ) -> None:
        """
        Set current question

        :param lang_test: Language test.
        """

        lang_test.current_question = lang_test.questions.pop()
        self.update_lang_test(lang_test=lang_test)

    def append_reply(
        self,
        lang_test: LangTest,
        reply: str,
    ) -> None:
        """
        Append reply from user

        :param lang_test: Language test.
        :param reply: Reply from user.
        """

        lang_test.current_question["reply"] = reply
        lang_test.replies.append(lang_test.current_question)

    def clear_current_queston(
        self,
        lang_test: LangTest,
    ) -> None:
        """
        Clear current question

        :param lang_test: Language test.
        """

        lang_test.current_question = {}
        self.update_lang_test(lang_test=lang_test)


def build_dialog_service() -> LangTestService:
    return LangTestService()
