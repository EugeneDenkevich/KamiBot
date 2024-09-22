
from kami.backend.domain.lang_test.enums import LangTestPromtEnum, RateEnum
from kami.backend.domain.lang_test.exceptions import (
    NoCurrentQuestionError,
    NoQuestionsError,
    NoRepliesError,
)
from kami.backend.domain.lang_test.models import QuestT
from kami.backend.domain.lang_test.services import LangTestService
from kami.backend.gateways.chat_gpt.gateway import GPTGateway
from kami.backend.repos.ai.repo import AIRepo
from kami.backend.repos.lang_test.repo import LangTestRepo
from kami.common import get_prompt


class StartTestUseCase():
    """Use case of language test starting"""

    def __init__(
        self,
        lang_test_service: LangTestService,
        lang_test_repo: LangTestRepo,
        ai_repo: AIRepo,
        gpt_gateway: GPTGateway,
    ) -> None:
        self.lang_test_service = lang_test_service
        self.lang_test_repo = lang_test_repo
        self.ai_repo = ai_repo
        self.gpt_gateway = gpt_gateway

    async def __call__(self, tg_id: str) -> None:
        """
        Start language test.

        :param prompt: Prompt for creating test.
        :param tg_id: Telegram id.
        :return: Language test.
        """

        lang_test = await self.lang_test_repo.get_lang_test_or_none(tg_id=tg_id)

        if lang_test:
            await self.lang_test_repo.delete_lang_test(lang_test=lang_test)

        ai = await self.ai_repo.get_ai()

        gpt_answer = await self.gpt_gateway.get_answer(
            api_key=ai.gpt_api_key,
            prompt=get_prompt(LangTestPromtEnum.LANG_TEST),
        )

        lang_test = self.lang_test_service.create_lang_test(
            tg_id=tg_id,
            row_questions=gpt_answer,
        )

        await self.lang_test_repo.save_lang_test(lang_test=lang_test)


class AskOneOrNoneUseCase():
    """Use case for getting question for user or None of no questions"""

    def __init__(
        self,
        lang_test_service: LangTestService,
        lang_test_repo: LangTestRepo,
    ) -> None:
        self.lang_test_service = lang_test_service
        self.lang_test_repo = lang_test_repo

    async def __call__(self, tg_id: str) -> QuestT:
        """
        Get question for user or None.

        :param tg_id: Telegram id.
        :return: Question for user or None.
        """

        lang_test = await self.lang_test_repo.get_lang_test(tg_id=tg_id)

        if not lang_test.questions:
            raise NoQuestionsError()

        lang_test.current_question = lang_test.questions.pop()
        self.lang_test_service.update_lang_test(lang_test=lang_test)
        await self.lang_test_repo.update_lang_test(lang_test=lang_test)

        return lang_test.current_question


class SaveReplyUseCase():
    """Use case from saving reply from user"""

    def __init__(
        self,
        lang_test_service: LangTestService,
        lang_test_repo: LangTestRepo,
    ) -> None:
        self.lang_test_service = lang_test_service
        self.lang_test_repo = lang_test_repo

    async def __call__(self, tg_id: str, reply: str) -> None:
        """
        Save reply from user.

        :param tg_id: Telegram id.
        :param reply: Reply from user.
        """

        lang_test = await self.lang_test_repo.get_lang_test(tg_id=tg_id)

        if not lang_test.current_question:
            raise NoCurrentQuestionError()

        self.lang_test_service.append_reply(lang_test=lang_test, reply=reply)
        self.lang_test_service.clear_current_queston(lang_test=lang_test)
        await self.lang_test_repo.update_lang_test(lang_test=lang_test)


class RateLangLevelUseCase():
    """Use case for rate language user level"""

    def __init__(
        self,
        lang_test_service: LangTestService,
        lang_test_repo: LangTestRepo,
        ai_repo: AIRepo,
        gpt_gateway: GPTGateway,
    ) -> None:
        self.lang_test_service = lang_test_service
        self.lang_test_repo = lang_test_repo
        self.ai_repo = ai_repo
        self.gpt_gateway = gpt_gateway

    async def __call__(self, tg_id: str) -> RateEnum:
        """
        Rate language level of user.

        :param tg_id: Telegram id.
        :return: Language lavel.
        """

        lang_test = await self.lang_test_repo.get_lang_test(tg_id=tg_id)

        if not lang_test.replies:
            raise NoRepliesError()

        ai = await self.ai_repo.get_ai()

        rate = await self.gpt_gateway.get_answer(
            api_key=ai.gpt_api_key,
            prompt=(
                get_prompt(LangTestPromtEnum.LANG_TEST_RESULT)
                .format(
                    replies=lang_test.replies,
                    rates=RateEnum.get_values(),
                )
            ),
        )

        return RateEnum(rate)
