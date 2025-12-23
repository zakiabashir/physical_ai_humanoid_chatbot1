"""
OAuth Account ORM model.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, func, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid


class OAuthAccount:
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

    def __repr__(self):
        return f"<OAuthAccount(id={self.id}, provider={self.provider}, user_id={self.user_id})>"

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "provider": self.provider,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
