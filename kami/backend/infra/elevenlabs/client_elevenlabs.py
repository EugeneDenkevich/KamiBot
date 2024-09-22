from typing import Optional

from elevenlabs.client import ElevenLabs
from httpx import AsyncClient


def get_elevenlabs_client(vpn_client: Optional[AsyncClient] = None) -> ElevenLabs:
    """
    Get ElevenLabs Client

    :param vpn_client: VPN client.
    :return: ElevenLabs client.
    """

    return ElevenLabs(
        api_key="",
        httpx_client=vpn_client,
    )
