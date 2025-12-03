from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, and_

from ..models.user import User, UserRole
from ..schemas.user import (
    UserRead,
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    UserRoleChange,
)
from ..utilities.database import get_db_session
from ..utilities.helper import get_utc_now
from ..utilities.logger import get_logger
from ..utilities.security import hash_password, verify_password

logger = get_logger(__name__)
user_router = APIRouter()


@user_router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db_session: Session = Depends(get_db_session)):
    try:
        now = get_utc_now()
        new_user = User(
            full_name=user.full_name,
            email_id=user.email_id,
            phone_no=user.phone_no,
            hashed_password=hash_password(user.password),
            role=UserRole.USER,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        logger.info(f"User created successfully with id: {new_user.id}")
        return new_user

    except HTTPException:
        detail = "Failed to create user"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@user_router.get("/", response_model=list[UserRead], status_code=200)
def read_all_users(db_session: Session = Depends(get_db_session)):
    try:
        users = db_session.exec(select(User).where(User.is_active == True)).all()  # noqa

        logger.info(f"Total users {len(users)}")
        return users

    except HTTPException:
        detail = "Failed to read all users"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@user_router.get("/deleted", response_model=list[UserRead], status_code=200)
def read_all_deleted_users(db_session: Session = Depends(get_db_session)):
    try:
        users = db_session.exec(select(User).where(User.is_active == False)).all()  # noqa
        logger.info(f"Total deleted users: {len(users)}")
        return users

    except HTTPException:
        detail = "Failed to read all deleted users"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


def get_user_by_id(db_session: Session, user_id: int) -> User:
    user = db_session.exec(
        select(User).where(and_(User.id == user_id, User.is_active == True))  # noqa
    ).first()

    if not user:
        detail = f"User with id {user_id} not found"
        logger.error(detail)
        raise HTTPException(status_code=404, detail=detail)

    return user


@user_router.get("/{user_id}", response_model=UserRead, status_code=200)
def read_single_user(user_id: int, db_session: Session = Depends(get_db_session)):
    try:
        db_user = get_user_by_id(db_session, user_id)
        logger.info(f"User read successfully with id: {db_user.id}")
        return db_user

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to read user"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@user_router.put("/{user_id}", response_model=UserRead, status_code=200)
def update_user(
    user_id: int, user: UserUpdate, db_session: Session = Depends(get_db_session)
):
    try:
        db_user = get_user_by_id(db_session, user_id)

        if user.full_name is None or user.phone_no is None:
            detail = "Missing required fields for full update"
            logger.info(detail)
            raise HTTPException(status_code=400, detail=detail)

        db_user.full_name = user.full_name
        db_user.phone_no = user.phone_no
        db_user.updated_at = get_utc_now()

        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        logger.info(f"User updated successfully with id: {db_user.id}")
        return db_user

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to update user"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@user_router.patch("/{user_id}", response_model=UserRead, status_code=200)
def edit_user(
    user_id: int, user: UserUpdate, db_session: Session = Depends(get_db_session)
):
    try:
        db_user = get_user_by_id(db_session, user_id)

        if user.full_name is not None:
            db_user.full_name = user.full_name
        if user.phone_no is not None:
            db_user.phone_no = user.phone_no
        db_user.updated_at = get_utc_now()

        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        logger.info(f"User updated successfully with id: {db_user.id}")
        return db_user

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to update user"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@user_router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db_session: Session = Depends(get_db_session)):
    try:
        db_user = get_user_by_id(db_session, user_id)

        db_user.is_active = False
        db_user.updated_at = get_utc_now()

        db_session.add(db_user)
        db_session.commit()

        logger.info(f"User deleted successfully with id: {user_id}")
    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to delete user"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@user_router.patch("/active/{user_id}", status_code=200)
def toggle_user_active_status(
    user_id: int, db_session: Session = Depends(get_db_session)
):
    try:
        user = db_session.exec(
            select(User).where(and_(User.id == user_id, User.is_active == False))  # noqa
        ).first()
        if not user:
            detail = f"User with id {user_id} not inactive or not found"
            logger.error(detail)
            raise HTTPException(status_code=404, detail=detail)

        user.is_active = not user.is_active
        user.updated_at = get_utc_now()

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        logger.info(f"Toggled active status for user {user.id}: now {user.is_active}")
        return {"user_id": user.id, "is_active": user.is_active}

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to toggle active status for user"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@user_router.patch("/password/{user_id}", status_code=200)
def change_user_password(
    user_id: int,
    data: UserPasswordUpdate,
    db_session: Session = Depends(get_db_session),
):
    try:
        db_user = get_user_by_id(db_session, user_id)

        if not verify_password(data.old_password, db_user.hashed_password):
            detail = "Old password is incorrect"
            logger.error(detail)
            raise HTTPException(status_code=400, detail=detail)

        db_user.hashed_password = hash_password(data.new_password)
        db_user.updated_at = get_utc_now()

        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        logger.info(f"Password updated for user {user_id}")
        return {"message": "Password updated successfully", "user_id": db_user.id}

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to change password"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@user_router.patch("/role/{user_id}", status_code=200)
def change_user_role(
    user_id: int, data: UserRoleChange, db_session: Session = Depends(get_db_session)
):
    try:
        db_user = get_user_by_id(db_session, user_id)

        db_user.role = data.role
        db_user.updated_at = get_utc_now()

        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        logger.info(f"Role updated for user {user_id}: now {db_user.role}")
        return {"user_id": db_user.id, "role": db_user.role}

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to change user role"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)
