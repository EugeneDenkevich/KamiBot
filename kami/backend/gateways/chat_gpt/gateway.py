import asyncio

from openai import APIConnectionError, AsyncOpenAI

from kami.backend.gateways.chat_gpt.exceptions import NoGPTContentError


class GPTGateway:
    """Gateway for ChatGPT service"""

    def __init__(self, gpt_client: AsyncOpenAI) -> None:
        self.gpt_client = gpt_client

    async def get_answer(self, api_key: str, prompt: str) -> str:
        """
        Get answer from ChatGPT using prompt

        :param api_key: API key for ChatGPT.
        :param prompt: Prompt for ChatGPT.
        :return: Answer to the client's request.
        """

        self.gpt_client.api_key = api_key

        attempt = 0
        delay = 0.5
        max_tries = 3
        while attempt <= max_tries:
            try:
                response = await self.gpt_client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    model="gpt-3.5-turbo",
                )
                break
            except APIConnectionError:
                attempt += 1
                if attempt > max_tries:
                    raise
                await asyncio.sleep(delay * attempt)
            except Exception:
                raise

        content = response.choices[0].message.content

        if not content:
            raise NoGPTContentError()

        return content
