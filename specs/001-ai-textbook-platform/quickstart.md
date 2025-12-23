# Quickstart Guide: AI-Native Textbook Platform

**Feature**: AI-Native Textbook Platform
**Branch**: `001-ai-textbook-platform`
**Date**: 2025-12-22

## Overview

This guide helps developers set up and run the AI-Native Textbook Platform locally. The platform consists of a Docusaurus frontend and three FastAPI backend services.

## Prerequisites

### Required Software

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Backend services |
| Node.js | 18+ | Frontend build |
| Git | Latest | Version control |
| Docker | Latest | Local development |
| pnpm/npm | Latest | Package management |

### Required Accounts (Free Tiers)

| Service | Purpose | Link |
|---------|---------|------|
| Neon | PostgreSQL database | https://neon.tech/ |
| Qdrant Cloud | Vector database | https://cloud.qdrant.io/ |
| Cohere | Embeddings | https://cohere.com/ |
| Groq | LLM inference | https://groq.com/ |
| Resend | Transactional emails | https://resend.com/ |
| Google OAuth | Social login | https://console.cloud.google.com/ |
| GitHub OAuth | Social login | https://github.com/settings/developers |

## Quick Start (5 Minutes)

### 1. Clone and Setup Environment

```bash
# Clone repository
git clone https://github.com/your-org/physical_ai_humanoid_chatbot1.git
cd physical_ai_humanoid_chatbot1

# Create .env from template
cp .env.example .env

# Edit .env with your API keys
# (See Environment Variables section below)
```

### 2. Start Backend Services

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Or run services individually
cd backend/auth_service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8001

# In separate terminals:
cd backend/chatbot_service
# ... (same process, port 8002)

cd backend/personalization_service
# ... (same process, port 8003)
```

### 3. Start Frontend

```bash
cd frontend
npm install
npm run start
```

### 4. Access the Platform

- Frontend: http://localhost:3000
- Auth API: http://localhost:8001/docs
- Chatbot API: http://localhost:8002/docs
- Personalization API: http://localhost:8003/docs

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

### Frontend (Vercel)

```bash
# API URLs (update with deployed URLs)
NEXT_PUBLIC_AUTH_API_URL=http://localhost:8001
NEXT_PUBLIC_CHATBOT_API_URL=http://localhost:8002
NEXT_PUBLIC_PERSONALIZATION_API_URL=http://localhost:8003
```

### Auth Service

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@ep-xyz.region.aws.neon.tech/neondb?sslmode=require

# JWT
JWT_SECRET_KEY=your-secret-key-min-32-characters
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=168

# Email (Resend)
RESEND_API_KEY=re_xxxxxxxxxxxx
FROM_EMAIL=noreply@yourdomain.com
FRONTEND_URL=http://localhost:3000

# OAuth - Google
OAUTH_GOOGLE_CLIENT_ID=your-google-client-id
OAUTH_GOOGLE_CLIENT_SECRET=your-google-secret
OAUTH_GOOGLE_REDIRECT_URI=http://localhost:3000/auth/callback/google

# OAuth - GitHub
OAUTH_GITHUB_CLIENT_ID=your-github-client-id
OAUTH_GITHUB_CLIENT_SECRET=your-github-secret
OAUTH_GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback/github
```

### Chatbot Service

```bash
# Qdrant
QDRANT_URL=https://xyz.aws.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_EN=textbook_en
QDRANT_COLLECTION_UR=textbook_ur

# Cohere (Embeddings)
COHERE_API_KEY=your-cohere-api-key
COHERE_MODEL=embed-multilingual-v3

# Groq (LLM)
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.1-70b-versatile

# Fallback: Cohere Command
COHERE_CHAT_API_KEY=your-cohere-api-key
COHERE_CHAT_MODEL=command-r-plus
```

### Personalization Service

```bash
# Database (same as auth service)
DATABASE_URL=postgresql+asyncpg://user:password@ep-xyz.region.aws.neon.tech/neondb?sslmode=require
```

## Development Workflow

### Running Tests

```bash
# Backend tests
cd backend/auth_service
pytest

# Frontend tests
cd frontend
npm test
```

### Building Content

```bash
# Generate textbook chapters (using Claude CLI)
cd scripts/content-generator
python generate-chapter.py --chapter "01-foundations" --output ../../frontend/docs/en/chapter-01-foundations.md

# Translate to Urdu
python translate-urdu.py --input ../../frontend/docs/en/chapter-01-foundations.md --output ../../frontend/docs/ur/chapter-01-foundations.md
```

### Indexing Content for RAG

```bash
# Generate embeddings and upload to Qdrant
cd scripts/embedding-indexer
python index-content.py --content-dir ../../frontend/docs/en --collection textbook_en
python index-content.py --content-dir ../../frontend/docs/ur --collection textbook_ur
```

### Database Migrations

```bash
cd backend/auth_service

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Project Structure Reference

```
physical_ai_humanoid_chatbot1/
├── backend/
│   ├── auth_service/         # Port 8001
│   ├── chatbot_service/      # Port 8002
│   └── personalization_service/  # Port 8003
├── frontend/                 # Docusaurus (Port 3000)
├── scripts/
│   ├── content-generator/    # Chapter generation
│   └── embedding-indexer/   # RAG indexing
└── docker-compose.yml        # All services
```

## Common Tasks

### Add a New Chapter

1. Generate content:
   ```bash
   python scripts/content-generator/generate-chapter.py \
       --chapter "07-new-topic" \
       --output frontend/docs/en/chapter-07-new-topic.md
   ```

2. Add to `frontend/sidebars.ts`:
   ```typescript
   {
     type: 'doc',
     id: 'chapter-07-new-topic',
     label: 'Chapter 7: New Topic',
   }
   ```

3. Re-index for RAG:
   ```bash
   python scripts/embedding-indexer/index-content.py \
       --content-dir frontend/docs/en \
       --collection textbook_en
   ```

### Add a New Language

1. Add locale to `frontend/docusaurus.config.ts`:
   ```typescript
   i18n: {
     defaultLocale: 'en',
     locales: ['en', 'ur', 'es'],  // Add 'es'
     localeConfigs: {
       es: { label: 'Español', direction: 'ltr' }
     }
   }
   ```

2. Create content directory:
   ```bash
   mkdir -p frontend/docs/es
   ```

3. Create translation file:
   ```bash
   cp i18n/en.json i18n/es.json
   # Translate strings
   ```

4. Update Qdrant collection:
   ```bash
   python scripts/embedding-indexer/index-content.py \
       --content-dir frontend/docs/es \
       --collection textbook_es \
       --language es
   ```

### Reset Database

```bash
# Drop all tables
psql $DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Re-run migrations
cd backend/auth_service
alembic upgrade head
```

## Deployment

### Deploy to Railway (Backend)

```bash
cd backend/auth_service
railway login
railway init
railway up

# Set environment variables in Railway dashboard
railway variables set DATABASE_URL=$DATABASE_URL
railway variables set JWT_SECRET_KEY=$JWT_SECRET_KEY
# ... etc

# Get deployed URL
railway domain
```

### Deploy to Vercel (Frontend)

```bash
cd frontend
vercel login
vercel

# Set environment variables
vercel env add NEXT_PUBLIC_AUTH_API_URL
vercel env add NEXT_PUBLIC_CHATBOT_API_URL
vercel env add NEXT_PUBLIC_PERSONALIZATION_API_URL

# Deploy
vercel --prod
```

## Troubleshooting

### Port Already in Use

```bash
# Find process on port
lsof -i :3001  # macOS/Linux
netstat -ano | findstr :3001  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Database Connection Issues

1. Verify Neon database is active
2. Check `DATABASE_URL` format
3. Ensure SSL mode is enabled (`sslmode=require`)
4. Check IP whitelist in Neon console

### Qdrant Connection Issues

1. Verify API key is correct
2. Check collection exists: `curl https://your-qdrant-url/collections`
3. Ensure free tier limits not exceeded

### Chatbot Returns No Results

1. Verify Qdrant collections are populated
2. Check embeddings were indexed
3. Test search manually:
   ```python
   from qdrant_client import QdrantClient
   client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
   results = client.search(collection_name="textbook_en", query_vector=embedding, limit=5)
   print(results)
   ```

## Useful Commands

```bash
# Backend health checks
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health

# Database connection test
psql $DATABASE_URL -c "SELECT 1;"

# Qdrant collection info
curl https://your-qdrant-url/collections/textbook_en

# Frontend build test
cd frontend && npm run build
```

## Resources

- **Constitution**: `.specify/memory/constitution.md`
- **Specification**: `specs/001-ai-textbook-platform/spec.md`
- **Data Model**: `specs/001-ai-textbook-platform/data-model.md`
- **Research**: `specs/001-ai-textbook-platform/research.md`
- **API Contracts**: `specs/001-ai-textbook-platform/contracts/`

## Getting Help

1. Check this quickstart guide first
2. Review the troubleshooting section
3. Check service logs: `docker-compose logs [service-name]`
4. Open an issue on GitHub with:
   - Error messages
   - Steps to reproduce
   - Environment details (OS, Python version, etc.)
