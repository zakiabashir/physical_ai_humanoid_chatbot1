# Data Model: AI-Native Textbook Platform

**Feature**: AI-Native Textbook Platform
**Branch**: `001-ai-textbook-platform`
**Date**: 2025-12-22

## Overview

This document defines the database schema and entity relationships for the AI-Native Textbook Platform. All data is stored in Neon Serverless PostgreSQL using SQLAlchemy async ORM.

## Database: Neon PostgreSQL

**Connection String Format**:
```
postgresql+asyncpg://user:password@ep-xyz.region.aws.neon.tech/dbname?sslmode=require
```

## Schema

### users

Stores user account information for authentication and personalization.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email (login identifier) |
| password_hash | VARCHAR(255) | NULLABLE | Bcrypt hash (NULL for OAuth-only users) |
| display_name | VARCHAR(100) | NOT NULL | Display name for UI |
| preferred_language | VARCHAR(5) | NOT NULL, DEFAULT 'en' | 'en' or 'ur' |
| is_verified | BOOLEAN | DEFAULT FALSE | Email verification status |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation timestamp |
| last_active | TIMESTAMP | DEFAULT NOW() | Last activity timestamp |

**Indexes**:
- `idx_users_email` on (email)
- `idx_users_preferred_language` on (preferred_language)

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Password must be 8+ characters before hashing
- preferred_language must be 'en' or 'ur'

**State Transitions**:
```
[NEW] → is_verified=FALSE
      ↓ (email verified)
[VERIFIED] → is_verified=TRUE
```

---

### oauth_accounts

Links users to their OAuth provider accounts (Google, GitHub).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| user_id | UUID | FK(users.id), NOT NULL | Reference to user |
| provider | VARCHAR(50) | NOT NULL | 'google' or 'github' |
| provider_user_id | VARCHAR(255) | NOT NULL | Provider's user ID |
| created_at | TIMESTAMP | DEFAULT NOW() | Link creation timestamp |

**Indexes**:
- `idx_oauth_user_id` on (user_id)
- `idx_oauth_provider` on (provider, provider_user_id) UNIQUE

**Relationships**:
- Many-to-one with users (one user can have multiple OAuth accounts)

---

### email_verifications

Stores email verification tokens for new account activation.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| user_id | UUID | FK(users.id), NOT NULL | Reference to user |
| token | VARCHAR(255) | UNIQUE, NOT NULL | Verification token |
| expires_at | TIMESTAMP | NOT NULL | Token expiration |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes**:
- `idx_email_verification_user` on (user_id)
- `idx_email_verification_token` on (token)

**Validation Rules**:
- Token expires after 24 hours
- Old tokens are invalidated when new token is generated

---

### password_resets

Stores password reset tokens for account recovery.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| user_id | UUID | FK(users.id), NOT NULL | Reference to user |
| token | VARCHAR(255) | UNIQUE, NOT NULL | Reset token |
| expires_at | TIMESTAMP | NOT NULL | Token expiration |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes**:
- `idx_password_reset_user` on (user_id)
- `idx_password_reset_token` on (token)

**Validation Rules**:
- Token expires after 1 hour

---

### progress_records

Tracks user reading progress through textbook chapters.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| user_id | UUID | FK(users.id), NOT NULL | Reference to user |
| chapter_id | VARCHAR(50) | NOT NULL | Chapter identifier (e.g., 'chapter-01-foundations') |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'not_started' | 'not_started', 'in_progress', 'complete' |
| last_position | VARCHAR(100) | NULLABLE | Last section_id read |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `idx_progress_user_chapter` on (user_id, chapter_id) UNIQUE
- `idx_progress_user_status` on (user_id, status)

**Validation Rules**:
- One record per (user_id, chapter_id) combination
- status must be one of: 'not_started', 'in_progress', 'complete'
- chapter_id must match valid chapter identifiers

**State Transitions**:
```
[not_started] → [in_progress] → [complete]
     ↑              ↓
     └──────────────┘ (can go back to previous states)
```

---

### bookmarks

Stores user-saved bookmarks for specific textbook sections.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| user_id | UUID | FK(users.id), NOT NULL | Reference to user |
| chapter_id | VARCHAR(50) | NOT NULL | Chapter identifier |
| section_id | VARCHAR(100) | NOT NULL | Section identifier |
| note | TEXT | NULLABLE | Optional user note |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes**:
- `idx_bookmark_user_chapter` on (user_id, chapter_id)
- `idx_bookmark_user_section` on (user_id, chapter_id, section_id) UNIQUE

**Validation Rules**:
- One bookmark per (user_id, chapter_id, section_id) combination
- note limited to 1000 characters

---

## Entity Relationships (ER Diagram)

```
┌─────────────┐
│    users    │
└──────┬──────┘
       │
       ├──┬─────────────────────────────────┐
       │ │                                 │
       ▼ ▼                                 ▼ ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│oauth_accounts│    │progress_records│    │  bookmarks   │
└──────────────┘    └──────────────┘    └──────────────┘

┌──────────────┐    ┌──────────────┐
│email_verifications│  │password_resets│
└──────────────┘    └──────────────┘
       │                   │
       └───────┬───────────┘
               ▼
        ┌─────────────┐
        │    users    │
        └─────────────┘
```

## SQLAlchemy ORM Models

### User Model

```python
# backend/auth_service/src/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    display_name = Column(String(100), nullable=False)
    preferred_language = Column(String(5), nullable=False, default='en', index=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    oauth_accounts = relationship("OAuthAccount", back_populates="user")
    progress_records = relationship("ProgressRecord", back_populates="user", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
```

### ProgressRecord Model

```python
# backend/auth_service/src/models/progress.py
class ProgressRecord(Base):
    __tablename__ = "progress_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    chapter_id = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default='not_started')
    last_position = Column(String(100), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="progress_records")

    __table_args__ = (
        UniqueConstraint('user_id', 'chapter_id', name='unique_user_chapter'),
        Index('idx_progress_user_status', 'user_id', 'status'),
    )
```

### Bookmark Model

```python
# backend/auth_service/src/models/bookmark.py
class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    chapter_id = Column(String(50), nullable=False)
    section_id = Column(String(100), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="bookmarks")

    __table_args__ = (
        UniqueConstraint('user_id', 'chapter_id', 'section_id', name='unique_user_section'),
        Index('idx_bookmark_user_chapter', 'user_id', 'chapter_id'),
    )
```

## Content Structure (Static Data)

The following entities are NOT stored in the database but exist as static markdown files:

### chapters

| Attribute | Type | Description |
|-----------|------|-------------|
| id | STRING | Chapter identifier (e.g., 'chapter-01-foundations') |
| title_en | STRING | English title |
| title_ur | STRING | Urdu title |
| order | INTEGER | Display order (1-6) |
| file_path_en | STRING | Path to English markdown |
| file_path_ur | STRING | Path to Urdu markdown |
| estimated_reading_time | INTEGER | Minutes |

**Chapter Identifiers**:
- `chapter-01-foundations`: Physical AI Foundations
- `chapter-02-ros2`: ROS 2
- `chapter-03-gazebo`: Gazebo & Digital Twins
- `chapter-04-isaac`: NVIDIA Isaac
- `chapter-05-vla`: Vision-Language-Action
- `chapter-06-capstone`: Capstone Project

### sections

| Attribute | Type | Description |
|-----------|------|-------------|
| id | STRING | Section identifier (e.g., 'intro', 'sensors', 'actuators') |
| chapter_id | STRING | Parent chapter |
| title_en | STRING | English title |
| title_ur | STRING | Urdu title |
| order | INTEGER | Display order within chapter |
| file_path | STRING | Path to markdown content (if separate) |

## Qdrant Collections (Vector Database)

### textbook_en

English content embeddings for RAG chatbot.

| Payload Field | Type | Description |
|---------------|------|-------------|
| chapter_id | STRING | Chapter identifier |
| section_id | STRING | Section identifier |
| header | STRING | Section header text |
| content_type | STRING | 'text', 'code', 'diagram' |
| language | STRING | 'en' |

### textbook_ur

Urdu content embeddings for RAG chatbot.

| Payload Field | Type | Description |
|---------------|------|-------------|
| chapter_id | STRING | Chapter identifier |
| section_id | STRING | Section identifier |
| header | STRING | Section header text (Urdu) |
| content_type | STRING | 'text', 'code', 'diagram' |
| language | STRING | 'ur' |

## Migration Strategy

### Initial Setup

1. **Create database** in Neon console
2. **Run SQLAlchemy migration**:
   ```bash
   cd backend/auth_service
   alembic upgrade head
   ```

### Schema Changes

1. Create Alembic migration:
   ```bash
   alembic revision --autogenerate -m "description"
   ```
2. Review generated migration
3. Apply to database:
   ```bash
   alembic upgrade head
   ```

### Rollback

```bash
alembic downgrade -1
```

## Data Retention & Cleanup

| Data Type | Retention Period | Cleanup Method |
|-----------|------------------|----------------|
| Email verification tokens | 24 hours | Automatic expiry check |
| Password reset tokens | 1 hour | Automatic expiry check |
| Inactive user accounts | 1 year | Manual review |
| Chat query history | 90 days | Optional feature (future) |

## GDPR Compliance

### User Rights

1. **Right to Access**: Users can export all their data via `/users/me/export`
2. **Right to Deletion**: Users can delete account via DELETE `/users/me`
3. **Right to Rectification**: Users can update profile via PUT `/users/me`

### Data Export Format

```json
{
  "user": {
    "email": "user@example.com",
    "display_name": "John Doe",
    "preferred_language": "en",
    "created_at": "2025-12-22T10:00:00Z"
  },
  "progress_records": [...],
  "bookmarks": [...],
  "oauth_accounts": [...]
}
```

### Deletion Cascade

When a user is deleted:
- `progress_records` → CASCADE DELETE
- `bookmarks` → CASCADE DELETE
- `oauth_accounts` → CASCADE DELETE
- `email_verifications` → CASCADE DELETE
- `password_resets` → CASCADE DELETE

Chatbot query history (if stored) is anonymized after deletion.
