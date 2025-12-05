import os

from sqlmodel import create_engine, Session, SQLModel

from app.utilities.config import Config

os.makedirs(Config.DATABASE_DIR, exist_ok=True)
database_path = f"{Config.DATABASE_DIR}/{Config.DATABASE_NAME}"
database_url = f"sqlite:///{database_path}"

engine = create_engine(database_url, echo=False)


def get_db_session():
    with Session(engine) as session:
        yield session


def init_table():
    from app.models.user import User  # noqa
    from app.models.task import Task  # noqa

    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
