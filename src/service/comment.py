from fastapi import HTTPException
from sqlmodel import Session, select

from src.domain.comment import (
    Comment,
    CommentCreateRequest,
    CommentResponse,
    CommentUpdateRequest,
)


def create_comment_service(
    data: CommentCreateRequest, session: Session, author: str
) -> CommentResponse:
    comment = Comment(author_id=author, **data.model_dump())
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return CommentResponse.model_validate(comment)


def get_comments_by_author_service(
    author_id: str, session: Session, limit: int, offset: int
) -> list[CommentResponse]:
    stmt = (
        select(Comment)
        .where(Comment.author_id == author_id)
        .offset(offset)
        .limit(limit)
    )
    comments = session.exec(stmt).all()
    return [CommentResponse.model_validate(c) for c in comments]


def get_comments_by_post_service(
    post_id: str, session: Session, limit: int, offset: int
) -> list[CommentResponse]:
    stmt = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .offset(offset)
        .limit(limit)
    )
    comments = session.exec(stmt).all()
    return [CommentResponse.model_validate(c) for c in comments]


def delete_comment_service(
    comment_id: str, session: Session, author: str
) -> None:
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != author:
        raise HTTPException(status_code=403, detail="Not authorized")
    session.delete(comment)
    session.commit()


def update_comment_service(
    comment_id: str,
    data: CommentUpdateRequest,
    session: Session,
    author: str,
) -> CommentResponse:
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != author:
        raise HTTPException(status_code=403, detail="Not authorized")
    comment.content = data.content
    session.commit()
    session.refresh(comment)
    return CommentResponse.model_validate(comment)


# from fastapi import HTTPException
# from sqlmodel import Session, select

# from src.domain.comment import Comment, CommentCreateRequest, CommentResponse


# def create_comment_service(
#     data: CommentCreateRequest, session: Session, author
# ) -> CommentResponse:
#     comment = Comment(author_id=author, **data.model_dump())
#     session.add(comment)
#     session.commit()
#     session.refresh(comment)
#     return CommentResponse.model_validate(comment)


# def get_comments_by_author_service(
#     author_id: str, session: Session
# ) -> list[CommentResponse]:
#     stmt = select(Comment).where(Comment.author_id == author_id)
#     comments = session.exec(stmt).all()
#     return [CommentResponse.model_validate(c) for c in comments]


# def get_comments_by_post_service(
#     post_id: str, session: Session
# ) -> list[CommentResponse]:
#     stmt = select(Comment).where(Comment.post_id == post_id)
#     comments = session.exec(stmt).all()
#     return [CommentResponse.model_validate(c) for c in comments]


# def delete_comment_service(
#     comment_id: str, session: Session, author: str
# ) -> None:
#     comment = session.get(Comment, comment_id)
#     if not comment:
#         raise HTTPException(status_code=404, detail="Comment not found")
#     if comment.author_id != author:
#         raise HTTPException(
#             status_code=403, detail="Not authorized to delete this comment"
#         )

#     session.delete(comment)
#     session.commit()


# def update_comment_service(
#     comment_id: str,
#     data: CommentCreateRequest,
#     session: Session,
#     author: str,
# ) -> CommentResponse:
#     comment = session.get(Comment, comment_id)
#     if not comment:
#         raise HTTPException(status_code=404, detail="Comment not found")
#     if comment.author_id != author:
#         raise HTTPException(
#             status_code=403, detail="Not authorized to update this comment"
#         )

#     comment.content = data.content
#     session.add(comment)
#     session.commit()
#     session.refresh(comment)
#     return CommentResponse.model_validate(comment)
