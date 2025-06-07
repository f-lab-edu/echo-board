from datetime import datetime
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlmodel import Session, select
from ulid import ULID

from src.domain.comment import CommentResponse
from src.domain.post import DeletePostResponse, Post, PostRequest, PostResponse
from src.service.comment import get_comments_by_post_service
from src.sqlite3.connection import get_session

post_router = APIRouter()

TIME_ZONE = ZoneInfo("Asia/Seoul")

# TODO: 의존성 주입에 대해 설명하기.
# ❕ 과제: DB가 바뀌어도, 이 안에있는 코드들은 바뀌지 않도록 설계 해보기
SessionDep = Annotated[Session, Depends(get_session)]


@post_router.post(
    "/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED
)
def create_post(
    post: PostRequest,
    session: SessionDep,
    author: str = Header(..., alias="Author"),
) -> PostResponse:
    # TODO: id를 만드는 여러 방식에 대해 설명하기.
    new_post = Post(
        id=str(ULID()),
        author_id=author,
        title=post.title,
        content=post.content,
        created_at=datetime.now(TIME_ZONE),
    )
    session.add(new_post)
    session.commit()

    # TODO: refersh와 flush의 차이 설명하기
    session.refresh(new_post)

    return PostResponse.model_validate(new_post, from_attributes=True)


# TODO: 페이지네이션 구현 필요.
# TODO: 페이지네이션 종류 찾아보고 설명하기 (ex. 전통적, 커서 기반)
@post_router.get(
    "/posts", response_model=list[PostResponse], status_code=status.HTTP_200_OK
)
def get_posts(session: SessionDep) -> list[PostResponse]:
    stmt = select(Post)
    results = session.exec(stmt).all()

    # TODO: 확장성 있게 응답 스키마를 만드려면, 과연 리스트가 좋을까요? 더 좋은 방법은 없을까요?
    # ex. 예를 들어 응답에 total, next page 등이 추가가 된다면?
    return [
        PostResponse.model_validate(p, from_attributes=True) for p in results
    ]


@post_router.get(
    "/posts/{post_id}",
    response_model=PostResponse,  # TODO: 아래 타입 힌팅이 있어서, 이 부분은 필요 없습니다. (이거 지우고 테스트 해보시죠!)
    status_code=status.HTTP_200_OK,
)
def get_post(session: SessionDep, post_id: str) -> PostResponse:
    stmt = select(Post).where(Post.id == post_id)
    post = session.exec(stmt).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            # TODO: 에러 메시지는 어떻게 작성하는 것이 좋은지 설명하기.
            detail=f"Post with id '{post_id}' not found.",
        )

    return PostResponse.model_validate(post, from_attributes=True)


@post_router.put(
    "/posts/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
def update_post(
    post_id: str,
    # COMMENT: 이건 팁인데, 저는 보통 헷갈림 방지를 위해 클래스 이름과 인스턴스 이름을 (거의) 동일하게 둡니다.
    # ex. request: PostRequest
    post_data: PostRequest,
    session: SessionDep,
    author: str = Header(..., alias="Author"),
) -> PostResponse:
    stmt = select(Post).where(Post.id == post_id)
    post = session.exec(stmt).first()

    if post is None:
        raise HTTPException(
            # TODO: 2XX, 4XX 등 Status Code들 설명하기 (401, 403, 404, 405, 409, 429, 422 설명 할 수 있어야 함)
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id '{post_id}' not found.",
        )

    if post.author != author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not the post owner.",
        )

    post.title = post_data.title
    post.content = post_data.content

    session.add(post)
    session.commit()
    session.refresh(post)

    return PostResponse.model_validate(post, from_attributes=True)


@post_router.delete(
    "/posts/{post_id}",
    response_model=DeletePostResponse,
    status_code=status.HTTP_200_OK,
)
def delete_post(
    post_id: str,
    session: SessionDep,
    author: str = Header(..., alias="Author"),
) -> DeletePostResponse:
    stmt = select(Post).where(Post.id == post_id)
    post = session.exec(stmt).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id '{post_id}' not found.",
        )

    if post.author != author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not the post owner.",
        )

    # TODO: Hard / Soft Delete 차이 설명하기.
    session.delete(post)
    session.commit()

    # TODO: 함수의 반환 값으로 dict를 사용하는게 왜 좋지 않은지, 클래스를 쓰는게 왜 더 좋은지 설명하기.
    # COMMENT: 이전에 UserCreateResponse를 본적이 있는데, 여기서는 DeletePostRespones 군요.
    #          이런 DTO 클래스의 이름은 일관되게 지어주는게 좋습니다.
    #          저는 보통 DTO 클래스가 사용되는 함수 이름을 따라서 동사+명사 형태로 짓습니다.
    #          ex. delete_post(request: DeletePostRequest) -> DeletePostResponse
    #          ex. create_user(request: CreateUserRequest) -> CreateUserResponse
    #          이와 관련해서는 "클린 아키텍처" 책을 읽어보시길 추천드립니다. 
    return DeletePostResponse(message=f"Post '{post_id}' deleted successfully.")


@post_router.get(
    "/posts/{post_id}/comments",
    response_model=list[CommentResponse],
    status_code=status.HTTP_200_OK,
)
def get_comments_by_post(
    post_id: str,
    session: SessionDep,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return get_comments_by_post_service(post_id, session, limit, offset)
