"""
Database session management for async PostgreSQL.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.core.config import config

# Create async engine
engine = create_async_engine(
    config.database_url,
    echo=False,
    future=True
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Declarative base for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Get a database session.

    Usage:
        async with get_db() as session:
            # Use session
            pass
    """
    async with async_session_maker() as session:
        yield session


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        # Import all models here to ensure they're registered
        from src.models.user import User
        from src.models.oauth import OAuthAccount
        from src.models.email_verification import EmailVerification
        from src.models.password_reset import PasswordReset

        # Import models from init_db as well
        from src.db.init_db import (
            User as InitUser,
            OAuthAccount as InitOAuthAccount,
            EmailVerification as InitEmailVerification,
            PasswordReset as InitPasswordReset,
            ProgressRecord,
            Bookmark
        )

        await conn.run_sync(Base.metadata.create_all)
