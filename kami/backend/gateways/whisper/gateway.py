import asyncio
from io import BytesIO

from openai import APIConnectionError, AsyncOpenAI

from kami.backend.gateways.whisper.exceptions import NoWhisperContentError


class WhisperGateway:
    """Gateway for Whisper service"""

    def __init__(self, whisper_client: AsyncOpenAI) -> None:
        self.whisper_client = whisper_client

    async def audio_to_text(self, api_key: str, voice: bytes) -> str:
        """
        Get text from voice client's using Whisper.

        :param api_key: API key for Whisper.
        :param voice: Voice file for Whisper.
        :return: Text from voice.
        """

        self.whisper_client.api_key = api_key

        attempt = 0
        delay = 0.5
        max_tries = 3
        while attempt <= max_tries:
            try:
                audio_file = BytesIO(voice)
                audio_file.name = "voice.ogg"

                response = await self.whisper_client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-1",
                )
                break
            except APIConnectionError:
                attempt += 1
                if attempt > max_tries:
                    raise
                await asyncio.sleep(delay * attempt)
            except Exception:
                raise

        content = response.text

        if not content:
            raise NoWhisperContentError()

        return content
