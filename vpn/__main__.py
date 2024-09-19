import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple, Union

from vpn.settings import get_settings

logger = logging.getLogger(name="vpn-logger")
handler = logging.StreamHandler()
logger.addHandler(hdlr=handler)
logger.setLevel(level=logging.INFO)


async def exec_command(
    *command: Tuple[str],
    input: Optional[Union[bytes, bytearray, memoryview]] = None,
    more_logs: Optional[bool] = False,
) -> None:
    """
    Async runnig subprocess with some command.

    :param command: List of arguments for building bash command.
    :param input: Input for sending to process.
    """

    process = await asyncio.subprocess.create_subprocess_exec(
        *command,  # type: ignore[arg-type]
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate(input=input)

    if more_logs:
        logger.info(f"{stdout.decode()}")
        logger.info(f"{stderr.decode()}")
        logger.info("-----------------")


async def run_ssh(date: str, server: str) -> None:
    """
    Connect to vpn server by ssh protocol.

    :param date: Date.
    :param server: DNS server.
    """

    settings = get_settings()

    start = time.monotonic()
    await exec_command(
        *(  # type: ignore[arg-type]
            f"sshpass -p 1234567890 ssh {date}-vpnjantit.com@{server}.vpnjantit.com "
            f"-ND 0.0.0.0:{settings.vpn_port} -o ExitOnForwardFailure=yes"
        ).split(),
    )
    stop = time.monotonic()

    logger.info(f"connection to {date}@{server} took {stop-start} seconds")


async def connect() -> None:
    """Connect to VPN"""

    try:
        while 1:
            now = datetime.now()
            day = timedelta(days=1)

            await asyncio.gather(
                *[
                    run_ssh(date, server)
                    for server in "nl1 nl2 nl3 nl4".split()
                    for date in [
                        f"{d.day:02d}{d.month:02d}"
                        for d in [
                            now - offset * day for offset in range(-2, 10)
                        ]
                    ]
                ],
            )
            logger.info(f"\nwaiting... {time.asctime()}\n")
            await asyncio.sleep(1)
    finally:
        await asyncio.sleep(0.1)


def main() -> None:
    """Program entrypoint"""

    asyncio.run(connect())


__name__ == "__main__" and main()  # type: ignore[func-returns-value]
