/**
 * Better Auth API Route Handler
 * Phase 3: Authentication Endpoint
 */
import { toNextJsHandler } from "better-auth/next-js";
import { NextRequest } from "next/server";

// Dynamically import and initialize BetterAuth to avoid build-time database connection
async function getAuth() {
  const { betterAuth } = await import("better-auth");

  return betterAuth({
    secret: process.env.BETTER_AUTH_SECRET || "fallback-secret-for-development",
    database: process.env.DATABASE_URL
      ? {
          provider: "postgresql",
          url: process.env.DATABASE_URL,
        }
      : undefined,
  });
}

export async function GET(request: NextRequest, { params }: { params: { all: string[] } }) {
  const auth = await getAuth();
  const handler = toNextJsHandler(auth);
  return handler.GET(request, { params });
}

export async function POST(request: NextRequest, { params }: { params: { all: string[] } }) {
  const auth = await getAuth();
  const handler = toNextJsHandler(auth);
  return handler.POST(request, { params });
}
