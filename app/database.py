"""Async SQLAlchemy engine, session factory and declarative base."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Declarative base for ORM models."""


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a request-scoped session and commit on success.

    :yields: async SQLAlchemy session
    """
    async with SessionLocal() as session:
        yield session
        await session.commit()
