import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_health(client: AsyncClient):
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
