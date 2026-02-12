# Quick Start Commands

## Start the Application

### Terminal 1 - Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
```

## Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Test Gemini API
```bash
cd backend
python test_gemini_native.py
```

## Configuration Files
- Backend: `backend/.env`
- Frontend: `frontend/.env.local`

## What's Configured
✅ Google Gemini API (gemini-2.5-flash)
✅ PostgreSQL Database (Neon Cloud)
✅ Better Auth Secret
✅ CORS and Security
✅ AI Service Factory (supports multiple providers)
