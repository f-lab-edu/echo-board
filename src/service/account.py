from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, select

from src.domain.user import User, UserCreateRequest, UserResponse
from src.service.password import hash_password
from src.sqlite3.connection import get_session

SessionDep = Annotated[Session, Depends(get_session)]


def check_user(user_id: str, session: SessionDep) -> bool:
    stmt = select(User).where(User.id == user_id)
    user = session.exec(stmt).first()
    return user is not None


def check_user_by_nickname(nickname: str, session: SessionDep) -> bool:
    stmt = select(User).where(User.nickname == nickname)
    user = session.exec(stmt).first()
    return user is not None


def create_user_service(
    data: UserCreateRequest, session: SessionDep
) -> UserResponse:
    new_user = User(
        username=data.username,
        nickname=data.nickname,
        password=hash_password(data.password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return UserResponse.model_validate(new_user)
