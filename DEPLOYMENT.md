# Deployment Guide: AI-Native Textbook Platform

## Prerequisites

- GitHub repository with the code
- Free accounts on:
  - [Vercel](https://vercel.com)
  - [Railway](https://railway.app)
  - [Neon PostgreSQL](https://neon.tech)
  - [Qdrant Cloud](https://qdrant.tech)
  - [Cohere](https://cohere.com)
  - [Groq](https://groq.com)

---

## Step 1: Deploy Frontend to Vercel

### 1.1 Connect Vercel to GitHub

1. Go to https://vercel.com
2. Click "Sign Up" → "Continue with GitHub"
3. Authorize Vercel to access your repositories
4. Install Vercel GitHub App if prompted

### 1.2 Import and Deploy Frontend

1. Click "Add New Project" → "Continue with GitHub"
2. Select the `ai-textbook-platform` repository
3. **Configure Project:**
   - **Framework Preset**: Docusaurus (should auto-detect)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`

4. **Environment Variables** (add these):
   ```
   NEXT_PUBLIC_AUTH_API_URL=https://your-auth-service.railway.app
   NEXT_PUBLIC_CHATBOT_API_URL=https://your-chatbot-service.railway.app
   NEXT_PUBLIC_PERSONALIZATION_API_URL=https://your-personalization-service.railway.app
   ```

5. Click "Deploy"

6. **Update variables after Railway deployment:**
   - Go to Project Settings → Environment Variables
   - Replace the placeholder URLs with actual Railway service URLs

---

## Step 2: Deploy Backend Services to Railway

### 2.1 Connect Railway to GitHub

1. Go to https://railway.app
2. Click "Sign Up" → "Continue with GitHub"
3. Select "New Project" → "Deploy from GitHub repo"
4. Install Railway GitHub App if prompted
5. Select the `ai-textbook-platform` repository

### 2.2 Deploy Auth Service

1. Click "New Service" → "Deploy from GitHub repo"
2. Select `ai-textbook-platform`
3. **Root Directory**: `backend/auth_service`
4. Click "Deploy"

5. **Add Environment Variables** (Variables tab):
   ```
   DATABASE_URL=postgresql://user:password@ep-xyz.region.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   JWT_SECRET_KEY=your-secure-random-min-32-char-string-here
   RESEND_API_KEY=re_your_resend_api_key_here
   OAUTH_GOOGLE_CLIENT_ID=your-google-client-id
   OAUTH_GOOGLE_CLIENT_SECRET=your-google-client-secret
   OAUTH_GITHUB_CLIENT_ID=your-github-client-id
   OAUTH_GITHUB_CLIENT_SECRET=your-github-client-secret
   ```

6. **Generate JWT_SECRET_KEY** (run in terminal):
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

7. Copy the deployed URL (e.g., `https://auth-service.up.railway.app`)

### 2.3 Deploy Chatbot Service

1. Click "New Service" → "Deploy from GitHub repo"
2. Select `ai-textbook-platform`
3. **Root Directory**: `backend/chatbot_service`
4. Click "Deploy"

5. **Add Environment Variables**:
   ```
   QDRANT_URL=https://your-qdrant-url.cloud.qdrant.io:6333
   QDRANT_API_KEY=your-qdrant-api-key-here
   COHERE_API_KEY=your-cohere-api-key-here
   GROQ_API_KEY=your-groq-api-key-here
   ```

6. Copy the deployed URL (e.g., `https://chatbot-service.up.railway.app`)

### 2.4 Deploy Personalization Service

1. Click "New Service" → "Deploy from GitHub repo"
2. Select `ai-textbook-platform`
3. **Root Directory**: `backend/personalization_service`
4. Click "Deploy"

5. **Add Environment Variables**:
   ```
   DATABASE_URL=postgresql://user:password@ep-xyz.region.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   ```

6. Copy the deployed URL (e.g., `https://personalization-service.up.railway.app`)

---

## Step 3: Update Vercel Environment Variables

1. Go to Vercel Dashboard → `ai-textbook-platform-frontend` → Settings → Environment Variables
2. Update the URLs with actual Railway service URLs:
   ```
   NEXT_PUBLIC_AUTH_API_URL=https://auth-service.up.railway.app
   NEXT_PUBLIC_CHATBOT_API_URL=https://chatbot-service.up.railway.app
   NEXT_PUBLIC_PERSONALIZATION_API_URL=https://personalization-service.up.railway.app
   ```
3. Redeploy (Vercel → Deployments → Redeploy)

---

## Step 4: Initialize Database

Run this to create database tables:

```bash
# Via Railway console (auth service):
python -c "from src.db.init_db import Base; from src.db.session import engine; import asyncio; asyncio.run(init_db())"
```

Or use the Railway console to run migrations:
```bash
python -m src.db.init_db
```

---

## Step 5: Index Content to Qdrant

Run the embedding indexer locally:

```bash
cd E:\physical_ai_humanoid_chatbot1
python scripts/embedding-indexer/index-content.py \
    --content-dir frontend/docs/en \
    --collection textbook_en \
    --qdrant-url "https://cfc968b3-733f-49f0-810f-7dcfd76c4caa.us-east4-0.gcp.cloud.qdrant.io:6333" \
    --qdrant-api-key "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.gEL4lT3h8va-4LdJ_Fhw9Wv2GR086XvoVhyukrmfuS4" \
    --cohere-api-key "0Bllz8EmifY8JfTsdewkFOjYJBlKsf6xp3i9Ar91"
```

For Urdu content:
```bash
python scripts/embedding-indexer/index-content.py \
    --content-dir frontend/docs/ur \
    --collection textbook_ur \
    --language ur \
    --qdrant-url "https://cfc968b3-733f-49f0-810f-7dcfd76c4caa.us-east4-0.gcp.cloud.qdrant.io:6333" \
    --qdrant-api-key "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.gEL4lT3h8va-4LdJ_Fhw9Wv2GR086XvoVhyukrmfuS4" \
    --cohere-api-key "0Bllz8EmifY8JfTsdewkFOjYJBlKsf6xp3i9Ar91"
```

---

## Step 6: Setup OAuth (Optional)

### Google OAuth
1. Go to https://console.cloud.google.com
2. Create new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add callback URL: `https://your-auth-service.railway.app/auth/oauth/google/callback`
6. Copy Client ID and Secret to Railway environment variables

### GitHub OAuth
1. Go to https://github.com/settings/developers
2. New OAuth App
3. Authorization callback: `https://your-auth-service.railway.app/auth/oauth/github/callback`
4. Copy Client ID and Secret to Railway environment variables

---

## Step 7: Verify Deployment

1. **Frontend**: Visit your Vercel URL
2. **Auth Health**: `https://auth-service.up.railway.app/health`
3. **Chatbot Health**: `https://chatbot-service.up.railway.app/health`
4. **Personalization Health**: `https://personalization-service.up.railway.app/health`

---

## Troubleshooting

### Railway: Container won't start
- Check build logs in Railway console
- Verify Dockerfile syntax
- Check PYTHON_VERSION in Dockerfile

### Vercel: Build fails
- Check that `frontend/package.json` has correct scripts
- Verify Node.js version (18+)

### Database connection errors
- Verify DATABASE_URL format
- Check Neon database is active
- Ensure SSL mode is enabled

### Qdrant connection errors
- Verify API key and URL
- Check collections exist

---

## Cost Summary (All Free Tiers)

| Service | Plan | Cost/Month |
|---------|------|------------|
| Vercel | Hobby | $0 |
| Railway | Free | $0 |
| Neon | Free | $0 |
| Qdrant | Free | $0 |
| Cohere | Free | $0 |
| Groq | Free | $0 |
| **Total** | | **$0** |
