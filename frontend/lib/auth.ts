import { betterAuth } from "better-auth";

// Determine if we're in build time vs runtime
const isBuildTime = !process.env.NODE_ENV || process.env.NEXT_PHASE === 'phase-production-build';

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "fallback-secret-for-development",
  ...(isBuildTime
    ? {}
    : {
        database: {
          provider: "postgresql",
          url: process.env.DATABASE_URL || "",
        }
      }
  ),
});