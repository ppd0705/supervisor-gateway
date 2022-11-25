import pytest
from aiohttp_xmlrpc.exceptions import ServerError
from httpx import AsyncClient
from pytest_mock import MockerFixture

from supervisor_gateway.error import InternalError
from supervisor_gateway.error import ProcessNotFoundError
from supervisor_gateway.supervisor import Faults
from supervisor_gateway.supervisor import ProcessStates


@pytest.mark.asyncio
async def test_get_rpc_state(client: AsyncClient, mocker: MockerFixture):
    mock = mocker.patch("supervisor_gateway.xml_rpc.rpc.get_state")
    mock.return_value = {"statename": "AAA"}
    response = await client.get("/rpc/state")
    assert response.status_code == 200
    assert response.json() == {"state": "AAA"}


@pytest.mark.asyncio
async def test_list_rpc_processes(client: AsyncClient, mocker: MockerFixture):
    mock = mocker.patch("supervisor_gateway.xml_rpc.rpc.get_all_process_info")

    data = [
        {
            "name": "AAA",
            "state": ProcessStates.RUNNING,
            "statename": ProcessStates.RUNNING.name,
            "stop": 1,
            "start": 0,
        },
        {
            "name": "BBB",
            "state": ProcessStates.STOPPED,
            "statename": ProcessStates.STOPPED.name,
            "stop": 1,
            "start": 0,
        },
    ]
    mock.return_value = data
    response = await client.get("/rpc/processes")
    assert response.status_code == 200
    assert response.json() == [
        {"name": "AAA", "state": "RUNNING", "from_state": "", "update_time": 0},
        {"name": "BBB", "state": "STOPPED", "from_state": "", "update_time": 1},
    ]


@pytest.mark.asyncio
async def test_get_rpc_process(client: AsyncClient, mocker: MockerFixture):
    mock = mocker.patch("supervisor_gateway.xml_rpc.rpc.get_process_info")

    data = {
        "name": "AAA",
        "state": ProcessStates.RUNNING,
        "statename": "BBB",
        "stop": 1,
        "start": 0,
    }
    mock.return_value = data
    response = await client.get("/rpc/processes/AAA")
    assert response.status_code == 200
    assert response.json() == {
        "name": "AAA",
        "state": "BBB",
        "from_state": "",
        "update_time": 0,
    }

    data["state"] = ProcessStates.STOPPED
    response = await client.get("/rpc/processes/AAA")
    assert response.status_code == 200
    assert response.json() == {
        "name": "AAA",
        "state": "BBB",
        "from_state": "",
        "update_time": 1,
    }

    server_error = ServerError()
    server_error.code = Faults.BAD_NAME
    mock.side_effect = server_error
    response = await client.get("/rpc/processes/AAA")
    assert response.status_code == 404
    assert "code" in response.json()
    assert response.json()["code"] == ProcessNotFoundError.code
    server_error.code = Faults.FAILED
    response = await client.get("/rpc/processes/AAA")
    assert response.status_code == 500
    assert "code" in response.json()
    assert response.json()["code"] == InternalError.code


@pytest.mark.asyncio
async def test_operate_process(client: AsyncClient, mocker: MockerFixture):

    for action, method in [
        ("start", "start_process"),
        ("stop", "stop_process"),
        ("restart", "restart_process"),
        ("add", "add_process_group"),
        ("remove", "remove_process_group"),
    ]:
        mock = mocker.patch(f"supervisor_gateway.xml_rpc.rpc.{method}")
        mock.return_value = True
        response = await client.post(f"/rpc/processes/aaa/{action}")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_operate_processes(client: AsyncClient, mocker: MockerFixture):
    for action, method in [
        ("start", "start_all_processes"),
        ("stop", "stop_all_processes"),
        ("restart", "restart_all_processes"),
    ]:
        mock = mocker.patch(f"supervisor_gateway.xml_rpc.rpc.{method}")
        mock.return_value = True
        response = await client.post(f"/rpc/processes/{action}")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_reread_processes(client: AsyncClient, mocker: MockerFixture):
    data = {"added": ["aaa"], "changed": ["b", "c"], "removed": ["d"]}
    for action, method in [
        ("reread", "reread"),
        ("update", "update_all_processes"),
    ]:
        mock = mocker.patch(f"supervisor_gateway.xml_rpc.rpc.{method}")
        mock.return_value = data
        response = await client.post(f"/rpc/processes/{action}")
        assert response.status_code == 200
        assert response.json() == data
