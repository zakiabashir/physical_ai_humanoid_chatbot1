# AI-Native Textbook Platform

A production-ready AI-native educational platform for **Physical AI and Humanoid Robotics** with:

- **Docusaurus-based static textbook** (6 chapters) deployed to Vercel
- **FastAPI backend services** (auth, RAG chatbot, personalization) deployed to Railway
- **Free-tier architecture**: Neon PostgreSQL, Qdrant Cloud, Cohere/Groq APIs
- **Multilingual support**: English + Urdu (RTL)
- **User authentication**: Email/password + OAuth (Google, GitHub)

## Features

- 📚 **6 Textbook Chapters**: Physical AI Foundations, ROS 2, Gazebo, NVIDIA Isaac, VLA Models, Capstone Project
- 🤖 **AI Chatbot**: RAG-based question answering with source references
- 👤 **User Authentication**: Email verification, OAuth login
- 📊 **Progress Tracking**: Track reading progress and bookmarks
- 🌐 **Multilingual**: English and Urdu with RTL support
- 💰 **Free-Tier Only**: All services use free tiers

## Architecture

```
┌─────────────────┐
│  Frontend (Vercel)│  Docusaurus static site
└─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  Backend (Railway)                          │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ Auth Service │  │ Chatbot      │        │
│  │  (FastAPI)   │  │ Service      │        │
│  └──────────────┘  │ (FastAPI)    │        │
│  ┌──────────────┐  └──────────────┘        │
│  │Personalization│                         │
│  │ Service      │                         │
│  │  (FastAPI)   │                         │
│  └──────────────┘                         │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  External Services                          │
│  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │   Neon   │  │  Qdrant  │  │ Cohere  ││
│  │PostgreSQL│  │  Cloud   │  │   LLM   ││
│  └──────────┘  └──────────┘  └─────────┘│
└─────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Docker (for local Qdrant)
- Free accounts on:
  - [Neon PostgreSQL](https://neon.tech)
  - [Qdrant Cloud](https://qdrant.tech)
  - [Cohere](https://cohere.com)
  - [Groq](https://groq.com)
  - [Resend](https://resend.com) (optional, for email)
  - [Railway](https://railway.app)
  - [Vercel](https://vercel.com)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/ai-textbook-platform.git
   cd ai-textbook-platform
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Start local services**
   ```bash
   docker-compose up -d qdrant
   ```

4. **Run backend services**
   ```bash
   # Auth service
   cd backend/auth_service
   pip install -r requirements.txt
   uvicorn src.main:app --reload

   # Chatbot service
   cd backend/chatbot_service
   pip install -r requirements.txt
   uvicorn src.main:app --reload

   # Personalization service
   cd backend/personalization_service
   pip install -r requirements.txt
   uvicorn src.main:app --reload
   ```

5. **Run frontend**
   ```bash
   cd frontend
   npm install
   npm run start
   ```

6. **Index content for RAG**
   ```bash
   python scripts/embedding-indexer/index-content.py \
       --content-dir frontend/docs/en \
       --collection textbook_en
   ```

### Deployment

#### Frontend (Vercel)

```bash
cd frontend
vercel
```

#### Backend (Railway)

```bash
# Deploy each service
cd backend/auth_service
railway init
railway up

cd ../chatbot_service
railway init
railway up

cd ../personalization_service
railway init
railway up
```

## Environment Variables

See `.env.example` for all required environment variables.

Key variables:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `QDRANT_URL` / `QDRANT_API_KEY`: Qdrant Cloud credentials
- `COHERE_API_KEY`: Cohere API key for embeddings
- `GROQ_API_KEY`: Groq API key for LLM
- `JWT_SECRET_KEY`: Secret for JWT tokens

## Project Structure

```
physical_ai_humanoid_chatbot1/
├── backend/                     # FastAPI services
│   ├── auth_service/           # Authentication API
│   ├── chatbot_service/         # RAG Chatbot API
│   └── personalization_service/  # Progress & Recommendations API
├── frontend/                    # Docusaurus textbook
│   ├── docs/                   # Textbook content
│   │   ├── en/                # English content
│   │   └── ur/                # Urdu content
│   └── src/                   # React components
├── scripts/                     # Utility scripts
│   ├── content-generator/       # Content generation
│   └── embedding-indexer/       # RAG indexing
├── specs/                       # Feature specifications
│   └── 001-ai-textbook-platform/
└── .specify/                    # Spec-Kit Plus artifacts
```

## API Documentation

### Auth Service
- `POST /auth/signup` - Create account
- `POST /auth/login` - Login with email/password
- `POST /auth/logout` - Logout
- `GET /users/me` - Get current user

### Chatbot Service
- `POST /chat/question` - Ask a question
- `GET /chat/streams` - Streaming responses

### Personalization Service
- `GET /progress` - Get reading progress
- `PUT /progress/{chapter_id}` - Update progress
- `GET /bookmarks` - List bookmarks
- `POST /bookmarks` - Create bookmark
- `GET /recommendations` - Get recommendations

## Constitution

This project follows the [Spec-Kit Plus methodology](.specify/memory/constitution.md) with these principles:

1. **Spec-Kit Plus Methodology**: Spec-driven development
2. **Free Tier Mandate**: All services use free tiers
3. **Claude Scope Discipline**: Claude for content generation only; Groq/Cohere for runtime
4. **Deployment-Aware Architecture**: Stateless services, environment variables
5. **RAG-Optimized Content**: 500-1000 token chunks, semantic headers
6. **Multilingual Support**: English + Urdu with RTL
7. **Authentication & Personalization**: JWT, OAuth, progress tracking

## License

MIT License - see LICENSE file for details.
