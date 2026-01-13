/**
 * Better Auth API Route Handler
 * Phase 3: Authentication Endpoint
 */
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

const { GET, POST, PUT, DELETE, PATCH } = toNextJsHandler(auth);

export { GET, POST, PUT, DELETE, PATCH };
