"""
Database initialization and schema for AI-Native Textbook Platform.

This module creates all database tables for the authentication and personalization services.
Tables: users, oauth_accounts, email_verifications, password_resets, progress_records, bookmarks
"""

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Text,
    Integer,
    CheckConstraint,
    Index,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class User(Base):
    """User account information for authentication and personalization."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # NULL for OAuth-only users
    display_name = Column(String(100), nullable=False)
    preferred_language = Column(String(5), nullable=False, default='en', index=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("preferred_language IN ('en', 'ur')", name="check_language"),
    )


class OAuthAccount(Base):
    """Links users to their OAuth provider accounts (Google, GitHub)."""

    __tablename__ = "oauth_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider = Column(String(50), nullable=False)
    provider_user_id = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('provider', 'provider_user_id', name='unique_oauth_provider_user'),
        Index('idx_oauth_provider', 'provider', 'provider_user_id'),
    )


class EmailVerification(Base):
    """Stores email verification tokens for new account activation."""

    __tablename__ = "email_verifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PasswordReset(Base):
    """Stores password reset tokens for account recovery."""

    __tablename__ = "password_resets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProgressRecord(Base):
    """Tracks user reading progress through textbook chapters."""

    __tablename__ = "progress_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default='not_started')
    last_position = Column(String(100), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'chapter_id', name='unique_user_chapter'),
        CheckConstraint("status IN ('not_started', 'in_progress', 'complete')", name="check_progress_status"),
        Index('idx_progress_user_chapter', 'user_id', 'chapter_id'),
        Index('idx_progress_user_status', 'user_id', 'status'),
    )


class Bookmark(Base):
    """Stores user-saved bookmarks for specific textbook sections."""

    __tablename__ = "bookmarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(String(50), nullable=False)
    section_id = Column(String(100), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'chapter_id', 'section_id', name='unique_user_section'),
        Index('idx_bookmark_user_chapter', 'user_id', 'chapter_id'),
        Index('idx_bookmark_user_section', 'user_id', 'chapter_id', 'section_id'),
    )


# Create all tables
async def create_all_tables(engine):
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Drop all tables (use with caution!)
async def drop_all_tables(engine):
    """Drop all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
