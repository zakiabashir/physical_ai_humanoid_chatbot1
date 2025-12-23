"""
Bookmark ORM model.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Text, func, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Bookmark:
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

    def __repr__(self):
        return f"<Bookmark(id={self.id}, user_id={self.user_id}, chapter_id={self.chapter_id}, section_id={self.section_id})>"

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "chapter_id": self.chapter_id,
            "section_id": self.section_id,
            "note": self.note,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
