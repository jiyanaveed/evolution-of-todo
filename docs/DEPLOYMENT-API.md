# Frontend (Vercel) and backend API URL

This repo’s **Next.js app** in `frontend/` calls a **separate FastAPI backend** for auth, tasks, and chat. The backend is not deployed by this Vercel project unless you add a separate deployment.

## Live backend (default)

The open reference deployment is on **Render**:

- **Base URL:** `https://evolution-of-todo-backend.onrender.com`

The frontend resolves the API base URL in this order:

1. **`NEXT_PUBLIC_API_BASE_URL`** — must be set in **Vercel → Project → Settings → Environment Variables** for **Production** and **Preview** (and optionally Development). It is inlined at **build** time.
2. **Local dev:** if the variable is unset, the app uses `http://localhost:8000`.
3. **Production/Preview build:** if the variable is still unset at build, the client bundle falls back to `https://evolution-of-todo-backend.onrender.com` (see `frontend/lib/api-base.ts`) so the UI does not default to localhost in the browser.

For your own backend, set `NEXT_PUBLIC_API_BASE_URL` to your real origin, e.g. `https://your-api.onrender.com`, with **no trailing slash**.

## Vercel checklist

1. **Root Directory:** `frontend` (if the Vercel project is connected to this monorepo).
2. **Environment variables:** add `NEXT_PUBLIC_API_BASE_URL` = your backend URL (not `http://localhost:8000`).
3. **Redeploy** after changing env vars so the Next build picks up the new value.

## Local development

Copy `frontend/.env.example` to `frontend/.env.local` and point `NEXT_PUBLIC_API_BASE_URL` at a running local API (`http://localhost:8000`) or at the hosted URL.

## Code references

| Area            | File                         |
|----------------|------------------------------|
| Central URL    | `frontend/lib/api-base.ts`   |
| Auth / session | `frontend/contexts/AuthContext.tsx` |
| Tasks          | `frontend/lib/task-api.ts`  |
| AI chat        | `frontend/components/AIChatBoxBase.tsx` |
