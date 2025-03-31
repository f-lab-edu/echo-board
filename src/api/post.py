from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

post_router = APIRouter()

TIME_ZONE = ZoneInfo("Asia/Seoul")


class PostResponse(BaseModel):
    id: str
    author: str
    title: str
    content: str
    created_at: datetime


class PostRequest(BaseModel):
    author: str
    title: str
    content: str


posts: list[PostResponse] = []


@post_router.post(
    "/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED
)
async def create_post(post: PostRequest) -> PostResponse:
    new_post = PostResponse(
        id=str(uuid4()),
        author=post.author,
        title=post.title,
        content=post.content,
        created_at=datetime.now(TIME_ZONE),
    )
    posts.append(new_post)
    return new_post


@post_router.get(
    "/posts", response_model=list[PostResponse], status_code=status.HTTP_200_OK
)
async def get_posts() -> list[PostResponse]:
    return posts


@post_router.get(
    "/posts/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def get_post(post_id: str) -> PostResponse:
    post = next((p for p in posts if p.id == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
