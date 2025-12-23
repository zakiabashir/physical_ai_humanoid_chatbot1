"""
User ORM model for authentication service.
"""

from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid


class User:
    """User account model for authentication and personalization."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # NULL for OAuth-only users
    display_name = Column(String(100), nullable=False)
    preferred_language = Column(String(5), nullable=False, default='en', index=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships (these will be defined in SQLAlchemy models)
    # oauth_accounts = relationship("OAuthAccount", back_populates="user")
    # progress_records = relationship("ProgressRecord", back_populates="user", cascade="all, delete-orphan")
    # bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, display_name={self.display_name})>"

    def to_dict(self):
        """Convert user to dictionary (excluding sensitive data)."""
        return {
            "id": str(self.id),
            "email": self.email,
            "display_name": self.display_name,
            "preferred_language": self.preferred_language,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_active": self.last_active.isoformat() if self.last_active else None,
        }
