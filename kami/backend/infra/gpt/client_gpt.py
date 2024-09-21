from typing import Optional

import httpx
from openai import AsyncOpenAI


def get_gpt_client(vpn_client: Optional[httpx.AsyncClient] = None) -> AsyncOpenAI:

    return AsyncOpenAI(
        api_key="",
        http_client=vpn_client
    )