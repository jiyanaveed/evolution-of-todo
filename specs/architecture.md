# Architecture Specification

## System Architecture Overview

### Phase I: Console Application
- **Technology Stack**: Pure Python with in-memory data structures
- **Components**:
  - Main application logic in `todo_app.py`
  - Task management functions in `add_task.py`
- **Data Storage**: In-memory lists/dictionaries (ephemeral)
- **User Interface**: Command-line interface

### Phase II: Full-Stack Web Application
- **Frontend**: Next.js application
  - Task management UI components
  - Authentication system
  - API client integration
- **Backend**: FastAPI REST API
  - SQLModel for database operations
  - JWT-based authentication
  - CRUD operations for tasks
- **Database**: SQLite (with Neon Postgres compatibility)
- **Authentication**: JWT tokens with user sessions

## Component Interaction
- Frontend communicates with backend via REST API calls
- Backend handles authentication and database operations
- Database stores user accounts and tasks with proper relationships

## Technology Stack
- **Frontend**:
  - Next.js 14+, TypeScript, Tailwind CSS
  - Vercel AI SDK (@ai-sdk/react, @ai-sdk/openai) for chat interface
  - Better Auth for authentication
  - React Markdown for message rendering
- **Backend**:
  - FastAPI 0.128+, SQLModel 0.0.16+, Pydantic 2.x
  - OpenAI SDK with Assistants API for AI agents
  - Official MCP SDK for Model Context Protocol
  - JWT tokens with bcrypt password hashing
- **Database**:
  - SQLite (development) with Neon Postgres compatibility (production)
  - SQLModel ORM with proper connection pooling
- **Authentication**: Better Auth with cookie-based sessions
- **AI Framework**: OpenAI Agents SDK with function calling
- **Testing**: Pytest for backend, Jest for frontend (where applicable)