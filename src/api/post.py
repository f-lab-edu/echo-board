from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel

post_router = APIRouter()

TIME_ZONE = ZoneInfo("Asia/Seoul")


class PostResponse(BaseModel):
    id: str
    author: str
    title: str
    content: str
    # TODO: 시각에 대한 표현방법이 어떤 것들이 있는지 알아보기. (ISO-8601, unix timestamp 등)
    created_at: datetime


class PostRequest(BaseModel):
    title: str
    content: str


posts: list[PostResponse] = []


@post_router.post(
    "/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED
)
async def create_post(
    post: PostRequest, x_author: str = Header(..., alias="X-Author")
) -> PostResponse:
    new_post = PostResponse(
        # TODO: uuid 대신 ulid 써보기.
        # TODO: id를 만드는 여러 방식에 대해 알아보기.
        id=str(uuid4()),
        author=x_author,
        title=post.title,
        content=post.content,
        created_at=datetime.now(TIME_ZONE),  # TODO: aware datetime vs naiva datetime 에 대해 알아보기
    )
    posts.append(new_post)
    return new_post


@post_router.get(
    "/posts", response_model=list[PostResponse], status_code=status.HTTP_200_OK
)
async def get_posts() -> list[PostResponse]:
    return posts


@post_router.get(
    "/posts/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def get_post(post_id: str) -> PostResponse:
    post = next((p for p in posts if p.id == post_id), None)
    if post is None:  # TODO: post is None vs not post 중 어떤게 더 좋은 방법일까? 알아보기
        raise HTTPException(status_code=404, detail="Post not found")  # TODO: fastapi.status 사용하기. 그리고 이게 왜 더 좋은지 설명하기
    return post


@post_router.put(
    "/posts/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def update_post(
    post_id: str, post_data: PostRequest, x_author: str = Header(..., alias="X-Author")  # TODO: 요청 헤더에 이름을 붙이는 컨벤션들은 뭐가 있는지 알아보기. ex. X-는 왜 붙일까?
) -> PostResponse:
    post_index = next((i for i, p in enumerate(posts) if p.id == post_id), None)

    if post_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {repr(post_id)} not found.",  # TODO: 에러 메시지는 어떻게 작성하는 것이 좋은지 알아보기
        )

    post = posts[post_index]
    if post.author != x_author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # TODO: 2XX, 4XX 에러 알아보기 (401, 403, 404, 405, 409 설명 할 수 있어야 함)
            detail="Access denied: not the post owner.",
        )

    updated_post = PostResponse(
        id=post.id,
        author=post.author,
        title=post_data.title,
        content=post_data.content,
        created_at=post.created_at,
    )
    posts[post_index] = updated_post
    return updated_post


@post_router.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_post(
    post_id: str,
    x_author: str = Header(..., alias="X-Author"),
) -> dict:
    post_index = next((i for i, p in enumerate(posts) if p.id == post_id), None)
    if post_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id '{repr(post_id)}' not found.",
        )
    # TODO: 나는 언제 개행을 사용하는지 일관된 규칙 설명할 수 있기 (ex. 언제 어디서 코드에 개행을 넣으시는 건가요? 기준이 있나요?)
    post = posts[post_index]

    if post.author != x_author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not the post owner.",
        )

    del posts[post_index]

    # TODO: 함수의 반환 값으로 dict를 사용하는게 왜 좋지 않은지 설명하기. 그리고 대안 찾아보고 적용해보기
    return {"message": f"Post '{repr(post_id)}' deleted successfully."}
