---
id: 002
title: AI Textbook Platform Implementation Plan
stage: plan
date: 2025-12-22
surface: agent
model: glm-4.6
feature: 001-ai-textbook-platform
branch: 001-ai-textbook-platform
user: User
command: /sp.plan
labels: ["plan","implementation","architecture"]
links:
  spec: specs/001-ai-textbook-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-ai-textbook-platform/plan.md
  - specs/001-ai-textbook-platform/research.md
  - specs/001-ai-textbook-platform/data-model.md
  - specs/001-ai-textbook-platform/quickstart.md
  - specs/001-ai-textbook-platform/contracts/auth-api.yaml
  - specs/001-ai-textbook-platform/contracts/chatbot-api.yaml
  - specs/001-ai-textbook-platform/contracts/personalization-api.yaml
tests:
  - N/A (planning phase, no code changes)
---

## Prompt

Create a PLAN aligned with Vercel and Railway deployment.

PHASE 1: Repository Setup
- Monorepo structure
- Spec-Kit files
- Environment variable strategy

PHASE 2: Book Generation
- Use Claude CLI to generate chapters
- Markdown optimized for static hosting
- AI-friendly chunking

PHASE 3: Frontend Deployment
- Docusaurus build
- Deploy to Vercel
- Connect frontend to backend APIs

PHASE 4: Backend Services
- FastAPI auth service
- FastAPI RAG chatbot
- Neon database integration
- Qdrant + Cohere setup

PHASE 5: Personalization & Translation
- User-based content rewriting
- Urdu translation via LLM
- Chapter-level UI controls

PHASE 6: Deployment & Validation
- Railway service configuration
- Health checks
- End-to-end testing

Output:
- Phase-wise execution steps
- Tool usage per phase
- Deployment checklist

## Response snapshot

Created comprehensive implementation plan for AI-Native Textbook Platform with 6 phases:

**Phase 1**: Repository Setup - Monorepo structure, backend scaffolds, Docusaurus frontend
**Phase 2**: Book Generation - Claude-based content generation, English + Urdu chapters
**Phase 3**: Frontend Deployment - Docusaurus configuration, Vercel deployment
**Phase 4**: Backend Services - 3 FastAPI services (auth, chatbot, personalization)
**Phase 5**: Content Indexing - Qdrant embeddings for RAG
**Phase 6**: Deployment & Validation - Railway backend, Vercel frontend, E2E testing

**Artifacts Created**:
- plan.md: Full implementation plan with constitution check
- research.md: Technology research (Docusaurus, FastAPI, Neon, Qdrant, Groq/Cohere)
- data-model.md: Database schema (users, progress_records, bookmarks, oauth_accounts)
- quickstart.md: Developer onboarding guide
- contracts/: OpenAPI specs for auth, chatbot, personalization APIs

**Constitution Check**: ALL PASS
- Free Tier Mandate: Vercel, Railway, Neon, Qdrant, Cohere, Groq
- Claude Scope Discipline: Content generation only, Groq/Cohere for runtime
- Deployment-Aware: Stateless services, environment variables
- RAG-Optimized: 500-1000 token chunks, semantic headers
- Multilingual: English + Urdu with RTL
- Authentication & Personalization: JWT, OAuth, progress tracking

## Outcome

- Impact: Complete architectural plan for AI-native textbook platform aligned with Spec-Kit Plus methodology and constitution
- Tests: N/A (planning phase)
- Files: 7 artifacts (plan.md, research.md, data-model.md, quickstart.md, 3 API contracts)
- Next prompts: Run /sp.tasks to generate detailed implementation tasks
- Reflection: Architecture supports 6 phased implementation with independent deployment of frontend (Vercel) and 3 backend services (Railway)

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check PASSED all principles
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin Phase 1 (Repository Setup) or create ADR for "Why three separate backend services?"
