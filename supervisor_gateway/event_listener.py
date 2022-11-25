import asyncio
import sys
from asyncio import StreamReader
from asyncio import StreamReaderProtocol
from asyncio import StreamWriter
from typing import Callable
from typing import Dict
from typing import Tuple
from typing import Union

from supervisor_gateway.log import logger
from supervisor_gateway.supervisor import ACKNOWLEDGED
from supervisor_gateway.supervisor import READY


class StandardStreamReaderProtocol(StreamReaderProtocol):
    def connection_made(self, transport):
        if self._stream_reader._transport is not None:  # noqa
            return
        super().connection_made(transport)


async def write(stream: StreamWriter, msg: str):
    stream.write(msg.encode())
    await stream.drain()


async def read(stream: StreamReader) -> Dict[str, Union[str, Dict]]:
    data = await stream.readline()
    header_line = data.decode()
    event: Dict = {}
    for line in header_line.split():
        k, v = line.split(":", 1)
        event[k] = v
    data = await stream.read(int(event["len"]))
    payload_str = data.decode()
    payload = {}
    for line in payload_str.split():
        k, v = line.split(":", 1)
        payload[k] = v
    event["payload"] = payload
    return event


async def open_connection(
    in_pipe=sys.stdin,
    out_pipe=sys.stdout,
) -> Tuple[StreamReader, StreamWriter]:
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader(loop=loop)
    protocol = StandardStreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, in_pipe)

    out_transport_connect = loop.connect_write_pipe(lambda: protocol, out_pipe)
    out_transport, _ = await out_transport_connect
    writer = asyncio.StreamWriter(out_transport, protocol, reader, loop)
    return reader, writer


class Listener:
    def __init__(self, handler: Callable[[dict], None] = None):
        self.handler = handler
        self.running = False

    def set_handler(self, handler: Callable[[dict], None]):
        self.handler = handler

    def stop(self):
        self.running = False

    async def start(self):
        self.running = True
        logger.info("event_listener started")
        reader, writer = await open_connection()
        while self.running:
            await write(writer, READY)
            event = await read(reader)
            logger.debug(f"event: {event}")
            self.handler(event)
            await write(writer, ACKNOWLEDGED)


listener = Listener()
