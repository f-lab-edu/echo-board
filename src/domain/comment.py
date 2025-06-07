from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from ulid import ULID

TIME_ZONE = ZoneInfo("Asia/Seoul")


class Comment(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ULID()), primary_key=True)
    author_id: str = Field(foreign_key="user.id")
    post_id: str = Field(foreign_key="post.id")
    content: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(TIME_ZONE), nullable=False
    )
    # TODO: updated_at 이 없군요!
    # 보통 created_at은 필수적으로 두고, 수정될 여지가 있는 엔티티들은 updated_at 도 같이 둡니다.
    # 수정될 여지가 없는 (ex. 로그, 이벤트 등)은 updated_at을 두지 않구요.


class CommentCreateRequest(BaseModel):
    post_id: str
    content: str


class CommentUpdateRequest(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: str
    post_id: str
    author_id: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


# TODO: 필요없는 코드는 항상 제거 해둡시다!

# class CommentResponse(BaseModel):
#     id: str
#     post_id: str
#     content: str
#     created_at: datetime

#     model_config = {"from_attributes": True}


# class CommentCreateRequest(BaseModel):
#     author_id: str
#     post_id: str
#     content: str
