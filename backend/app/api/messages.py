from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.message import Message
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/messages", tags=["messages"])

class MsgCreate(BaseModel):
    channel: str = "app"
    content: str
    message_type: str = "text"
    metadata: Optional[dict] = None

@router.get("/")
def list_messages(channel: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    q = db.query(Message)
    if channel: q = q.filter(Message.channel == channel)
    return q.order_by(Message.created_at.desc()).limit(limit).all()

@router.post("/")
def send_message(msg: MsgCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    m = Message(channel=msg.channel, sender_id=user.id, sender_name=user.full_name, sender_type="user", message_type=msg.message_type, content=msg.content, metadata=msg.metadata or {})
    db.add(m); db.commit(); db.refresh(m)
    return m

@router.post("/line-webhook")
async def line_webhook(payload: dict):
    """LINE Messaging API webhook — receives messages from LINE groups"""
    # TODO: Verify LINE signature, parse events, store messages
    return {"status": "ok"}
