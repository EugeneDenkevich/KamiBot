from openai import AsyncOpenAI


class GPTGateway:
    """Gateway for ChatGPT service"""

    def __init__(self, gpt_client: AsyncOpenAI) -> None:
        self.gpt_client = gpt_client
    
    async def get_answer(self, api_key: str, prompt: str) -> str | None:
        """
        Get answer from ChatGPT using prompt
        
        :param api_key: API key for ChatGPT.
        :param prompt: Prompt for ChatGPT.
        :return: Answer to the client's request.
        """

        self.gpt_client.api_key = api_key

        response = await self.gpt_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )

        return response.choices[0].message.content