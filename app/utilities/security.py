from datetime import timedelta
from typing import Any, Dict

import bcrypt
import jwt
from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from sqlmodel import Session

from app.models.user import User, UserRole
from app.utilities.config import Config
from app.utilities.database import get_db_session
from app.utilities.helper import get_utc_now
from app.utilities.logger import get_logger

logger = get_logger(__name__)
security = HTTPBearer()


def hash_password(plain_password: str) -> str:
    """
    Hash a plain password using bcrypt.

    Args:
        plain_password (str): The plain text password.

    Returns:
        str: The hashed password as a UTF-8 string.
    """
    salt = bcrypt.gensalt(rounds=Config.SALT_LENGTH)
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if password matches, False otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_token(user_id: str, expires_delta: timedelta) -> str:
    """
    Create a JWT token with a specific expiration.

    Args:
        user_id (str): User identifier to include in token.
        expires_delta (timedelta): Token expiration duration.

    Returns:
        str: Encoded JWT token.
    """
    expire = get_utc_now() + expires_delta
    to_encode: Dict[str, Any] = {"sub": user_id, "exp": expire}
    token = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return token


def verify_token(token: str, token_type: str = "access") -> Dict[str, Any]:
    """
    Verify a JWT token and return its payload.

    Args:
        token (str): JWT token string.
        token_type (str, optional): Type of token for logging purposes. Defaults to "access".

    Returns:
        dict: Decoded JWT payload.

    Raises:
        HTTPException: If token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM]
        )
        return payload

    except jwt.ExpiredSignatureError:
        detail = f"{token_type.capitalize()} token expired"
        logger.error(detail)
        raise HTTPException(status_code=401, detail=detail)
    except jwt.InvalidTokenError:
        detail = f"{token_type.capitalize()} token invalid"
        logger.error(detail)
        raise HTTPException(status_code=401, detail=detail)
    except Exception:
        detail = f"Failed to verify {token_type} token"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)


def get_current_user(
    x_api_token: str = Header(...), db: Session = Depends(get_db_session)
) -> User:
    """
    Authenticate and return the current user based on the provided JWT token.

    Args:
        x_api_token (str): The access token provided in the request header.
        db (Session): Database session dependency.

    Returns:
        User: The authenticated user retrieved from the database.

    Raises:
        HTTPException:
            - 401 if the token is missing, invalid, expired, or user does not exist.
            - 500 if an unexpected error occurs during authentication.
    """
    try:
        if not x_api_token:
            detail = "Missing access token"
            logger.error(detail)
            raise HTTPException(status_code=401, detail=detail)

        payload = verify_token(x_api_token, "access")
        user_id = payload["sub"]

        if not user_id:
            detail = "Token missing user identifier"
            logger.error(detail)
            raise HTTPException(status_code=401, detail=detail)

        user = db.get(User, user_id)

        if not user:
            detail = "User not found"
            logger.error(detail)
            raise HTTPException(status_code=401, detail=detail)

        return user  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during user authentication")
        raise HTTPException(status_code=500, detail="Failed to authenticate user")


def has_admin_role(user: User = Depends(get_current_user)) -> bool:
    """
    Verify that the authenticated user has admin privileges.

    Args:
        user (User): The authenticated user obtained from `get_current_user`.

    Returns:
        bool: True if the user has admin role.

    Raises:
        HTTPException:
            - 403 if the user lacks admin privileges.
            - 500 if an unexpected error occurs during role verification.
    """
    try:
        if user.role != UserRole.ADMIN:
            detail = "Admin privileges required"
            logger.warning(detail)
            raise HTTPException(status_code=403, detail=detail)

        return True

    except HTTPException:
        raise
    except Exception:
        detail = "Failed to check user role"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)