import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize(
    "payload",
    [
        {
            "author": "kimcoding",
            "title": "First Post",
            "content": "This is the first test post.",
        },
        {
            "author": "parkcoding",
            "title": "Second Post",
            "content": "This is the second test post.",
        },
    ],
)
@pytest.mark.asyncio
async def test_create_post(client: AsyncClient, payload: dict):
    response = await client.post("/api/posts", json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["author"] == payload["author"]
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_post_list_persists(client: AsyncClient):
    response = await client.get("/api/posts")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 2


@pytest.mark.asyncio
async def test_get_post_by_id_persists(client: AsyncClient):
    payload = {
        "author": "ecoding",
        "title": "Third Post",
        "content": "This is the third test post.",
    }
    create_response = await client.post("/api/posts", json=payload)
    post_id = create_response.json()["id"]

    response = await client.get(f"/api/posts/{post_id}")
    data = response.json()
    assert response.status_code == status.HTTP_200_OK

    assert data["id"] == post_id
    assert data["author"] == payload["author"]
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]


@pytest.mark.asyncio
async def test_get_post_not_found(client: AsyncClient):
    invalid_id = "non-id"
    response = await client.get(f"/api/posts/{invalid_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Post not found"
