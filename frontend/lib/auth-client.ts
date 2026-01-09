/**
 * Better Auth Client Configuration
 * Phase 3: Client-side Authentication
 */
import { createAuthClient } from 'better-auth/react';

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  // Point to backend API for authentication
  credentials: 'include',
});

export const { signIn, signOut, useSession } = authClient;
