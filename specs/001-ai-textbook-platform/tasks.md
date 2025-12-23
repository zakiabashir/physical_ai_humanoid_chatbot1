# Tasks: AI-Native Textbook Platform

**Input**: Design documents from `/specs/001-ai-textbook-platform/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/, research.md

**Tests**: Tests are OPTIONAL for this feature - focus on deployment and integration validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- All tasks include exact file paths for deployment targets (Vercel/Railway)

## Path Conventions

- **Frontend (Vercel)**: `frontend/` - Docusaurus static site
- **Backend (Railway)**: `backend/{service}/src/` - FastAPI services
- **Services**: auth_service, chatbot_service, personalization_service

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure

- [X] T001 Create monorepo directory structure: backend/{auth_service,chatbot_service,personalization_service}/, frontend/, scripts/
- [X] T002 Create .gitignore with Python, Node, Docker, .env patterns
- [X] T003 [P] Create .env.example with all environment variables documented
- [X] T004 [P] Create docker-compose.yml for local development (Neon, Qdrant local)
- [ ] T005 [P] Initialize Git repository and initial commit

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation (Railway Services)

- [X] T006 [P] Create auth_service/pyproject.toml with FastAPI, uvicorn, sqlalchemy, asyncpg dependencies
- [X] T007 [P] Create auth_service/requirements.txt from pyproject.toml
- [X] T008 [P] Create auth_service/Dockerfile for Railway deployment
- [X] T009 [P] Create chatbot_service/requirements.txt with FastAPI, qdrant-client, cohere, groq
- [X] T010 [P] Create chatbot_service/Dockerfile for Railway deployment
- [X] T011 [P] Create personalization_service/requirements.txt with FastAPI, sqlalchemy, asyncpg
- [X] T012 [P] Create personalization_service/Dockerfile for Railway deployment

### Frontend Foundation (Vercel)

- [X] T013 Initialize Docusaurus in frontend/ with `npx create-docusaurus@latest textbook classic`
- [X] T014 Install frontend dependencies: `npm install --save @docusaurus/theme-mermaid` in frontend/
- [X] T015 [P] Create frontend/vercel.json with build configuration

### Database Foundation

- [X] T016 Create database migration script in backend/auth_service/src/db/init_db.py with SQLAlchemy schema
- [X] T017 [P] Create alembic.ini in backend/auth_service/ for database migrations

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Read Textbook Content (Priority: P1) 🎯 MVP

**Goal**: Deliver static textbook content with chapter navigation and language switching (English/Urdu with RTL)

**Independent Test**: Deploy frontend to Vercel; verify users can navigate chapters, read content, switch languages without authentication

**Deployment Target**: Vercel (frontend)

### Content Generation

- [ ] T018 [P] [US1] Create chapter generation script in scripts/content-generator/generate-chapter.py
- [ ] T019 [P] [US1] Create Urdu translation script in scripts/content-generator/translate-urdu.py
- [X] T020 [US1] Generate Chapter 1: Physical AI Foundations in frontend/docs/en/chapter-01-foundations.md
- [X] T021 [US1] Generate Chapter 2: ROS 2 in frontend/docs/en/chapter-02-ros2.md
- [X] T022 [US1] Generate Chapter 3: Gazebo & Digital Twins in frontend/docs/en/chapter-03-gazebo.md
- [X] T023 [US1] Generate Chapter 4: NVIDIA Isaac in frontend/docs/en/chapter-04-isaac.md
- [X] T024 [US1] Generate Chapter 5: Vision-Language-Action in frontend/docs/en/chapter-05-vla.md
- [X] T025 [US1] Generate Chapter 6: Capstone Project in frontend/docs/en/chapter-06-capstone.md
- [X] T026 [US1] Generate intro page in frontend/docs/en/intro.md

### Docusaurus Configuration

- [X] T027 [P] [US1] Configure i18n for English/Urdu in frontend/docusaurus.config.ts
- [X] T028 [P] [US1] Create sidebar navigation in frontend/sidebars.ts
- [X] T029 [P] [US1] Create RTL CSS styles for Urdu in frontend/src/css/custom.css

### Urdu Content

- [X] T030 [US1] Translate Chapter 1 to Urdu in frontend/docs/ur/chapter-01-foundations.md
- [X] T031 [US1] Translate Chapter 2 to Urdu in frontend/docs/ur/chapter-02-ros2.md
- [X] T032 [US1] Translate Chapter 3 to Urdu in frontend/docs/ur/chapter-03-gazebo.md
- [X] T033 [US1] Translate Chapter 4 to Urdu in frontend/docs/ur/chapter-04-isaac.md
- [X] T034 [US1] Translate Chapter 5 to Urdu in frontend/docs/ur/chapter-05-vla.md
- [X] T035 [US1] Translate Chapter 6 to Urdu in frontend/docs/ur/chapter-06-capstone.md
- [X] T036 [US1] Create Urdu intro in frontend/docs/ur/intro.md

### UI Components

- [ ] T037 [P] [US1] Create LanguageSwitcher component in frontend/src/components/LanguageSwitcher.tsx
- [X] T038 [P] [US1] Create i18n translation files in frontend/i18n/en.json and frontend/i18n/ur.json

**Checkpoint**: Deploy to Vercel and verify: chapters load, language toggle works, Urdu renders RTL

---

## Phase 4: User Story 2 - Ask AI Chatbot Questions (Priority: P2)

**Goal**: RAG chatbot that answers questions about textbook content with source references

**Independent Test**: Deploy chatbot service to Railway; verify users can ask questions and receive answers with sources without authentication

**Deployment Target**: Railway (chatbot_service)

### Content Indexing

- [X] T039 [P] [US2] Create embedding indexer script in scripts/embedding-indexer/index-content.py
- [X] T040 [P] [US2] Create Qdrant client wrapper in backend/chatbot_service/src/core/retrieval.py
- [X] T041 [US2] Create Cohere embeddings client in backend/chatbot_service/src/core/embeddings.py
- [ ] T042 [US2] Index English content to Qdrant collection `textbook_en`
- [ ] T043 [US2] Index Urdu content to Qdrant collection `textbook_ur`

### Chatbot Service

- [X] T044 [P] [US2] Create chatbot config in backend/chatbot_service/src/core/config.py
- [X] T045 [P] [US2] Create Groq LLM client in backend/chatbot_service/src/core/llm.py
- [X] T046 [P] [US2] Create FastAPI app entry in backend/chatbot_service/src/main.py
- [ ] T047 [US2] Create health check endpoint in backend/chatbot_service/src/api/routes/health.py

### Chatbot API

- [X] T048 [US2] Create POST /chat/question endpoint in backend/chatbot_service/src/api/routes/chat.py
- [ ] T049 [US2] Create POST /chat/streams SSE endpoint in backend/chatbot_service/src/api/routes/chat.py

### Frontend Chatbot Widget

- [ ] T050 [P] [US2] Create ChatbotWidget component in frontend/src/components/ChatbotWidget.tsx
- [ ] T051 [P] [US2] Create API client in frontend/src/lib/api.ts with chatbot endpoints
- [X] T052 [P] [US2] Add chatbot environment variables to frontend/.env.example (NEXT_PUBLIC_CHATBOT_API_URL)

**Checkpoint**: Deploy chatbot_service to Railway; verify question/answer flow with sources

---

## Phase 5: User Story 3 - Create Account and Sign In (Priority: P3)

**Goal**: User authentication with email/password and OAuth (Google, GitHub)

**Independent Test**: Deploy auth service to Railway; verify users can sign up, receive verification email, sign in, maintain session

**Deployment Target**: Railway (auth_service)

### Database Models

- [X] T053 [P] [US3] Create User model in backend/auth_service/src/models/user.py
- [X] T054 [P] [US3] Create OAuthAccount model in backend/auth_service/src/models/oauth.py
- [X] T055 [P] [US3] Create EmailVerification model in backend/auth_service/src/models/email_verification.py
- [X] T056 [P] [US3] Create PasswordReset model in backend/auth_service/src/models/password_reset.py

### Auth Service Foundation

- [X] T057 [P] [US3] Create auth config in backend/auth_service/src/core/config.py
- [X] T058 [P] [US3] Create JWT security module in backend/auth_service/src/core/security.py
- [X] T059 [P] [US3] Create password hashing utilities in backend/auth_service/src/core/security.py
- [X] T060 [P] [US3] Create database session in backend/auth_service/src/db/session.py
- [X] T061 [P] [US3] Create Resend email client in backend/auth_service/src/core/email.py
- [X] T062 [P] [US3] Create FastAPI app entry in backend/auth_service/src/main.py

### Auth API Endpoints

- [X] T063 [US3] Create POST /auth/signup endpoint in backend/auth_service/src/api/routes/auth.py
- [X] T064 [US3] Create POST /auth/login endpoint in backend/auth_service/src/api/routes/auth.py
- [X] T065 [US3] Create POST /auth/logout endpoint in backend/auth_service/src/api/routes/auth.py
- [X] T066 [US3] Create GET /auth/oauth/google endpoint in backend/auth_service/src/api/routes/auth.py
- [X] T067 [US3] Create GET /auth/oauth/google/callback endpoint in backend/auth_service/src/api/routes/auth.py
- [X] T068 [US3] Create GET /auth/oauth/github endpoint in backend/auth_service/src/api/routes/auth.py
- [X] T069 [US3] Create GET /auth/oauth/github/callback endpoint in backend/auth_service/src/api/routes/auth.py
- [X] T070 [US3] Create POST /auth/verify-email endpoint in backend/auth_service/src/api/routes/auth.py
- [X] T071 [US3] Create POST /auth/resend-verification endpoint in backend/auth_service/src/api/routes/auth.py
- [X] T072 [US3] Create POST /auth/forgot-password endpoint in backend/auth_service/src/api/routes/auth.py
- [X] T073 [US3] Create POST /auth/reset-password endpoint in backend/auth_service/src/api/routes/auth.py

### User Management

- [X] T074 [US3] Create GET /users/me endpoint in backend/auth_service/src/api/routes/users.py
- [X] T075 [US3] Create PUT /users/me endpoint in backend/auth_service/src/api/routes/users.py
- [X] T076 [US3] Create DELETE /users/me endpoint in backend/auth_service/src/api/routes/users.py
- [X] T077 [US3] Create GET /users/me/export endpoint in backend/auth_service/src/api/routes/users.py

### Frontend Auth Components

- [ ] T078 [P] [US3] Create AuthModal component in frontend/src/components/AuthModal.tsx
- [ ] T079 [P] [US3] Add auth API methods to frontend/src/lib/api.ts
- [X] T080 [P] [US3] Add auth environment variables to frontend/.env.example (NEXT_PUBLIC_AUTH_API_URL)

**Checkpoint**: Deploy auth_service to Railway; verify signup/login/OAuth flows

---

## Phase 6: User Story 4 - Track Reading Progress (Priority: P4)

**Goal**: Authenticated users can track chapter progress and bookmark sections

**Independent Test**: After auth is complete, verify signed-in users see progress indicators, can mark chapters complete, bookmarks persist

**Deployment Target**: Railway (personalization_service)

### Database Models

- [X] T081 [P] [US4] Create ProgressRecord model in backend/personalization_service/src/models/progress.py
- [X] T082 [P] [US4] Create Bookmark model in backend/personalization_service/src/models/bookmark.py

### Personalization Service Foundation

- [X] T083 [P] [US4] Create personalization config in backend/personalization_service/src/core/config.py
- [X] T084 [P] [US4] Create database session in backend/personalization_service/src/db/session.py
- [X] T085 [P] [US4] Create FastAPI app entry in backend/personalization_service/src/main.py

### Progress API

- [X] T086 [US4] Create GET /progress endpoint in backend/personalization_service/src/api/routes/progress.py
- [X] T087 [US4] Create GET /progress/{chapter_id} endpoint in backend/personalization_service/src/api/routes/progress.py
- [X] T088 [US4] Create PUT /progress/{chapter_id} endpoint in backend/personalization_service/src/api/routes/progress.py
- [X] T089 [US4] Create GET /progress/summary endpoint in backend/personalization_service/src/api/routes/progress.py

### Bookmarks API

- [X] T090 [US4] Create GET /bookmarks endpoint in backend/personalization_service/src/api/routes/bookmarks.py
- [X] T091 [US4] Create POST /bookmarks endpoint in backend/personalization_service/src/api/routes/bookmarks.py
- [X] T092 [US4] Create GET /bookmarks/{bookmark_id} endpoint in backend/personalization_service/src/api/routes/bookmarks.py
- [X] T093 [US4] Create PUT /bookmarks/{bookmark_id} endpoint in backend/personalization_service/src/api/routes/bookmarks.py
- [X] T094 [US4] Create DELETE /bookmarks/{bookmark_id} endpoint in backend/personalization_service/src/api/routes/bookmarks.py

### Frontend Progress Components

- [ ] T095 [P] [US4] Create ProgressBar component in frontend/src/components/ProgressBar.tsx
- [ ] T096 [P] [US4] Create bookmark button component in frontend/src/components/BookmarkButton.tsx
- [ ] T097 [P] [US4] Add progress/bookmark APIs to frontend/src/lib/api.ts
- [X] T098 [P] [US4] Add personalization environment variables to frontend/.env.example (NEXT_PUBLIC_PERSONALIZATION_API_URL)

**Checkpoint**: Deploy personalization_service; verify progress tracking and bookmarks work

---

## Phase 7: User Story 5 - Receive Personalized Recommendations (Priority: P5)

**Goal**: Recommend next chapters based on completed content and reading patterns

**Independent Test**: After users have read content, verify recommendations appear and are relevant

**Deployment Target**: Railway (personalization_service)

### Recommendation Engine

- [X] T099 [US5] Create recommender module in backend/personalization_service/src/core/recommender.py

### Recommendations API

- [X] T100 [US5] Create GET /recommendations endpoint in backend/personalization_service/src/api/routes/recommendations.py

### Frontend Recommendations

- [ ] T101 [P] [US5] Create Recommendations component in frontend/src/components/Recommendations.tsx
- [ ] T102 [P] [US5] Add recommendations API method to frontend/src/lib/api.ts

**Checkpoint**: Verify recommendations appear based on user progress

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Deployment configuration, documentation, validation

### Deployment Configuration

- [ ] T103 [P] Configure Railway environment variables for auth_service (DATABASE_URL, JWT_SECRET, RESEND_API_KEY, OAUTH_GOOGLE_*, OAUTH_GITHUB_*)
- [ ] T104 [P] Configure Railway environment variables for chatbot_service (QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY, GROQ_API_KEY)
- [ ] T105 [P] Configure Railway environment variables for personalization_service (DATABASE_URL)
- [ ] T106 [P] Configure Vercel environment variables for frontend (NEXT_PUBLIC_AUTH_API_URL, NEXT_PUBLIC_CHATBOT_API_URL, NEXT_PUBLIC_PERSONALIZATION_API_URL)

### Documentation

- [X] T107 [P] Update README.md with deployment instructions
- [ ] T108 [P] Create DEPLOYMENT.md with Railway/Vercel setup steps
- [ ] T109 [P] Verify quickstart.md validation steps work

### Testing & Validation

- [ ] T110 Run Vercel build: `cd frontend && npm run build`
- [ ] T111 Deploy frontend to Vercel and verify all pages load
- [ ] T112 Deploy auth_service to Railway and verify health endpoint
- [ ] T113 Deploy chatbot_service to Railway and verify health endpoint
- [ ] T114 Deploy personalization_service to Railway and verify health endpoint
- [ ] T115 Run end-to-end test: Anonymous user can read content
- [ ] T116 Run end-to-end test: Language switch EN ↔ UR works
- [ ] T117 Run end-to-end test: Chatbot answers questions with sources
- [ ] T118 Run end-to-end test: User signup and email verification
- [ ] T119 Run end-to-end test: OAuth login (Google/GitHub)
- [ ] T120 Run end-to-end test: Progress tracking persists
- [ ] T121 Run end-to-end test: Bookmarks work
- [ ] T122 Run end-to-end test: Recommendations display

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase
  - US1 (Read Content) - No dependencies on other user stories
  - US2 (Chatbot) - Independent of US1, can be developed in parallel
  - US3 (Auth) - Independent of US1/US2, can be developed in parallel
  - US4 (Progress) - Depends on US3 (Auth)
  - US5 (Recommendations) - Depends on US4 (Progress)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

```
US1 (Read Content) ───────┐
US2 (Chatbot) ────────────┤
US3 (Auth) ───────────────┼──→ Can develop in parallel after Foundational
                         │
US4 (Progress) ───────────┤  (depends on US3 for authentication)
US5 (Recommendations) ────┘  (depends on US4 for progress data)
```

### Critical Path (MVP)

For minimum viable product:
1. Setup → Foundational → US1 (Read Content) → Deploy to Vercel
2. **MVP DELIVERABLE**: Working textbook with content navigation

### Full Platform Critical Path

1. Setup → Foundational
2. US1 (Content) + US2 (Chatbot) + US3 (Auth) in parallel
3. US4 (Progress) after US3
4. US5 (Recommendations) after US4
5. Polish & Deploy

---

## Parallel Opportunities

### Setup Phase (T001-T005)

```bash
# These can run in parallel (different files):
T003: Create .env.example
T004: Create docker-compose.yml
T005: Initialize Git repository
```

### Foundational Phase (T006-T017)

```bash
# Backend services (independent):
T006-T008: auth_service setup
T009-T010: chatbot_service setup
T011-T012: personalization_service setup

# Frontend (independent):
T013-T015: Docusaurus setup

# Database (independent):
T016-T017: Migration scripts
```

### User Story 1 (T018-T038)

```bash
# Content generation (independent chapters):
T020-T025: Generate all English chapters (can parallelize)
T026: Generate intro

# Docusaurus config (independent):
T027-T029: Configuration files

# Urdu content (can parallelize with English):
T030-T035: Translate all chapters
T036: Translate intro
```

### User Story 2 (T039-T052)

```bash
# Indexing setup (independent):
T039-T041: Create indexer and clients

# Service setup (independent):
T044-T047: Chatbot service

# Index content (sequential, language-dependent):
T042: Index English content
T043: Index Urdu content

# Frontend (independent):
T050-T052: Chatbot widget
```

### User Story 3 (T053-T080)

```bash
# Models (all independent):
T053-T056: Create all database models

# Service foundation (all independent):
T057-T062: Create config, security, database, email, main

# Endpoints (sequential implementation):
T063-T073: Auth endpoints
T074-T077: User management

# Frontend (independent):
T078-T080: Auth components
```

### User Story 4 (T081-T098)

```bash
# Models (independent):
T081-T082: Create models

# Service foundation (independent):
T083-T085: Create config, database, main

# Progress API (sequential):
T086-T089: Progress endpoints

# Bookmarks API (sequential):
T090-T094: Bookmark endpoints

# Frontend (independent):
T095-T098: Progress components
```

### Deployment Configuration (T103-T106)

```bash
# All can run in parallel:
T103: Configure auth_service env vars
T104: Configure chatbot_service env vars
T105: Configure personalization_service env vars
T106: Configure frontend env vars
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational frontend only (T013-T015, T016-T017 for future)
3. Complete Phase 3: User Story 1 (T018-T038)
4. **STOP and VALIDATE**: Deploy to Vercel, verify content delivery
5. **MVP DELIVERABLE**: Working textbook platform with multilingual content

### Incremental Delivery (Recommended)

1. **Sprint 1**: Setup + Foundational → Foundation ready
2. **Sprint 2**: Add US1 (Content) → Deploy/Demo **MVP!**
3. **Sprint 3**: Add US2 (Chatbot) → Deploy/Demo
4. **Sprint 4**: Add US3 (Auth) → Deploy/Demo
5. **Sprint 5**: Add US4 (Progress) → Deploy/Demo
6. **Sprint 6**: Add US5 (Recommendations) → Deploy/Demo
7. **Sprint 7**: Polish & Deploy production

### Parallel Team Strategy

With 3 developers:

1. **Sprint 1**: All complete Setup + Foundational together
2. **Sprint 2+**: Once Foundational is done:
   - **Developer A**: US1 (Content) → US4 (Progress)
   - **Developer B**: US2 (Chatbot) → US5 (Recommendations)
   - **Developer C**: US3 (Auth) → Polish
3. Stories integrate independently; deploy after each sprint

---

## Deployment Targets Summary

| Task ID | Target | Service/Component |
|---------|--------|-------------------|
| T001-T005 | Local | Monorepo setup |
| T006-T012 | Railway | Backend service scaffolds |
| T013-T015 | Vercel | Docusaurus frontend |
| T016-T017 | Neon | Database schema |
| T018-T038 | Vercel | Textbook content (US1) |
| T039-T052 | Railway | Chatbot service (US2) |
| T053-T080 | Railway | Auth service (US3) |
| T081-T098 | Railway | Personalization service (US4) |
| T099-T102 | Railway | Recommendations (US5) |
| T103-T122 | All | Deployment & validation |

---

## Notes

- **[P] tasks**: Different files, no dependencies, can run in parallel
- **[USn] label**: Maps task to user story for traceability
- **Checkpoints**: Verify story independently before proceeding
- **MVP**: User Story 1 (Content delivery) is standalone value
- **Deploy incrementally**: Each story adds value without breaking previous stories
- **Free-tier constraints**: All services designed for Railway/Vercel free tiers
