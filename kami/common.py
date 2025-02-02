from io import BytesIO
from pathlib import Path

from aiogram import Bot


def get_work_dir() -> Path:
    """Get project work dir"""

    return Path(__file__).parent


def get_prompt(prompt_file: str) -> str:
    """
    Get prompt by file name.

    :param prompt_file: File with prompt.
    """

    promt_path = get_work_dir() / "prompts" / prompt_file
    with open(promt_path, encoding="utf-8") as f:
        return f.read()


def get_bot_admin(bot_admin_token: str) -> Bot:
    """
    Get bot admin.

    :Bot: Bot admin.
    """

    return Bot(token=bot_admin_token)


def get_bot_client(bot_client_token: str) -> Bot:
    """
    Get bot client.

    :Bot: Bot client.
    """

    return Bot(token=bot_client_token)


async def get_bytes(file_id: str, bot: Bot) -> bytes:
    """
    Get bytes from telegram file object.

    :param file_id: Telegram file object id.
    """

    photo_io = BytesIO()
    await bot.download(file=file_id, destination=photo_io)

    return photo_io.getvalue()
