import pytest
from fastapi.exceptions import HTTPException
from httpx import AsyncClient
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from supervisor_gateway.main import app


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 404
    assert response.json() == {
        "code": 40400,
        "detail": "Not Found",
        "message": "PATH_NOT_FOUND",
    }


@pytest.mark.asyncio
async def test_method_not_allowed(client: AsyncClient):
    response = await client.post("/processes")
    assert response.status_code == 405
    assert response.json() == {
        "code": 40500,
        "detail": "Method Not Allowed",
        "message": "METHOD_NOT_ALLOWED",
    }


@pytest.mark.asyncio
async def test_bad_request(client: AsyncClient):
    def bad_request(*args):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="bad_request")

    app.add_route("/_test/bad-request", bad_request, methods=["GET"])
    response = await client.get("/_test/bad-request")
    assert response.status_code == 400
    assert response.json() == {
        "code": 40000,
        "detail": "bad_request",
        "message": "BAD_REQUEST",
    }


@pytest.mark.asyncio
async def test_unknown_http_exception(client: AsyncClient):
    def bad_request(*args):
        raise HTTPException(status_code=HTTP_429_TOO_MANY_REQUESTS, detail="...")

    app.add_route("/_test/too-many-requests", bad_request, methods=["GET"])
    response = await client.get("/_test/too-many-requests")
    assert response.status_code == 500
    assert response.json() == {
        "code": 50000,
        "detail": "",
        "message": "INTERNAL_ERROR",
    }
