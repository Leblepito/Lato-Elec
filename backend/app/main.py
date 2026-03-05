"""
ElectroPMS v5 — Backend API
FastAPI + PostgreSQL + Redis + Claude AI
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.api import auth

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

# Placeholder routes (implement as needed)
@app.get("/api/health")
def health():
    return {"status": "ok", "version": "5.0.0", "service": "ElectroPMS"}

@app.get("/api/equipment")
def list_equipment():
    return {"message": "Implement with DB query — see models/equipment.py"}

@app.get("/api/workorders")
def list_work_orders():
    return {"message": "Implement with DB query — see models/work_order.py"}

@app.get("/api/messages")
def list_messages():
    return {"message": "Implement with DB query — see models/message.py"}

@app.post("/api/analyze/url")
async def analyze_url():
    return {"message": "Implement — see services/ai_analysis.py"}

@app.post("/api/analyze/photo")
async def analyze_photo():
    return {"message": "Implement — see services/ai_analysis.py"}

@app.post("/api/upload")
async def upload_file():
    return {"message": "Implement — see services/file_processor.py"}
