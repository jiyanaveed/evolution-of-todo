import { betterAuth } from "better-auth";

// For serverless environments, BetterAuth will use the DATABASE_URL environment variable at runtime
// The build process may not have access to runtime environment variables
export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "fallback-secret-for-development",
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL || "postgresql://placeholder:placeholder@localhost:5432/placeholder",
  },
});