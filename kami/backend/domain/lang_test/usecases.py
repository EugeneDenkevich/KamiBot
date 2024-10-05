from typing import Union, cast

from kami.backend.domain.lang_test.enums import LangTestPromtEnum, RateEnum
from kami.backend.domain.lang_test.exceptions import (
    NoCurrentQuestionError,
    NoQuestionsError,
    NoRepliesError,
)
from kami.backend.domain.lang_test.services import LangTestService
from kami.backend.gateways.chat_gpt.gateway import GPTGateway
from kami.backend.gateways.whisper.gateway import WhisperGateway
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
        test_count: int,
    ) -> None:
        self.lang_test_service = lang_test_service
        self.lang_test_repo = lang_test_repo
        self.ai_repo = ai_repo
        self.gpt_gateway = gpt_gateway
        self.test_count = test_count

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

        questions = []
        for _ in range(self.test_count):
            gpt_answer = await self.gpt_gateway.get_answer(
                api_key=ai.gpt_api_key,
                prompt=get_prompt(LangTestPromtEnum.LANG_TEST),
            )

            questions.append(gpt_answer)

        lang_test = self.lang_test_service.create_lang_test(
            tg_id=tg_id,
            questions=questions,
        )

        await self.lang_test_repo.save_lang_test(lang_test=lang_test)


class AskOne():
    """Use case for getting question for user"""

    def __init__(
        self,
        lang_test_service: LangTestService,
        lang_test_repo: LangTestRepo,
    ) -> None:
        self.lang_test_service = lang_test_service
        self.lang_test_repo = lang_test_repo

    async def __call__(self, tg_id: str) -> str:
        """
        Get question for user.

        :param tg_id: Telegram id.
        :return: Question for user.
        """

        lang_test = await self.lang_test_repo.get_lang_test(tg_id=tg_id)

        if not lang_test.questions:
            raise NoQuestionsError()

        self.lang_test_service.set_current_question(lang_test=lang_test)
        assert lang_test.current_question

        await self.lang_test_repo.update_lang_test(lang_test=lang_test)

        return lang_test.current_question


class SaveReplyUseCase():
    """Use case from saving reply from user"""

    def __init__(
        self,
        lang_test_service: LangTestService,
        lang_test_repo: LangTestRepo,
        gpt_gateway: GPTGateway,
        whisper_gateway: WhisperGateway,
        ai_repo: AIRepo,
    ) -> None:
        self.lang_test_service = lang_test_service
        self.lang_test_repo = lang_test_repo
        self.gpt_gateway = gpt_gateway
        self.whisper_gateway = whisper_gateway
        self.ai_repo = ai_repo

    async def __call__(self, tg_id: str, reply: Union[str, bytes]) -> None:
        """
        Save reply from user.

        :param tg_id: Telegram id.
        :param reply: Reply from user.
        """

        lang_test = await self.lang_test_repo.get_lang_test(tg_id=tg_id)

        if not lang_test.current_question:
            raise NoCurrentQuestionError()

        gpt_answer = None
        if isinstance(reply, bytes):
            ai = await self.ai_repo.get_ai()

            text_reply =  await self.whisper_gateway.audio_to_text(
                api_key=ai.gpt_api_key,
                voice=reply,
            )

            gpt_answer = await self.gpt_gateway.get_answer(
                api_key=ai.gpt_api_key,
                prompt=(
                    get_prompt(LangTestPromtEnum.LANG_TEST_REPLY)
                    .replace(
                        "<<question>>",
                        lang_test.current_question,
                    )
                    .replace(
                        "<<reply>>", text_reply,
                    )
                ),
            )

        self.lang_test_service.append_reply(
            lang_test=lang_test,
            reply=gpt_answer if gpt_answer else cast(str, reply),
        )
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
