from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes.auth import auth_router
from app.routes.task import task_router
from app.routes.user import user_router
from app.utilities.config import Config
from app.utilities.database import init_table
from app.utilities.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    # Startup
    logger.info("Starting up...")
    init_table()

    yield

    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title=Config.TITLE,
    description=Config.DESCRIPTION,
    version=Config.VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:9191",
    ],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT", "PATCH"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "ok"}


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(task_router, prefix="/task", tags=["Tasks"])
app.include_router(user_router, prefix="/user", tags=["Users"])
