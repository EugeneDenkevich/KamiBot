from typing import Optional

from httpx import AsyncClient
from openai import AsyncOpenAI


def get_gpt_client(vpn_client: Optional[AsyncClient] = None) -> AsyncOpenAI:
    """
    Get ChatGPT Client

    :param vpn_client: VPN client.
    :return: Async OpenAI client.
    """

    return AsyncOpenAI(
        api_key="",
        http_client=vpn_client,
    )
