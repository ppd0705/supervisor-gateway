import asyncio
from tempfile import NamedTemporaryFile

import pytest  # noqa
from aiofiles import tempfile  # noqa

from supervisor_gateway.config import conf
from supervisor_gateway.event_listener import listener
from supervisor_gateway.event_listener import read
from supervisor_gateway.event_listener import write
from supervisor_gateway.supervisor import READY


@pytest.mark.asyncio
async def test_write():
    async with tempfile.TemporaryFile(mode="w+") as f:
        for i in range(3):
            await write(f, READY)
        await f.seek(0)
        async for line in f:
            assert line == READY


@pytest.mark.asyncio
async def test_read():
    msg = (
        "ver:3.0 server:lid001 serial:52611 "
        "pool:supervisor_gateway poolserial:13190 eventname:PROCESS_STATE_RUNNING len:69\n"
        "processname:exits_10s groupname:Counter from_state:STARTING pid:31168"
    )
    target = {
        "ver": "3.0",
        "server": "lid001",
        "serial": "52611",
        "pool": "supervisor_gateway",
        "poolserial": "13190",
        "eventname": "PROCESS_STATE_RUNNING",
        "len": "69",
        "payload": {
            "processname": "exits_10s",
            "groupname": "Counter",
            "from_state": "STARTING",
            "pid": "31168",
        },
    }
    async with tempfile.TemporaryFile(mode="w+") as f:
        await write(f, msg)
        await f.seek(0)
        event = await read(f)
        assert event == target


@pytest.mark.asyncio
async def test_listener():
    rets = []

    def handler(event: dict):
        rets.append(event)

    listener.set_handler(handler)
    loop = asyncio.get_event_loop()

    stdin_msg_template = (
        "ver:3.0 server:lid001 serial:52611 "
        "pool:supervisor_gateway poolserial:13190 eventname:PROCESS_STATE_%s len:69\n"
        "processname:%s groupname:Counter from_state:STARTING pid:31168"
    )
    args = [
        ("AAA", "aaaaaaaaa"),
        ("BB", "bbbbbbbbb"),
    ]
    with NamedTemporaryFile() as tmp_stdin:
        with NamedTemporaryFile() as tmp_stdout:
            conf.stdin = tmp_stdin.name
            conf.stdout = tmp_stdout.name

            loop.create_task(listener.start())
            for process_state, process_name in args:
                msg = stdin_msg_template % (process_state, process_name)
                tmp_stdin.write(msg.encode())
                tmp_stdin.flush()
            await asyncio.sleep(1)
            listener.stop()

    assert len(rets) == 2
    for i, event in enumerate(rets):
        assert event["eventname"].rsplit("_", 1)[1] == args[i][0]
        assert event["payload"]["processname"] == args[i][1]
