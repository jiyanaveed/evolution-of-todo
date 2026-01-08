# Task 03: Database Connection Implementation

## Description
Set up the database connection with Neon Postgres using SQLModel, including engine configuration and session management.

## Dependencies
- Task 01: Backend Project Setup completed
- Task 02: Database Models Implementation completed
- SQLModel and environment variables configured

## Steps
1. Create database engine with Neon Postgres connection string from environment
2. Implement get_session dependency function for FastAPI
3. Create database initialization function to create tables
4. Set up proper connection parameters and pooling
5. Add error handling for database connection issues

## Deliverable
- `backend/database.py` containing:
  - DATABASE_URL loaded from environment variables
  - SQLModel engine configured with Neon connection
  - get_session generator function for dependency injection
  - init_db function to create all tables
  - Proper error handling and connection management
  - All necessary imports (sqlmodel, os, contextlib, etc.)

## Verification
- [ ] Database engine connects to Neon Postgres successfully
- [ ] get_session function works as FastAPI dependency
- [ ] init_db function creates all required tables
- [ ] Connection parameters are properly configured
- [ ] Error handling is implemented for connection issues
- [ ] All necessary imports are included
- [ ] Session management follows best practices
- [ ] Database URL is loaded from environment variables