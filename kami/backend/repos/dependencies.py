from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from kami.backend.infra.db import Base
from kami.settings import Settings


async def get_async_engine(
    settings: Settings,
) -> AsyncGenerator[AsyncEngine, None]:
    """
    Get async DB engine.

    :param settings: Project settings.
    :return: Async DB engine.
    """

    engine = create_async_engine(
        url=settings.get_db_url(),
        future=True,
        pool_pre_ping=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


async def get_async_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """
    Get async DB session using provided async engine.

    :param settings: Async DB engine.
    :return: Async DB session.
    """

    return async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
