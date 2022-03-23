from unittest.mock import AsyncMock
from unittest.mock import MagicMock

import pytest
from aiohttp_xmlrpc.exceptions import ServerError
from pytest_mock import MockerFixture

from supervisor_gateway.supervisor import Faults
from supervisor_gateway.xml_rpc import rpc


@pytest.fixture(scope="function")
def rpc_client(mocker: MockerFixture):
    return mocker.patch("supervisor_gateway.xml_rpc.rpc.client")


@pytest.fixture(scope="function")
def rpc_client_system(mocker: MockerFixture, rpc_client: MockerFixture) -> MagicMock:
    return mocker.patch.object(rpc_client, "system", create=True)


@pytest.fixture(scope="function")
def rpc_client_supervisor(
    mocker: MockerFixture, rpc_client: MockerFixture
) -> MagicMock:
    return mocker.patch.object(rpc_client, "supervisor", create=True)


@pytest.mark.asyncio
async def test_init():
    rpc.url = "unix://"
    rpc.init_client()
    assert rpc.client.url == "http://127.0.0.1/RPC2"
    rpc.url = "http://test.com"
    rpc.init_client()
    assert rpc.client.url == rpc.url
    await rpc.close()
    assert rpc.client is None


@pytest.mark.asyncio
async def test_list_methods(mocker: MockerFixture, rpc_client_system: MagicMock):
    async_mock: AsyncMock = AsyncMock()
    mock = mocker.patch.object(
        rpc_client_system, "listMethods", create=True, new=async_mock
    )
    data = ["aaa", "bbb"]
    mock.return_value = data
    ret = await rpc.list_methods()
    assert isinstance(ret, list)
    assert ret == data


@pytest.mark.asyncio
async def test_get_state(mocker: MockerFixture, rpc_client_supervisor: MagicMock):
    async_mock: AsyncMock = AsyncMock()
    mock = mocker.patch.object(
        rpc_client_supervisor, "getState", create=True, new=async_mock
    )
    data = {}
    mock.return_value = data
    ret = await rpc.get_state()
    assert isinstance(ret, dict)
    assert ret == data


@pytest.mark.asyncio
async def test_reread(mocker: MockerFixture, rpc_client_supervisor: MagicMock):
    async_mock: AsyncMock = AsyncMock()
    mock = mocker.patch.object(
        rpc_client_supervisor, "reloadConfig", create=True, new=async_mock
    )
    data = [[[], [], []]]
    mock.return_value = data
    ret = await rpc.reread()
    assert isinstance(ret, list)
    assert ret == data[0]


@pytest.mark.asyncio
async def test_get_all_process_info(
    mocker: MockerFixture, rpc_client_supervisor: MagicMock
):
    async_mock: AsyncMock = AsyncMock()
    mock = mocker.patch.object(
        rpc_client_supervisor, "getAllProcessInfo", create=True, new=async_mock
    )
    data = []
    mock.return_value = data
    ret = await rpc.get_all_process_info()
    assert isinstance(ret, list)
    assert ret == data


@pytest.mark.asyncio
async def test_get_process_info(
    mocker: MockerFixture, rpc_client_supervisor: MagicMock
):
    async_mock: AsyncMock = AsyncMock()
    mock = mocker.patch.object(
        rpc_client_supervisor, "getProcessInfo", create=True, new=async_mock
    )
    data = {}
    mock.return_value = data
    ret = await rpc.get_process_info("aaa")
    assert isinstance(ret, dict)
    assert ret == data


@pytest.mark.asyncio
async def test_operate_process(mocker: MockerFixture, rpc_client_supervisor: MagicMock):

    async_mock: AsyncMock = AsyncMock()
    bad_name_error = ServerError()
    bad_name_error.code = Faults.BAD_NAME
    not_running_error = ServerError()
    not_running_error.code = Faults.NOT_RUNNING
    already_stated_error = ServerError()
    already_stated_error.code = Faults.ALREADY_STARTED
    already_added_error = ServerError()
    already_added_error.code = Faults.ALREADY_ADDED

    for action, format_action in (
        ("start_process", "startProcess"),
        ("stop_process", "stopProcess"),
        ("restart_process", "restartProcess"),
        ("stop_process_group", "stopProcessGroup"),
        ("add_process_group", "addProcessGroup"),
        ("remove_process_group", "removeProcessGroup"),
    ):
        mock = mocker.patch.object(
            rpc_client_supervisor, format_action, create=True, new=async_mock
        )
        func = getattr(rpc, action)
        mock.return_value = True
        mock.side_effect = bad_name_error
        if action != "restart_process":
            with pytest.raises(ServerError) as e:
                await func("aaa")
            assert e.value.code == Faults.BAD_NAME
        if action == "start_process":
            mock.side_effect = already_stated_error
            ret = await func("aaa")
            assert ret is True
        elif action == "stop_process":
            mock.side_effect = not_running_error
            ret = await func("aaa")
            assert ret is True
        elif action == "add_process_group":
            mock.side_effect = already_added_error
            ret = await func("aaa")
            assert ret is True

        mock.side_effect = None
        ret = await func("aaa")
        assert ret is True
