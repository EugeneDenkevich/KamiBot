import io

import pyttsx3
from elevenlabs.client import ElevenLabs


class ElevenLabsGateway:
    """Gateway for ElevenLabs service"""

    def __init__(self, elevenlabs_client: ElevenLabs) -> None:
        self.elevenlabs_client = elevenlabs_client
    
    # async def get_audio(self, api_key: str, text: str, voice_id: str) -> bytes:
    #     """
    #     Converting text to voice using ElevenLabs.
        
    #     :param api_key: API key for ElevenLabs.
    #     :param prompt: Text to speech for ElevenLabs.
    #     :param voice_id: Client's voice ID.
    #     :return: Voiced audio.
    #     """

    #     self.elevenlabs_client.api_key = api_key

    #     audio = self.elevenlabs_client.generate(
    #         text=text,
    #         voice=voice_id,
    #         model="eleven_multilingual_v2"
    #     )



    #     return audio

    async def get_audio(self, text: str) -> bytes:

        engine = pyttsx3.init()

        audio_bytes = io.BytesIO()

        engine.setProperty("audioDestination", audio_bytes)

        engine.say(text)
        engine.runAndWait()

        audio_bytes.seek(0)

        return audio_bytes.read()
