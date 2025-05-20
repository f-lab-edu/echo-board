from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from ulid import ULID

TIME_ZONE = ZoneInfo("Asia/Seoul")


class Comment(SQLModel, table=True):
    comment_id: str = Field(
        default_factory=lambda: str(ULID()), primary_key=True
    )
    author_id: str = Field(foreign_key="user.id")
    post_id: str = Field(foreign_key="post.id")
    content: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(TIME_ZONE), nullable=False
    )


class CommentResponse(BaseModel):
    comment_id: str
    author_id: str
    post_id: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CommentCreateRequest(BaseModel):
    author_id: str
    post_id: str
    content: str
