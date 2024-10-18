import asyncio
import logging
import time

from aiogram import Bot

semaphore = asyncio.Semaphore(30)


async def send_photo(
    bot: Bot,
    chat_id: int,
    photo: str,
    caption: str | None = None,
) -> None:
    """
    Send photo with semaphore pattern.

    :param bot: Bot.
    :param chat_id: Chat id.
    :param photo: Photo telegram id.
    :param caption: Caption for photo.
    """

    async with semaphore:
        async with bot:
            start_time = time.time()
            await bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                parse_mode="html",
            )
            duration = time.time() - start_time
            logging.info(
                 f"Photo was sent: telegram_id: {chat_id}",
            )
            if duration < 1:
                await asyncio.sleep(1 - duration)


async def send_video(
    bot: Bot,
    chat_id: int,
    video: str,
    caption: str | None = None,
) -> None:
    """
    Send photo with semaphore pattern.

    :param bot: Bot.
    :param chat_id: Chat id.
    :param video: Video telegram id.
    :param caption: Caption for video.
    """

    async with semaphore:
        async with bot:
            start_time = time.time()
            await bot.send_video(
                chat_id=chat_id,
                video=video,
                caption=caption,
                parse_mode="html",
            )
            duration = time.time() - start_time
            logging.info(
                f"Video was sent: telegram_id: {chat_id}",
            )
            if duration < 1:
                await asyncio.sleep(1 - duration)


async def send_video_note(
    bot: Bot,
    chat_id: int,
    video_note: str,
) -> None:
    """
    Send photo with semaphore pattern.

    :param bot: Bot.
    :param chat_id: Chat id.
    :param video_note: Video note telegram id.
    """

    async with semaphore:
        async with bot:
            start_time = time.time()
            await bot.send_video_note(
                chat_id=chat_id,
                video_note=video_note,
            )
            duration = time.time() - start_time
            logging.info(
                 f"Video note was sent: telegram_id: {chat_id}",
            )

            if duration < 1:
                await asyncio.sleep(1 - duration)


async def send_text(
    bot: Bot,
    chat_id: int,
    text: str,
) -> None:
    """
    Send photo with semaphore pattern.

    :param bot: Bot.
    :param chat_id: Chat id.
    :param text: Text of message.
    """

    async with semaphore:
        async with bot:
            start_time = time.time()
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="html",
            )
            duration = time.time() - start_time
            logging.info(
                 f"Message was sent: telegram_id: {chat_id}",
            )
            if duration < 1:
                await asyncio.sleep(1 - duration)
