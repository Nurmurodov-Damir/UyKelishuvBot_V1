"""
Database connection and session management
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.config import settings
from src.database.models import Base
import logging

logger = logging.getLogger(__name__)

# Async engine yaratish
if settings.database_url.startswith("sqlite"):
    # SQLite uchun aiosqlite drayverini ishlatish
    if not settings.database_url.startswith("sqlite+"):
        database_url = settings.database_url.replace("sqlite://", "sqlite+aiosqlite://")
    else:
        database_url = settings.database_url
elif settings.database_url.startswith("postgresql://"):
    # PostgreSQL uchun asyncpg drayverini ishlatish
    if not settings.database_url.startswith("postgresql+"):
        database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
    else:
        database_url = settings.database_url
else:
    database_url = settings.database_url

engine = create_async_engine(
    database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Database jadvallarini yaratish"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def close_db():
    """Database connectionni yopish"""
    await engine.dispose()
    logger.info("Database connections closed")