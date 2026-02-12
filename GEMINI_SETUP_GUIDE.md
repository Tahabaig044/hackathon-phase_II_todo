# Gemini API Setup - Complete Guide

## Configuration Summary

Your application is now configured to use Google Gemini API for the AI chatbot features.

### What Was Configured

1. **Backend Environment Variables** (`backend/.env`)
   - AI_PROVIDER=gemini
   - OPENAI_API_KEY=AIzaSyDR4EUBLFD31tx4JI1uVsYXEwfRC5X60uw
   - MODEL=gemini-2.5-flash
   - BETTER_AUTH_SECRET=5Q0gJ2D_hw3H7ex_w8hBck1PVaof9bbcxOWFwrKkwBE
   - DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_Xg4mGZlWwOA3@ep-muddy-sea-adequxlf-pooler.c-2.us-east-1.aws.neon.tech/neondb

2. **Frontend Environment Variables** (`frontend/.env.local`)
   - NEXT_PUBLIC_API_URL=http://localhost:8000

3. **New Files Created**
   - `backend/src/services/gemini_service.py` - Native Gemini API integration
   - `backend/src/services/ai_service_factory.py` - AI provider factory
   - `backend/test_gemini_native.py` - API test script
   - `backend/list_gemini_models.py` - Model listing utility

4. **Updated Files**
   - `backend/requirements.txt` - Added google-generativeai package
   - `backend/src/api/v1/chat_endpoints.py` - Uses AI service factory
   - `backend/.env.example` - Updated with Gemini configuration
   - `frontend/.env.example` - Created template

## Quick Start

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Test Gemini API (Optional but Recommended)

```bash
python test_gemini_native.py
```

Expected output: `[SUCCESS] Gemini API is configured correctly!`

### 3. Start Backend Server

```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at: http://localhost:8000

### 4. Start Frontend (New Terminal)

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at: http://localhost:3000

## API Endpoints

- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs
- **Chat Endpoint**: POST http://localhost:8000/api/chat

## Available Gemini Models

Your API key has access to these models (configured in .env):

- **gemini-2.5-flash** (Current) - Fast, efficient, recommended
- **gemini-2.5-pro** - More capable, slower
- **gemini-2.0-flash** - Previous generation
- **gemini-flash-latest** - Always latest flash version

To change models, update the `MODEL` variable in `backend/.env`

## Troubleshooting

### Test API Connection
```bash
cd backend
python test_gemini_native.py
```

### List Available Models
```bash
cd backend
python list_gemini_models.py
```

### Check Backend Health
```bash
curl http://localhost:8000/health
```

### View Backend Logs
The backend will show logs in the terminal where you ran `uvicorn`

## Switching to OpenRouter (Optional)

If you want to use OpenRouter instead of Gemini:

1. Get an API key from https://openrouter.ai/
2. Update `backend/.env`:
   ```
   AI_PROVIDER=openrouter
   OPENAI_BASE_URL=https://openrouter.ai/api/v1
   OPENAI_API_KEY=your-openrouter-key
   MODEL=openai/gpt-3.5-turbo
   ```
3. Restart the backend server

## Features

- ✅ Google Gemini AI integration
- ✅ Natural language task management
- ✅ Conversation history
- ✅ English and Roman Urdu support
- ✅ PostgreSQL database (Neon)
- ✅ JWT authentication
- ✅ Rate limiting
- ✅ CORS configured

## Next Steps

1. Start both backend and frontend servers
2. Open http://localhost:3000 in your browser
3. Create an account or log in
4. Start chatting with the AI to manage your tasks!

## Support

If you encounter any issues:
1. Check the backend logs for errors
2. Verify your API key at https://aistudio.google.com/app/apikey
3. Ensure all dependencies are installed
4. Check that ports 8000 and 3000 are not in use
