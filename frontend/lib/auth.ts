import { betterAuth } from "better-auth";

// Initialize BetterAuth with conditional database configuration for serverless environments
const databaseConfig = process.env.DATABASE_URL
  ? {
      provider: "postgresql" as const,
      url: process.env.DATABASE_URL,
    }
  : undefined;

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "fallback-secret-for-development",
  ...(databaseConfig && { database: databaseConfig }),
});