import os, json, base64, tempfile
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.config import get_settings
from app.middleware.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api/analyze", tags=["analysis"])
settings = get_settings()

SYSTEM = """Sen 5 yıldızlı otel elektrik sistemleri uzmanı bir mühendissin. Havuz pompaları, MCC panoları, dağıtım panoları, jeneratör, UPS konusunda uzmansın. Güvenlik öncelikli analiz yap. Türkçe ve Tayca çift dil çıktı üret. SADECE JSON DÖNDÜR."""

class URLRequest(BaseModel):
    url: str
    lang: str = "th"

@router.post("/url")
async def analyze_url(req: URLRequest):
    """Video URL analizi — yt-dlp + Claude"""
    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(500, "ANTHROPIC_API_KEY ayarlanmamış")
    try:
        import yt_dlp
        ydl_opts = {"quiet": True, "extract_flat": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(req.url, download=False)
            video_info = {"title": info.get("title", ""), "description": info.get("description", "")[:2000], "tags": info.get("tags", [])}
    except Exception as e:
        raise HTTPException(400, f"Video bilgisi çekilemedi: {e}")

    import anthropic
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    prompt = f"""Video: {video_info['title']}\nAçıklama: {video_info['description']}\nEtiketler: {video_info['tags']}\n\nJSON döndür: topic, topic_th, risk_level, safety_warnings, workflow, workspace, electrical_specs, search_keywords"""
    try:
        resp = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=2048, temperature=0.2, system=SYSTEM, messages=[{"role": "user", "content": prompt}])
        text = resp.content[0].text.replace("```json", "").replace("```", "").strip()
        return {"status": "success", "input_type": "video_url", "analysis": json.loads(text), "video_info": video_info, "timestamp": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(500, f"AI analiz hatası: {e}")

@router.post("/photo")
async def analyze_photo(file: UploadFile = File(...), lang: str = Form("th")):
    """Fotoğraf analizi — Claude Vision"""
    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(500, "ANTHROPIC_API_KEY ayarlanmamış")
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "Dosya 10MB'dan büyük olamaz")
    b64 = base64.b64encode(contents).decode("utf-8")

    import anthropic
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    prompt = """Bu elektrik sistemi fotoğrafını analiz et. JSON döndür: topic, topic_th, risk_level, safety_warnings, observations (wiring, protection, grounding, condition), electrical_specs, immediate_actions"""
    try:
        resp = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=2048, temperature=0.2, system=SYSTEM, messages=[{"role": "user", "content": [{"type": "image", "source": {"type": "base64", "media_type": file.content_type, "data": b64}}, {"type": "text", "text": prompt}]}])
        text = resp.content[0].text.replace("```json", "").replace("```", "").strip()
        return {"status": "success", "input_type": "photo", "analysis": json.loads(text), "timestamp": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(500, f"Fotoğraf analiz hatası: {e}")
