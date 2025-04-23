from datetime import datetime
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
from ulid import ULID

from src.sqlite3.connection import get_session
from src.sqlite3.models.post import Post

post_router = APIRouter()

TIME_ZONE = ZoneInfo("Asia/Seoul")

SessionDep = Annotated[Session, Depends(get_session)]


class PostResponse(BaseModel):
    id: str
    author: str
    title: str
    content: str
    created_at: datetime


class PostRequest(BaseModel):
    title: str
    content: str


class DeletePostResponse(BaseModel):
    message: str


@post_router.post(
    "/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED
)
async def create_post(
    post: PostRequest,
    session: SessionDep,
    author: str = Header(..., alias="Author"),
) -> PostResponse:
    new_post = Post(
        id=str(ULID()),
        author=author,
        title=post.title,
        content=post.content,
        created_at=datetime.now(TIME_ZONE),
    )
    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return PostResponse.model_validate(new_post, from_attributes=True)


@post_router.get(
    "/posts", response_model=list[PostResponse], status_code=status.HTTP_200_OK
)
async def get_posts(session: SessionDep) -> list[PostResponse]:
    stmt = select(Post)
    results = session.exec(stmt).all()
    return [
        PostResponse.model_validate(p, from_attributes=True) for p in results
    ]


@post_router.get(
    "/posts/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def get_post(session: SessionDep, post_id: str) -> PostResponse:
    stmt = select(Post).where(Post.id == post_id)
    post = session.exec(stmt).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id '{post_id}' not found.",
        )

    return PostResponse.model_validate(post, from_attributes=True)


@post_router.put(
    "/posts/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def update_post(
    post_id: str,
    post_data: PostRequest,
    session: SessionDep,
    author: str = Header(..., alias="Author"),
) -> PostResponse:
    stmt = select(Post).where(Post.id == post_id)
    post = session.exec(stmt).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id '{post_id}' not found.",
        )

    if post.author != author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not the post owner.",
        )

    post.title = post_data.title
    post.content = post_data.content

    session.add(post)
    session.commit()
    session.refresh(post)

    return PostResponse.model_validate(post, from_attributes=True)


@post_router.delete(
    "/posts/{post_id}",
    response_model=DeletePostResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_post(
    post_id: str,
    session: SessionDep,
    author: str = Header(..., alias="Author"),
) -> DeletePostResponse:
    stmt = select(Post).where(Post.id == post_id)
    post = session.exec(stmt).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id '{post_id}' not found.",
        )

    if post.author != author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not the post owner.",
        )

    session.delete(post)
    session.commit()

    return DeletePostResponse(message=f"Post '{post_id}' deleted successfully.")
