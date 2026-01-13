/**
 * Better Auth API Route Handler
 * Phase 3: Authentication Endpoint
 * Using dynamic import to prevent build-time database initialization
 */
import { toNextJsHandler } from "better-auth/next-js";
import { NextRequest } from "next/server";

export async function GET(request: NextRequest, { params }: { params: Promise<{ all: string[] }> }) {
  const resolvedParams = await params;
  const { auth } = await import("@/lib/auth");
  const handler = toNextJsHandler(auth);
  return handler.GET(request);
}

export async function POST(request: NextRequest, { params }: { params: Promise<{ all: string[] }> }) {
  const resolvedParams = await params;
  const { auth } = await import("@/lib/auth");
  const handler = toNextJsHandler(auth);
  return handler.POST(request);
}

export async function PUT(request: NextRequest, { params }: { params: Promise<{ all: string[] }> }) {
  const resolvedParams = await params;
  const { auth } = await import("@/lib/auth");
  const handler = toNextJsHandler(auth);
  return handler.PUT(request);
}

export async function DELETE(request: NextRequest, { params }: { params: Promise<{ all: string[] }> }) {
  const resolvedParams = await params;
  const { auth } = await import("@/lib/auth");
  const handler = toNextJsHandler(auth);
  return handler.DELETE(request);
}

export async function PATCH(request: NextRequest, { params }: { params: Promise<{ all: string[] }> }) {
  const resolvedParams = await params;
  const { auth } = await import("@/lib/auth");
  const handler = toNextJsHandler(auth);
  return handler.PATCH(request);
}
