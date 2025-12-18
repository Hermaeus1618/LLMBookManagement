from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

#
# SQLAlchemy Base
#
class Base(DeclarativeBase):
    pass

#
# Async Engine
#
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    future=True,
)

#
# Async Session Factory
#
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

#
# Dependency
#
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

#
# DB Initialization
#
async def init_db() -> None:
    """
    Initializes database tables.
    In production, migrations (Alembic) should be used instead.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
