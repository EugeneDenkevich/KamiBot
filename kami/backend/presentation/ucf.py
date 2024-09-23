from contextlib import asynccontextmanager
from typing import AsyncIterator

from elevenlabs.client import ElevenLabs
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from kami.backend.domain.ai.usecases import VoiceToVoiceUseCase
from kami.backend.domain.dialog.services import DialogService
from kami.backend.domain.dialog.usecases import CreateDialogUseCase
from kami.backend.domain.lang_test.services import LangTestService
from kami.backend.domain.lang_test.usecases import (
    AskOne,
    RateLangLevelUseCase,
    SaveReplyUseCase,
    StartTestUseCase,
)
from kami.backend.gateways.chat_gpt.gateway import GPTGateway
from kami.backend.gateways.elevenlabs.gateway import ElevenLabsGateway
from kami.backend.gateways.whisper.gateway import WhisperGateway
from kami.backend.repos.ai.repo import AIRepo
from kami.backend.repos.dialog.repo import DialogRepo
from kami.backend.repos.lang_test.repo import LangTestRepo


class UseCaseFactory:

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        gpt_client: AsyncOpenAI,
        whisper_client: AsyncOpenAI,
        elevenlabs_client: ElevenLabs,
    ):
        self.session_factory = session_factory
        self.gpt_client = gpt_client
        self.whisper_client = whisper_client
        self.elevenlabs_client = elevenlabs_client

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
    async def ask_one(self) -> AsyncIterator[AskOne]:
        async with self.session_factory() as session:
            yield AskOne(
                lang_test_service=LangTestService(),
                lang_test_repo=LangTestRepo(session=session),
            )

    @asynccontextmanager
    async def save_reply(self) -> AsyncIterator[SaveReplyUseCase]:
        async with self.session_factory() as session:
            yield SaveReplyUseCase(
                lang_test_service=LangTestService(),
                lang_test_repo=LangTestRepo(session=session),
                gpt_gateway=GPTGateway(gpt_client=self.gpt_client),
                whisper_gateway=WhisperGateway(whisper_client=self.whisper_client),
                ai_repo=AIRepo(session=session),
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

    @asynccontextmanager
    async def voice_to_voice(self) -> AsyncIterator[VoiceToVoiceUseCase]:
        async with self.session_factory() as session:
            yield VoiceToVoiceUseCase(
                gpt_gateway=GPTGateway(gpt_client=self.gpt_client),
                whisper_gateway=WhisperGateway(whisper_client=self.whisper_client),
                elevenlabs_gateway=ElevenLabsGateway(
                    elevenlabs_client=self.elevenlabs_client,
                ),
                ai_repo=AIRepo(session=session),
            )
