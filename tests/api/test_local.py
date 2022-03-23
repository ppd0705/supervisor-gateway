import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from supervisor_gateway.error import InvalidParameterError


@pytest.mark.asyncio
async def test_list_processes(client: AsyncClient, mocker: MockerFixture):
    data = {
        "AAA": {"name": "AAA", "state": "aaa", "update_time": 1},
        "ABB": {"name": "ABB", "state": "bbb", "update_time": 2},
        "CCC": {"name": "CCC", "state": "bbb", "update_time": 3},
    }
    mocker.patch.dict("supervisor_gateway.local_state.state.processes", data)
    response = await client.get("/processes")
    assert response.status_code == 200
    assert response.json() == {"total": 3, "processes": list(data.values())}

    response = await client.get(
        "/processes",
        params={
            "limit": 1,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"total": 3, "processes": list(data.values())[:1]}

    response = await client.get(
        "/processes",
        params={
            "limit": 1,
            "page": 2,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"total": 3, "processes": list(data.values())[1:2]}

    response = await client.get(
        "/processes", params={"limit": 1, "page": 2, "status": "bbb"}
    )
    assert response.status_code == 200
    assert response.json() == {"total": 2, "processes": list(data.values())[2:3]}

    response = await client.get(
        "/processes",
        params={
            "keywords": "A",
            "status": "bbb",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"total": 1, "processes": list(data.values())[1:2]}

    response = await client.get(
        "/processes",
        params={
            "page": "A",
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert sorted(data) == sorted(InvalidParameterError().dict())
    assert data["code"] == InvalidParameterError.code
    assert data["name"] == InvalidParameterError.name
    assert isinstance(data["detail"], list)
