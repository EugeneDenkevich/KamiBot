from typing import Optional, Tuple, Union

from kami.backend.domain.dialog.models import ContextT, Dialog
from kami.backend.domain.lang_test.enums import RateEnum
from kami.backend.domain.lang_test.models import QuestT
from kami.backend.domain.user.models import User
from kami.backend.presentation.ucf import UseCaseFactory


class BackendClient():
    """Base backend interface implementation"""

    def __init__(self, ucf: UseCaseFactory):
        self.ucf = ucf

    async def create_dialog(
        self,
        tg_id: str,
        topic: str,
        context: ContextT,
    ) -> Dialog:
        async with self.ucf.create_dialog() as create_dialog:
            return await create_dialog(tg_id=tg_id, topic=topic)

    async def start_test(
        self,
        tg_id: str,
    ) -> None:
        async with self.ucf.start_test() as start_test:
            return await start_test(tg_id=tg_id)

    async def ask_one(
        self,
        tg_id: str,
    ) -> QuestT:
        async with self.ucf.ask_one() as ask_one:
            return await ask_one(tg_id=tg_id)

    async def save_reply(
        self,
        tg_id: str,
        reply: Union[str, bytes],
    ) -> None:
        async with self.ucf.save_reply() as save_reply:
            return await save_reply(tg_id=tg_id, reply=reply)

    async def rate_lang_level(
        self,
        tg_id: str,
    ) -> RateEnum:
        async with self.ucf.rate_lang_level() as rate_lang_level:
            return await rate_lang_level(tg_id=tg_id)

    async def continue_dialog(
        self,
        tg_id: str,
        voice: bytes,
    ) -> Tuple[bytes, Optional[str]]:
        async with self.ucf.continue_dialog() as continue_dialog:
            return await continue_dialog(tg_id=tg_id, voice=voice)

    async def start_dialog(
        self,
        tg_id: str,
        topic: str,
    ) -> bytes:
        async with self.ucf.start_dialog() as start_dialog:
            return await start_dialog(tg_id=tg_id, topic=topic)

    async def create_user(
        self,
        tg_id: str,
        fio: str,
        phone: str,
        username: Optional[str] = None,
    ) -> User:
        async with self.ucf.create_user() as create_user:
            return await create_user(
                tg_id=tg_id,
                fio=fio,
                phone=phone,
                username=username,
            )

    async def get_user(
        self,
        tg_id: str,
    ) -> User:
        async with self.ucf.get_user() as get_user:
            return await get_user(tg_id=tg_id)

    async def update_user(
        self,
        tg_id: str,
        fio: Optional[str] = None,
        phone: Optional[str] = None,
        username: Optional[str] = None,
        active: Optional[bool] = None,
        onboarded: Optional[bool] = None,
    ) -> User:
        async with self.ucf.update_user() as update_user:
            return await update_user(
                tg_id=tg_id,
                fio=fio,
                phone=phone,
                username=username,
                active=active,
                onboarded=onboarded,
            )

    async def get_dialog(
        self,
        tg_id: str,
    ) -> Dialog:
        async with self.ucf.get_dialog() as get_dialog:
            return await get_dialog(tg_id=tg_id)

    async def return_to_dialog(
        self,
        tg_id: str,
    ) -> bytes:
        async with self.ucf.return_to_dialog() as return_to_dialog:
            return await return_to_dialog(tg_id=tg_id)
