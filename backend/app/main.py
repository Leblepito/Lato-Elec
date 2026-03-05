"""
ElectroPMS v6 — Backend API
FastAPI + PostgreSQL + Claude AI
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.api import auth, equipment, work_orders, messages, analysis

settings = get_settings()

app = FastAPI(title="ElectroPMS API", version="6.0.0", description="ระบบจัดการไฟฟ้าโรงแรม — AntiGravity Ventures")

app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS.split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Routes — all real endpoints
app.include_router(auth.router)
app.include_router(equipment.router)
app.include_router(work_orders.router)
app.include_router(messages.router)
app.include_router(analysis.router)

@app.get("/api/health")
def health():
    return {"status": "ok", "version": "6.0.0", "service": "ElectroPMS", "modules": ["auth","equipment","work_orders","messages","analysis"]}
