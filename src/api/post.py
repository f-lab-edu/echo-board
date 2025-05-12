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

# TODO: 의존성 주입에 대해 설명하기.
SessionDep = Annotated[Session, Depends(get_session)]


class PostResponse(BaseModel):
    id: str
    author: str
    title: str
    content: str
    # TODO: 시각에 대한 표현방법(ISO-8601, unix timestamp 등)이 어떤 것들이 있는지 설명하기.
    created_at: datetime


class PostRequest(BaseModel):
    title: str
    content: str


class DeletePostResponse(BaseModel):
    message: str


@post_router.post(
    "/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED
)
def create_post(
    post: PostRequest,
    session: SessionDep,
    author: str = Header(..., alias="Author"),
) -> PostResponse:
    # TODO: id를 만드는 여러 방식에 대해 설명하기.
    new_post = Post(
        id=str(ULID()),
        author=author,
        title=post.title,
        content=post.content,
        created_at=datetime.now(TIME_ZONE),
    )
    session.add(new_post)
    session.commit()

    # TODO: refersh와 flush의 차이 설명하기
    session.refresh(new_post)

    return PostResponse.model_validate(new_post, from_attributes=True)


@post_router.get(
    "/posts", response_model=list[PostResponse], status_code=status.HTTP_200_OK
)
def get_posts(session: SessionDep) -> list[PostResponse]:
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
def get_post(session: SessionDep, post_id: str) -> PostResponse:
    stmt = select(Post).where(Post.id == post_id)
    post = session.exec(stmt).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            # TODO: 에러 메시지는 어떻게 작성하는 것이 좋은지 설명하기.
            detail=f"Post with id '{post_id}' not found.",
        )

    return PostResponse.model_validate(post, from_attributes=True)


@post_router.put(
    "/posts/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
def update_post(
    post_id: str,
    post_data: PostRequest,
    session: SessionDep,
    author: str = Header(..., alias="Author"),
) -> PostResponse:
    stmt = select(Post).where(Post.id == post_id)
    post = session.exec(stmt).first()

    if post is None:
        raise HTTPException(
            # TODO: 2XX, 4XX 등 Status Code들 설명하기 (401, 403, 404, 405, 409 설명 할 수 있어야 함)
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
def delete_post(
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

    # Hard / Soft Delete 차이 설명하기.
    session.delete(post)
    session.commit()

    # TODO: 함수의 반환 값으로 dict를 사용하는게 왜 좋지 않은지, 클래스를 쓰는게 왜 더 좋은지 설명하기.
    return DeletePostResponse(message=f"Post '{post_id}' deleted successfully.")
