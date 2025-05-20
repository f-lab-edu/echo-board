from sqlmodel import Session, select

from src.domain.comment import Comment, CommentCreateRequest, CommentResponse


def create_comment_service(
    data: CommentCreateRequest, session: Session
) -> CommentResponse:
    comment = Comment(**data.model_dump())
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return CommentResponse.model_validate(comment)


def get_comments_by_author_service(
    author_id: str, session: Session
) -> list[CommentResponse]:
    stmt = select(Comment).where(Comment.author_id == author_id)
    comments = session.exec(stmt).all()
    return [CommentResponse.model_validate(c) for c in comments]


def get_comments_by_post_service(
    post_id: str, session: Session
) -> list[CommentResponse]:
    stmt = select(Comment).where(Comment.post_id == post_id)
    comments = session.exec(stmt).all()
    return [CommentResponse.model_validate(c) for c in comments]
