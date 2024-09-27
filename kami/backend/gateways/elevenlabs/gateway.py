from typing import AsyncIterator

from kami.backend.infra.elevenlabs.client_elevenlabs import AsyncElevenLabsClient


class ElevenLabsGateway:
    """Gateway for ElevenLabs service"""

    def __init__(self, elevenlabs_client: AsyncElevenLabsClient) -> None:
        self.elevenlabs_client = elevenlabs_client

    # async def get_audio(self, api_key: str, text: str, voice_id: str) -> bytes:
    #     """
    #     Converting text to voice using ElevenLabs.

    #     :param api_key: API key for ElevenLabs.
    #     :param prompt: Text to speech for ElevenLabs.
    #     :param voice_id: Client's voice ID.
    #     :return: Voiced audio.
    #     """

    async def get_audio(self, api_key: str, text: str) -> bytes:
        """
        Converting text to voice using ElevenLabs.

        :param api_key: API key for ElevenLabs.
        :param text: Text to speech for ElevenLabs.
        :return: Voiced audio.
        """

        response = await self.elevenlabs_client(api_key=api_key).generate(
            text=text,
            model="eleven_multilingual_v2",
        )

        return await self._response_to_audio(response=response)

    async def _response_to_audio(self, response: AsyncIterator[bytes]) -> bytes:
        """
        Convert response from elevelnabs to bytes.


        :param response: Response from elevenlabs
        """

        audio = b""
        async for audio_chunk in response:
            audio += audio_chunk

        return audio
