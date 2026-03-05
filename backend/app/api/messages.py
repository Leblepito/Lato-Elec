"""Messages API — in-memory message store"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/messages", tags=["messages"])

_messages = [
    {"id": 1, "channel": "line", "from_user": "สมชาย", "avatar": "👷", "time": "08:15", "text": "PP-01 สตาร์ทแล้ว กระแส 21.5A ปกติ", "type": "status", "created_at": "2026-03-05T08:15:00"},
    {"id": 2, "channel": "line", "from_user": "ระบบ", "avatar": "🤖", "time": "08:22", "text": "[แจ้งเตือน] ค่า PF ต่ำ 0.84 เพิ่มขั้น PFC แล้ว", "type": "alarm", "created_at": "2026-03-05T08:22:00"},
    {"id": 3, "channel": "app", "from_user": "Utku", "avatar": "👤", "time": "10:00", "text": "ปั๊มสระ 2 บำรุงรักษาครั้งถัดไปเมื่อไหร่?", "type": "msg", "created_at": "2026-03-05T10:00:00"},
    {"id": 4, "channel": "app", "from_user": "AI", "avatar": "🤖", "time": "10:01", "text": "PP-02 บำรุงล่าสุด: 20 ม.ค. 2026 ครั้งถัดไป: 20 เม.ย. ค่าฉนวน 120MΩ สภาพดี", "type": "answer", "created_at": "2026-03-05T10:01:00"},
]

_next_id = 5


class SendMessage(BaseModel):
    channel: str = "app"
    text: str
    from_user: str = "User"


@router.get("")
def list_messages(channel: Optional[str] = None):
    if channel and channel != "all":
        filtered = [m for m in _messages if m["channel"] == channel]
    else:
        filtered = _messages
    return {"messages": filtered, "total": len(filtered)}


@router.post("")
def send_message(msg: SendMessage):
    global _next_id
    now = datetime.now()
    new_msg = {
        "id": _next_id,
        "channel": msg.channel,
        "from_user": msg.from_user,
        "avatar": "👤",
        "time": now.strftime("%H:%M"),
        "text": msg.text,
        "type": "msg",
        "created_at": now.isoformat(),
    }
    _messages.append(new_msg)
    _next_id += 1
    return new_msg
