import uuid
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_conference(client: AsyncClient):
    res = await client.post("/api/conferences", json={
        "acronym": f"CONF-{uuid.uuid4().hex[:6]}",
        "name": "ASCO Annual Meeting",
        "year": 2026,
        "location": "Chicago, IL",
    })
    assert res.status_code == 201
    data = res.json()
    assert "id" in data
    return data["id"]


@pytest.mark.asyncio
async def test_list_conferences(client: AsyncClient):
    res = await client.get("/api/conferences")
    assert res.status_code == 200
    assert res.json()["total"] >= 0


@pytest.mark.asyncio
async def test_get_conference(client: AsyncClient):
    create_res = await client.post("/api/conferences", json={"acronym": f"GET-{uuid.uuid4().hex[:6]}", "name": "Test Conf", "year": 2026})
    id = create_res.json()["id"]
    res = await client.get(f"/api/conferences/{id}")
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_update_conference(client: AsyncClient):
    create_res = await client.post("/api/conferences", json={"acronym": f"UPD-{uuid.uuid4().hex[:6]}", "name": "Test Conf", "year": 2025})
    id = create_res.json()["id"]
    res = await client.patch(f"/api/conferences/{id}", json={"location": "Online"})
    assert res.status_code == 200
    assert res.json()["location"] == "Online"