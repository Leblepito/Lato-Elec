"""
Auth API — Email/Password + LINE + Facebook + Google OAuth
"""
from datetime import datetime, timedelta
from typing import Optional
import uuid, httpx
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.config import get_settings
from app.models.user import User, OAuthAccount

router = APIRouter(prefix="/api/auth", tags=["auth"])
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()

# ─── SCHEMAS ──────────────────────────────────────
class RegisterReq(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    lang: str = "tr"

class LoginReq(BaseModel):
    email: EmailStr
    password: str

class TokenResp(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

# ─── JWT ──────────────────────────────────────────
def create_token(user_id: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    return jwt.encode({"sub": user_id, "role": role, "exp": expire}, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def _user_dict(u: User) -> dict:
    return {"id": str(u.id), "email": u.email, "full_name": u.full_name, "role": u.role, "lang": u.lang, "avatar_url": u.avatar_url}

# ─── EMAIL REGISTER ──────────────────────────────
@router.post("/register", response_model=TokenResp)
def register(req: RegisterReq, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(400, "Bu email zaten kayıtlı")
    user = User(email=req.email, password_hash=pwd.hash(req.password), full_name=req.full_name, lang=req.lang)
    db.add(user); db.commit(); db.refresh(user)
    return TokenResp(access_token=create_token(str(user.id), user.role), user=_user_dict(user))

# ─── EMAIL LOGIN ─────────────────────────────────
@router.post("/login", response_model=TokenResp)
def login(req: LoginReq, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not pwd.verify(req.password, user.password_hash):
        raise HTTPException(401, "Email veya şifre hatalı")
    user.last_login = datetime.utcnow(); db.commit()
    return TokenResp(access_token=create_token(str(user.id), user.role), user=_user_dict(user))

# ═══ OAUTH HELPERS ════════════════════════════════
async def _oauth_upsert(db: Session, provider: str, provider_uid: str, email: Optional[str], name: str, avatar: Optional[str], raw: dict) -> TokenResp:
    """Find or create user from OAuth data"""
    oa = db.query(OAuthAccount).filter(OAuthAccount.provider == provider, OAuthAccount.provider_user_id == provider_uid).first()
    if oa:
        user = oa.user
        user.last_login = datetime.utcnow()
        db.commit()
    else:
        user = None
        if email:
            user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(email=email, full_name=name, avatar_url=avatar, role="technician")
            db.add(user); db.flush()
        oa = OAuthAccount(user_id=user.id, provider=provider, provider_user_id=provider_uid, provider_email=email, provider_name=name, raw_data=raw)
        db.add(oa); db.commit(); db.refresh(user)
    return TokenResp(access_token=create_token(str(user.id), user.role), user=_user_dict(user))

# ═══ LINE LOGIN ═══════════════════════════════════
@router.get("/line")
def line_login():
    url = f"https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={settings.LINE_CHANNEL_ID}&redirect_uri={settings.LINE_LOGIN_CALLBACK_URL}&state=electropms&scope=profile%20openid%20email"
    return RedirectResponse(url)

@router.get("/line/callback")
async def line_callback(code: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_resp = await client.post("https://api.line.me/oauth2/v2.1/token", data={"grant_type": "authorization_code", "code": code, "redirect_uri": settings.LINE_LOGIN_CALLBACK_URL, "client_id": settings.LINE_CHANNEL_ID, "client_secret": settings.LINE_CHANNEL_SECRET})
        tokens = token_resp.json()
        profile_resp = await client.get("https://api.line.me/v2/profile", headers={"Authorization": f"Bearer {tokens['access_token']}"})
        profile = profile_resp.json()
    email_resp = None
    if "id_token" in tokens:
        try:
            async with httpx.AsyncClient() as client:
                verify_resp = await client.post("https://api.line.me/oauth2/v2.1/verify", data={"id_token": tokens["id_token"], "client_id": settings.LINE_CHANNEL_ID})
                email_resp = verify_resp.json().get("email")
        except: pass
    result = await _oauth_upsert(db, "line", profile["userId"], email_resp, profile.get("displayName", "LINE User"), profile.get("pictureUrl"), profile)
    return RedirectResponse(f"http://localhost:5173/auth/callback?token={result.access_token}")

# ═══ FACEBOOK LOGIN ═══════════════════════════════
@router.get("/facebook")
def facebook_login():
    url = f"https://www.facebook.com/v19.0/dialog/oauth?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={settings.FACEBOOK_CALLBACK_URL}&scope=email,public_profile"
    return RedirectResponse(url)

@router.get("/facebook/callback")
async def facebook_callback(code: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_resp = await client.get(f"https://graph.facebook.com/v19.0/oauth/access_token?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={settings.FACEBOOK_CALLBACK_URL}&client_secret={settings.FACEBOOK_APP_SECRET}&code={code}")
        access_token = token_resp.json()["access_token"]
        profile_resp = await client.get(f"https://graph.facebook.com/me?fields=id,name,email,picture.type(large)&access_token={access_token}")
        profile = profile_resp.json()
    avatar = profile.get("picture", {}).get("data", {}).get("url")
    result = await _oauth_upsert(db, "facebook", profile["id"], profile.get("email"), profile.get("name", "FB User"), avatar, profile)
    return RedirectResponse(f"http://localhost:5173/auth/callback?token={result.access_token}")

# ═══ GOOGLE LOGIN ═════════════════════════════════
@router.get("/google")
def google_login():
    url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_CALLBACK_URL}&response_type=code&scope=openid%20email%20profile&access_type=offline"
    return RedirectResponse(url)

@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_resp = await client.post("https://oauth2.googleapis.com/token", data={"code": code, "client_id": settings.GOOGLE_CLIENT_ID, "client_secret": settings.GOOGLE_CLIENT_SECRET, "redirect_uri": settings.GOOGLE_CALLBACK_URL, "grant_type": "authorization_code"})
        tokens = token_resp.json()
        profile_resp = await client.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization": f"Bearer {tokens['access_token']}"})
        profile = profile_resp.json()
    result = await _oauth_upsert(db, "google", profile["id"], profile.get("email"), profile.get("name", "Google User"), profile.get("picture"), profile)
    return RedirectResponse(f"http://localhost:5173/auth/callback?token={result.access_token}")

# ═══ TOKEN VERIFY ═════════════════════════════════
@router.get("/me")
def get_me(db: Session = Depends(get_db), token: str = Depends(lambda: None)):
    # Bu endpoint middleware ile korunacak, placeholder
    return {"status": "implement with auth middleware"}
