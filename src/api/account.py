from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.domain.user import UserCreateRequest, UserResponse
from src.service.account import (
    check_user,
    check_user_by_nickname,
    create_user_service,
)
from src.service.password import validate_password
from src.sqlite3.connection import get_session

auth_router = APIRouter()

TIME_ZONE = ZoneInfo("Asia/Seoul")

# TODO: 의존성 주입에 대해 설명하기.
SessionDep = Annotated[Session, Depends(get_session)]


@auth_router.post(
    "/auth", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(data: UserCreateRequest, session: SessionDep) -> None:
    if check_user(data.username, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists.",
        )

    if check_user_by_nickname(data.nickname, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Nickname already in use.",
        )

    validate_password(data.password)

    return create_user_service(data, session)
