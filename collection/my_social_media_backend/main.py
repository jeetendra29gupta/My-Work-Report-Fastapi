from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .models.post import init_post_tables
from .models.user import init_user_tables
from .routes.post import post_router
from .routes.user import user_router
from .utilities.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    # Startup
    logger.info("Starting up...")
    init_user_tables()
    init_post_tables()

    yield

    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title="Blogger API",
    description="API for managing posts",
    version="1.0.0",
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

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(post_router, prefix="/posts", tags=["Posts"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8181, reload=True)

    # uv run uvicorn my_social_media_backend.main:app --reload --host 0.0.0.0 --port 8181
