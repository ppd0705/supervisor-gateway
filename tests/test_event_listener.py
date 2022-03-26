import asyncio
import os

import pytest
from pytest_mock import MockerFixture

from supervisor_gateway.event_listener import listener
from supervisor_gateway.event_listener import open_connection


@pytest.mark.asyncio
async def test_listener(mocker: MockerFixture):
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
    read_fd, write_fd = os.pipe()
    tmp_stdin_r = open(read_fd, "r")
    tmp_stdin_w = open(write_fd, "w")

    read_fd, write_fd = os.pipe()
    tmp_stdout_w = open(write_fd, "w")

    reader, writer = await open_connection(tmp_stdin_r, tmp_stdout_w)
    mock = mocker.patch("supervisor_gateway.event_listener.open_connection")
    mock.return_value = (reader, writer)

    loop.create_task(listener.start())
    for process_state, process_name in args:
        msg = stdin_msg_template % (process_state, process_name)
        tmp_stdin_w.write(msg)
        tmp_stdin_w.flush()
    await asyncio.sleep(0.5)
    listener.stop()

    assert len(rets) == 2
    for i, event in enumerate(rets):
        assert event["eventname"].rsplit("_", 1)[1] == args[i][0]
        assert event["payload"]["processname"] == args[i][1]
