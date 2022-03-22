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
