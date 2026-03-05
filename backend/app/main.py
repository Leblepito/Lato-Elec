"""
ElectroPMS v5 — Backend API
FastAPI + PostgreSQL + Redis + Claude AI
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.api import auth, equipment, messages, workorders

settings = get_settings()

app = FastAPI(
    title="ElectroPMS API",
    version="5.0.0",
    description="Otel Elektrik Bakım Yönetim Sistemi — AntiGravity Ventures",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static uploads
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Routes
app.include_router(auth.router)
app.include_router(equipment.router)
app.include_router(messages.router)
app.include_router(workorders.router)

@app.get("/api/health")
def health():
    return {"status": "ok", "version": "5.0.0", "service": "ElectroPMS"}
