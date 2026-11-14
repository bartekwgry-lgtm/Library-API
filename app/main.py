"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.books import router as books_router
from app.config import settings
from app.database import engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Dispose the database engine on shutdown.

    :param _app: FastAPI application instance
    """
    yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(books_router)
