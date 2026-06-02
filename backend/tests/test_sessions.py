import pytest
from httpx import AsyncClient


@pytest.fixture
async def conference_id(client: AsyncClient):
    res = await client.post("/api/conferences", json={"acronym": "ASCO", "name": "ASCO 2026", "year": 2026})
    return res.json()["id"]


@pytest.mark.asyncio
async def test_create_session(client: AsyncClient, conference_id: str):
    res = await client.post("/api/sessions", json={
        "conference_id": conference_id,
        "title": "Plenary Session",
        "session_type": "Plenary",
    })
    assert res.status_code == 201
    assert res.json()["title"] == "Plenary Session"


@pytest.mark.asyncio
async def test_list_sessions(client: AsyncClient, conference_id: str):
    await client.post("/api/sessions", json={"conference_id": conference_id, "title": "Session A"})
    res = await client.get(f"/api/sessions?conference_id={conference_id}")
    assert res.status_code == 200
    assert res.json()["total"] >= 1