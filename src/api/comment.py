from typing import Annotated

from fastapi import APIRouter, Depends, Header, status
from sqlmodel import Session

from src.domain.comment import (
    CommentCreateRequest,
    CommentResponse,
)
from src.service.comment import (
    create_comment_service,
)
from src.sqlite3.connection import get_session

SessionDep = Annotated[Session, Depends(get_session)]

comment_router = APIRouter()


@comment_router.post(
    "/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    data: CommentCreateRequest,
    session: SessionDep,
    author: str = Header(..., alias="Author"),
):
    return create_comment_service(data, session, author)
