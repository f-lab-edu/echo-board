from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from ulid import ULID

TIME_ZONE = ZoneInfo("Asia/Seoul")


class Post(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ULID()), primary_key=True)
    author_id: str = Field(foreign_key="user.id", nullable=False)
    title: str
    content: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(TIME_ZONE), nullable=False
    )


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
