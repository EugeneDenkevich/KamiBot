from kami.backend.infra.elevenlabs.client_elevenlabs import get_elevenlabs_client
from kami.backend.infra.gpt.client_gpt import get_gpt_client
from kami.backend.infra.vpn.vpn_client import get_vpn_client
from kami.backend.infra.whisper.client_whisper import get_whisper_client
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

    vpn_client = None
    if settings.vpn_conn_string:
        vpn_client = get_vpn_client(
            vpn_conn_string=settings.vpn_conn_string,
        )

    gpt_client = get_gpt_client(vpn_client=vpn_client)

    whisper_client = get_whisper_client(vpn_client=vpn_client)

    elevenlabs_client = get_elevenlabs_client()

    return UseCaseFactory(
        session_factory=session_factory,
        gpt_client=gpt_client,
        whisper_client=whisper_client,
        elevenlabs_client=elevenlabs_client,
        context_limit=settings.context_limit,
        admin_id=settings.admin_id,
        test_count=settings.test_count,
    )


async def get_backend_client() -> BackendClient:
    """Get backend_client"""

    return BackendClient(
        ucf=await get_ucf(),
    )
