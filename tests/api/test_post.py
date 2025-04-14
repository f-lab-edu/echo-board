import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize(
    "author, payload",
    [
        (
            "kimcoding",
            {
                "title": "First Post",
                "content": "This is the first test post.",
            },
        ),
        (
            "parkcoding",
            {
                "title": "Second Post",
                "content": "This is the second test post.",
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_post(client: AsyncClient, author: str, payload: dict):
    response = await client.post(
        "/api/posts", json=payload, headers={"X-Author": author}
    )
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["author"] == author
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
    author = "ecoding"
    payload = {
        "title": "Third Post",
        "content": "This is the third test post.",
    }
    create_response = await client.post(
        "/api/posts", json=payload, headers={"X-Author": author}
    )
    post_id = create_response.json()["id"]

    response = await client.get(f"/api/posts/{post_id}")
    data = response.json()
    assert response.status_code == status.HTTP_200_OK

    assert data["id"] == post_id
    assert data["author"] == author
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]


@pytest.mark.asyncio
async def test_get_post_not_found(client: AsyncClient):
    invalid_id = "non-id"
    response = await client.get(f"/api/posts/{invalid_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Post not found"


@pytest.mark.asyncio
async def test_update_post_success(client: AsyncClient):
    author = "test_author"
    post_data = {
        "title": "First Post",
        "content": "This is the first test post.",
    }
    create_response = await client.post(
        "/api/posts", json=post_data, headers={"X-Author": author}
    )
    post_id = create_response.json()["id"]

    updated_data = {"title": "Updated Title", "content": "Updated Content"}
    response = await client.put(
        f"/api/posts/{post_id}",
        json=updated_data,
        headers={"X-Author": author},
    )
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["title"] == updated_data["title"]
    assert data["content"] == updated_data["content"]
    assert data["author"] == author


@pytest.mark.asyncio
async def test_delete_post_success(client: AsyncClient):
    author = "deleter"
    create_response = await client.post(
        "/api/posts",
        json={"title": "Post to delete", "content": "soon gone"},
        headers={"X-Author": author},
    )
    post_id = create_response.json()["id"]

    response = await client.delete(
        f"/api/posts/{post_id}",
        headers={"X-Author": author},
    )
    assert response.status_code == status.HTTP_200_OK
    assert "deleted successfully" in response.json()["message"]
