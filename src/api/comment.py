from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.domain.comment import CommentCreateRequest, CommentResponse
from src.service.comment import (
    create_comment_service,
    get_comments_by_author_service,
    get_comments_by_post_service,
)
from src.sqlite3.connection import get_session

SessionDep = Annotated[Session, Depends(get_session)]

comment_router = APIRouter()


@comment_router.post(
    "/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(data: CommentCreateRequest, session: SessionDep):
    return create_comment_service(data, session)


@comment_router.get(
    "/comments/by-author/{author_id}", response_model=list[CommentResponse]
)
def get_comments_by_author(
    author_id: str,
    session: SessionDep,
):
    return get_comments_by_author_service(author_id, session)


@comment_router.get(
    "/comments/by-post/{post_id}", response_model=list[CommentResponse]
)
def get_comments_by_post(
    post_id: str,
    session: SessionDep,
):
    return get_comments_by_post_service(post_id, session)
