# OpenAI ChatKit Configuration Checklist

Use this checklist to ensure your ChatKit configuration is complete and working properly.

## Configuration Checklist

### OpenAI Platform Setup

- [ ] Logged into OpenAI Platform (https://platform.openai.com)
- [ ] Navigated to Organization Settings → Domain Allowlist
- [ ] Added local development domain: `http://localhost:3000`
- [ ] Added production domain (if deploying): Your Vercel/deployment URL
- [ ] Copied the generated domain key (starts with `domain_pk_`)

### Local Environment Configuration

- [ ] Created `frontend/.env.local` file
- [ ] Added `NEXT_PUBLIC_API_BASE_URL` variable
- [ ] Added `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` variable
- [ ] Replaced placeholder domain key with actual key from OpenAI
- [ ] Saved the `.env.local` file
- [ ] Verified `.env.local` is in `.gitignore` (for security)

### Backend Configuration

- [ ] Backend `.env` file has `OPENAI_API_KEY`
- [ ] Backend is running and accessible
- [ ] Backend API key is valid and active

### Development Server

- [ ] Restarted frontend development server after env changes
- [ ] Frontend running at http://localhost:3000
- [ ] No console errors related to environment variables
- [ ] Browser DevTools Console checked for errors

### Testing the Integration

- [ ] Can access the application at http://localhost:3000
- [ ] Can log in successfully
- [ ] AI chat interface is visible
- [ ] Can send a message to the AI assistant
- [ ] AI responds to messages (try: "list my tasks")
- [ ] No "domain not allowed" errors
- [ ] No "invalid domain key" errors
- [ ] Task operations work through AI (create, list, update)

### Production Deployment (if applicable)

- [ ] Production domain added to OpenAI Domain Allowlist
- [ ] Got production domain key from OpenAI
- [ ] Added `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` to Vercel environment variables
- [ ] Redeployed application after adding environment variables
- [ ] Tested AI chat on production URL
- [ ] Verified no CORS or domain errors in production

### Security Verification

- [ ] `.env.local` is NOT committed to git
- [ ] Domain keys are different for dev and production
- [ ] API keys are stored securely
- [ ] No keys exposed in frontend code
- [ ] Checked OpenAI usage dashboard for unexpected activity

## Common Issues and Solutions

### Issue: "Domain not allowed" error

**Check:**
- [ ] Domain is added to OpenAI's Domain Allowlist
- [ ] Domain matches exactly (including protocol and port)
- [ ] For localhost, tried both `localhost` and `127.0.0.1`

**Solution:**
1. Go to OpenAI Platform Domain Allowlist
2. Verify the domain is listed
3. Check for typos in the domain
4. Wait a few minutes for changes to propagate

### Issue: AI chat not loading

**Check:**
- [ ] `.env.local` has correct domain key
- [ ] Development server restarted after env changes
- [ ] Browser console for JavaScript errors
- [ ] Network tab for failed API requests

**Solution:**
1. Verify `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` is set
2. Restart: `npm run dev`
3. Clear browser cache
4. Check backend is running

### Issue: AI not responding

**Check:**
- [ ] Backend `OPENAI_API_KEY` is valid
- [ ] Backend is running and accessible
- [ ] No errors in backend logs
- [ ] OpenAI API quota not exceeded

**Solution:**
1. Check backend logs for errors
2. Verify OpenAI API key in backend `.env`
3. Test backend API endpoint directly
4. Check OpenAI dashboard for API status

## Verification Commands

Run these commands to verify your setup:

```bash
# Check if .env.local exists
ls -la frontend/.env.local

# Verify environment variables are loaded (while dev server is running)
# Open browser console and type:
console.log(process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY?.substring(0, 20))
# Should show: domain_pk_xxxxxxxxx

# Check backend is running
curl http://localhost:8000/health
# Should return: {"status": "healthy"}

# Check if frontend can reach backend
curl http://localhost:3000/api/health
```

## Next Steps After Configuration

Once all items are checked:

1. **Test Core Functionality**
   - Create a task via AI: "Add buy groceries"
   - List tasks via AI: "Show my tasks"
   - Complete a task via AI: "Mark task 1 as complete"
   - Delete a task via AI: "Delete task 1"

2. **Review Documentation**
   - Read `docs/CHATKIT_SETUP.md` for detailed information
   - Review `docs/QUICK_START_CHATKIT.md` for quick reference

3. **Deploy to Production**
   - Follow production deployment checklist above
   - Test thoroughly on production URL

4. **Monitor Usage**
   - Check OpenAI Dashboard for API usage
   - Set up billing alerts if available
   - Monitor for any unusual activity

## Support Resources

If you encounter issues not covered here:

- **Comprehensive Setup Guide**: `docs/CHATKIT_SETUP.md`
- **Quick Start Guide**: `docs/QUICK_START_CHATKIT.md`
- **OpenAI Platform Status**: https://status.openai.com/
- **OpenAI API Documentation**: https://platform.openai.com/docs

## Configuration Files Reference

### `frontend/.env.local`
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=domain_pk_your_key_here
```

### `backend/.env`
```bash
OPENAI_API_KEY=sk-your_key_here
DATABASE_URL=your_database_url
BETTER_AUTH_SECRET=your_secret
```

## Success Criteria

Your ChatKit configuration is successful when:

✅ AI chat interface loads without errors
✅ AI responds to natural language queries
✅ Task operations work through AI commands
✅ No domain or authentication errors
✅ Works in both development and production (if deployed)

---

**Last Updated**: Configuration complete - ready for testing
**Status**: Ready for OpenAI domain key configuration
