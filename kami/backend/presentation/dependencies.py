from kami.backend.presentation.client import BackendClient
from kami.backend.presentation.ucf import UseCaseFactory
from kami.backend.repos.dependencies import get_async_engine, get_async_sessionmaker
from kami.settings import get_settings


async def get_ucf() -> UseCaseFactory:
    """Get usecase factory (U.C.F.)"""

    settings = get_settings()
    engine_factory = get_async_engine(settings=settings)
    engine = await anext(engine_factory)
    session_factory = await get_async_sessionmaker(engine)

    return UseCaseFactory(
        session_factory=session_factory,
    )


async def get_backend_client() -> BackendClient:
    """Get backend_client"""

    return BackendClient(
        ucf=await get_ucf(),
    )
