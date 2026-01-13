import { betterAuth } from "better-auth";

// Basic auth configuration without database for client-side usage
export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "fallback-secret-for-development",
  // Database will be configured at runtime in the API routes for serverless compatibility
});