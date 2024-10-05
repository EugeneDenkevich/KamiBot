from contextlib import asynccontextmanager
from typing import AsyncIterator

from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from kami.backend.domain.ai.usecases import (
    ContinueDialogUseCase,
    ReturnToDialogUseCase,
    StartDialogUseCase,
    TranslateTextToTextUseCase,
    TranslateVoiceToTextUseCase,
    VoiceToTextUseCase,
)
from kami.backend.domain.audit.services import AuditService
from kami.backend.domain.audit.usecases import (
    LogToDBUseCase,
)
from kami.backend.domain.dialog.services import DialogService
from kami.backend.domain.dialog.usecases import (
    CreateDialogUseCase,
    GetDialogOrNoneUseCase,
    GetDialogUseCase,
)
from kami.backend.domain.lang_test.services import LangTestService
from kami.backend.domain.lang_test.usecases import (
    AskOne,
    RateLangLevelUseCase,
    SaveReplyUseCase,
    StartTestUseCase,
)
from kami.backend.domain.user.services import UserService
from kami.backend.domain.user.usecases import (
    CreateUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
)
from kami.backend.gateways.chat_gpt.gateway import GPTGateway
from kami.backend.gateways.elevenlabs.gateway import ElevenLabsGateway
from kami.backend.gateways.whisper.gateway import WhisperGateway
from kami.backend.infra.elevenlabs.client_elevenlabs import AsyncElevenLabsClient
from kami.backend.repos.ai.repo import AIRepo
from kami.backend.repos.audit.repo import AuditRepo
from kami.backend.repos.dialog.repo import DialogRepo
from kami.backend.repos.lang_test.repo import LangTestRepo
from kami.backend.repos.user.repo import UserRepo


class UseCaseFactory:
    """Factory of usecases"""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        gpt_client: AsyncOpenAI,
        whisper_client: AsyncOpenAI,
        elevenlabs_client: AsyncElevenLabsClient,
        context_limit: int,
        admin_id: str,
        test_count: int,
    ):
        self.session_factory = session_factory
        self.gpt_client = gpt_client
        self.whisper_client = whisper_client
        self.elevenlabs_client = elevenlabs_client
        self.context_limit = context_limit
        self.admin_id = admin_id
        self.test_count = test_count

    @asynccontextmanager
    async def create_dialog(self) -> AsyncIterator[CreateDialogUseCase]:
        async with self.session_factory() as session:
            yield CreateDialogUseCase(
                dialog_service=DialogService(),
                dialog_repo=DialogRepo(session=session),
            )

    @asynccontextmanager
    async def get_dialog(self) -> AsyncIterator[GetDialogUseCase]:
        async with self.session_factory() as session:
            yield GetDialogUseCase(
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
                test_count=self.test_count,
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
    async def start_dialog(self) -> AsyncIterator[StartDialogUseCase]:
        async with self.session_factory() as session:
            yield StartDialogUseCase(
                gpt_gateway=GPTGateway(gpt_client=self.gpt_client),
                elevenlabs_gateway=ElevenLabsGateway(elevenlabs_client=self.elevenlabs_client),
                ai_repo=AIRepo(session=session),
                dialog_repo=DialogRepo(session=session),
                dialog_service=DialogService(),
            )

    @asynccontextmanager
    async def continue_dialog(self) -> AsyncIterator[ContinueDialogUseCase]:
        async with self.session_factory() as session:
            yield ContinueDialogUseCase(
                gpt_gateway=GPTGateway(gpt_client=self.gpt_client),
                whisper_gateway=WhisperGateway(whisper_client=self.whisper_client),
                elevenlabs_gateway=ElevenLabsGateway(
                    elevenlabs_client=self.elevenlabs_client,
                ),
                ai_repo=AIRepo(session=session),
                dialog_repo=DialogRepo(session=session),
                dialog_service=DialogService(),
                context_limit=self.context_limit,
            )

    @asynccontextmanager
    async def voice_to_text(self) -> AsyncIterator[VoiceToTextUseCase]:
        async with self.session_factory() as session:
            yield VoiceToTextUseCase(
                whisper_gateway=WhisperGateway(whisper_client=self.whisper_client),
                ai_repo=AIRepo(session=session),
            )

    @asynccontextmanager
    async def return_to_dialog(self) -> AsyncIterator[ReturnToDialogUseCase]:
        async with self.session_factory() as session:
            yield ReturnToDialogUseCase(
                gpt_gateway=GPTGateway(gpt_client=self.gpt_client),
                elevenlabs_gateway=ElevenLabsGateway(
                    elevenlabs_client=self.elevenlabs_client,
                ),
                ai_repo=AIRepo(session=session),
                dialog_repo=DialogRepo(session=session),
            )

    @asynccontextmanager
    async def create_user(self) -> AsyncIterator[CreateUserUseCase]:
        async with self.session_factory() as session:
            yield CreateUserUseCase(
                user_service=UserService(),
                user_repo=UserRepo(session=session),
            )

    @asynccontextmanager
    async def get_user(self) -> AsyncIterator[GetUserUseCase]:
        async with self.session_factory() as session:
            yield GetUserUseCase(
                user_repo=UserRepo(session=session),
            )

    @asynccontextmanager
    async def update_user(self) -> AsyncIterator[UpdateUserUseCase]:
        async with self.session_factory() as session:
            yield UpdateUserUseCase(
                user_service=UserService(),
                user_repo=UserRepo(session=session),
            )

    @asynccontextmanager
    async def translate_text_to_text(self) -> AsyncIterator[TranslateTextToTextUseCase]:
        async with self.session_factory() as session:
            yield TranslateTextToTextUseCase(
                gpt_gateway=GPTGateway(gpt_client=self.gpt_client),
                ai_repo=AIRepo(session=session),
            )

    @asynccontextmanager
    async def translate_voice_to_text(
        self,
    ) -> AsyncIterator[TranslateVoiceToTextUseCase]:
        async with self.session_factory() as session:
            yield TranslateVoiceToTextUseCase(
                gpt_gateway=GPTGateway(gpt_client=self.gpt_client),
                whisper_gateway=WhisperGateway(whisper_client=self.whisper_client),
                ai_repo=AIRepo(session=session),
            )

    @asynccontextmanager
    async def log_to_db(self) -> AsyncIterator[LogToDBUseCase]:
        async with self.session_factory() as session:
            yield LogToDBUseCase(
                audit_service=AuditService(),
                audit_repo=AuditRepo(session=session),
                user_repo=UserRepo(session=session),
                admin_id=self.admin_id,
            )

    @asynccontextmanager
    async def get_dialog_or_none(self) -> AsyncIterator[GetDialogOrNoneUseCase]:
        async with self.session_factory() as session:
            yield GetDialogOrNoneUseCase(
                dialog_repo=DialogRepo(session=session),
            )
