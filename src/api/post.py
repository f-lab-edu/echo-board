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
    created_at: datetime  # TODO: 시각에 대한 표현방법이 어떤 것들이 있는지. string, int을 사용 방식 -> 언제 내가 사용해야 하는지?


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
        # TODO: uuid, ulid 써보기.
        # NOTE: id를 만드는 방식 AUTO INCREMENT, uuid 이게 뭔지, 각 장단점
        # ulid 는 왜? 언제? 어떤 문제를 해결하는지
        id=str(uuid4()),
        author=x_author,
        title=post.title,
        content=post.content,
        created_at=datetime.now(TIME_ZONE),
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
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")  # TODO: 404 fastapi.status <- 사용해보기
    return post


@post_router.put(
    "/posts/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def update_post(
    post_id: str, post_data: PostRequest, x_author: str = Header(..., alias="X-Author")  # TODO: 요청 헤더에 이름을 붙이는 컨벤션들 뭐가 있을까?
) -> PostResponse:
    post_index = next((i for i, p in enumerate(posts) if p.id == post_id), None)

    if post_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {repr(post_id)} not found.",
        )

    post = posts[post_index]
    if post.author != x_author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # TODO: 4XX 에러 다 정리하기 (401, 403, 404, 405, 409 설명 할 수 있어야 함)
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

    post = posts[post_index]

    if post.author != x_author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not the post owner.",
        )

    del posts[post_index]

    return {"message": f"Post '{repr(post_id)}' deleted successfully."}
