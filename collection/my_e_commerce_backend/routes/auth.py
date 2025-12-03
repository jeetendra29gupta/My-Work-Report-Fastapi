from datetime import datetime, timezone, timedelta

import jwt
from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session, select, and_

from ..models.auth import Auth, UserRole
from ..schemas.auth import AuthUser, AuthSignup, AuthToken
from ..utilities.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
)
from ..utilities.database import get_db_session
from ..utilities.helper import get_utc_now
from ..utilities.logger import get_logger
from ..utilities.security import hash_password, verify_password

logger = get_logger(__name__)

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": data, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db_session: Session = Depends(get_db_session)
):
    try:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        db_user = db_session.exec(
            select(Auth).where(
                and_(Auth.id == user_id, Auth.is_active == True)  # noqa
            )
        ).first()
        if not db_user:
            detail = "User not found"
            logger.error(detail)
            raise HTTPException(status_code=404, detail=detail)

        return AuthUser(
            id=db_user.id,
            full_name=db_user.full_name,
            email_id=db_user.email_id,
            phone_no=db_user.phone_no,
            role=db_user.role,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )

    except jwt.ExpiredSignatureError:
        detail = "Token expired"
        logger.error(detail)
        raise HTTPException(status_code=401, detail=detail)
    except jwt.InvalidTokenError:
        detail = "Invalid token"
        logger.error(detail)
        raise HTTPException(status_code=401, detail=detail)
    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to get current user"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@auth_router.post("/signup", response_model=AuthUser, status_code=201)
def signup(user: AuthSignup, db_session: Session = Depends(get_db_session)):
    try:
        # Check if user already exists
        db_user = db_session.exec(
            select(Auth).where(and_(Auth.email_id == user.email_id))
        ).first()
        if db_user:
            detail = "User already exists"
            logger.error(detail)
            raise HTTPException(status_code=409, detail=detail)

        # Create user
        now = get_utc_now()
        db_user = Auth(
            full_name=user.full_name,
            email_id=user.email_id,
            phone_no=user.phone_no,
            hashed_password=hash_password(user.password),
            is_active=True,
            role=UserRole.USER,
            created_at=now,
            updated_at=now,
        )
        db_session.add(db_user)
        db_session.commit()

        return db_user

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to signup"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


@auth_router.post("/login", response_model=AuthToken, status_code=200)
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session),
):
    try:
        db_user = db_session.exec(
            select(Auth).where(
                and_(Auth.email_id == user.username, Auth.is_active == True)  # noqa
            )
        ).first()
        if not db_user:
            detail = "User not found"
            logger.error(detail)
            raise HTTPException(status_code=404, detail=detail)

        if not verify_password(user.password, db_user.hashed_password):
            detail = "Incorrect password"
            logger.error(detail)
            raise HTTPException(status_code=401, detail=detail)

        logger.info(f"User logged in successfully with id: {db_user.id}")
        token = AuthToken(
            access_token=create_access_token(str(db_user.id)),
            token_type="bearer",
        )
        return token

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to login"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)
