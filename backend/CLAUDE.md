# Backend CLAUDE Instructions

## Overview
FastAPI backend service for the Evolution of Todo application.

## Tech Stack
- FastAPI 0.104+ for web framework
- SQLModel for database modeling and ORM
- Pydantic 2.x for data validation
- SQLite (with Neon Postgres compatibility) for database
- bcrypt for password hashing
- JWT for authentication

## Key Components
- `main.py` - FastAPI application and API routes
- `models.py` - SQLModel database models and Pydantic schemas
- `crud.py` - Database operations (Create, Read, Update, Delete)
- `database.py` - Database connection and session management
- `auth.py` - Authentication logic and JWT handling
- `run_simple.py` - Application startup

## API Endpoints
- `/auth/` - Authentication routes (register, login, me)
- `/tasks/` - Task management routes (CRUD operations)
- Proper authentication required for task endpoints
- JWT token validation for protected routes

## Database Models
- `User` - User account information with authentication fields
- `Task` - Task information linked to users
- Proper relationships and constraints defined

## Development Guidelines
- Follow FastAPI best practices with dependency injection
- Use SQLModel for database operations
- Implement proper error handling and validation
- Follow security best practices for authentication
- Maintain consistent API response formats

## Safety Constraints
- Do not modify core functionality that enables task CRUD operations
- Do not break authentication and authorization logic
- Maintain database integrity and relationships
- Preserve existing API contract with frontend
- Keep existing database schema and migration patterns