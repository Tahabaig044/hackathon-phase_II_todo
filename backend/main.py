from fastapi import FastAPI
from api.v1 import tasks, auth
import os
from sqlmodel import SQLModel
from db.session import sync_engine

from core.security_config import add_security_middlewares

# Import models to register them with SQLModel
from models import user, task

app = FastAPI(title="Hackathon Todo Backend", version="1.0.0" )

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(sync_engine)

# Add security middlewares
add_security_middlewares(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hackathon Todo Backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Backend is running"}

# Include API routes
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
