# Deployment Guide - Evolution of Todo

## Overview
This guide covers deploying both the frontend (Next.js) and backend (FastAPI) to production.

## Quick Deployment (Recommended)

### Frontend → Vercel
### Backend → Railway

---

## Frontend Deployment (Vercel)

### Prerequisites
- GitHub account
- Vercel account (free tier available)
- Code pushed to GitHub

### Steps

1. **Push to GitHub** (if not done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/evolution-of-todo.git
   git push -u origin main
   ```

2. **Import to Vercel**:
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Configure project:
     - **Root Directory**: `frontend/`
     - **Framework Preset**: Next.js (auto-detected)
     - **Build Command**: `npm run build`
     - **Output Directory**: `.next`

3. **Add Environment Variables**:
   ```
   NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.railway.app
   ```

4. **Deploy**: Click "Deploy" - Vercel will build and deploy automatically!

5. **Custom Domain** (Optional):
   - Go to Project Settings → Domains
   - Add your custom domain

---

## Backend Deployment Options

### Option 1: Railway (Easiest)

1. **Create Railway Account**: https://railway.app
2. **New Project**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
3. **Configure**:
   - Railway auto-detects FastAPI
   - Root directory: `backend/`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   ```
   NEON_DATABASE_URL=your_neon_postgres_url
   OPENAI_API_KEY=your_openai_key
   BETTER_AUTH_SECRET=your_secret_key
   PORT=8000
   ```
5. **Database**: Use Railway's built-in PostgreSQL or connect Neon
6. **Deploy**: Railway deploys automatically!

### Option 2: Render

1. **Create Render Account**: https://render.com
2. **New Web Service**:
   - Connect GitHub repository
   - Runtime: Python 3.11
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
3. **Environment Variables**: Same as Railway
4. **Database**: Connect external PostgreSQL (Neon recommended)

### Option 3: Fly.io

1. **Install Fly CLI**: https://fly.io/docs/hands-on/install-flyctl/
2. **Create Dockerfile** in `backend/`:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```
3. **Deploy**:
   ```bash
   cd backend
   fly launch
   fly secrets set OPENAI_API_KEY=xxx BETTER_AUTH_SECRET=xxx
   fly deploy
   ```

---

## Database Options

### Option 1: Neon (Serverless PostgreSQL) - Recommended

1. **Create Account**: https://neon.tech
2. **Create Database**:
   - Choose region close to your backend
   - Copy connection string
3. **Update Environment**:
   ```
   NEON_DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
   ```
4. **Migrate**: Database tables are auto-created on first run

### Option 2: Railway PostgreSQL

1. In Railway project, click "+ New" → "Database" → "PostgreSQL"
2. Connection string is auto-generated
3. Use `DATABASE_URL` from Railway

### Option 3: Supabase

1. Create project at https://supabase.com
2. Get connection string from Settings → Database
3. Use as `DATABASE_URL`

---

## Environment Variables Setup

### Backend (.env)
```bash
# Database
NEON_DATABASE_URL=postgresql://xxx

# OpenAI
OPENAI_API_KEY=sk-proj-xxx
OPENAI_MODEL=gpt-4o-mini

# Auth
BETTER_AUTH_SECRET=<run: openssl rand -hex 32>

# Server
PORT=8000
LOG_LEVEL=info
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_BASE_URL=https://your-backend.railway.app
```

---

## Post-Deployment Checklist

- [ ] Frontend accessible and loads correctly
- [ ] Backend API responding (check /docs endpoint)
- [ ] User registration works
- [ ] User login works
- [ ] Task operations work (add, list, complete, delete)
- [ ] AI chat responds correctly
- [ ] Database persists data correctly
- [ ] CORS configured for your frontend domain

---

## Troubleshooting

### Frontend Issues

**404 on routes**: Ensure `frontend/` is set as root directory in Vercel

**API calls fail**:
- Check `NEXT_PUBLIC_API_BASE_URL` is set correctly
- Verify backend CORS allows your frontend domain

### Backend Issues

**Database connection fails**:
- Verify connection string format
- Check SSL requirements (`sslmode=require` for Neon)
- Ensure database exists and is accessible

**OpenAI errors**:
- Verify API key is valid
- Check you have credits in OpenAI account
- Test key locally first

**CORS errors**:
- Update `allow_origins` in `backend/main.py` to include your Vercel domain

---

## Monitoring & Logs

### Vercel
- Dashboard → Your Project → Deployments → View Logs

### Railway
- Dashboard → Your Project → Deployments → View Logs
- Click on service to see real-time logs

### Render
- Dashboard → Your Service → Logs tab

---

## Scaling Considerations

- **Frontend**: Vercel scales automatically
- **Backend**:
  - Railway: Upgrade plan for more resources
  - Consider adding Redis for caching
  - Use connection pooling for database
- **Database**: Neon autoscales, Railway has limits by plan

---

## Cost Estimates (Monthly)

**Free Tier:**
- Vercel: Free (hobby plan)
- Railway: $5 credit/month (enough for light usage)
- Neon: Free tier (0.5GB storage)
- OpenAI: Pay per use (~$1-5 for light usage)

**Total: ~$6-10/month for production**

---

## Support

For issues:
1. Check deployment logs
2. Verify environment variables
3. Test endpoints individually
4. Check GitHub Issues
