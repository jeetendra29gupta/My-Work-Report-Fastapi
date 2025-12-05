from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select, is_

from app.models.user import User
from app.schemas.user import ReadUser, UpdateUser, PasswordChange, RoleChange, UserSuccessMessage
from app.utilities.database import get_db_session
from app.utilities.helper import get_utc_now
from app.utilities.logger import get_logger
from app.utilities.security import has_admin_role, get_current_user, verify_password, hash_password

logger = get_logger(__name__)
user_router = APIRouter()


def get_user_by_id(user_id: int, db_session: Session) -> User:
    """
    Retrieve an active user by ID or raise HTTP 404.
    """
    try:
        user = db_session.exec(
            select(User).where(User.id == user_id, User.is_active == True)
        ).one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during user retrieval")
        raise HTTPException(status_code=500, detail="Failed to retrieve user")


@user_router.get("/list", response_model=list[ReadUser], status_code=200)
def list_users(
        db_session: Session = Depends(get_db_session),
        is_admin: bool = Depends(has_admin_role),
) -> list[ReadUser]:
    """
    List all active users (admin only).
    """
    try:
        users = db_session.exec(
            select(User).where(User.is_active == True)
        ).all()

        logger.info(f"Total active users: {len(users)}")
        return users  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during user listing")
        raise HTTPException(status_code=500, detail="Failed to list users")


@user_router.get("/get/{user_id}", response_model=ReadUser, status_code=200)
def get_user(
        user_id: int,
        db_session: Session = Depends(get_db_session),
        is_admin: bool = Depends(has_admin_role),
) -> ReadUser:
    """
    Retrieve a single user by ID (admin only).
    """
    try:
        db_user = get_user_by_id(user_id, db_session)
        logger.info(f"User retrieved with ID: {db_user.id}")
        return db_user  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during user retrieval")
        raise HTTPException(status_code=500, detail="Failed to retrieve user")


@user_router.put("/update/{user_id}", response_model=ReadUser, status_code=200)
def update_user(
        user_id: int,
        user: UpdateUser,
        db_session: Session = Depends(get_db_session),
        is_admin: bool = Depends(has_admin_role),
) -> ReadUser:
    """
    Full update of a user (admin only).
    """
    try:
        db_user = get_user_by_id(user_id, db_session)
        if user.full_name is None:
            raise HTTPException(
                status_code=400, detail="Missing required fields for full update"
            )

        db_user.full_name = user.full_name.strip()
        db_user.phone_no = user.phone_no.strip() if user.phone_no else None
        db_user.updated_at = get_utc_now()

        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        logger.info(f"User updated with ID: {db_user.id}")
        return db_user  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during updating user")
        raise HTTPException(status_code=500, detail="Failed to update user")


@user_router.patch("/edit/{user_id}", response_model=ReadUser, status_code=200)
def edit_user(
        user_id: int,
        user: UpdateUser,
        db_session: Session = Depends(get_db_session),
        is_admin: bool = Depends(has_admin_role),
) -> ReadUser:
    """
    Partial update of a user (admin only).
    """
    try:
        db_user = get_user_by_id(user_id, db_session)

        if user.full_name is not None:
            db_user.full_name = user.full_name.strip()
        if user.phone_no is not None:
            db_user.phone_no = user.phone_no.strip()
        db_user.updated_at = get_utc_now()

        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        logger.info(f"User edited with ID: {db_user.id}")
        return db_user  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during editing user")
        raise HTTPException(status_code=500, detail="Failed to edit user")


@user_router.delete("/delete/{user_id}", status_code=204)
def delete_user(
        user_id: int,
        db_session: Session = Depends(get_db_session),
        is_admin: bool = Depends(has_admin_role),
) -> None:
    """
    Soft-delete a user (admin only).
    Returns no content (204).
    """
    try:
        db_user = get_user_by_id(user_id, db_session)

        db_user.is_active = False
        db_user.updated_at = get_utc_now()

        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        logger.info(f"User deleted with ID: {db_user.id}")

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during deleting user")
        raise HTTPException(status_code=500, detail="Failed to delete user")


@user_router.get("/list/deleted", response_model=list[ReadUser], status_code=200)
def list_deleted_users(
        db_session: Session = Depends(get_db_session),
        is_admin: bool = Depends(has_admin_role),
) -> list[ReadUser]:
    """
    List soft-deleted users (admin only).
    """
    try:
        users = db_session.exec(select(User).where(User.is_active == False)).all()  # noqa

        logger.info(f"Total deleted users: {len(users)}")
        return users  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during deleted user listing")
        raise HTTPException(status_code=500, detail="Failed to list deleted users")


@user_router.patch("/activate/{user_id}", response_model=ReadUser, status_code=200)
def activate_user(
        user_id: int,
        db_session: Session = Depends(get_db_session),
        is_admin: bool = Depends(has_admin_role),
) -> ReadUser:
    """
    Reactivate a previously deleted user (admin only).
    """
    try:
        db_user = db_session.exec(
            select(User).where(User.id == user_id, User.is_active == False)  # noqa
        ).one_or_none()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not deleted or notfound")

        db_user.is_active = True
        db_user.updated_at = get_utc_now()

        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        logger.info(f"User activated with ID: {db_user.id}")
        return db_user  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during activating user")
        raise HTTPException(status_code=500, detail="Failed to activate user")


@user_router.patch("/role/{user_id}", response_model=ReadUser, status_code=200)
def change_role(
        user_id: int,
        role: RoleChange,
        db_session: Session = Depends(get_db_session),
        is_admin: bool = Depends(has_admin_role),
) -> ReadUser:
    """
    Change a user's role (admin only).
    """
    try:
        db_user = get_user_by_id(user_id, db_session)

        db_user.role = role.role
        db_user.updated_at = get_utc_now()

        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        logger.info(f"User role changed to {db_user.role} with ID: {db_user.id}")
        return db_user  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during user role change")
        raise HTTPException(status_code=500, detail="Failed to change user role")


@user_router.patch("/password/{user_id}", response_model=UserSuccessMessage, status_code=200)
def change_password(
        password: PasswordChange,
        db_session: Session = Depends(get_db_session),
        user: User = Depends(get_current_user),
) -> UserSuccessMessage:
    """
    Change the currently authenticated user's password.
    """
    try:

        if not verify_password(password.old_password, user.hashed_password):
            detail = "Old password is incorrect"
            logger.error(detail)
            raise HTTPException(status_code=400, detail=detail)

        user.hashed_password = hash_password(password.new_password)
        user.updated_at = get_utc_now()

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        logger.info(f"Password updated for user {user.id}")
        return UserSuccessMessage(
            status_code=200,
            detail={"message": "Password updated successfully"},
        )

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during changing password")
        raise HTTPException(status_code=500, detail="Failed to change password")


@user_router.get("/profile", response_model=ReadUser, status_code=200)
def get_profile(
        user: User = Depends(get_current_user),
) -> ReadUser:
    """
    Retrieve the authenticated user's own profile.
    """
    return user  # noqa
