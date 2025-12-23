"""
Progress Record ORM model.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, func, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ProgressRecord:
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
        Index('idx_progress_user_chapter', 'user_id', 'chapter_id'),
        Index('idx_progress_user_status', 'user_id', 'status'),
    )

    def __repr__(self):
        return f"<ProgressRecord(id={self.id}, user_id={self.user_id}, chapter_id={self.chapter_id}, status={self.status})>"

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "chapter_id": self.chapter_id,
            "status": self.status,
            "last_position": self.last_position,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
