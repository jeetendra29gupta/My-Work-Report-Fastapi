import bcrypt

from ..utilities.config import SALT_LENGTH
from ..utilities.logger import get_logger

logger = get_logger(__name__)


def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt(rounds=SALT_LENGTH)
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
