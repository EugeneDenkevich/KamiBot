
import json

from kami.backend.domain.ai.enums import DialoguePromtEnum
from kami.backend.domain.dialog.services import DialogService
from kami.backend.gateways.chat_gpt.gateway import GPTGateway
from kami.backend.gateways.elevenlabs.gateway import ElevenLabsGateway
from kami.backend.gateways.whisper.gateway import WhisperGateway
from kami.backend.repos.ai.repo import AIRepo
from kami.backend.repos.dialog.repo import DialogRepo
from kami.common import get_prompt


class ContinueDialogueUseCase:
    """Use case to receive answer from ChatGPT"""

    def __init__(
        self,
        gpt_gateway: GPTGateway,
        whisper_gateway: WhisperGateway,
        elevenlabs_gateway: ElevenLabsGateway,
        ai_repo: AIRepo,
        dialog_repo: DialogRepo,
        dialog_service: DialogService,
        context_limit: int,
    ) -> None:
        self.gpt_gateway = gpt_gateway
        self.whisper_gateway = whisper_gateway
        self.elevenlabs_gateway = elevenlabs_gateway
        self.ai_repo = ai_repo
        self.dialog_repo = dialog_repo
        self.dialog_service = dialog_service
        self.context_limit = context_limit

    async def __call__(self, tg_id: str, voice: bytes) -> bytes:
        """
        Use case to receive answer from ChatGPT

        :param voice: Voice for ChatGPT.
        :return: Answer in voice form.
        """

        ai = await self.ai_repo.get_ai()

        dialog = await self.dialog_repo.get_dialog(tg_id=tg_id)

        reply =  await self.whisper_gateway.audio_to_text(
            api_key=ai.gpt_api_key,
            voice=voice,
        )

        gpt_answer = await self.gpt_gateway.get_answer(
            api_key=ai.gpt_api_key,
            prompt=get_prompt(DialoguePromtEnum.CONTINUE_DIALOG)
            .replace(
                "<<topic>>", dialog.topic,
            )
            .replace(
                "<<context>>", json.dumps(dialog.context, ensure_ascii=False),
            )
            .replace(
                "<<reply>>", reply,
            ),
        )

        if len(dialog.context) > self.context_limit:
            dialog.context.pop(0)

        dialog.context.append(
            {
                "student": reply,
                "chat_gpt": gpt_answer,
            },
        )

        self.dialog_service.update_dialog(dialog)
        await self.dialog_repo.update_dialog(dialog)

        return await self.elevenlabs_gateway.get_audio(
            api_key=ai.elevenlabs_api_key,
            text=gpt_answer,
        )

class StartDialogUseCase:
    """Use case to receive answer from ChatGPT"""

    def __init__(
        self,
        gpt_gateway: GPTGateway,
        elevenlabs_gateway: ElevenLabsGateway,
        ai_repo: AIRepo,
        dialog_repo: DialogRepo,
        dialog_service: DialogService,
    ) -> None:

        self.gpt_gateway = gpt_gateway
        self.elevenlabs_gateway = elevenlabs_gateway
        self.ai_repo = ai_repo
        self.dialog_repo = dialog_repo
        self.dialog_service = dialog_service

    async def __call__(self, tg_id: str, topic: str) -> bytes:
        """
        Use case to receive answer from ChatGPT

        :param voice: Prompt for ChatGPT.
        :return: Answer in voice form..
        """

        ai = await self.ai_repo.get_ai()

        dialog = await self.dialog_repo.get_dialogue_or_none(tg_id=tg_id)

        if dialog:
            await self.dialog_repo.delete_dialogs(tg_id=tg_id)

        dialog = self.dialog_service.create_dialog(tg_id=tg_id, topic=topic)
        await self.dialog_repo.save_dialog(dialog)

        gpt_answer = await self.gpt_gateway.get_answer(
            api_key=ai.gpt_api_key,
            prompt=get_prompt(DialoguePromtEnum.START_DIALOG)
            .replace(
                "<<topic>>", topic,
            ),
        )

        return await self.elevenlabs_gateway.get_audio(
            api_key=ai.elevenlabs_api_key,
            text=gpt_answer,
        )

class VoiceToTextUseCase:
    """Use case to receive answer from ChatGPT"""

    def __init__(
        self,
        whisper_gateway: WhisperGateway,
        ai_repo: AIRepo,
    ) -> None:

        self.whisper_gateway = whisper_gateway
        self.ai_repo = ai_repo

    async def __call__(self, voice: bytes) -> str:
        """
        Use case to transcribe telegram voice to text.

        :param voice: Prompt for ChatGPT.
        :return: Answer in voice form..
        """

        ai = await self.ai_repo.get_ai()

        return await self.whisper_gateway.audio_to_text(
            api_key=ai.gpt_api_key,
            voice=voice,
        )
