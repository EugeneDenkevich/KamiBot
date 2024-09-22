from kami.backend.domain.dialog.models import Dialog
from kami.backend.domain.lang_test.enums import RateEnum
from kami.backend.domain.lang_test.models import QuestT
from kami.backend.presentation.ucf import UseCaseFactory


class BackendClient():
    """Base backend interface implementation"""

    def __init__(self, ucf: UseCaseFactory):
        self.ucf = ucf

    def get_example(self) -> str:
        return "Btw, hello from backend client!"

    async def create_dialog(
        self,
        topic: str,
    ) -> Dialog:
        async with self.ucf.create_dialog() as create_dialog:
            return await create_dialog(topic=topic)

    async def start_test(
        self,
        tg_id: str,
    ) -> None:
        async with self.ucf.start_test() as start_test:
            return await start_test(tg_id=tg_id)

    async def ask_one_or_none(
        self,
        tg_id: str,
    ) -> QuestT:
        async with self.ucf.ask_one_or_none() as ask_one_or_none:
            return await ask_one_or_none(tg_id=tg_id)

    async def save_reply(
        self,
        tg_id: str,
        reply: str,
    ) -> None:
        async with self.ucf.save_reply() as save_reply:
            return await save_reply(tg_id=tg_id, reply=reply)

    async def rate_lang_level(
        self,
        tg_id: str,
    ) -> RateEnum:
        async with self.ucf.rate_lang_level() as rate_lang_level:
            return await rate_lang_level(tg_id=tg_id)
