---
id: 003
title: AI Textbook Platform Tasks
stage: tasks
date: 2025-12-22
surface: agent
model: glm-4.6
feature: 001-ai-textbook-platform
branch: 001-ai-textbook-platform
user: User
command: /sp.tasks
labels: ["tasks","implementation","dependencies"]
links:
  spec: specs/001-ai-textbook-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-ai-textbook-platform/tasks.md
tests:
  - N/A (tasks generated, no code changes)
---

## Prompt

Generate a TASKS file from the Plan.

Each task must:
- Be deployable on Vercel or Railway
- Produce a clear output
- Avoid server-state dependencies

TASKS:
- Initialize Docusaurus project
- Generate textbook chapters
- Prepare markdown for RAG ingestion
- Implement Better-Auth integration
- Define Neon PostgreSQL schema
- Build FastAPI auth endpoints
- Build FastAPI RAG chatbot
- Integrate Qdrant and Cohere
- Add personalization endpoints
- Add Urdu translation endpoints
- Configure Railway deployment
- Configure Vercel deployment

Output:
- Ordered tasks
- Output files
- Deployment targets per task

## Response snapshot

Generated comprehensive task list with 122 tasks organized by user story:

**Phase 1**: Setup (T001-T005) - Monorepo structure, .gitignore, .env.example, docker-compose

**Phase 2**: Foundational (T006-T017) - Backend service scaffolds (auth, chatbot, personalization), Docusaurus initialization, database migration setup

**Phase 3**: User Story 1 - Read Textbook Content (T018-T038) - Content generation scripts, 6 English chapters, 6 Urdu chapters, Docusaurus i18n config, RTL CSS, LanguageSwitcher component

**Phase 4**: User Story 2 - Ask AI Chatbot Questions (T039-T052) - Embedding indexer, Qdrant integration, Cohere embeddings, Groq LLM, chatbot API endpoints, ChatbotWidget component

**Phase 5**: User Story 3 - Create Account and Sign In (T053-T080) - User/OAuth/EmailVerification/PasswordReset models, JWT security, Resend email integration, auth API endpoints (signup, login, OAuth, password reset), user management endpoints, AuthModal component

**Phase 6**: User Story 4 - Track Reading Progress (T081-T098) - ProgressRecord/Bookmark models, progress/bookmark API endpoints, ProgressBar/BookmarkButton components

**Phase 7**: User Story 5 - Receive Personalized Recommendations (T099-T102) - Recommender engine, recommendations API, Recommendations component

**Phase 8**: Polish & Cross-Cutting Concerns (T103-T122) - Environment variable configuration, documentation, deployment validation, end-to-end testing

**Task Organization**:
- All tasks follow checkbox format: `- [ ] [ID] [P?] [Story] Description with file path`
- [P] marks parallelizable tasks (different files, no dependencies)
- [Story] labels (US1-US5) map tasks to user stories
- Each user story phase includes goal, independent test criteria

**Dependencies**:
- US1 (Content): Independent, no dependencies
- US2 (Chatbot): Independent of US1
- US3 (Auth): Independent of US1/US2
- US4 (Progress): Depends on US3 (Auth)
- US5 (Recommendations): Depends on US4 (Progress)

**Deployment Targets**:
- Vercel: Frontend (US1 content, UI components for all stories)
- Railway: 3 backend services (auth_service, chatbot_service, personalization_service)
- Neon: PostgreSQL database
- Qdrant: Vector embeddings for RAG

## Outcome

- Impact: Complete, dependency-ordered task breakdown for AI-native textbook platform implementation
- Tests: N/A (tasks document, no code changes)
- Files: specs/001-ai-textbook-platform/tasks.md (122 tasks across 8 phases)
- Next prompts: Begin Phase 1 (Setup) or follow MVP path (Setup → Foundational → US1 only)
- Reflection: Tasks are organized by user story for independent implementation and testing; parallel opportunities identified throughout; MVP defined as US1 (Content delivery only)

## Evaluation notes (flywheel)

- Failure modes observed: PowerShell redirection syntax error when attempting create-phr.sh, fell back to agent-native PHR creation
- Graders run and results (PASS/FAIL): N/A (tasks generation phase)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with Phase 1 Setup tasks (T001-T005)
