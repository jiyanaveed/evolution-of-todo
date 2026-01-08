# Database Schema Specification

## Overview
The database schema for the Evolution of Todo application uses SQLModel for object-relational mapping.

## Database Engine
- **Development**: SQLite for local development
- **Production**: Neon Serverless PostgreSQL with connection pooling
- **Configuration**: Environment-based switching between SQLite and PostgreSQL

## Tables

### User Table
**Purpose**: Store user account information

**Fields**:
- `id` (VARCHAR): Primary key, UUID string, unique identifier for the user
- `email` (VARCHAR): User's email address, unique constraint
- `password_hash` (VARCHAR): Bcrypt hash of user's password
- `created_at` (DATETIME): Timestamp of account creation, defaults to current time
- `is_active` (BOOLEAN): Account status, defaults to true

**Constraints**:
- Primary key: id
- Unique constraint: email
- NOT NULL: email, password_hash

### Task Table
**Purpose**: Store task information linked to users

**Fields**:
- `id` (INTEGER): Primary key, auto-incrementing unique identifier
- `title` (VARCHAR/TEXT): Task description, maximum 255 characters
- `completed` (BOOLEAN): Task completion status, defaults to false
- `user_id` (VARCHAR): Foreign key referencing user.id

**Constraints**:
- Primary key: id
- Foreign key: user_id references user.id
- NOT NULL: title, user_id
- Default: completed = false

### Message Table (Phase 3)
**Purpose**: Store conversation history for AI chatbot

**Fields**:
- `id` (INTEGER): Primary key, auto-incrementing unique identifier
- `conversation_id` (VARCHAR): UUID to group conversation messages
- `user_id` (VARCHAR): Foreign key referencing user.id
- `role` (VARCHAR): Message role (user/assistant), non-nullable
- `content` (TEXT): Message content, non-nullable
- `timestamp` (DATETIME): Message timestamp, defaults to current time

**Constraints**:
- Primary key: id
- Foreign key: user_id references user.id
- NOT NULL: conversation_id, user_id, role, content

## Relationships
- One User to Many Tasks (one-to-many relationship)
- One User to Many Messages (one-to-many relationship)
- Messages are grouped by conversation_id
- Tasks and messages are linked to users via foreign key constraint

## Connection Configuration
- **SQLite**: Direct file access with proper locking for development
- **PostgreSQL**: Connection pooling with SSL enforcement for Neon production
- **Environment Variables**:
  - `DATABASE_URL` for SQLite configuration
  - `NEON_DATABASE_URL` for Neon PostgreSQL configuration