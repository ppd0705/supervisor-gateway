import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 404
    assert response.json() == {
        "code": 40400,
        "detail": "Not Found",
        "name": "PATH_NOT_FOUND",
    }


@pytest.mark.asyncio
async def test_method_not_allowed(client: AsyncClient):
    response = await client.post("/processes")
    assert response.status_code == 405
    assert response.json() == {
        "code": 40500,
        "detail": "Method Not Allowed",
        "name": "METHOD_NOT_ALLOWED",
    }
