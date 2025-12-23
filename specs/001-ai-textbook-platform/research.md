# Research: AI-Native Textbook Platform

**Feature**: AI-Native Textbook Platform
**Branch**: `001-ai-textbook-platform`
**Date**: 2025-12-22

## Overview

This document captures technology research and architectural decisions for the AI-Native Textbook Platform. All decisions align with the constitution's free-tier mandate and deployment-aware architecture principles.

## Frontend Technology Stack

### Decision: Docusaurus 3.0+

**Chosen**: Docusaurus 3.0+ for static site generation

**Rationale**:
- Purpose-built for documentation and textbook content
- Excellent i18n support with locale-specific content files
- Built-in search, versioning, and navigation
- Static site deployment compatible with Vercel free tier
- MDX support for interactive components
- Zero-build-cost with edge caching

**Alternatives Considered**:
- **Next.js 14**: More flexible but heavier for pure content sites; requires more setup for i18n
- **Astro**: Excellent performance but less mature i18n ecosystem; fewer textbook-specific features
- **Hugo**: Very fast but less React ecosystem integration; harder to customize

**Implementation Notes**:
- Use `@docusaurus/theme-mermaid` for diagram support
- `next-intl` not needed - Docusaurus has built-in i18n
- Custom React components for ChatbotWidget, ProgressBar, AuthModal

---

## Backend Technology Stack

### Decision: FastAPI (Python 3.11+)

**Chosen**: FastAPI for all three backend services

**Rationale**:
- Async/await support for better performance on Railway's limited resources
- Automatic OpenAPI documentation
- Pydantic for request/response validation
- Modern Python with strong typing
- Excellent OAuth library support (`python-jose`, `httpx`)
- Cold start optimization with `uvicorn` workers

**Alternatives Considered**:
- **Node.js/Express**: Good ecosystem but heavier memory footprint; less suitable for Railway's 512MB limit
- **Go/Fiber**: Excellent performance but more complex OAuth integration; fewer AI/ML libraries

---

## Database Architecture

### Decision: Neon Serverless PostgreSQL

**Chosen**: Neon for all user data (auth, progress, bookmarks)

**Rationale**:
- Serverless = scales to zero when unused (cost savings)
- Free tier: 0.5GB storage, 300 hours compute
- Full PostgreSQL compatibility ( SQLAlchemy works out-of-box)
- Excellent Python driver support (`asyncpg`, `psycopg2`)
- Branching for development/testing

**Schema Design**:
```
users (id, email, password_hash, display_name, preferred_language, is_verified, created_at, last_active)
progress_records (id, user_id, chapter_id, status, last_position, updated_at)
bookmarks (id, user_id, chapter_id, section_id, note, created_at)
oauth_accounts (id, user_id, provider, provider_user_id) - for Google/GitHub OAuth
email_verifications (id, user_id, token, expires_at)
password_resets (id, user_id, token, expires_at)
```

**Connection Pooling**:
- Use `sqlalchemy.ext.asyncio` with asyncpg
- Pool size: 5 connections (Railway free tier optimization)
- Lazy connection initialization

---

## Vector Database

### Decision: Qdrant Cloud

**Chosen**: Qdrant for vector embeddings storage

**Rationale**:
- Free tier: 1GB storage, 1k requests/day
- Excellent Python client (`qdrant-client`)
- Hybrid search (semantic + keyword) built-in
- Payload filtering for chapter/section metadata
- Cloud-hosted (no self-hosting needed)

**Collections**:
- `textbook_en`: English content embeddings
- `textbook_ur`: Urdu content embeddings
- `code_examples`: Separate collection for code snippets

**Embedding Model**:
- Cohere `embed-multilingual-v3` (free tier)
- 1024 dimensions
- Supports English and Urdu in single model

---

## Authentication Strategy

### Decision: JWT with httpOnly Cookies + OAuth

**Chosen**: Custom JWT implementation with OAuth provider support

**Rationale**:
- No paid Auth0/Firebase required
- Full control over user data (GDPR compliance)
- JWT stateless = works with free-tier constraints
- httpOnly cookies prevent XSS attacks
- OAuth for social login (Google, GitHub)

**Implementation**:
- `python-jose[cryptography]` for JWT handling
- `passlib[bcrypt]` for password hashing
- `httpx` for OAuth provider communication
- Session expiry: 7 days (configurable)

**Email Verification**:
- Resend free tier for transactional emails
- Verification tokens: 24-hour expiry
- Password reset tokens: 1-hour expiry

---

## RAG Chatbot Architecture

### Decision: Groq LLaMA 3 + Cohere Embeddings

**Chosen**: Groq for LLM inference, Cohere for embeddings

**Rationale**:
- **Groq LLaMA 3 70B**:
  - Free tier with excellent speed
  - 70B parameters for quality responses
  - Low latency (~1-2 seconds for typical queries)

- **Cohere Command R+** (fallback):
  - Free tier alternative if Groq unavailable
  - Good multilingual support

**Alternatives Considered**:
- **OpenAI GPT**: Paid only - violates free-tier mandate
- **Anthropic Claude**: Paid for runtime use - violates Claude Scope Discipline principle
- **Local LLM (Ollama)**: Too heavy for Railway 512MB RAM

**RAG Pipeline**:
1. User question → Detect language (en/ur)
2. Select collection based on language
3. Qdrant semantic search (top 5 chunks)
4. Groq LLaMA 3 with retrieved context
5. Format response with source references

**Chunking Strategy**:
- 500-1000 tokens per chunk
- 100 token overlap between chunks
- Metadata: chapter, section, header, language

---

## Personalization Engine

### Decision: Rule-Based with Content Analysis

**Chosen**: Simple rule-based recommendations

**Rationale**:
- No ML model training needed (saves complexity)
- Sufficient for initial 100-500 users
- Can evolve to ML-based later

**Recommendation Rules**:
1. **Sequential**: Completed Chapter N → Recommend Chapter N+1
2. **Bookmark-based**: Frequently bookmarked topics → Recommend related chapters
3. **Progress-based**: Stuck on Chapter N → Suggest foundational chapters

**Data Points Tracked**:
- Chapter status: not_started, in_progress, complete
- Last read position: section_id
- Bookmarks: section_id with optional notes
- Reading streak: consecutive days

---

## Deployment Architecture

### Decision: Vercel + Railway

**Chosen**: Vercel for frontend, Railway for backend

**Vercel (Frontend)**:
- Free tier: 100GB bandwidth, 100GB-Hours execution
- Edge deployment for global CDN
- Automatic HTTPS
- Preview deployments for branches

**Railway (Backend)**:
- Free tier: 512MB RAM, $5 credit monthly
- Container-based (Dockerfile required)
- Three separate services (auth, chatbot, personalization)
- Each service scales independently

**Cold Start Optimization**:
- Use Alpine-based Docker images
- Lazy import heavy libraries
- Connection pooling for databases
- Health check at `/health` endpoint

---

## Multilingual Support

### Decision: Docusaurus i18n + Separate Content Files

**Chosen**: Locale-specific markdown files

**Rationale**:
- Docusaurus has built-in i18n support
- Separate files per language = easier content management
- URL structure: `/en/chapter-01` vs `/ur/chapter-01`
- RTL CSS for Urdu (`direction: rtl`)

**Supported Languages**:
- English (`en`) - default
- Urdu (`ur`) - RTL layout

**Future Extensibility**:
- Arabic (`ar`) - RTL
- Hindi (`hi`)
- Spanish (`es`)

**UI Translation**:
- `i18n/en.json`: English UI strings
- `i18n/ur.json`: Urdu UI strings
- Component use `useDocusaurusContext()` for translations

---

## Performance Optimization

### Frontend

- Code splitting by chapter
- Lazy load images (`loading="lazy"`)
- Inline critical CSS
- Prefetch next chapter links
- Service Worker for offline caching (future)

### Backend

- Async/await for I/O operations
- Response compression (gzip)
- Cache Qdrant search results (5-minute TTL)
- Database query optimization (indexes on user_id, chapter_id)
- Rate limiting: 100 requests/minute per IP

---

## Security Considerations

### Frontend

- Content Security Policy (CSP) headers
- Sanitize all user input
- HTTPS only (Vercel automatic)
- No secrets in frontend code

### Backend

- Rate limiting on auth endpoints
- CORS whitelist for frontend domain
- JWT secret from environment variable
- Password hashing with bcrypt (cost=12)
- SQL injection prevention (SQLAlchemy ORM)

---

## Monitoring & Observability

### Free-Tier Compatible Options

- **Logging**: stdout/stderr (Railway captures)
- **Health Checks**: `/health` endpoint on all services
- **Error Tracking**: Sentry free tier (optional)
- **Analytics**: Vercel Analytics (built-in, free)

### Metrics to Track

- Response times (p50, p95, p99)
- Error rates by endpoint
- Active user count
- Chatbot query success rate

---

## Free Tier Limits Summary

| Service | Free Tier Limit | Expected Usage | Buffer |
|---------|----------------|----------------|--------|
| Vercel | 100GB bandwidth | ~50GB (100 users × 10 chapters) | 50% |
| Railway | 512MB RAM, $5 credit | ~256MB per service | 50% |
| Neon | 0.5GB storage, 300h compute | ~100MB, 50h/month | 80% |
| Qdrant | 1GB storage, 1k requests/day | ~500MB, 500 requests | 50% |
| Cohere | Free tier API limits | Embeddings only (build-time) | N/A |
| Groq | Free tier API limits | LLM queries only | N/A |
| Resend | 100 emails/day | ~50 emails/day | 50% |

---

## Open Questions & Decisions Deferred

1. **Custom Domain**: Use `vercel.app` subdomain initially; custom domain can be added later
2. **Analytics**: Start with Vercel Analytics; add Google Analytics if needed
3. **Content Updates**: Initially manual (edit markdown, rebuild); consider CMS for future
4. **Backup Strategy**: Neon provides automated backups; no additional backup needed initially

---

## References

- Docusaurus: https://docusaurus.io/
- FastAPI: https://fastapi.tiangolo.com/
- Neon PostgreSQL: https://neon.tech/
- Qdrant: https://qdrant.tech/
- Groq: https://groq.com/
- Cohere: https://cohere.com/
- Railway: https://railway.app/
- Vercel: https://vercel.com/
