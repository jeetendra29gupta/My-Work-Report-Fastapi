from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .models.auth import init_auth_tables
from .models.product import init_product_tables
from .routes.auth import auth_router
from .routes.product import product_router
from .utilities.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    # Startup
    logger.info("Starting up...")
    init_auth_tables()
    init_product_tables()

    yield

    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title="Products API",
    description="API for managing products",
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

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(product_router, prefix="/products", tags=["products"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8181, reload=True)

    # uv run uvicorn my_e_commerce_backend.main:app --reload --host 0.0.0.0 --port 8181
