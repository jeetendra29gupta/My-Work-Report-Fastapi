import os

from sqlmodel import create_engine, Session

from ..utilities.config import DATABASE_DIR, DATABASE_NAME

os.makedirs(DATABASE_DIR, exist_ok=True)
database_path = f"{DATABASE_DIR}/{DATABASE_NAME}"
database_url = f"sqlite:///{database_path}"

engine = create_engine(database_url, echo=False)


def get_db_session():
    with Session(engine) as session:
        yield session
