"""
Personalization Service - Main FastAPI application

This service handles progress tracking, bookmarks, and recommendations.
"""

from fastapi import FastAPI, HTTPException, status, Depends, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
import uuid
from datetime import datetime

from src.core.config import config
from src.core.security import verify_token
from src.core.recommender import RecommendationEngine
from src.db.session import get_db, init_db

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Personalization Service API",
    description="Progress tracking, bookmarks, and recommendations API for AI-Native Textbook Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Initialize recommendation engine
recommender = RecommendationEngine()


# Request/Response Models
class ProgressRecordResponse(BaseModel):
    id: str
    chapter_id: str
    status: str  # not_started, in_progress, complete
    last_position: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UpdateProgressRequest(BaseModel):
    status: str = Field(..., regex="^(not_started|in_progress|complete)$")
    last_position: Optional[str] = Field(None, max_length=100)


class ProgressSummaryResponse(BaseModel):
    total_chapters: int
    completed_chapters: int
    in_progress_chapters: int
    completion_percentage: float
    current_chapter: Optional[str] = None
    streak_days: int = 0


class BookmarkResponse(BaseModel):
    id: str
    chapter_id: str
    section_id: str
    note: Optional[str] = None
    created_at: str


class CreateBookmarkRequest(BaseModel):
    chapter_id: str
    section_id: str
    note: Optional[str] = Field(None, max_length=1000)


class UpdateBookmarkRequest(BaseModel):
    note: Optional[str] = Field(None, max_length=1000)


class RecommendationResponse(BaseModel):
    chapter_id: str
    chapter_title: str
    reason: str  # sequential, bookmark_based, foundational
    description: str


class HealthResponse(BaseModel):
    status: str


# Dependency to get current user
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """Verify token and return user_id."""
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user_id


# API Routes
@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok")


# Progress endpoints
@app.get("/progress", response_model=List[ProgressRecordResponse], tags=["progress"])
async def get_progress(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get user's reading progress for all chapters."""
    try:
        from src.db.init_db import ProgressRecord

        result = await db.execute(
            select(ProgressRecord).where(ProgressRecord.user_id == uuid.UUID(user_id))
        )
        records = result.scalars().all()

        return [
            ProgressRecordResponse(
                id=str(record.id),
                chapter_id=record.chapter_id,
                status=record.status,
                last_position=record.last_position,
                updated_at=record.updated_at.isoformat() if record.updated_at else None
            )
            for record in records
        ]

    except Exception as e:
        logger.error(f"Error getting progress: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get progress"
        )


@app.get("/progress/{chapter_id}", response_model=ProgressRecordResponse, tags=["progress"])
async def get_chapter_progress(
    chapter_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get progress for a specific chapter."""
    try:
        from src.db.init_db import ProgressRecord

        result = await db.execute(
            select(ProgressRecord).where(
                ProgressRecord.user_id == uuid.UUID(user_id),
                ProgressRecord.chapter_id == chapter_id
            )
        )
        record = result.scalar_one_or_none()

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Progress record not found"
            )

        return ProgressRecordResponse(
            id=str(record.id),
            chapter_id=record.chapter_id,
            status=record.status,
            last_position=record.last_position,
            updated_at=record.updated_at.isoformat() if record.updated_at else None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chapter progress: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get chapter progress"
        )


@app.put("/progress/{chapter_id}", response_model=ProgressRecordResponse, tags=["progress"])
async def update_progress(
    chapter_id: str,
    request: UpdateProgressRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Update progress for a chapter."""
    try:
        from src.db.init_db import ProgressRecord

        # Check if record exists
        result = await db.execute(
            select(ProgressRecord).where(
                ProgressRecord.user_id == uuid.UUID(user_id),
                ProgressRecord.chapter_id == chapter_id
            )
        )
        record = result.scalar_one_or_none()

        if record:
            # Update existing record
            record.status = request.status
            record.last_position = request.last_position
            record.updated_at = datetime.utcnow()
        else:
            # Create new record
            record = ProgressRecord(
                user_id=uuid.UUID(user_id),
                chapter_id=chapter_id,
                status=request.status,
                last_position=request.last_position
            )
            db.add(record)

        await db.commit()
        await db.refresh(record)

        return ProgressRecordResponse(
            id=str(record.id),
            chapter_id=record.chapter_id,
            status=record.status,
            last_position=record.last_position,
            updated_at=record.updated_at.isoformat() if record.updated_at else None
        )

    except Exception as e:
        logger.error(f"Error updating progress: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update progress"
        )


@app.get("/progress/summary", response_model=ProgressSummaryResponse, tags=["progress"])
async def get_progress_summary(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get overall progress summary."""
    try:
        from src.db.init_db import ProgressRecord

        result = await db.execute(
            select(ProgressRecord).where(ProgressRecord.user_id == uuid.UUID(user_id))
        )
        records = result.scalars().all()

        total_chapters = 6  # Number of textbook chapters
        completed = sum(1 for r in records if r.status == "complete")
        in_progress = sum(1 for r in records if r.status == "in_progress")

        # Find current chapter (most recently updated in_progress)
        current_chapter = None
        latest_update = None
        for record in records:
            if record.status == "in_progress":
                if latest_update is None or record.updated_at > latest_update:
                    latest_update = record.updated_at
                    current_chapter = record.chapter_id

        return ProgressSummaryResponse(
            total_chapters=total_chapters,
            completed_chapters=completed,
            in_progress_chapters=in_progress,
            completion_percentage=round((completed / total_chapters) * 100, 2) if total_chapters > 0 else 0,
            current_chapter=current_chapter,
            streak_days=0  # TODO: Implement streak calculation
        )

    except Exception as e:
        logger.error(f"Error getting progress summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get progress summary"
        )


# Bookmark endpoints
@app.get("/bookmarks", response_model=List[BookmarkResponse], tags=["bookmarks"])
async def list_bookmarks(
    chapter_id: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """List user's bookmarks, optionally filtered by chapter."""
    try:
        from src.db.init_db import Bookmark

        query = select(Bookmark).where(Bookmark.user_id == uuid.UUID(user_id))

        if chapter_id:
            query = query.where(Bookmark.chapter_id == chapter_id)

        result = await db.execute(query.order_by(Bookmark.created_at.desc()))
        records = result.scalars().all()

        return [
            BookmarkResponse(
                id=str(record.id),
                chapter_id=record.chapter_id,
                section_id=record.section_id,
                note=record.note,
                created_at=record.created_at.isoformat() if record.created_at else ""
            )
            for record in records
        ]

    except Exception as e:
        logger.error(f"Error listing bookmarks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list bookmarks"
        )


@app.post("/bookmarks", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED, tags=["bookmarks"])
async def create_bookmark(
    request: CreateBookmarkRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Create a new bookmark."""
    try:
        from src.db.init_db import Bookmark

        # Check if bookmark already exists
        result = await db.execute(
            select(Bookmark).where(
                Bookmark.user_id == uuid.UUID(user_id),
                Bookmark.chapter_id == request.chapter_id,
                Bookmark.section_id == request.section_id
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bookmark already exists for this section"
            )

        bookmark = Bookmark(
            user_id=uuid.UUID(user_id),
            chapter_id=request.chapter_id,
            section_id=request.section_id,
            note=request.note
        )
        db.add(bookmark)
        await db.commit()
        await db.refresh(bookmark)

        return BookmarkResponse(
            id=str(bookmark.id),
            chapter_id=bookmark.chapter_id,
            section_id=bookmark.section_id,
            note=bookmark.note,
            created_at=bookmark.created_at.isoformat() if bookmark.created_at else ""
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating bookmark: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create bookmark"
        )


@app.delete("/bookmarks/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["bookmarks"])
async def delete_bookmark(
    bookmark_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Delete a bookmark."""
    try:
        from src.db.init_db import Bookmark

        result = await db.execute(
            select(Bookmark).where(
                Bookmark.id == uuid.UUID(bookmark_id),
                Bookmark.user_id == uuid.UUID(user_id)
            )
        )
        bookmark = result.scalar_one_or_none()

        if not bookmark:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bookmark not found"
            )

        await db.delete(bookmark)
        await db.commit()

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting bookmark: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete bookmark"
        )


# Recommendations endpoint
@app.get("/recommendations", response_model=List[RecommendationResponse], tags=["recommendations"])
async def get_recommendations(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized chapter recommendations."""
    try:
        # Get user progress
        from src.db.init_db import ProgressRecord, Bookmark

        progress_result = await db.execute(
            select(ProgressRecord).where(ProgressRecord.user_id == uuid.UUID(user_id))
        )
        progress_records = progress_result.scalars().all()

        # Get user bookmarks
        bookmark_result = await db.execute(
            select(Bookmark).where(Bookmark.user_id == uuid.UUID(user_id))
        )
        bookmark_records = bookmark_result.scalars().all()

        # Convert to dicts
        progress_list = [r.to_dict() for r in progress_records]
        bookmark_list = [b.to_dict() for b in bookmark_records]

        # Get recommendations
        recommendations = recommender.get_recommendations(progress_list, bookmark_list)

        return [
            RecommendationResponse(**rec)
            for rec in recommendations
        ]

    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get recommendations"
        )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Personalization Service...")
    await init_db()
    logger.info("Database tables initialized")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Personalization Service...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.host, port=config.port)
