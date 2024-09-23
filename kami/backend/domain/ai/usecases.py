from typing import Any, Coroutine

from kami.backend.gateways.chat_gpt.gateway import GPTGateway
from kami.backend.gateways.elevenlabs.gateway import ElevenLabsGateway
from kami.backend.gateways.whisper.gateway import WhisperGateway
from kami.backend.repos.ai.repo import AIRepo


class VoiceToVoiceUseCase:
    """Use case to receive answer from ChatGPT"""

    def __init__(
        self,
        gpt_gateway: GPTGateway,
        whisper_gateway: WhisperGateway,
        elevenlabs_gateway: ElevenLabsGateway,
        ai_repo: AIRepo,
    ) -> None:

        self.gpt_gateway = gpt_gateway
        self.whisper_gateway = whisper_gateway
        self.elevenlabs_gateway = elevenlabs_gateway
        self.ai_repo = ai_repo

    async def __call__(self, voice: bytes) -> Coroutine[Any, Any, bytes]:
        """
        Use case to receive answer from ChatGPT

        :param voice: Prompt for ChatGPT.
        :return: Answer in voice form..
        """

        ai = await self.ai_repo.get_ai()

        gpt_request =  await self.whisper_gateway.audio_to_text(
            api_key=ai.gpt_api_key,
            voice=voice,
        )

        gpt_answer = await self.gpt_gateway.get_answer(
            api_key=ai.gpt_api_key,
            prompt=gpt_request,
        )

        return self.elevenlabs_gateway.get_audio(text=gpt_answer)
