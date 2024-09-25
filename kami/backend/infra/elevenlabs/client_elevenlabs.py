
from elevenlabs.client import AsyncElevenLabs


class AsyncElevenLabsClient:
    """Wrapper for asyn elevenlabs client"""

    def __call__(self, api_key: str) -> AsyncElevenLabs:
        """
        Get async client for elevenlabs.

        :param api_key: Api key for elevenlabs.
        """

        return AsyncElevenLabs(api_key=api_key)


def get_elevenlabs_client() -> AsyncElevenLabsClient:
    """
    Get AsyncElevenLabs Client

    :return: AsyncElevenLabs client.
    """

    return AsyncElevenLabsClient()
