import { betterAuth } from "better-auth";
import { pgAdapter } from "@better-auth/pg-adapter";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "fallback-secret-for-development",
  plugins: [
    pgAdapter({
      url: process.env.DATABASE_URL || "",
    })
  ]
});