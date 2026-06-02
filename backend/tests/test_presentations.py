import uuid
import pytest
from httpx import AsyncClient


@pytest.fixture
async def conference_id(client: AsyncClient):
    res = await client.post("/api/conferences", json={"acronym": f"PRES-{uuid.uuid4().hex[:6]}", "name": "Test Conf", "year": 2026})
    return res.json()["id"]


@pytest.fixture
async def presentation_id(client: AsyncClient, conference_id: str):
    res = await client.post("/api/presentations", json={
        "conference_id": conference_id,
        "title": "Test Presentation",
    })
    return res.json()["id"]


@pytest.mark.asyncio
async def test_create_presentation(client: AsyncClient, conference_id: str):
    res = await client.post("/api/presentations", json={
        "conference_id": conference_id,
        "title": "Novel therapy",
        "presentation_type": "Oral",
    })
    assert res.status_code == 201
    assert res.json()["title"] == "Novel therapy"


@pytest.mark.asyncio
async def test_list_presentations(client: AsyncClient, conference_id: str):
    await client.post("/api/presentations", json={"conference_id": conference_id, "title": "Pres A"})
    res = await client.get(f"/api/presentations?conference_id={conference_id}")
    assert res.status_code == 200
    assert res.json()["total"] >= 1


@pytest.mark.asyncio
async def test_search_presentations(client: AsyncClient, conference_id: str):
    await client.post("/api/presentations", json={"conference_id": conference_id, "title": "Immunotherapy breakthrough"})
    res = await client.get("/api/presentations?query=immunotherapy")
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_comments_crud(client: AsyncClient, presentation_id: str):
    res = await client.post(f"/api/presentations/{presentation_id}/comments", json={"body": "Great talk!", "author": "Dr. Smith"})
    assert res.status_code == 201
    comment_id = res.json()["id"]

    res = await client.get(f"/api/presentations/{presentation_id}/comments")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    res = await client.patch(f"/api/comments/{comment_id}", json={"body": "Updated comment"})
    assert res.status_code == 200
    assert res.json()["body"] == "Updated comment"

    res = await client.delete(f"/api/comments/{comment_id}")
    assert res.status_code == 204