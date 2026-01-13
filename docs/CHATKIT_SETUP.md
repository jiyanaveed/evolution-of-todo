# OpenAI ChatKit Configuration Guide

## Overview
This guide helps you configure OpenAI ChatKit for the Evolution of Todo application, enabling AI-powered task management through natural language.

## Prerequisites
- An OpenAI account with API access
- Your domain or localhost for development
- Access to OpenAI Platform settings

## Configuration Steps

### 1. Get Your ChatKit Domain Key

1. **Log in to OpenAI Platform**
   - Visit: https://platform.openai.com/settings/organization/general

2. **Navigate to Domain Allowlist**
   - Scroll down to the "Security" section
   - Find "Domain Allowlist" settings

3. **Add Your Domain**
   For **Local Development**:
   - Add: `http://localhost:3000`
   - Add: `http://127.0.0.1:3000`

   For **Production**:
   - Add your deployed frontend URL (e.g., `https://your-app.vercel.app`)

4. **Copy the Domain Key**
   - After adding your domain, OpenAI will generate a domain key
   - It will look like: `domain_pk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Copy this key

### 2. Update Environment Variables

#### Frontend Configuration

1. **Open** `frontend/.env.local` (create if it doesn't exist)

2. **Add or update the following**:
   ```bash
   # OpenAI ChatKit Configuration
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY=domain_pk_your_actual_key_here
   ```

3. **For Production (Vercel)**:
   - Go to your Vercel project settings
   - Navigate to Environment Variables
   - Add: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` with your domain key

#### Backend Configuration

Ensure your backend `.env` file has:
```bash
OPENAI_API_KEY=sk-your-openai-api-key
```

### 3. Verify Configuration

1. **Start your development server**:
   ```bash
   cd frontend
   npm run dev
   ```

2. **Test the AI Chat**:
   - Open http://localhost:3000
   - Log in to your account
   - Try sending a message to the AI assistant
   - Example: "List my tasks" or "Add buy groceries"

3. **Check for errors**:
   - Open browser DevTools (F12)
   - Check Console for any errors
   - Look for messages about missing domain keys or authentication issues

## Troubleshooting

### Error: "Domain not allowed"
**Solution**:
- Verify your domain is added to OpenAI's Domain Allowlist
- Make sure you're using the exact domain (including protocol and port)
- For localhost, try both `localhost` and `127.0.0.1`

### Error: "Invalid domain key"
**Solution**:
- Double-check the domain key in your `.env.local`
- Ensure there are no extra spaces or quotes
- Copy the key again from OpenAI Platform

### ChatKit not loading
**Solution**:
- Restart your development server after adding environment variables
- Clear browser cache and reload
- Check that `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` is set correctly

### Backend API errors
**Solution**:
- Verify your backend `OPENAI_API_KEY` is valid
- Check backend logs for authentication errors
- Ensure backend is running and accessible

## Security Best Practices

1. **Never commit `.env.local`** to version control
   - It's already in `.gitignore`
   - Keep your keys secret

2. **Use different keys** for development and production
   - Create separate domain entries in OpenAI Platform
   - Use environment-specific keys

3. **Rotate keys regularly**
   - Generate new domain keys periodically
   - Update them in your environment variables

4. **Monitor usage**
   - Check OpenAI Dashboard for API usage
   - Set up usage alerts if available

## Architecture

The ChatKit integration works as follows:

```
User Browser
    ↓ (sends message with domain key)
Frontend (Next.js)
    ↓ (sends message + domain key to backend)
Backend (FastAPI)
    ↓ (authenticates with OpenAI API key)
OpenAI API
    ↓ (validates domain key + processes request)
    ← (returns AI response)
Backend
    ← (returns formatted response)
Frontend
    ← (displays to user)
```

### Key Components

1. **Frontend** (`frontend/components/AIChatBoxBase.tsx`):
   - Sends domain key in request headers
   - Header: `OpenAI-Domain-Key: domain_pk_xxx`

2. **Backend** (`backend/app/routes/chat.py`):
   - Receives domain key from frontend
   - Uses OpenAI API key for authentication
   - Routes requests to OpenAI API

3. **OpenAI Platform**:
   - Validates domain key against allowlist
   - Processes AI requests securely

## Environment Variables Reference

### Frontend (`frontend/.env.local`)
```bash
# API Configuration
NEXT_PUBLIC_API_BASE_URL=<your-backend-url>

# ChatKit Domain Key (from OpenAI Platform)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=domain_pk_xxxxx
```

### Backend (`.env`)
```bash
# OpenAI API Configuration
OPENAI_API_KEY=sk-xxxxx

# Database
DATABASE_URL=<your-database-url>

# Authentication
BETTER_AUTH_SECRET=<your-secret>
```

## Testing Checklist

- [ ] OpenAI domain allowlist includes your domain
- [ ] `.env.local` has `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`
- [ ] Backend `.env` has `OPENAI_API_KEY`
- [ ] Development server restarted after env changes
- [ ] AI chat loads without console errors
- [ ] AI responds to test messages
- [ ] Task operations work through AI (create, list, update)

## Support

If you encounter issues:
1. Check the [OpenAI Platform Status](https://status.openai.com/)
2. Review [OpenAI API Documentation](https://platform.openai.com/docs)
3. Check backend logs for detailed error messages
4. Verify all environment variables are set correctly

## Additional Resources

- [OpenAI Platform Dashboard](https://platform.openai.com/dashboard)
- [Domain Allowlist Settings](https://platform.openai.com/settings/organization/general)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [Usage and Billing](https://platform.openai.com/usage)
