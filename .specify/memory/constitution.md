<!--
  SYNC IMPACT REPORT
  ==================
  Version change: 1.0.0 -> 2.0.0
  Modified principles:
    - "Open-Source Only" -> "Free Tier Mandate" (expanded to include free cloud APIs)
    - "Docusaurus-Native Deployment" -> "Deployment-Aware Architecture" (expanded to include Next.js and Railway backend)
    - "Free API Alternatives Mandate" -> merged into "Free Tier Mandate"
  Added principles:
    - "Spec-Kit Plus Methodology" (new governance principle)
    - "Claude Scope Discipline" (new AI tool usage principle)
    - "RAG-Optimized Content" (new content structuring principle)
    - "Multilingual Support" (new accessibility principle)
    - "User Personalization" (new UX principle)
  Removed sections: None
  Templates updated:
    ✅ .specify/templates/plan-template.md (reviewed - compatible, no changes needed)
    ✅ .specify/templates/spec-template.md (reviewed - compatible, no changes needed)
    ✅ .specify/templates/tasks-template.md (reviewed - compatible, no changes needed)
  Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Spec-Kit Plus Methodology

All project work MUST strictly follow the Spec-Kit Plus Spec-Driven Development (SDD) methodology.

- **Rationale**: Ensures systematic development with proper documentation, traceability, and architectural decision records; prevents ad-hoc decisions and technical debt
- **Requirements**:
  - Every feature MUST have a spec.md before any code is written
  - Implementation planning MUST use plan.md with architectural analysis
  - Tasks MUST be defined in tasks.md with clear dependencies and acceptance criteria
  - Significant architectural decisions MUST be recorded in ADRs
  - All user interactions MUST be recorded in PHRs (Prompt History Records)
  - Templates in `.specify/templates/` MUST be used for all artifacts

### II. Free Tier Mandate

All tools, libraries, frameworks, and platforms used in this project MUST be free (FOSS or free-tier cloud services).

- **Rationale**: Ensures accessibility for all learners regardless of financial status; promotes sustainability for student/educator projects; demonstrates that production-quality systems can be built without budget
- **Requirements**:
  - **Frontend/Content**: Docusaurus or Next.js with free hosting (Vercel, Netlify, GitHub Pages)
  - **Backend APIs**: FastAPI deployed to free-tier Railway, Render, or similar
  - **Databases**: Neon Serverless PostgreSQL (free tier) for auth/data
  - **Vector DB**: Qdrant Cloud free tier for RAG embeddings
  - **Embeddings**: Cohere free tier or open-source sentence-transformers
  - **LLMs**: Cohere Command free tier or Groq LLaMA free tier
  - **Paid APIs are PROHIBITED** unless no free alternative exists (requires explicit justification and ADR)
  - When commercial alternatives exist, MUST document and prefer free equivalents

### III. Claude Scope Discipline

Claude AI is used ONLY for book and documentation generation, NOT for runtime services.

- **Rationale**: Separates content creation from runtime infrastructure; ensures cost control; allows deployment on free hosting tiers without API dependencies
- **Requirements**:
  - Claude (Anthropic API) is ONLY used during content authoring and documentation phases
  - Runtime chatbot MUST use free alternatives: Groq LLaMA, Cohere Command, or local models
  - No Claude API calls in deployed user-facing applications
  - Content generation workflows are offline/authoring-time only
  - All generated content MUST be version-controlled and static at deployment time

### IV. Deployment-Aware Architecture

The platform MUST be deployable on free-tier hosting: Vercel (frontend) and Railway (backend).

- **Rationale**: Zero-cost hosting enables sustainability; standard deployment targets ensure reproducibility; serverless/containers scale to zero when unused
- **Requirements**:
  - **Frontend**: Docusaurus or Next.js deployable to Vercel free tier
  - **Backend**: FastAPI deployable to Railway free tier as containerized service
  - **Stateless Design**: All services MUST be stateless (state in databases only)
  - **Cold Start Tolerance**: Services MUST handle cold starts gracefully (<30s)
  - **Environment Variables**: All configuration via environment variables (no hardcoded secrets)
  - **Build Artifacts**: Site MUST build as static files or edge functions
  - **Resource Limits**: MUST operate within free tier limits (e.g., Railway 512MB RAM, Vercel 100GB bandwidth)

### V. Embodied Intelligence First

This textbook prioritizes physical AI and embodied intelligence over purely digital/cyber AI systems.

- **Rationale**: Physical AI represents the frontier of robotics; embodied intelligence creates real-world understanding; differentiates this curriculum from generic AI courses
- **Requirements**:
  - Content MUST emphasize how AI systems interact with physical environments
  - Simulators and physical robot platforms are central, not auxiliary
  - Every major concept SHOULD include physical-world applications or demonstrations
  - Sensor integration, actuation, and real-world constraints are core topics
  - Pure software-only AI examples are permitted only when directly applicable to robotics

### VI. RAG-Optimized Content

All content MUST be structured for optimal RAG (Retrieval-Augmented Generation) retrieval.

- **Rationale**: Enables intelligent tutoring systems; allows AI chatbot to answer questions accurately; supports personalized learning paths; improves content discoverability
- **Requirements**:
  - **Modular Structure**: Each chapter/section MUST be independently consumable
  - **Semantic Chunking**: Content MUST support 500-1000 token chunks with overlap
  - **Clear Headers**: Every section MUST have descriptive, semantic headers
  - **Self-Contained Examples**: Code examples MUST include context and comments
  - **Explicit Dependencies**: Prerequisite concepts MUST be explicitly linked
  - **Frontmatter**: Every page MUST include title, description, and metadata for indexing
  - **Multiple Representations**: Concepts explained with text, diagrams, code, and examples

### VII. Authentication & Personalization

The platform MUST include user authentication and personalization features.

- **Rationale**: Enables progress tracking; supports personalized learning paths; allows bookmarking and note-taking; creates engaging learning experience
- **Requirements**:
  - **Authentication**: Email/password + OAuth (Google, GitHub) using free services
  - **User Profiles**: Store reading progress, bookmarks, and notes in PostgreSQL
  - **Progress Tracking**: Track chapter completion and quiz scores
  - **Personalized Recommendations**: Suggest content based on reading history and quiz performance
  - **Session Management**: Secure JWT-based sessions with appropriate expiration
  - **Privacy-First**: Clear data handling; user data export; GDPR compliance

### VIII. Multilingual Support

The platform MUST support English and Urdu languages, with architecture for additional languages.

- **Rationale**: Increases accessibility for Urdu-speaking learners; demonstrates internationalization best practices; serves diverse global audience
- **Requirements**:
  - **Primary Languages**: English (default) and Urdu (RTL support)
  - **Content Structure**: MUST support i18n with language-specific content files
  - **UI Translation**: All interface elements MUST be translatable
  - **Translation Workflow**: Content authored in English, translated to Urdu
  - **RTL Support**: Proper right-to-left layout for Urdu
  - **Language Switching**: User can switch languages without losing progress
  - **Extensibility**: Architecture MUST allow adding more languages (e.g., Arabic, Hindi)

### IX. AI-Agent Learning Support

All content MUST be structured for consumption by both human learners and AI agents (RAG systems).

- **Rationale**: Enables intelligent tutoring systems; allows AI chatbot to answer questions accurately; future-proofs content for AI-assisted learning
- **Requirements**:
  - Each chapter/section MUST include clear semantic headers with descriptive titles
  - Code examples MUST be self-contained with comments explaining context
  - Concepts MUST be explained with multiple representations (text, diagrams, code, examples)
  - Key terms MUST be consistently defined and referenced
  - Dependencies between concepts MUST be explicitly stated
  - Code snippets MUST be copy-paste executable (or include setup instructions)
  - Mathematical notation SHOULD be accompanied by plain-language explanations

### X. Startup-Ready Pedagogy

Content MUST bridge academic theory with practical industry application and entrepreneurial thinking.

- **Rationale**: Learners need skills applicable to startups and industry; robotics is rapidly evolving with many emerging companies; practical knowledge creates immediate value
- **Requirements**:
  - Each topic MUST include real-world industry applications and case studies
  - Hardware/software recommendations MUST consider startup-scale budgets
  - Content SHOULD highlight commercialization opportunities and challenges
  - Labs and projects SHOULD be portfolio-worthy (demonstrable to employers/investors)
  - Include considerations for scaling from prototype to production
  - Cover both technical and non-technical aspects (team composition, funding paths, market validation)

### XI. Structured, Practical, Clear Writing Style

All content MUST follow a consistent writing style optimized for technical comprehension and practical application.

- **Rationale**: Reduces cognitive load; supports diverse learning backgrounds; ensures content is scannable and referenceable; improves AI agent comprehension
- **Requirements**:
  - **Structure**: Each topic follows: Concept → Theory → Example → Practice → Extension
  - **Tone**: Direct, active voice, avoid unnecessary jargon, define technical terms on first use
  - **Code**: All code examples must be runnable, commented, and include expected output
  - **Diagrams**: Use ASCII art or Mermaid diagrams for concepts requiring visual representation
  - **Length**: Keep sections focused—break complex topics into multiple digestible sections
  - **Prerequisites**: Each chapter MUST list required background knowledge
  - **Learning Outcomes**: Each section MUST state measurable learning objectives

## Technical Constraints

### Build & Deployment

- **Frontend Framework**: Docusaurus 3.0+ OR Next.js 14+ (App Router)
- **Frontend Deployment**: Vercel free tier
- **Backend Framework**: FastAPI (Python 3.11+)
- **Backend Deployment**: Railway free tier (containerized)
- **Auth Database**: Neon Serverless PostgreSQL free tier
- **Vector Database**: Qdrant Cloud free tier
- **Embedding Model**: Cohere embed-v3 (free tier) OR sentence-transformers (self-hosted)
- **LLM for Chatbot**: Groq LLaMA 3 (free) OR Cohere Command (free tier)
- **Build Time**: Full site build MUST complete in under 5 minutes on standard CI
- **Site Size**: Initial target under 500MB (including assets)

### Content Format

- **Primary Format**: Markdown (.md) with MDX support for interactive elements
- **Code Blocks**: Must specify language for syntax highlighting
- **Images**: Prefer SVG diagrams; use WebP for photos; include alt text
- **Math**: Use LaTeX syntax (KaTeX or MathJax compatible)
- **Frontmatter**: Every page MUST include title, description, and metadata for RAG indexing
- **i18n Structure**: Language-specific content directories (e.g., `en/`, `ur/`)

### RAG Chatbot Requirements

- **Vector Database**: Qdrant Cloud free tier (collections for chapters, code examples, glossary)
- **Embedding Model**: Cohere embed-multilingual-v3 (supports English + Urdu)
- **Chunking Strategy**: 500-1000 token chunks with 100 token overlap
- **Retrieval**: Hybrid search (semantic + keyword) for best results
- **LLM**: Groq LLaMA 3 70B or Cohere Command R+ (free tiers)
- **Hosting**: Deploy as Railway container or Vercel edge function
- **Context Window**: Configure appropriate context limits per query

### Authentication & User Data

- **Auth Provider**: NextAuth.js (if Next.js) or FastAPI with JWT
- **OAuth Providers**: Google, GitHub (free developer accounts)
- **User Database**: Neon PostgreSQL (users, progress, bookmarks, notes tables)
- **Session Storage**: JWT tokens stored in httpOnly cookies
- **Password Hashing**: bcrypt or argon2
- **Email Service**: Resend free tier or similar (for password resets)

### Hardware & Simulation

- **Preferred Simulators**: Gazebo, Webots, PyBullet, Isaac Sim (free tier), MuJoCo (free for research)
- **Hardware Platforms**: Document low-cost options (e.g., Raspberry Pi + microcontrollers) alongside professional platforms
- **Local Execution**: All examples SHOULD run on consumer hardware (laptop/workstation) or free cloud tiers

### Internationalization

- **i18n Framework**: Docusaurus i18n OR next-intl
- **Supported Languages**: English (en), Urdu (ur)
- **RTL Support**: Proper CSS for Urdu right-to-left text
- **Content Translation**: Separate content files per language
- **Date/Number Formatting**: Locale-aware formatting

## Learning Philosophy

### Progressive Complexity

Content follows a "scaffolding" approach: simple foundations → intermediate integration → advanced systems.

- **Foundational Level**: Math/physics basics, introductory programming, core robotics concepts
- **Intermediate Level**: Sensor fusion, motion planning, perception systems, control theory
- **Advanced Level**: SLAM, learning-based control, multi-robot systems, human-robot interaction
- **Each level MUST be independently valuable**—learners can stop at any point with applicable skills

### Learning by Doing

Every major concept includes practical implementation, not just theory.

- **Code-First Approach**: Concepts are introduced through working examples, then explained
- **Lab Exercises**: Hands-on activities using simulators or real hardware
- **Project-Based Learning**: Capstone projects that integrate multiple concepts
- **Failure Analysis**: Include common pitfalls and how to debug them

### Multi-Modal Learning

Content accommodates diverse learning preferences.

- **Text**: Clear explanations with structured formatting
- **Visual**: Diagrams, flowcharts, and architecture illustrations
- **Code**: Working examples with comments and explanations
- **Math**: Formal notation alongside plain-language interpretations
- **Practice**: Exercises, quizzes, and projects with solutions

### Personalized Learning Paths

The platform adapts to individual learner needs and progress.

- **Adaptive Content**: Recommend next topics based on quiz performance
- **Progress Tracking**: Visual progress indicators and completion status
- **Bookmarking**: Save important sections for later review
- **Note-Taking**: In-line notes attached to specific content sections
- **Difficulty Adjustment**: Offer simpler/advanced explanations for key concepts

## Content Quality Standards

### Accuracy & Currency

- **Verification**: All code examples MUST be tested and runnable
- **Version Pinning**: Specify exact versions of critical dependencies
- **Update Policy**: Review and update content at least annually for major framework changes
- **Community Contributions**: Encourage pull requests for corrections and improvements

### Accessibility

- **WCAG 2.1 AA**: Site MUST meet accessibility standards (contrast, screen reader support, keyboard navigation)
- **Plain Language**: Use clear, simple language; avoid unnecessary complexity
- **Multilingual**: Primary support for English and Urdu with extensibility for more languages
- **RTL Support**: Proper right-to-left rendering for Urdu and future Arabic content

### Citations & Attribution

- **Sources**: Cite original papers, resources, and inspirations
- **Images**: Use original creations or properly licensed content with attribution
- **Code**: Specify licenses and attribute code origins

## Governance

### Amendment Process

- **Proposal**: Any contributor MAY propose amendments via issues or pull requests
- **Review**: Constitution changes require review by maintaining authors
- **Versioning**: Semantic versioning (MAJOR.MINOR.PATCH)
  - MAJOR: Fundamental principle changes (e.g., allowing paid APIs, removing Spec-Kit Plus requirement)
  - MINOR: New principles or sections added (e.g., adding new language support)
  - PATCH: Clarifications, wording improvements, non-semantic refinements
- **Migration**: When principles change, existing content MUST be updated with clear migration guidance

### Compliance

- **All new content MUST adhere to this constitution**
- **PR reviews MUST verify compliance with core principles**
- **Non-compliant content MAY be grandfathered if removal would be destructive, but MUST be marked for update**
- **Spec-Kit Plus artifacts MUST be created for all features (spec, plan, tasks)**

### ADR Requirements

Significant architectural decisions require an Architecture Decision Record:

- **Trigger**: Decisions affecting long-term system architecture
- **Examples**: Tech stack changes, deployment architecture, data modeling, API design
- **Process**: Use `/sp.adr <decision-title>` to create ADRs
- **Review**: ADRs should be reviewed before implementation

### Living Document

- This constitution evolves with the project and community needs
- Feedback channels (issues, discussions) MUST be monitored
- Revisions prioritized based on learner impact and technical necessity
- PHRs track all constitution-related discussions and decisions

---

**Version**: 2.0.0 | **Ratified**: 2025-12-22 | **Last Amended**: 2025-12-22
