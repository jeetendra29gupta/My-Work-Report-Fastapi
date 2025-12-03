from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select, and_

from ..models.post import Post
from ..schemas.post import PostCreate, PostRead, PostUpdate
from ..utilities.database import get_db_session
from ..utilities.helper import get_utc_now
from ..utilities.logger import get_logger

logger = get_logger(__name__)
post_router = APIRouter()


@post_router.post("/", response_model=PostRead, status_code=201)
def create_post(post: PostCreate, db_session: Session = Depends(get_db_session)):
    try:
        now = get_utc_now()
        new_post = Post(
            title=post.title,
            content=post.content,
            is_published=False,
            is_active=True,
            created_at=now,
            updated_at=now,
            user_id=1,
        )

        db_session.add(new_post)
        db_session.commit()
        db_session.refresh(new_post)

        statement = (
            select(Post)
            .options(selectinload(Post.author))
            .where(Post.id == new_post.id)
        )
        post_with_author = db_session.exec(statement).one()

        logger.info(f"Post created successfully with id: {post_with_author.id}")
        return post_with_author

    except HTTPException:
        detail = "Failed to create post"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@post_router.get("/", response_model=list[PostRead], status_code=200)
def read_all_posts(db_session: Session = Depends(get_db_session)):
    try:
        posts = db_session.exec(select(Post).where(Post.is_active == True)).all()  # noqa

        logger.info(f"Total posts {len(posts)}")
        return posts

    except HTTPException:
        detail = "Failed to read all posts"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@post_router.get("/deleted", response_model=list[PostRead], status_code=200)
def read_all_deleted_posts(db_session: Session = Depends(get_db_session)):
    try:
        posts = db_session.exec(
            select(Post)
            .options(selectinload(Post.author))
            .where(Post.is_active == False)  # noqa
        ).all()

        logger.info(f"Total deleted posts: {len(posts)}")
        return posts

    except HTTPException:
        detail = "Failed to read all deleted posts"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


def get_post_by_id(db_session: Session, post_id: int) -> Post:
    post = db_session.exec(
        select(Post)
        .options(selectinload(Post.author))
        .where(and_(Post.id == post_id, Post.is_active == True))  # noqa
    ).first()

    if not post:
        detail = f"Post with id {post_id} not found"
        logger.error(detail)
        raise HTTPException(status_code=404, detail=detail)

    return post


@post_router.get("/{post_id}", response_model=PostRead, status_code=200)
def read_single_post(post_id: int, db_session: Session = Depends(get_db_session)):
    try:
        db_post = get_post_by_id(db_session, post_id)
        logger.info(f"Post read successfully with id: {db_post.id}")
        return db_post

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to read post"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@post_router.put("/{post_id}", response_model=PostRead, status_code=200)
def update_post(
    post_id: int, post: PostUpdate, db_session: Session = Depends(get_db_session)
):
    try:
        db_post = get_post_by_id(db_session, post_id)

        if post.title is None or post.content is None:
            detail = "Missing required fields for full update"
            logger.error(detail)
            raise HTTPException(status_code=400, detail=detail)
        db_post.title = post.title
        db_post.content = post.content
        db_post.updated_at = get_utc_now()

        db_session.add(db_post)
        db_session.commit()

        statement = (
            select(Post).options(selectinload(Post.author)).where(Post.id == post_id)
        )
        post_with_author = db_session.exec(statement).one()

        logger.info(f"Post updated successfully with id: {post_with_author.id}")
        return post_with_author

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to update post"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@post_router.patch("/{post_id}", response_model=PostRead, status_code=200)
def edit_post(
    post_id: int, post: PostUpdate, db_session: Session = Depends(get_db_session)
):
    try:
        db_post = get_post_by_id(db_session, post_id)

        if post.title is not None:
            db_post.title = post.title
        if post.content is not None:
            db_post.content = post.content
        db_post.updated_at = get_utc_now()

        db_session.add(db_post)
        db_session.commit()

        statement = (
            select(Post).options(selectinload(Post.author)).where(Post.id == post_id)
        )
        post_with_author = db_session.exec(statement).one()

        logger.info(f"Post updated successfully with id: {post_with_author.id}")
        return post_with_author

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to update post"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@post_router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db_session: Session = Depends(get_db_session)):
    try:
        db_post = get_post_by_id(db_session, post_id)

        db_post.is_active = False
        db_post.updated_at = get_utc_now()

        db_session.add(db_post)
        db_session.commit()

        logger.info(f"Post deleted successfully with id: {post_id}")

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to delete post"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@post_router.patch("/publish/{post_id}", status_code=200)
def toggle_post_publish_status(
    post_id: int, db_session: Session = Depends(get_db_session)
):
    try:
        post = get_post_by_id(db_session, post_id)

        post.is_published = not post.is_published
        post.updated_at = get_utc_now()

        db_session.add(post)
        db_session.commit()
        db_session.refresh(post)

        logger.info(
            f"Toggled publish status for post {post.id}: now {post.is_published}"
        )
        return {"post_id": post.id, "is_published": post.is_published}

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to toggle publish status for post"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@post_router.patch("/active/{post_id}", status_code=200)
def toggle_post_active_status(
    post_id: int, db_session: Session = Depends(get_db_session)
):
    try:
        post = db_session.exec(
            select(Post)
            .options(selectinload(Post.author))
            .where(and_(Post.id == post_id, Post.is_active == False))  # noqa
        ).first()

        if not post:
            detail = f"Post with id {post_id} not inactive or not found"
            logger.error(detail)
            raise HTTPException(status_code=404, detail=detail)

        post.is_active = not post.is_active
        post.updated_at = get_utc_now()

        db_session.add(post)
        db_session.commit()
        db_session.refresh(post)

        logger.info(f"Toggled active status for post {post.id}: now {post.is_active}")
        return {"post_id": post.id, "is_active": post.is_active}

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to toggle active status for post"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)
