import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # API metadata
    TITLE: str = os.environ["TITLE"]
    DESCRIPTION: str = os.environ["DESCRIPTION"]
    VERSION: str = os.environ["VERSION"]
    SECRET_KEY: str = os.environ["SECRET_KEY"]

    # FastAPI server
    HOST: str = os.environ["HOST"]
    PORT: int = int(os.environ["PORT"])
    RELOAD: bool = os.environ["RELOAD"].lower() == "true"

    # Logging
    LOG_DIR: str = os.environ["LOG_DIR"]
    LOG_FILE: str = os.environ["LOG_FILE"]
    MAX_BYTES: int = int(os.environ["MAX_BYTES"])
    BACKUP_COUNT: int = int(os.environ["BACKUP_COUNT"])

    # Database
    DATABASE_DIR: str = os.environ["DATABASE_DIR"]
    DATABASE_NAME: str = os.environ["DATABASE_NAME"]

    # JWT
    JWT_SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]
    JWT_ALGORITHM: str = os.environ["JWT_ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
    REFRESH_TOKEN_EXPIRE_HOURS: int = int(os.environ["REFRESH_TOKEN_EXPIRE_HOURS"])

    # Security
    SALT_LENGTH: int = int(os.environ["SALT_LENGTH"])
