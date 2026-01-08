# Frontend Specification - Phase 3 AI Chatbot

## Overview
The Phase 3 frontend transitions from a standard CRUD application to an AI-first interface. It acts as a deterministic mirror of the AI Agent's state, enforcing safety rules and maintaining a stateless, persistent conversation log.

## Technology Stack
- **Framework**: Next.js 14+ with React 18+
- **AI Integration**: Vercel AI SDK (@ai-sdk/react, @ai-sdk/openai)
- **Authentication**: Better Auth with cookie-based sessions
- **Styling**: Tailwind CSS
- **Markdown Rendering**: React Markdown

## Components
- **AIChatBox**: Orchestrates the `conversation_id`, history fetching, and message routing using Vercel AI SDK.
- **VerbatimMessageList**: Displays the history unsummarized. Rendered with React Markdown.
- **ChatInput**: The primary interaction point using Vercel AI SDK's `useChat` hook. No manual CRUD forms.
- **ReactiveTaskSidebar**: A sidebar that re-fetches the task list when a mutation is confirmed by the agent.

## Rule Enforcement
- **Statelessness**: Fetches history on mount using the `conversation_id`.
- **Authentication**: Uses Better Auth session cookies for all requests (no JWT Bearer tokens).
- **Two-Step Mutation**: Relies on the Agent's "Are you sure?" responses for Delete and Rename intents.
- **Completion Constraint**: Interactive toggle for tasks is disabled once `completed=True`.
- **No Hallucination**: Only displays data returned from the `/chat` endpoint.
- **Secure Communication**: All API requests include proper authentication via Better Auth cookies.

## Dynamic Sync Sequence
1. User sends message via `ChatInput` (using Vercel AI SDK's `useChat` hook).
2. `AIChatBox` POSTs to `/api/chat` with proper authentication context.
3. Backend performs FETCH -> APPEND -> RUN -> PERSIST -> RESPOND using OpenAI Agents.
4. `AIChatBox` appends response to `VerbatimMessageList` via Vercel AI SDK.
5. If response indicates a successful mutation, `ReactiveTaskSidebar` re-fetches via `list_todo_tasks`.

## Authentication Flow
- **Better Auth Integration**: Uses `useSession`, `signIn`, and `signOut` from Better Auth client
- **Session Management**: Automatic cookie handling for authentication state
- **Protected Routes**: Authentication state checked via Better Auth session context
