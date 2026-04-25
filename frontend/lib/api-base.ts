/**
 * Public API base URL for browser `fetch` calls.
 *
 * `NEXT_PUBLIC_*` is inlined at build time. In Vercel, set
 * `NEXT_PUBLIC_API_BASE_URL` for Production and Preview (not only Development).
 */
const PRODUCTION_FALLBACK = 'https://evolution-of-todo-backend.onrender.com';

export function getPublicApiBaseUrl(): string {
  const raw = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (typeof raw === 'string' && raw.trim() !== '') {
    return raw.replace(/\/$/, '');
  }
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:8000';
  }
  // Production/Preview: never fall back to localhost in the client bundle
  return PRODUCTION_FALLBACK;
}
