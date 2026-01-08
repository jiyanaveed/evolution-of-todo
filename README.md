# The Evolution of Todo

## Project Theme: From CLI to Distributed Cloud-Native AI Systems

This project demonstrates the evolution of a simple todo application through multiple phases, showcasing different technologies and architectural patterns.

## Project Structure

```
├── .spec-kit/           # Spec-Kit configuration
├── specs/              # Current project specifications
├── specs-history/      # Historical specification snapshots
├── frontend/           # Next.js web application
├── backend/            # FastAPI backend service
├── phase-1/            # Phase I implementation and specs (legacy)
├── phase-2/            # Phase II implementation and specs (legacy)
└── ...
```

## Phases

### Phase I: Console Application
- Pure Python implementation with in-memory storage
- Command-line interface for task management
- Basic CRUD operations for tasks

### Phase II: Full-Stack Web Application
- Next.js frontend with responsive UI
- FastAPI backend with REST API
- SQLite database with user authentication
- Complete task management with user accounts

### Phase III: AI Integration (Implemented)
- AI Chatbot interface using Vercel AI SDK for natural language task management
- OpenAI Agents SDK for intelligent task operations
- Model Context Protocol (MCP) tools for secure task operations
- Better Auth for enhanced authentication
- Neon PostgreSQL serverless database support
- AI-powered task suggestions and organization

## Current Status
✅ Both Phase I and Phase II are fully implemented and functional.

## Getting Started

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- SQLite (for local development)
- PostgreSQL/Neon (optional, for production)
- OpenAI API Key (for AI features)

### Local Development Setup

1. **Clone and Install**:
   ```bash
   git clone <your-repo-url>
   cd evolution-of-todo
   ```

2. **Backend Setup**:
   ```bash
   # Install dependencies
   pip install -r backend/requirements.txt

   # Copy environment variables
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY and BETTER_AUTH_SECRET

   # Run the backend
   python run_backend.py
   ```

3. **Frontend Setup** (in a new terminal):
   ```bash
   cd frontend
   npm install

   # Copy environment variables
   cp .env.example .env.local
   # Edit .env.local if needed (defaults to localhost:8000)

   # Run the frontend
   npm run dev
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Production Deployment

#### Vercel (Frontend)
1. Push your code to GitHub
2. Import project in Vercel Dashboard
3. Set root directory to `frontend/`
4. Add environment variable: `NEXT_PUBLIC_API_BASE_URL` (your backend URL)
5. Deploy!

#### Backend Deployment Options
- **Railway**: Connect GitHub repo, Railway auto-detects FastAPI
- **Render**: Create new Web Service, add backend/ as root
- **AWS/GCP/Azure**: Use Docker container or serverless functions
- **Fly.io**: Deploy with Dockerfile

**Environment Variables for Backend**:
- `DATABASE_URL` or `NEON_DATABASE_URL`
- `OPENAI_API_KEY`
- `BETTER_AUTH_SECRET`
- `PORT` (default: 8000)

## Specifications
All project specifications are available in the `specs/` directory, organized by category:
- Feature specifications
- API documentation
- Database schema
- UI components
- Architecture overview

Historical specifications by phase are available in the `specs-history/` directory.

## Architecture
- **Frontend**: Next.js 14+, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLModel, Pydantic
- **Database**: SQLite with SQLModel ORM
- **Authentication**: JWT tokens with bcrypt password hashing