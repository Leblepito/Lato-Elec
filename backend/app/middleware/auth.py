from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import get_settings
from app.models.user import User

security = HTTPBearer(auto_error=False)
settings = get_settings()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token gerekli")
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Geçersiz token")
    except JWTError:
        raise HTTPException(401, "Token süresi dolmuş veya geçersiz")
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(401, "Kullanıcı bulunamadı")
    return user

async def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role not in ("admin", "chief_engineer"):
        raise HTTPException(403, "Yetkiniz yok")
    return user
