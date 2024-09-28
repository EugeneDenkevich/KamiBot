from typing import AsyncIterator

from elevenlabs import Voice

from kami.backend.infra.elevenlabs.client_elevenlabs import AsyncElevenLabsClient


class ElevenLabsGateway:
    """Gateway for ElevenLabs service"""

    def __init__(self, elevenlabs_client: AsyncElevenLabsClient) -> None:
        self.elevenlabs_client = elevenlabs_client

    async def get_audio(self, api_key: str, text: str) -> bytes:
        """
        Converting text to voice using ElevenLabs.

        :param api_key: API key for ElevenLabs.
        :param text: Text to speech for ElevenLabs.
        :return: Voiced audio.
        """

        voice = await self._get_voice(api_key)

        response = await self.elevenlabs_client(api_key=api_key).generate(
            text=text,
            model="eleven_multilingual_v2",
            voice=voice,
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

    async def _get_voice(self, api_key: str) -> Voice:
        """
        Get particular voice.

        :param api_key: Api ket for elevenlabs.
        :return: Particular teacher's Voice.
        """

        response = await self.elevenlabs_client(api_key=api_key).voices.get_all()

        return response.voices[22]
