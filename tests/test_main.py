import pytest
from pytest_mock import MockerFixture

from supervisor_gateway.event_listener import listener
from supervisor_gateway.main import app
from supervisor_gateway.xml_rpc import rpc


@pytest.mark.asyncio
async def test_on_event(mocker: MockerFixture):
    mock = mocker.patch("supervisor_gateway.xml_rpc.rpc.get_state")
    mock.return_value = {"statename": "AAA"}
    mock = mocker.patch("supervisor_gateway.xml_rpc.rpc.get_all_process_info")
    mock.return_value = []
    mocker.patch("supervisor_gateway.event_listener.listener.start")
    await app.router.startup()
    assert rpc.client is not None
    assert listener.handler is not None
    await app.router.shutdown()
    assert rpc.client is None
    assert listener.running is False
