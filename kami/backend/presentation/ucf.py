from contextlib import asynccontextmanager
from typing import AsyncIterator

from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from kami.backend.domain.dialog.services import DialogService
from kami.backend.domain.dialog.usecases import CreateDialogUseCase
from kami.backend.domain.lang_test.services import LangTestService
from kami.backend.domain.lang_test.usecases import (
    AskOneOrNoneUseCase,
    RateLangLevelUseCase,
    SaveReplyUseCase,
    StartTestUseCase,
)
from kami.backend.gateways.chat_gpt.gateway import GPTGateway
from kami.backend.repos.ai.repo import AIRepo
from kami.backend.repos.dialog.repo import DialogRepo
from kami.backend.repos.lang_test.repo import LangTestRepo


class UseCaseFactory:

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        gpt_client: AsyncOpenAI,
    ):
        self.session_factory = session_factory
        self.gpt_client = gpt_client

    @asynccontextmanager
    async def create_dialog(self) -> AsyncIterator[CreateDialogUseCase]:
        async with self.session_factory() as session:
            yield CreateDialogUseCase(
                dialog_service=DialogService(),
                dialog_repo=DialogRepo(session=session),
            )

    @asynccontextmanager
    async def start_test(self) -> AsyncIterator[StartTestUseCase]:
        async with self.session_factory() as session:
            yield StartTestUseCase(
                lang_test_service=LangTestService(),
                lang_test_repo=LangTestRepo(session=session),
                ai_repo=AIRepo(session=session),
                gpt_gateway=GPTGateway(gpt_client=self.gpt_client),
            )

    @asynccontextmanager
    async def ask_one_or_none(self) -> AsyncIterator[AskOneOrNoneUseCase]:
        async with self.session_factory() as session:
            yield AskOneOrNoneUseCase(
                lang_test_service=LangTestService(),
                lang_test_repo=LangTestRepo(session=session),
            )

    @asynccontextmanager
    async def save_reply(self) -> AsyncIterator[SaveReplyUseCase]:
        async with self.session_factory() as session:
            yield SaveReplyUseCase(
                lang_test_service=LangTestService(),
                lang_test_repo=LangTestRepo(session=session),
            )

    @asynccontextmanager
    async def rate_lang_level(self) -> AsyncIterator[RateLangLevelUseCase]:
        async with self.session_factory() as session:
            yield RateLangLevelUseCase(
                lang_test_service=LangTestService(),
                lang_test_repo=LangTestRepo(session=session),
                ai_repo=AIRepo(session=session),
                gpt_gateway=GPTGateway(gpt_client=self.gpt_client),
            )
