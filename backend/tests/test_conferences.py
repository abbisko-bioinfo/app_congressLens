import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_conference(client: AsyncClient):
    res = await client.post("/api/conferences", json={
        "acronym": "ASCO",
        "name": "ASCO Annual Meeting",
        "year": 2026,
        "location": "Chicago, IL",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["acronym"] == "ASCO"
    assert data["year"] == 2026
    assert "id" in data
    return data["id"]


@pytest.mark.asyncio
async def test_list_conferences(client: AsyncClient):
    await client.post("/api/conferences", json={"acronym": "ESMO", "name": "ESMO Congress", "year": 2026})
    res = await client.get("/api/conferences")
    assert res.status_code == 200
    assert res.json()["total"] >= 1


@pytest.mark.asyncio
async def test_get_conference(client: AsyncClient):
    create_res = await client.post("/api/conferences", json={"acronym": "AACR", "name": "AACR Annual Meeting", "year": 2026})
    id = create_res.json()["id"]
    res = await client.get(f"/api/conferences/{id}")
    assert res.status_code == 200
    assert res.json()["acronym"] == "AACR"


@pytest.mark.asyncio
async def test_update_conference(client: AsyncClient):
    create_res = await client.post("/api/conferences", json={"acronym": "TEST", "name": "Test Conf", "year": 2025})
    id = create_res.json()["id"]
    res = await client.patch(f"/api/conferences/{id}", json={"location": "Online"})
    assert res.status_code == 200
    assert res.json()["location"] == "Online"