/**
 * Better Auth API Route Handler
 * Phase 3: Authentication Endpoint
 */
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

const handler = toNextJsHandler(auth);

export { handler as GET, handler as POST };
