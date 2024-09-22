from httpx import AsyncClient


def get_vpn_client(vpn_host: str, vpn_port: int) -> AsyncClient:
    return AsyncClient(
        proxy=f"socks5://{vpn_host}:{vpn_port}",
    )
