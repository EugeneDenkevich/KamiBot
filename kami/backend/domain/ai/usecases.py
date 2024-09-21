from kami.backend.gateways.chat_gpt.gateway import GPTGateway
from kami.backend.repos.ai.repo import AIRepo


class VoiceToVoiceUseCase:
    """Use case to receive a answer from ChatGPT"""

    def __init__(self, gpt_gateway: GPTGateway, ai_repo: AIRepo) -> None:
        self.gpt_gateway = gpt_gateway
        self.ai_repo = ai_repo
    
    async def __call__(self, prompt: bytes) -> bytes:
        """
        Use case to receive a answer from ChatGPT
        
        :param prompt: Prompt for ChatGPT.
        :return: Answer to the client's request.
        """

        ai = self.ai_repo.get_ai()
        gpt_answer = await self.gpt_gateway.get_answer(api_key=ai.gpt_api_key, prompt=prompt)
        
        return b"foo-bar"
