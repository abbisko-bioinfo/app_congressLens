import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    res = await client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_api_health(client: AsyncClient):
    res = await client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "version" in data