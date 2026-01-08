# Frontend CLAUDE Instructions

## Overview
Next.js frontend for the Evolution of Todo application.

## Tech Stack
- Next.js 14+ with App Router
- TypeScript
- Tailwind CSS for styling
- React for UI components
- Axios for API communication

## Key Components
- `app/page.tsx` - Main task management page
- `app/login/page.tsx` - Authentication interface
- `components/` - Reusable UI components (TaskItem, TaskList, etc.)
- `hooks/useTasks.ts` - Task management logic
- `contexts/AuthContext.tsx` - Authentication state management
- `lib/` - API clients and utilities

## API Integration
- API calls handled through `lib/task-api.ts` and `lib/auth-api.ts`
- Uses axios with interceptors for auth token management
- All backend communication requires JWT authentication

## Development Guidelines
- Follow Next.js best practices for App Router
- Use TypeScript for type safety
- Maintain responsive design with Tailwind
- Follow existing component architecture patterns
- Preserve existing functionality when making changes

## Safety Constraints
- Do not modify core functionality that enables task CRUD operations
- Do not break authentication flow
- Maintain existing UI/UX patterns
- Preserve data flow through existing hooks and contexts