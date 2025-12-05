from datetime import timedelta

from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select

from app.models.user import User
from app.schemas.auth import UserSignup, UserLogin, UserToken
from app.schemas.user import ReadUser
from app.utilities.config import Config
from app.utilities.database import get_db_session
from app.utilities.logger import get_logger
from app.utilities.security import hash_password, verify_password, create_token

auth_router = APIRouter()
logger = get_logger(__name__)


@auth_router.post("/signup", response_model=ReadUser, status_code=201)
def signup(user: UserSignup, db_session: Session = Depends(get_db_session)) -> ReadUser:
    try:
        # Normalize email
        email_normalized = str(user.email_id).lower()

        # Check if user already exists
        existing_user = db_session.exec(
            select(User).where(User.email_id == email_normalized)
        ).first()

        if existing_user:
            detail = f"User with email {email_normalized} already exists."
            logger.warning(detail)
            raise HTTPException(status_code=409, detail=detail)

        # Create new user
        new_user = User(
            full_name=user.full_name.strip(),
            email_id=email_normalized,
            phone_no=user.phone_no,
            hashed_password=hash_password(user.password),
        )

        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        logger.info(f"New user created: {new_user.email_id} (id={new_user.id})")

        return new_user  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during signup")
        raise HTTPException(status_code=500, detail="Failed to signup")


@auth_router.post("/login", response_model=UserToken, status_code=200)
def login(user: UserLogin, db_session: Session = Depends(get_db_session)) -> UserToken:
    try:
        # Normalize email
        email_normalized = str(user.email_id).lower()

        # Get user from database
        db_user = db_session.exec(
            select(User).where(User.email_id == email_normalized)
        ).first()

        if not db_user:
            detail = f"User with email {email_normalized} not found."
            logger.warning(detail)
            raise HTTPException(status_code=404, detail=detail)

        # Validate password
        if not verify_password(user.password, db_user.hashed_password):
            detail = "Incorrect password"
            logger.warning(detail)
            raise HTTPException(status_code=401, detail=detail)

        logger.info(
            f"User logged in successfully: {db_user.email_id} (id={db_user.id})"
        )

        return UserToken(
            access_token=create_token(
                str(db_user.id), timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
            ),
            refresh_token=create_token(
                str(db_user.id), timedelta(hours=Config.REFRESH_TOKEN_EXPIRE_HOURS)
            ),
        )

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during login")
        raise HTTPException(status_code=500, detail="Failed to login")
