import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from supervisor_gateway.error import InvalidParameterError

mock_local_data = {
    "AAA": {"name": "AAA", "state": "aaa", "from_state": "", "update_time": 1},
    "ABB": {"name": "ABB", "state": "bbb", "from_state": "aaa", "update_time": 2},
    "CCC": {"name": "CCC", "state": "bbb", "from_state": "", "update_time": 3},
}


@pytest.mark.asyncio
async def test_list_processes(client: AsyncClient, mocker: MockerFixture):
    mocker.patch.dict("supervisor_gateway.local_state.state.processes", mock_local_data)
    response = await client.get("/processes")
    assert response.status_code == 200
    assert response.json() == {"total": 3, "processes": list(mock_local_data.values())}

    response = await client.get(
        "/processes",
        params={
            "limit": 1,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "total": 3,
        "processes": list(mock_local_data.values())[:1],
    }

    response = await client.get(
        "/processes",
        params={
            "limit": 1,
            "page": 2,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "total": 3,
        "processes": list(mock_local_data.values())[1:2],
    }

    response = await client.get(
        "/processes", params={"limit": 1, "page": 2, "status": "bbb"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "total": 2,
        "processes": list(mock_local_data.values())[2:3],
    }

    response = await client.get(
        "/processes",
        params={
            "keywords": "A",
            "status": "bbb",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "total": 1,
        "processes": list(mock_local_data.values())[1:2],
    }

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
    assert data["message"] == InvalidParameterError.message
    assert isinstance(data["detail"], str)


@pytest.mark.asyncio
async def test_get_processes(client: AsyncClient, mocker: MockerFixture):
    mocker.patch.dict("supervisor_gateway.local_state.state.processes", mock_local_data)
    process = "not_found"
    response = await client.get(f"/processes/{process}")
    assert response.status_code == 404
    error = response.json()
    assert error.get("code", 0) == 40401

    process = "ABB"
    response = await client.get(f"/processes/{process}")
    assert response.status_code == 200
    assert response.json() == mock_local_data[process]
