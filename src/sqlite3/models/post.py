from datetime import datetime
from zoneinfo import ZoneInfo

from sqlmodel import Field, SQLModel
from ulid import ULID

TIME_ZONE = ZoneInfo("Asia/Seoul")


class Post(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ULID()), primary_key=True)
    author: str
    title: str
    content: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(TIME_ZONE), nullable=False
    )
