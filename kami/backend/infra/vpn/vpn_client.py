from httpx import AsyncClient


def get_vpn_client(vpn_conn_string: str) -> AsyncClient:
    """
    Get async vpn client.

    :param vpn_conn_string: VPN connection string.
    :return: Async VPN client.
    """

    return AsyncClient(proxy=vpn_conn_string)
