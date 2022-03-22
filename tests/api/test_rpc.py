import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture


@pytest.mark.asyncio
async def test_get_rpc_state(client: AsyncClient, mocker: MockerFixture):
    mock = mocker.patch("supervisor_gateway.xml_rpc.rpc.get_state")
    mock.return_value = {"statename": "AAA"}
    response = await client.get("/rpc/state")
    assert response.status_code == 200
    assert response.json() == {"state": "AAA"}


@pytest.mark.asyncio
async def test_get_rpc_process(client: AsyncClient, mocker: MockerFixture):
    mock = mocker.patch("supervisor_gateway.xml_rpc.rpc.get_process_info")
    mock.return_value = {
        "name": "AAA",
        "state": 20,
        "statename": "BBB",
        "stop": 1,
        "start": 0,
    }
    response = await client.get("/rpc/processes/AAA")
    assert response.status_code == 200
    assert response.json() == {"name": "AAA", "state": "BBB", "update_time": 0}

    mock.return_value = {
        "name": "AAA",
        "state": 0,
        "statename": "BBB",
        "stop": 1,
        "start": 0,
    }
    response = await client.get("/rpc/processes/AAA")
    assert response.status_code == 200
    assert response.json() == {"name": "AAA", "state": "BBB", "update_time": 1}
