---
id: 001
title: Constitution Update v2.0.0
stage: constitution
date: 2025-12-22
surface: agent
model: glm-4.6
feature: none
branch: master
user: User
command: /sp.constitution
labels: ["constitution","update","version-2"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution update, no code changes)
---

## Prompt

udate my constitution You are an AI Textbook Engineer building an AI-native textbook platform
using Spec-Kit Plus methodology.

Create a CONSTITUTION for the project:
"Physical AI & Humanoid Robotics"

Core Principles:
- Follow Spec-Kit Plus strictly
- Claude is used ONLY for book and documentation generation
- Runtime services must be deployable on Vercel or Railway
- Use FREE tiers only
- The system must include:
  - Authentication
  - RAG chatbot
  - Personalization
  - Urdu translation
- Focus on embodied intelligence and robotics education
- Content must be modular and RAG-optimized

Technical Constraints:
- Frontend: Docusaurus / Next.js (Vercel compatible)
- Backend APIs: FastAPI (Railway compatible)
- Auth Database: Neon Serverless PostgreSQL
- Vector DB: Qdrant Cloud Free Tier
- Embeddings: Cohere (free tier)
- LLMs: Cohere Command / Groq LLaMA (free)
- Deployment: Vercel (frontend), Railway (backend)

Output:
- Writing principles
- Architecture rules
- Deployment-aware constraints

## Response snapshot

Constitution updated to version 2.0.0 with the following changes:

**Modified Principles:**
- "Open-Source Only" → "Free Tier Mandate" (expanded to include free cloud APIs like Cohere, Groq)
- "Docusaurus-Native Deployment" → "Deployment-Aware Architecture" (added Next.js option and Railway backend)
- "Free API Alternatives Mandate" → merged into "Free Tier Mandate"

**New Principles Added:**
1. "Spec-Kit Plus Methodology" - All work must follow Spec-Driven Development with spec.md, plan.md, tasks.md, ADRs, PHRs
2. "Claude Scope Discipline" - Claude ONLY for content generation, NOT runtime services (use Groq/Cohere free tiers)
3. "RAG-Optimized Content" - Modular content with 500-1000 token chunks, semantic headers
4. "Multilingual Support" - English + Urdu with RTL support, extensible architecture
5. "Authentication & Personalization" - User auth, progress tracking, bookmarks, recommendations

**Updated Technical Constraints:**
- Frontend: Docusaurus 3.0+ OR Next.js 14+ on Vercel free tier
- Backend: FastAPI on Railway free tier
- Database: Neon Serverless PostgreSQL free tier
- Vector DB: Qdrant Cloud free tier
- Embeddings: Cohere embed-multilingual-v3 (supports EN+UR)
- LLM: Groq LLaMA 3 or Cohere Command free tiers
- i18n: Docusaurus i18n OR next-intl

## Outcome

- ✅ Impact: Constitution now governs full AI-native textbook platform with authentication, RAG chatbot, personalization, and multilingual support
- 🧪 Tests: N/A (constitution update, no code changes)
- 📁 Files: .specify/memory/constitution.md (version 1.0.0 → 2.0.0)
- 🔁 Next prompts: Create initial feature spec for core platform components
- 🧠 Reflection: Major version bump (1.0.0 → 2.0.0) due to significant expansion from textbook-only to full AI-native platform with user services

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature planning for authentication or RAG chatbot components
