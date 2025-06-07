from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from ulid import ULID

TIME_ZONE = ZoneInfo("Asia/Seoul")


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ULID()), primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    nickname: str = Field(unique=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(TIME_ZONE), nullable=False
    )


class UserCreateRequest(BaseModel):
    # TODO: 서비스 레벨에서 값을 검증하는 것과, API 레벨에서 검증하는 것. 섞여있네요.
    # 언제 서비스 레벨에서 검증해야 하고, 언제 API 레벨에서 검증해야할까요?
    # 레이어드 아키텍처에서 API 레이어와 비즈니스, 도메인 레이어의 역할에 대해 찾아보세요!
    username: str = Field(
        min_length=3, max_length=30, description="Unique user ID"
    )
    nickname: str = Field(
        min_length=2, max_length=20, description="User display name"
    )
    password: str = Field(
        min_length=8, max_length=30, description="User display name"
    )


class UserResponse(BaseModel):
    id: str
    username: str
    nickname: str

    model_config = {
        "from_attributes": True,
    }
