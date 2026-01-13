import { betterAuth } from "better-auth";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "fallback-secret-for-development",
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL || "",
  },
});