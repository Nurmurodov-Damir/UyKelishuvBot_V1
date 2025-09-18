"""
Database connection and session management
"""
import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.config import settings
from src.database.models import Base

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

# Railway environment uchun maxsus parametrlar
engine_kwargs = {
    "echo": settings.debug,
    "pool_pre_ping": True,
    "pool_recycle": 300
}

# Railway PostgreSQL uchun maxsus parametrlar
if database_url.startswith('postgresql+asyncpg://') and os.getenv('RAILWAY_ENVIRONMENT'):
    engine_kwargs.update({
        "connect_args": {
            "server_settings": {
                "application_name": "uykelishuv_bot",
            },
            "command_timeout": 60,
            "ssl": "prefer",  # Railway SSL ishlatadi
        },
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_recycle": 1800
    })

engine = create_async_engine(database_url, **engine_kwargs)

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