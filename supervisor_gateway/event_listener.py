import asyncio
from typing import Callable

from aiofiles import open as aio_open
from aiofiles.threadpool.binary import AsyncBufferedIOBase

from supervisor_gateway.log import logger

READY = "READY\n"
ACKNOWLEDGED = "RESULT 2\nOK"


async def write(stream: AsyncBufferedIOBase, msg: str):
    await stream.write(msg)
    await stream.flush()


async def read(stream: AsyncBufferedIOBase) -> dict:
    header_line = str(await stream.readline())
    event = {}
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
    def __init__(self, event_handler: Callable):
        self.event_handler = event_handler
        self.running = True

    def stop(self):
        self.running = False

    async def start(self):
        logger.info("event_listener started")
        async with aio_open("/dev/stdout", "w") as std_out:
            async with aio_open("/dev/stdin", "r") as std_in:
                while self.running:
                    try:
                        await write(std_out, READY)
                        event = await read(std_in)
                        self.event_handler(event)
                        logger.debug(f"event: {event}")
                        await write(std_out, ACKNOWLEDGED)
                    except asyncio.CancelledError:
                        logger.info("listener task canceled")
                        break
        logger.info("event_listener stopped")
