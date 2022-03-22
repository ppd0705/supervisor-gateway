import asyncio
from typing import Callable
from typing import Dict
from typing import Union

from aiofiles import open as aio_open
from aiofiles.threadpool.text import AsyncTextIOWrapper

from supervisor_gateway.config import conf
from supervisor_gateway.log import logger
from supervisor_gateway.supervisor import ACKNOWLEDGED
from supervisor_gateway.supervisor import READY


async def write(stream: AsyncTextIOWrapper, msg: str):
    await stream.write(msg)
    await stream.flush()


async def read(stream: AsyncTextIOWrapper) -> Dict[str, Union[str, Dict]]:
    header_line = await stream.readline()
    event: Dict = {}
    for line in header_line.split():
        k, v = line.split(":", 1)
        event[k] = v
    payload_str = str(await stream.read(int(event["len"])))
    payload = {}
    for line in payload_str.split():
        k, v = line.split(":", 1)
        payload[k] = v
    event["payload"] = payload
    return event


class Listener:
    def __init__(self, handler: Callable[[dict], None] = None):
        self.handler = handler
        self.running = True

    def set_handler(self, handler: Callable[[dict], None]):
        self.handler = handler

    def stop(self):
        self.running = False

    async def start(self):
        logger.info("event_listener started")
        async with aio_open(conf.stdout, "w") as std_out:
            async with aio_open(conf.stdin, "r") as std_in:
                while self.running:
                    try:
                        await write(std_out, READY)
                        event = await read(std_in)
                        self.handler(event)
                        logger.debug(f"event: {event}")
                        await write(std_out, ACKNOWLEDGED)
                    except asyncio.CancelledError:
                        logger.info("listener task canceled")
                        break
        logger.info("event_listener stopped")


listener = Listener()
