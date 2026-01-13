# Evolution of Todo - Frontend

A modern task management application built with Next.js, TypeScript, and Tailwind CSS.

## Project Overview

This is the frontend for the Evolution of Todo application, a comprehensive task management system. The application provides a clean, responsive interface for managing tasks with full CRUD functionality.

## Features

- Create, read, update, and delete tasks
- Toggle task completion status
- Responsive design for mobile and desktop
- Real-time updates
- Loading and error states
- Inline task editing
- Confirmation for destructive actions

## Tech Stack

- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Axios for API requests
- Jest and React Testing Library for testing

## Setup Instructions

1. Clone the repository
2. Navigate to the `frontend` directory
3. Install dependencies:

```bash
npm install
```

4. Set up environment variables (optional):

```bash
# Copy the example environment file
cp .env.example .env.local

# Edit the file to set your API base URL
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

5. Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Running Tests

To run the unit tests:

```bash
npm test
```

To run tests in watch mode:

```bash
npm run test:watch
```

## API Integration

The frontend communicates with the backend API through the following endpoints:

- `GET /tasks` - Retrieve all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Retrieve a specific task
- `PUT /tasks/{id}` - Update a specific task
- `DELETE /tasks/{id}` - Delete a specific task
- `PATCH /tasks/{id}/complete` - Toggle task completion status

API calls are handled through the service layer in `lib/task-api.ts`.

## Component Documentation

### TaskForm
The form component for creating new tasks.

**Props:**
- `onCreateTask`: Function called when a task is created
- `isLoading`: Boolean to show loading state

### TaskItem
Represents a single task with functionality to edit, delete, and toggle completion.

**Props:**
- `task`: Task object with id, title, and completed status
- `onUpdateTask`: Function called when a task is updated
- `onDeleteTask`: Function called when a task is deleted
- `onToggleTask`: Function called when task completion is toggled
- `isLoading`: Boolean to show loading state

### TaskList
Container component for displaying multiple tasks.

**Props:**
- `tasks`: Array of task objects
- `onUpdateTask`: Function called when a task is updated
- `onDeleteTask`: Function called when a task is deleted
- `onToggleTask`: Function called when task completion is toggled
- `isLoading`: Boolean to show loading state
- `error`: Error message to display

### useTasks Hook
Custom hook for managing task state and API operations.

**Returns:**
- `tasks`: Array of tasks
- `loading`: Boolean indicating if tasks are loading
- `error`: Error message if any
- `isAnyOperationLoading`: Boolean indicating if any operation is loading
- `fetchTasks`: Function to fetch all tasks
- `createTask`: Function to create a new task
- `updateTask`: Function to update a task
- `deleteTask`: Function to delete a task
- `toggleTaskCompletion`: Function to toggle task completion

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL` - Base URL for the backend API (default: http://localhost:8000)
- `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` - OpenAI ChatKit domain key for AI chat features (get from OpenAI Platform)

### Setting up OpenAI ChatKit

For AI-powered task management features:

1. Get your domain key from [OpenAI Platform](https://platform.openai.com/settings/organization/general)
2. Add your domain to the Domain Allowlist (e.g., `http://localhost:3000` for local dev)
3. Copy the generated domain key
4. Add it to your `.env.local`:
   ```bash
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY=domain_pk_your_key_here
   ```

For detailed ChatKit setup instructions, see [ChatKit Setup Guide](../docs/CHATKIT_SETUP.md).

## Development

To build the application for production:

```bash
npm run build
```

To start the production server:

```bash
npm start
```

To lint the code:

```bash
npm run lint
```

## Accessibility

The application follows WCAG 2.1 AA guidelines with:

- Semantic HTML elements
- Proper ARIA attributes
- Keyboard navigation support
- Sufficient color contrast
- Focus indicators

## Responsive Design

The application is designed with a mobile-first approach and includes responsive layouts for:

- Mobile (up to 640px)
- Tablet (640px to 1024px)
- Desktop (1024px and above)