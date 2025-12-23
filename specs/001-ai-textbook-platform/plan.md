# Implementation Plan: AI-Native Textbook Platform

**Branch**: `001-ai-textbook-platform` | **Date**: 2025-12-22 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-ai-textbook-platform/spec.md`

## Summary

Build a production-ready AI-native educational platform for Physical AI and Humanoid Robotics with:
- Docusaurus-based static textbook (6 chapters) deployed to Vercel
- FastAPI backend services (auth, RAG chatbot, personalization) deployed to Railway
- Free-tier architecture: Neon PostgreSQL, Qdrant Cloud, Cohere/Groq APIs
- Multilingual support (English + Urdu with RTL)
- User authentication with OAuth (Google, GitHub)

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/JavaScript (Docusaurus frontend)
**Primary Dependencies**:
- Frontend: Docusaurus 3.0+, React 18+
- Backend: FastAPI, uvicorn, pydantic, sqlalchemy, asyncpg
- Auth: python-jose[cryptography], passlib[bcrypt], httpx
- RAG: qdrant-client, cohere, groq
**Storage**: Neon Serverless PostgreSQL (user data), Qdrant Cloud (vector embeddings)
**Testing**: pytest (backend), jest (frontend)
**Target Platform**: Vercel (frontend), Railway (backend containers)
**Project Type**: web (full-stack monorepo)
**Performance Goals**:
- Static pages load < 3 seconds (3G)
- Chatbot responds < 10 seconds (95th percentile)
- Auth requests < 2 seconds
- 100 concurrent users
**Constraints**:
- Free-tier only (no paid services)
- Stateless services (state in databases)
- Cold start tolerance < 30 seconds
- Vercel: 100GB bandwidth, Railway: 512MB RAM
**Scale/Scope**: 100-500 initial MAU, scaling to 1,000-5,000; 6 textbook chapters; 28 functional requirements

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Kit Plus Methodology

| Requirement | Status | Notes |
|-------------|--------|-------|
| spec.md before code | ✅ PASS | spec.md created at specs/001-ai-textbook-platform/spec.md |
| plan.md with architecture | ✅ PASS | This file |
| tasks.md with dependencies | ⏳ TODO | Will be created by /sp.tasks |
| ADRs for decisions | ⏳ TODO | Create if needed during implementation |
| PHRs for interactions | ⏳ TODO | Create after each user interaction |

### Principle II: Free Tier Mandate

| Requirement | Status | Notes |
|-------------|--------|-------|
| Frontend: Docusaurus/Next.js free hosting | ✅ PASS | Vercel free tier |
| Backend: FastAPI free hosting | ✅ PASS | Railway free tier |
| Databases: Neon free tier | ✅ PASS | Neon Serverless PostgreSQL |
| Vector DB: Qdrant free tier | ✅ PASS | Qdrant Cloud free tier |
| Embeddings: Cohere free tier | ✅ PASS | Cohere embed-multilingual-v3 |
| LLMs: Groq/Cohere free | ✅ PASS | Groq LLaMA 3 or Cohere Command |
| No paid APIs | ✅ PASS | All services use free tiers |

### Principle III: Claude Scope Discipline

| Requirement | Status | Notes |
|-------------|--------|-------|
| Claude ONLY for content generation | ✅ PASS | Content authoring phase only |
| Runtime uses free alternatives | ✅ PASS | Chatbot uses Groq/Cohere, not Claude |
| No Claude API in deployed apps | ✅ PASS | Confirmed in architecture |

### Principle IV: Deployment-Aware Architecture

| Requirement | Status | Notes |
|-------------|--------|-------|
| Frontend: Vercel deployable | ✅ PASS | Docusaurus static site |
| Backend: Railway container | ✅ PASS | FastAPI with Dockerfile |
| Stateless design | ✅ PASS | State in Neon PostgreSQL |
| Cold start < 30s | ✅ PASS | Railway container optimization |
| Environment variables | ✅ PASS | All config via env vars |
| Within resource limits | ✅ PASS | Architecture designed for free tiers |

### Principle VI: RAG-Optimized Content

| Requirement | Status | Notes |
|-------------|--------|-------|
| Modular structure | ✅ PASS | Chapters/sections as standalone markdown |
| 500-1000 token chunks | ✅ PASS | Content structure supports chunking |
| Clear semantic headers | ✅ PASS | Markdown with proper heading hierarchy |
| Self-contained examples | ✅ PASS | Code blocks include context |
| Frontmatter for indexing | ✅ PASS | Docusaurus frontmatter |

### Principle VIII: Multilingual Support

| Requirement | Status | Notes |
|-------------|--------|-------|
| English (default) + Urdu | ✅ PASS | Docusaurus i18n configured |
| RTL support for Urdu | ✅ PASS | CSS direction: rtl |
| i18n content structure | ✅ PASS | Separate content files per language |
| Extensible for more languages | ✅ PASS | Architecture supports additions |

### Principle VII: Authentication & Personalization

| Requirement | Status | Notes |
|-------------|--------|-------|
| Email/password auth | ✅ PASS | FastAPI auth service |
| OAuth (Google, GitHub) | ✅ PASS | OAuth integration |
| Progress tracking | ✅ PASS | PostgreSQL progress tables |
| Bookmarks | ✅ PASS | PostgreSQL bookmarks table |
| JWT sessions | ✅ PASS | httpOnly cookies |

**CONSTITUTION CHECK: ✅ ALL PASS - Proceed to implementation**

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-textbook-platform/
├── plan.md              # This file
├── research.md          # Phase 0: Technology research and decisions
├── data-model.md        # Phase 1: Database schema and entities
├── quickstart.md        # Phase 1: Developer onboarding guide
├── contracts/           # Phase 1: API contracts (OpenAPI)
│   ├── auth-api.yaml
│   ├── chatbot-api.yaml
│   └── personalization-api.yaml
└── tasks.md             # Phase 2: /sp.tasks output (NOT in this plan)
```

### Source Code (repository root)

```text
physical_ai_humanoid_chatbot1/
├── backend/                     # FastAPI services
│   ├── auth_service/           # Authentication API
│   │   ├── src/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── auth.py      # Login, signup, OAuth
│   │   │   │   │   └── users.py     # Profile, settings
│   │   │   ├── core/
│   │   │   │   ├── config.py       # Environment config
│   │   │   │   ├── security.py     # JWT, password hashing
│   │   │   │   └── email.py        # Resend integration
│   │   │   ├── models/
│   │   │   │   ├── user.py         # User ORM model
│   │   │   │   ├── progress.py     # ProgressRecord ORM
│   │   │   │   └── bookmark.py     # Bookmark ORM
│   │   │   ├── db/
│   │   │   │   ├── session.py      # Database session
│   │   │   │   └── init_db.py      # Schema initialization
│   │   │   └── main.py             # FastAPI app entry
│   │   ├── tests/
│   │   │   ├── test_auth.py
│   │   │   └── test_users.py
│   │   ├── Dockerfile
│   │   ├── pyproject.toml
│   │   └── requirements.txt
│   │
│   ├── chatbot_service/         # RAG Chatbot API
│   │   ├── src/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes/
│   │   │   │       └── chat.py     # Question answering
│   │   │   ├── core/
│   │   │   │   ├── config.py
│   │   │   │   ├── embeddings.py   # Cohere integration
│   │   │   │   ├── retrieval.py    # Qdrant search
│   │   │   │   └── llm.py          # Groq/Cohere LLM
│   │   │   ├── models/
│   │   │   │   └── query.py        # ChatQuery ORM (optional)
│   │   │   └── main.py
│   │   ├── tests/
│   │   │   └── test_chat.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── personalization_service/  # Progress & Recommendations API
│       ├── src/
│       │   ├── api/
│       │   │   ├── __init__.py
│       │   │   └── routes/
│       │   │       ├── progress.py  # Reading progress
│       │   │       ├── bookmarks.py # Bookmarks
│       │   │       └── recommendations.py
│       │   ├── core/
│       │   │   ├── config.py
│       │   │   └── recommender.py  # Recommendation engine
│       │   ├── models/
│       │   │   └── main.py
│       │   └── main.py
│       ├── tests/
│       ├── Dockerfile
│       └── requirements.txt
│
├── frontend/                    # Docusaurus textbook
│   ├── blog/                   # Optional: News/updates
│   ├── docs/                   # Textbook content
│   │   ├── en/                # English content
│   │   │   ├── chapter-01-foundations.md
│   │   │   ├── chapter-02-ros2.md
│   │   │   ├── chapter-03-gazebo.md
│   │   │   ├── chapter-04-isaac.md
│   │   │   ├── chapter-05-vla.md
│   │   │   ├── chapter-06-capstone.md
│   │   │   └── intro.md
│   │   └── ur/                # Urdu content
│   │       ├── chapter-01-foundations.md
│   │       └── ...
│   ├── i18n/                  # Translation files
│   │   ├── en.json
│   │   └── ur.json
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatbotWidget.tsx    # Floating chat interface
│   │   │   ├── ProgressBar.tsx      # Reading progress
│   │   │   ├── LanguageSwitcher.tsx # EN/UR toggle
│   │   │   └── AuthModal.tsx        # Login/signup
│   │   ├── pages/
│   │   │   └── index.tsx            # Custom homepage
│   │   ├── css/
│   │   │   └── custom.css          # RTL styles, theme
│   │   └── theme/
│   │       └── Mermaid.tsx         # Diagram support
│   ├── static/                  # Static assets
│   ├── docusaurus.config.ts      # Site configuration
│   ├── sidebars.ts              # Navigation structure
│   └── package.json
│
├── scripts/                     # Utility scripts
│   ├── content-generator/       # Claude-based content generation
│   │   ├── generate-chapter.py  # Per-chapter generation
│   │   └── translate-urdu.py    # Urdu translation
│   ├── embedding-indexer/       # Build-time content indexing
│   │   └── index-content.py     # Generate Qdrant embeddings
│   └── deploy/
│       ├── vercel-deploy.sh
│       └── railway-deploy.sh
│
├── .specify/                    # Spec-Kit Plus artifacts
├── specs/                       # Feature specifications
├── docker-compose.yml           # Local development
├── .env.example                 # Environment variables template
└── README.md
```

**Structure Decision**: Monorepo with separate frontend and backend directories. Frontend is pure Docusaurus static site. Backend has three independent FastAPI services that can be deployed separately to Railway. This separation allows independent scaling and deployment.

## Phase-wise Implementation

### PHASE 1: Repository Setup

**Goal**: Establish project structure, configuration, and development environment.

**Tools**: Git, Node.js, Python, Docker

**Deliverables**:
- Monorepo directory structure
- Backend service scaffolds with requirements.txt
- Frontend Docusaurus initialized
- .env.example with all variables documented
- .gitignore configured

---

### PHASE 2: Book Generation (Using Claude)

**Goal**: Generate all 6 textbook chapters in English and Urdu, optimized for RAG.

**Tools**: Claude CLI, Python scripts

**Deliverables**:
- 6 chapters in English (markdown)
- 6 chapters in Urdu (markdown with RTL)
- Docusaurus i18n configured
- Content generation scripts documented

---

### PHASE 3: Frontend Deployment Preparation

**Goal**: Configure Docusaurus for Vercel deployment with API integration.

**Tools**: Docusaurus, Vercel CLI, npm

**Deliverables**:
- Docusaurus fully configured
- Custom React components created
- API client with environment-based URLs
- Vercel deployment config

---

### PHASE 4: Backend Services

**Goal**: Implement three FastAPI services with database and external API integrations.

**Tools**: FastAPI, SQLAlchemy, asyncpg, Docker

**Deliverables**:
- 3 FastAPI services implemented
- Database models and migrations
- OpenAPI documentation
- Dockerfiles for Railway deployment

---

### PHASE 5: Content Indexing & Integration

**Goal**: Build and deploy content embeddings to Qdrant for RAG.

**Tools**: Python scripts, Cohere API, Qdrant

**Deliverables**:
- Embedding indexer script
- Qdrant collections populated
- Verification tests passing

---

### PHASE 6: Deployment & Validation

**Goal**: Deploy frontend to Vercel and backend services to Railway.

**Tools**: Vercel CLI, Railway CLI, docker

**Deliverables**:
- 3 Railway services deployed and healthy
- Vercel frontend deployed
- End-to-end test results
- Deployment documentation

---

## Deployment Checklist

### Vercel (Frontend)

- [ ] Docusaurus builds successfully
- [ ] Environment variables set
- [ ] i18n working (EN/UR switch)
- [ ] Chatbot widget loads
- [ ] RTL layout correct for Urdu

### Railway (Backend Services)

#### Auth Service
- [ ] Container builds and deploys
- [ ] Environment variables set (DATABASE_URL, JWT_SECRET, RESEND_API_KEY, OAuth)
- [ ] Health endpoint returns 200
- [ ] Database migrations run successfully

#### Chatbot Service
- [ ] Environment variables set (QDRANT_URL, COHERE_API_KEY, GROQ_API_KEY)
- [ ] Collections exist in Qdrant
- [ ] Question endpoint returns answers with sources

#### Personalization Service
- [ ] Environment variables set (DATABASE_URL)
- [ ] Progress endpoints work
- [ ] Bookmark endpoints work

### External Services

- [ ] Neon PostgreSQL: Database and tables created
- [ ] Qdrant Cloud: Collections created and indexed
- [ ] Cohere: Free tier account configured
- [ ] Groq: Free tier account configured
- [ ] OAuth Providers: Apps created
- [ ] Resend: Free tier account configured

### Testing

- [ ] Anonymous user can access all content
- [ ] Language switch works correctly
- [ ] Chatbot answers questions (EN and UR)
- [ ] Signup flow complete with email verification
- [ ] OAuth login works (Google, GitHub)
- [ ] Progress tracking persists
- [ ] Bookmarks work
- [ ] Recommendations display
- [ ] Performance targets met

---

## Complexity Tracking

> No constitution violations requiring justification. All requirements align with free-tier, deployment-aware, multilingual platform principles.

---

## Next Steps After This Plan

1. **Run `/sp.tasks`** to generate detailed implementation tasks
2. **Begin Phase 1** (Repository Setup)
3. **Create ADRs** if any architectural decisions need documentation (e.g., "Why three separate backend services instead of monolith?")

---

**Phase 0 Output**: See [research.md](./research.md) for technology research and decisions.

**Phase 1 Output**: See [data-model.md](./data-model.md), [quickstart.md](./quickstart.md), and [contracts/](./contracts/) for detailed design artifacts.
