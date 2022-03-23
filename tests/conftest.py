import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient

from supervisor_gateway.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
